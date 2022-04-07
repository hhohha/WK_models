#!/usr/bin/python3

from itertools import combinations
from typing import Dict, List, Tuple, Set, Union, Optional, TypeVar, Any
from queue import PriorityQueue
from copy import deepcopy
import time
import re

DEBUG = 0
def debug(s):
	if DEBUG:
		print(s)

tNonTerm = str
tTerm = str
tTermLetter = Tuple[List[tTerm], List[tTerm]]
#tLetter = Union[tNonTerm, tTermLetter]
tLetter = TypeVar('tLetter')
tWord = List[tLetter]
tRelation = Tuple[tTerm, tTerm]

t4DInt = Tuple[int, int, int, int]

def hashTerminal(letter: tTermLetter) -> int:
	return hash(str(letter)) # TODO: improve this


def get_all_combinations(l):
	for i in range(len(l) + 1):
		yield from combinations(l, i)

def is_nonterm(letter: tLetter) -> bool:
	return not isinstance(letter, tuple)


E_STR_NO_HEURISTIC = 0
E_STR_PREF_TERMS = 1
E_STR_TERMS_MATCH = 2

class cWordStatus:
	def __init__(self, word: tWord, upperStrLen: int, lowerStrLen: int, ntLen: int, parent: Optional['cWordStatus'], distance: int) -> None:
		self.word = word
		self.upperStrLen = upperStrLen
		self.lowerStrLen = lowerStrLen
		self.ntLen = ntLen
		self.parent = parent
		self.hashNo = hash(str(word)) # TODO: improve this
		self.distance = distance

	def __hash__(self) -> int:
		return self.hashNo

	def __eq__(self, other: object) -> bool:
		if not isinstance(other, cWordStatus):
			return NotImplemented
		return self.hashNo == other.hashNo

	def __lt__(self, other: 'cWordStatus') -> bool:
		return self.distance < other.distance


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

		self.calculate_cnts()

	def calculate_cnts(self):
		self.ntCnt = 0
		self.upperCnt = 0
		self.lowerCnt = 0
		for letter in self.rhs:
			if not is_nonterm(letter):
				self.upperCnt += len(letter[0])
				self.lowerCnt += len(letter[1])
			else:
				self.ntCnt += 1


	def __eq__(self, other):
		return self.rhs == other.rhs and self.lhs == other.lhs

	def __str__(self) -> str:
		return f'{self.lhs} -> {wordToStr(self.rhs)}'

	__repr__ = __str__

	def __hash__(self) -> int:
		return hash((self.lhs, str(self.rhs)))


