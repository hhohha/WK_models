#!/usr/bin/python3

from itertools import combinations
from typing import Dict, List, Tuple, Set, Union, Optional, TypeVar, Any
from queue import PriorityQueue

DEBUG = 0
def debug(s):
	if DEBUG:
		print(s)

tNonTerm = str
tTerm = str
tTermLetter = Tuple[List[tTerm], List[tTerm]]
#tLetter = Union[tNonTerm, tTermLetter]
tLetter = TypeVar('tLetter', tNonTerm, tTermLetter)
tWord = List[tLetter]
tRelation = Tuple[tTerm, tTerm]

def hashWord(word: tWord) -> int:
	return hash(str(word)) # TODO: improve this


def get_all_combinations(l):
	for i in range(len(l) + 1):
		yield from combinations(l, i)

def is_nonterm(letter: tLetter) -> bool:
	return not isinstance(letter, tuple)

class cWordStatus:
	def __init__(self, word: tWord, upperStrLen: int, lowerStrLen: int, ntLen: int, parent: Optional['cWordStatus'], goalStr: str) -> None:
		self.word = word
		self.upperStrLen = upperStrLen
		self.lowerStrLen = lowerStrLen
		self.ntLen = ntLen
		self.parent = parent
		self.hashNo = hash(str(word)) # TODO: improve this
		self.distance = self.computeDistance(word, goalStr)

	def __hash__(self) -> int:
		return self.hashNo

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, cWordStatus):
			return NotImplemented
		return self.hashNo == other.hashNo

	def __lt__(self, other: 'cWordStatus') -> bool:
		return self.distance < other.distance

	def computeDistance(self, word: tWord, goal: str):
		val = 100
		for idx, letter in enumerate(word):
			if is_nonterm(letter):
				val += 1
			else:
				val -= 10
		return val

	def computeDistance2(self, word: tWord, goal: str):
		val = 0
		for letter in word:
			if is_nonterm(letter):
				val += 1
		return val

def wordToStr(word: tWord) -> str:
	rs = []
	for symbol in word:
		if not is_nonterm(symbol):
			e1 = ''.join(symbol[0]) if len(symbol[0]) > 0 else 'λ'
			e2 = ''.join(symbol[1]) if len(symbol[1]) > 0 else 'λ'
			rs.append(e1 + '/' + e2)
		else:
			rs.append(symbol)

	return(f'{" ".join(rs)}')

class cRule:
	#makes rules compact: A -> (a lambda)(lambda a) == A -> (a a)
	def compactize(self, word: tWord) -> tWord:
		i = 0
		while i < len(word) - 1:
			syllable1 = word[i]
			syllable2 = word[i+1]
			if not is_nonterm(syllable1) and not is_nonterm(syllable2):
				newSyllable = (syllable1[0] + syllable2[0], syllable1[1] + syllable2[1])
				word[i:i+2] = [newSyllable]
			else:
				i += 1
		return word

	def __init__(self, lhs: tNonTerm, rhs: tWord) -> None:
		self.lhs = lhs
		self.rhs = self.compactize(rhs)
		self.ntCnt = 0
		self.upperCnt = 0
		self.lowerCnt = 0

		for letter in rhs:
			if not is_nonterm(letter):
				self.upperCnt += len(letter[0])
				self.lowerCnt += len(letter[1])
			else:
				self.ntCnt += 1

	def __eq__(self, other):
		return self.rhs == other.rhs and self.lhs == other.lhs

	def __str__(self) -> str:
		return f'{self.lhs} -> {wordToStr(self.rhs)}'

