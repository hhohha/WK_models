#!/usr/bin/python3

from typing import Dict, List, Tuple, Set, Union, Optional, TypeVar

DEBUG = 1
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

def is_nonterm(letter: tLetter) -> bool:
	return not isinstance(letter, tuple)

class cWordStatus:
	def __init__(self, word: tWord, upperStrLen: int, lowerStrLen: int, ntLen: int, parent: Optional['cWordStatus']) -> None:
		self.word = word
		self.upperStrLen = upperStrLen
		self.lowerStrLen = lowerStrLen
		self.ntLen = ntLen
		self.parent = parent
		self.hashNo = hash(str(word))

	def __hash__(self) -> int:
		return self.hashNo

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, cWordStatus):
			return NotImplemented
		return self.hashNo == other.hashNo

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

class cWK_CFG:
	def __init__(self, nts: List[tNonTerm], ts: List[tTerm], startSymbol: tNonTerm, rules: List[cRule], relation: List[tRelation]) -> None:
		self.nts = nts
		self.ts = ts
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = set(relation)
		self.erasableNts: Set[tNonTerm] = set()

		if not self.is_consistent():
			raise ValueError

		self.ruleDict: Dict[tNonTerm, List[cRule]] = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
		for rule in rules:
			self.ruleDict[rule.lhs].append(rule)

		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if self.is_word_erasable(rule.rhs) and rule.lhs not in self.erasableNts:
					loop = True
					self.erasableNts.add(rule.lhs)

		for rule in self.rules:
			for letter in rule.rhs:
				if is_nonterm(letter) and letter in self.erasableNts:
					rule.ntCnt -= 1

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


	def can_generate(self, upperStr: str) -> Optional[bool]:
		initStatus = cWordStatus([self.startSymbol], 0, 0, 1, None)
		openQueue: List[cWordStatus] = [initStatus]
		openSet: Set[int] = set()
		openSet.add(initStatus.hashNo)
		closedSet: Set[int] = set()
		cnt = 0

		while openQueue:
			if cnt == 1000000:
				print('taking too long')
				return None
			else:
				cnt += 1
			debug('\n--------------------------------------')
			debug(f'cnt: {cnt} (O: {len(openSet)}, C: {len(closedSet)})')
			debug('--------------------------------------')
			if cnt % 1000 == 0:
				print(cnt)
			currentWordStatus = openQueue.pop(0)
			closedSet.add(currentWordStatus.hashNo)

			for nextWordStatus in self.get_all_next_states(currentWordStatus, upperStr):
				if self.is_result(nextWordStatus.word, upperStr):
					self.printPath(nextWordStatus)
					return True
				if nextWordStatus.hashNo not in openSet and nextWordStatus.hashNo not in closedSet:
					openQueue.append(nextWordStatus)
					openSet.add(nextWordStatus.hashNo)

		return False

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
					newWordStatus = cWordStatus(newWord, wordStatus.upperStrLen + rule.upperCnt, wordStatus.lowerStrLen + rule.lowerCnt, wordStatus.ntLen + rule.ntCnt - 1, wordStatus)

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