class cWK_CFG:
	def __init__(self, nts: List[tNonTerm], ts: List[tTerm], startSymbol: tNonTerm, rules: List[cRule], relation: List[tRelation]) -> None:
		self.nts = set(nts)
		self.ts = set(ts)
		self.startSymbol = startSymbol
		self.rules = set(rules)
		self.relation = set(relation)
		self.erasableNts: Set[tNonTerm] = set()
		self.lastCreatedNonTerm = 0
		self.timeLimit = 5

		if not self.is_consistent():
			raise ValueError

		self.generate_rule_dict()
		self.find_erasable_nts()

		self.distance_calc_strategy = 0
		self.distance_calc_strategies_list = [
			('no heuristic', self.compute_distance_no_heuristic),
			('prefer less non-terminals', self.compute_distance_prefer_terms),
			('prefer prefix matching goal', self.compute_distance_terms_match)
		]

		for rule in self.rules:
			for letter in rule.rhs:
				if is_nonterm(letter) and letter in self.erasableNts:
					rule.ntCnt -= 1

	def restore(self) -> None:
		self.rules = self.rules_backup
		self.nts = self.nts_backup
		self.ts = self.ts_backup
		self.generate_rule_dict()

	def backup(self) -> None:
		self.rules_backup = deepcopy(self.rules)
		self.nts_backup = self.nts.copy()
		self.ts_backup = self.ts.copy()

	def calculate_distance(self, word: tWord, goalStr: str) -> int:
		return self.distance_calc_strategies_list[self.distance_calc_strategy][1](word, goalStr)


	def compute_distance_no_heuristic(self, word: tWord, goal: str) -> int:
		return 0


	def compute_distance_prefer_terms(self, word: tWord, goal: str) -> int:
		distance = 0
		for letter in word:
			if is_nonterm(letter):
				distance += 1
		return distance


	def compute_distance_terms_match(self, word: tWord, goal: str) -> int:
		goalIdx, distance = 0, 0

		for letter in word:
			if not is_nonterm(letter):
				for symbol in letter[0]:
					if len(goal) > goalIdx and symbol == goal[goalIdx]:
						distance -= 1
						goalIdx += 1
					else:
						return distance
		return distance


	def find_erasable_nts(self) -> None:
		loop = True
		while loop:
			loop = False
			for rule in self.rules:
				if self.is_word_erasable(rule.rhs) and rule.lhs not in self.erasableNts:
					loop = True
					self.erasableNts.add(rule.lhs)


	def generate_rule_dict(self) -> None:
		self.ruleDict: Dict[tNonTerm, List[cRule]] = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
		for rule in self.rules:
			self.ruleDict[rule.lhs].append(rule)


	def remove_lambda_rules(self) -> None:
		newRules: Set[cRule] = set()

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
					newRules.add(newRule)

		self.rules = newRules
		self.generate_rule_dict()


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

		newRules: Set[cRule] = set()
		for rule in self.rules:
			if len(rule.rhs) != 1 or not is_nonterm(rule.rhs[0]):
				for k, v in simpleRules.items():
					if rule.lhs in v:
						newRules.add(cRule(k, rule.rhs))

		self.rules = newRules
		self.generate_rule_dict()


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


		newRules: Set[cRule] = set()
		for rule in self.rules:
			if rule.lhs in non_empty_nts and all(map(lambda letter: not is_nonterm(letter) or letter in non_empty_nts, rule.rhs)):
				newRules.add(rule)

		self.nts = self.nts.intersection(non_empty_nts)
		self.rules = newRules
		self.generate_rule_dict()


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

		newRules: Set[cRule] = set()
		for rule in self.rules:
			if rule not in newRules and all(map(lambda letter: not is_nonterm(letter) or letter in reachableNts, rule.rhs)):
				newRules.add(rule)

		self.nts = self.nts.intersection(reachableNts)
		self.ts = self.ts.intersection(reachableTs)
		self.rules = newRules
		self.generate_rule_dict()


	def remove_useless_rules(self) -> None:
		self.remove_unterminatable_symbols()
		self.remove_unreachable_symbols()


	def dismantleRule(self, rule: cRule) -> List[cRule]:
		newRules: List[cRule] = []

		for idx, letter in enumerate(rule.rhs):
			if not is_nonterm(letter):
				newNt = self.createNewNt()
				newRules.append(cRule(newNt, [letter]))
				rule.rhs[idx] = newNt
				self.nts.add(newNt)

		currentNt: tNonTerm = rule.lhs

		while len(rule.rhs) > 2:
			newNt = self.createNewNt()
			self.nts.add(newNt)
			newRules.append(cRule(currentNt, [rule.rhs.pop(0), newNt]))
			currentNt = newNt

		newRules.append(cRule(currentNt, rule.rhs))
		return newRules

	def pop_term_from_letter(self, letter: tTermLetter) -> tTermLetter:
		if len(letter[0]) > len(letter[1]):
			t = letter[0].pop(0)
			return ([t], [])
		else:
			t = letter[1].pop(0)
			return ([], [t])

	def printDebug(self):
		print('rules:')
		for rule in self.rules:
			print('   ', rule)
		#print('ts: ', self.nts)
		#print('nts', self.ts)

	def dismantle_term_letters(self) -> None:
		newRules: List[cRule] = []

		for rule in self.rules:
			if len(rule.rhs) == 1 and not is_nonterm(rule.rhs[0]) and len(rule.rhs[0][0]) + len(rule.rhs[0][1]) == 1:
				continue
			for idx, letter in enumerate(rule.rhs):
				if not is_nonterm(letter):
					newNt = self.createNewNt()
					self.nts.add(newNt)

					rule.rhs[idx] = newNt

					if len(rule.rhs) == 1:
						rule.rhs.insert(0, self.pop_term_from_letter(letter))

					currentNt = newNt
					while len(letter[0]) + len(letter[1]) > 1:
						t = self.pop_term_from_letter(letter)
						newNt = self.createNewNt()
						self.nts.add(newNt)
						newRules.append(cRule(currentNt, [t, newNt]))
						currentNt = newNt

					newRules.append(cRule(currentNt, [letter]))
			rule.calculate_cnts()

		self.rules.update(newRules)
		self.generate_rule_dict()

	def transform_to_wk_cnf_form(self) -> None:
		newRules: Set[cRule] = set()

		for rule in self.rules:
			if len(rule.rhs) == 1 and not is_nonterm(rule.rhs[0]) or len(rule.rhs) == 2 and is_nonterm(rule.rhs[0]) and is_nonterm(rule.rhs[1]):
				newRules.add(rule)

			# swap terminal letters for respective non-terminals and break down words longer than 2
			elif len(rule.rhs) >= 2:
				newRules.update(self.dismantleRule(rule))

		self.rules = newRules
		self.generate_rule_dict()


	def to_wk_cnf(self) -> None:
		#self.printDebug()
		#print('--------------------------------------')

		self.remove_lambda_rules()

		#self.printDebug()
		#print('--------------------------------------')

		self.remove_unit_rules()
		self.remove_useless_rules()
		self.remove_unreachable_symbols()

		#self.printDebug()
		#print('A-------------------------------------')
		self.dismantle_term_letters()
		#self.printDebug()
		#print('B-------------------------------------')
		self.transform_to_wk_cnf_form()
		#self.printDebug()

		# possible TODO - optimize terminal covering non-terms

	def addToX(self, idx: t4DInt, nt: tNonTerm) -> None:
		if idx not in self.X:
			self.X[idx] = []

		self.X[idx].append(nt)


	def checkRules(self, idx1: t4DInt, idx2: t4DInt, target: t4DInt) -> None:
		if idx1 not in self.X or idx2 not in self.X:
			return
		for rule in self.rules:
			if rule.rhs[0] in self.X[idx1] and rule.rhs[1] in self.X[idx2]:
				self.addToX(target, rule.lhs)

	def computeSet(self, i: int, j: int, k: int ,l: int) -> None:
		if i == 0 and j == 0:
			for t in range(k, l):
				self.checkRules((0, 0, k, t), (0, 0 ,t+1, l), (i, j, k, l))

		elif k == 0 and l == 0:
			for s in range(i, j):
				self.checkRules((i, s, 0, 0), (s+1, j ,0 , 0), (i, j, k, l))

		else:
			self.checkRules((i, j, 0, 0), (0, 0, k, l), (i, j, k, l))
			self.checkRules((0, 0, k, l), (i, j, 0, 0), (i, j, k, l))

			for s in range(i, j):
				for t in range(k, l):
					self.checkRules((i, s, k, t), (s+1, j, t+1, l), (i, j, k, l))

			for s in range(i, j):
				self.checkRules((i, s, k, l), (s+1, j, 0, 0), (i, j, k, l))
				self.checkRules((i, s, 0, 0), (s+1, j, k, l), (i, j, k, l))

			for t in range(k, l):
				self.checkRules((i, j, k, t), (0, 0, t+1, l), (i, j, k, l))
				self.checkRules((0, 0, k, t), (i, j, t+1, l), (i, j, k, l))


	def run_wk_cyk(self, sentence: str) -> Optional[bool]:
		start_time = time.time()
		n = len(sentence)
		self.X: Dict[t4DInt, List[tNonTerm]] = {}

		for i, word in enumerate(sentence):
			current_time = time.time()
			if current_time - start_time > self.timeLimit:
				return None

			for rule in self.rules:
				if len(rule.rhs) == 1 and not is_nonterm(rule.rhs[0]):
					letter = rule.rhs[0]
					if len(letter[0]) == 1 and letter[0][0] == word:
						self.addToX((i+1, i+1, 0, 0), rule.lhs)
					elif len(letter[1]) == 1 and letter[1][0] == word:
						self.addToX((0, 0, i+1, i+1), rule.lhs)

		#print('*********************************************')
		#print(self.X)
		#print('*********************************************')

		for y in range(2, 2*n+1):
			current_time = time.time()
			if current_time - start_time > self.timeLimit:
				return None

			for beta in range(max(y - n, 0), min(n, y)+1):
			#for beta in range(0, n+1):
				alpha = y - beta

				if alpha == 0:
					i = j = 0
					for k in range(1, n-y+2):
						l = k + y - 1
						self.computeSet(i, j, k, l)

				elif beta == 0:
					k = l = 0
					for i in range(1, n - y + 2):
						j = i + y - 1
						self.computeSet(i, j, k, l)

				else:
					for i in range(1, n - alpha + 2):
						for k in range(1, n - beta + 2):
							j = i + alpha - 1
							l = k + beta - 1
							self.computeSet(i, j, k, l)

		return (1, n, 1, n) in self.X and self.startSymbol in self.X[(1, n, 1, n)]


	def createNewNt(self, prefix: str = '') -> tNonTerm:
		self.lastCreatedNonTerm += 1
		while prefix + str(self.lastCreatedNonTerm) in self.nts:
			self.lastCreatedNonTerm += 1
		return prefix + str(self.lastCreatedNonTerm)


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
		distance = self.calculate_distance([self.startSymbol], upperStr)
		initStatus = cWordStatus([self.startSymbol], 0, 0, 1, None, distance)
		openQueue: Any = PriorityQueue()
		openQueue.put(initStatus)
		openSet: Set[int] = set()
		openSet.add(initStatus.hashNo)
		closedSet: Set[int] = set()

		startTime = time.time()

		while not openQueue.empty():
			currentTime = time.time()
			if currentTime - startTime > self.timeLimit:
				debug('taking too long')
				return len(openSet), len(closedSet), None

			debug('\n--------------------------------------')
			debug(f'OPEN STATES: {len(openSet)}, CLOSED STATES: {len(closedSet)}')
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


	def word_to_regex(self, word: tWord) -> str:
		if is_nonterm(word[0]):
			regex = ''
		else:
			regex = '^'

		for idx, letter in enumerate(word):
			if is_nonterm(letter) and idx > 0 and not is_nonterm(word[idx-1]):
				regex += '.*'
			elif not is_nonterm(letter):
				regex += ''.join(letter[0])

		if not is_nonterm(word[-1]):
			regex += '$'

		return regex

	def is_word_feasible(self, wordStatus: cWordStatus, goalStr: str) -> bool:
		longerStrand = max(wordStatus.upperStrLen, wordStatus.lowerStrLen)
		shorterStrand = min(wordStatus.upperStrLen, wordStatus.lowerStrLen)

		if longerStrand > len(goalStr) or shorterStrand + longerStrand + wordStatus.ntLen > 2* len(goalStr):
			debug(f'not feasible (getting too long) >{wordStatus.upperStrLen}, {wordStatus.lowerStrLen}, {wordStatus.ntLen}')
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

		regex = self.word_to_regex(word)
		if re.compile(regex).search(goalStr) is None:
			debug(f'no feasible (re search failed)   regex: {regex},  string: {goalStr},    word: {word}')
			return False

		debug('feasible')
		return True


	def get_all_next_states(self, wordStatus: cWordStatus, goalStr: str) -> List[cWordStatus]:
		retLst: List[cWordStatus] = []
		for ntIdx, symbol in enumerate(wordStatus.word):
			if is_nonterm(symbol):
				for rule in self.ruleDict[symbol]:
					newWord = self.apply_rule(wordStatus.word, ntIdx, rule.rhs)
					if rule.lhs in self.erasableNts:
						d = 0
					else:
						d = 1
					newWordStatus = cWordStatus(newWord, wordStatus.upperStrLen + rule.upperCnt, wordStatus.lowerStrLen + rule.lowerCnt, wordStatus.ntLen + rule.ntCnt - d, wordStatus, 0)
					if self.is_word_feasible(newWordStatus, goalStr):
						newWordStatus.distance = self.calculate_distance(newWord, goalStr)
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