class cWK_CFG:
	def __init__(self, nts: List[tNonTerm], ts: List[tTerm], startSymbol: tNonTerm, rules: List[cRule], relation: List[tRelation]) -> None:
		self.nts = set(nts)
		self.ts = set(ts)
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = set(relation)
		self.erasableNts: Set[tNonTerm] = set()

		if not self.is_consistent():
			raise ValueError

		self.generete_rule_dict()
		self.find_erasable_nts()
		#self.remove_lambda_rules()

		for rule in self.rules:
			for letter in rule.rhs:
				if is_nonterm(letter) and letter in self.erasableNts:
					rule.ntCnt -= 1


	def find_erasable_nts(self) -> None:
		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if self.is_word_erasable(rule.rhs) and rule.lhs not in self.erasableNts:
					loop = True
					self.erasableNts.add(rule.lhs)


	def generete_rule_dict(self) -> None:
		self.ruleDict: Dict[tNonTerm, List[cRule]] = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
		for rule in self.rules:
			self.ruleDict[rule.lhs].append(rule)


	def remove_lambda_rules(self) -> None:
		newRules: List[cRule] = []

		for rule in self.rules:
			erasableIdxs: List[int] = []
			for idx, letter in enumerate(rule.rhs):
				if is_nonterm(letter) and letter in self.erasableNts:
					erasableIdxs.append(idx)

			for idxLst in get_all_combinations(erasableIdxs):
				newRuleRhs = []
				for idx, letter in enumerate(rule.rhs):
					if idx not in erasableIdxs or idx in idxLst:
						newRuleRhs.append(letter)

				newRule = cRule(rule.lhs, newRuleRhs)
				if newRule.rhs != [([], [])] and newRule.rhs != [] and newRule not in newRules:
					newRules.append(newRule)

		self.rules = newRules
		self.generete_rule_dict()


	def remove_unit_rules(self) -> None:

		simpleRules: Dict[tNonTerm, List[tNonTerm]] = {}
		for nt in self.nts:
			simpleRules[nt] = [nt]

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if len(rule.rhs) == 1 and is_nonterm(rule.rhs[0]) and rule.lhs != rule.rhs:
					# find all non terminals which have lhs in their N but no rhs
					for k, v in simpleRules.items():
						if rule.lhs in v and rule.rhs[0] not in v:
							simpleRules[k].append(rule.rhs[0])
							loop = True

		newRules: List[cRule] = []
		for rule in self.rules:
			if len(rule.rhs) != 1 or not is_nonterm(rule.rhs[0]):
				for k, v in simpleRules.items():
					if rule.lhs in v:
						newRules.append(cRule(k, rule.rhs))

		self.rules = newRules
		self.generete_rule_dict()


	def remove_unterminatable_symbols(self) -> None:
		non_empty_nts: Set[tNonTerm] = set()

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if len(list(filter(lambda letter: is_nonterm(letter) and letter not in non_empty_nts, rule.rhs))) == 0:
					if rule.lhs not in non_empty_nts:
						non_empty_nts.add(rule.lhs)
						loop = True


		newRules: List[cRule] = []
		for rule in self.rules:
			if rule.lhs in non_empty_nts and all(map(lambda letter: not is_nonterm(letter) or letter in non_empty_nts, rule.rhs)):
				newRules.append(rule)

		self.nts = self.nts.intersection(non_empty_nts)
		self.rules = newRules
		self.generete_rule_dict()

	def remove_unreachable_symbols(self) -> None:
		reachableNts: Set[tNonTerm] = set(self.startSymbol)
		reachableTs: Set[tTerm] = set()

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if rule.lhs in reachableNts:
					for letter in rule.rhs:
						if is_nonterm(letter):
							if letter not in reachableNts:
								reachableNts.add(letter)
								loop = True
						else:
							for terminal in letter[0] + letter[1]:
								if terminal not in reachableTs:
									reachableTs.add(terminal)
									loop = True

		newRules: List[cRule] = []
		for rule in self.rules:
			if rule.lhs in reachableNts and all(map(lambda letter: not is_nonterm(letter) or letter in reachableNts, rule.rhs)):
				newRules.append(rule)

		self.nts = self.nts.intersection(reachableNts)
		self.ts = self.ts.intersection(reachableTs)
		self.rules = newRules
		self.generete_rule_dict()

	def remove_useless_rules(self):
		self.remove_unterminatable_symbols()
		self.remove_unreachable_symbols()

	def transform_to_wk_cnf(self):
		#coveredTs = []
		#for rule in self.rules:
			#if len(rule.rhs) == 1 and not is_nonterm(rule.rhs[0]) and len(self.ruleDict[rule.lhs]) == 1:
				#coveredTs.append(rule.rhs[0])


	def run_wk_cyk(self):
		pass



	def is_word_erasable(self, word: tWord) -> bool:
		for letter in word:
			if not is_nonterm(letter):
				if letter == ([], []):
					continue
				else:
					return False

			if letter not in self.erasableNts:
				return False

		return True

	def is_consistent(self) -> bool:
		if self.startSymbol not in self.nts:
			print(f'the starting symbol {self.startSymbol} not found among non-terminals')
			return False

		for t in self.ts:
			if t in self.nts:
				print(f'terminal {t} found among non-terminals')
				return False

		for rule in self.rules:
			if rule.lhs not in self.nts:
				print(f'rule left-hand side {rule.lhs} not found among non-terminals')
				return False
			#TODO - finish this
			#for symbol in rule.lhs:
				#if symbol not in self.nts and symbol not in self.ts:
					#return False

		for r in self.relation:
			if r[0] not in self.ts or r[1] not in self.ts:
				print(f'relation {r} is invalid')
				return False

		return True

	def printPath(self, wordStatus: cWordStatus) -> None:
		currentWordStatus: Optional[cWordStatus] = wordStatus
		while currentWordStatus:
			debug(f' >>> {wordToStr(currentWordStatus.word)}')
			currentWordStatus = currentWordStatus.parent


	def can_generate(self, upperStr: str) -> Tuple[int, int, Optional[bool]]:
		initStatus = cWordStatus([self.startSymbol], 0, 0, 1, None, upperStr)
		openQueue: Any = PriorityQueue()
		openQueue.put(initStatus)
		openSet: Set[int] = set()
		openSet.add(initStatus.hashNo)
		closedSet: Set[int] = set()
		cnt = 0

		while not openQueue.empty():
			if cnt == 1000000:
				print('taking too long')
				return len(openSet), len(closedSet), None
			else:
				cnt += 1
			debug('\n--------------------------------------')
			debug(f'cnt: {cnt} (O: {len(openSet)}, C: {len(closedSet)})')
			debug('--------------------------------------')
			currentWordStatus = openQueue.get()
			closedSet.add(currentWordStatus.hashNo)

			for nextWordStatus in self.get_all_next_states(currentWordStatus, upperStr):
				if self.is_result(nextWordStatus.word, upperStr):
					self.printPath(nextWordStatus)
					return len(openSet), len(closedSet), True
				if nextWordStatus.hashNo not in openSet and nextWordStatus.hashNo not in closedSet:
					openQueue.put(nextWordStatus)
					openSet.add(nextWordStatus.hashNo)

		return len(openSet), len(closedSet), False

	def is_result(self, word: tWord, goal: str) -> bool:
		# word lenght must be 1
		# word must be terminal
		# upper and lower strands must have the same length
		# upper and lower strands must fulfil compl. relation
		# upper strand must equal goal string

		if len(word) != 1:
			return False

		if isinstance(word[0], tNonTerm):
			return False

		if len(word[0][0]) != len(word[0][1]):
			return False

		for symbol1, symbol2 in zip(word[0][0], word[0][1]):
			if (symbol1, symbol2) not in self.relation:
				return False

		if ''.join(word[0][0]) != goal:
			return False

		return True

	def is_word_feasible(self, wordStatus: cWordStatus, goalStr: str):
		longerStrand = max(wordStatus.upperStrLen, wordStatus.lowerStrLen)
		shorterStrand = min(wordStatus.upperStrLen, wordStatus.lowerStrLen)

		if longerStrand > len(goalStr) or shorterStrand + wordStatus.ntLen > len(goalStr):
			debug(f'not feasible (getting too long)')
			return False

		word = wordStatus.word
		if not is_nonterm(word[0]):
			if not goalStr.startswith(''.join(word[0][0])):
				debug('not feasible (doesn\'t match goal string)')
				return False

			shorter_len = min(len(word[0][0]), len(word[0][1]))
			for idx in range(shorter_len):
				if (word[0][0][idx], word[0][1][idx]) not in self.relation:
					debug('not feasible (doesn\'t fulfil relation)')
					return False
		debug ('feasible')
		return True

	def get_all_next_states(self, wordStatus: cWordStatus, goalStr: str) -> List[cWordStatus]:
		retLst: List[cWordStatus] = []
		for ntIdx, symbol in enumerate(wordStatus.word):
			if is_nonterm(symbol):
				for rule in self.ruleDict[symbol]:
					newWord = self.apply_rule(wordStatus.word, ntIdx, rule.rhs)
					newWordStatus = cWordStatus(newWord, wordStatus.upperStrLen + rule.upperCnt, wordStatus.lowerStrLen + rule.lowerCnt, wordStatus.ntLen + rule.ntCnt - 1, wordStatus, goalStr)

					if self.is_word_feasible(newWordStatus, goalStr):
						retLst.append(newWordStatus)
		return retLst


	def apply_rule(self, word: tWord, ntIdx: int, ruleRhs: tWord) -> tWord:
		if DEBUG:
			debug(f'\nword: {wordToStr(word)}')
			debug(f'ntIdx: {ntIdx}')
			debug(f'rule: {word[ntIdx] + " -> " + wordToStr(ruleRhs)}')

		mergePrev = ntIdx > 0 and not is_nonterm(word[ntIdx - 1]) # can we merge with the previous terminal
		mergeNext = ntIdx < len(word) - 1 and not is_nonterm(word[ntIdx + 1]) # can we merge with the next terminal

		if len(ruleRhs) == 1 and not is_nonterm(ruleRhs[0]):    # rule right side is just a terminal pair
			if mergePrev and mergeNext:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			elif mergePrev:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1]
				retval = word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 1:]

			elif mergeNext:
				mergedUpper = ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = ruleRhs[0][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			else:
				retval = word[:ntIdx] + [ruleRhs[0]] + word[ntIdx + 1:]
		else:
			mergePrev = mergePrev and not is_nonterm(ruleRhs[0])
			mergeNext = mergeNext and not is_nonterm(ruleRhs[-1])

			if ntIdx > 0 and mergePrev and mergeNext:
				mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
				mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
				mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
			elif mergePrev:
				mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
				retval = word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:] + word[ntIdx + 1:]
			elif mergeNext:
				mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
				mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
				retval = word[:ntIdx] + ruleRhs[:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
			else:
				retval = word[:ntIdx] + ruleRhs + word[ntIdx + 1:]

		debug(f'result: {wordToStr(retval)}')
		return retval

#nts: List[tNonTerm] = ['A']
#ts: List[tTerm] = ['a']
#startSymbol: tNonTerm = 'A'
#rules: List[cRule] = [
	#cRule('A', ['A', 'A', 'A']),
	#cRule('A', [(['a'], ['a'])])
#]

#relation: List[tRelation] = [('a', 'a')]
#g = cWK_CFG(nts, ts, startSymbol, rules, relation)

##print('>>', g.rules[0].upperCnt)
##print('>>', g.rules[0].lowerCnt)
##print('>>', g.rules[0].ntCnt)

#res = g.can_generate('aaaaaaaaaaaaaaa')
#print(f'RESULT: {res}')

#for x in g.get_all_next_states([(['a', 'a'], ['a', 'a']), 'A']):
	#print(f'-----> {wordToStr(x)}\n\n\n')

#rules: List[cRule] = [
	#cRule('S', [(['a'], []), 'S']),
	#cRule('S', [(['a'], []), 'A']),
	#cRule('A', [(['b'], ['a']), 'A']),
	#cRule('A', [(['b'], ['a']), 'B']),
	#cRule('B', [([], ['b']), 'B']),
	#cRule('B', [([], ['b'])])
#]

#g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])

#res = g.can_generate('aaaaaaaaaaabbbbbbbbbbb')
#print(f'RESULT: {res}')
