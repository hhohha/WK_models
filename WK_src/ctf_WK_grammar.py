#!/usr/bin/python3

from typing import Dict, List, Tuple, Set, TypeVar, Optional

tNonTerm = str
tTerm = str
tTermLetter = Tuple[List[tTerm], List[tTerm]]
tLetter = TypeVar("tLetter", tNonTerm, tTermLetter)
tWord = List[tLetter]
tRule = Tuple[tNonTerm, tWord]
tRelation = Tuple[tTerm, tTerm]

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

def tuplify(l):
	if type(l) == list:
		return tuple(tuplify(x) for x in l)
	else:
		return l

def wordToStr(word: tWord) -> str:
	rs = []
	for symbol in word:
		if isinstance(symbol, list) or isinstance(symbol, tuple):
			e1 = ''.join(symbol[0]) if len(symbol[0]) > 0 else 'λ'
			e2 = ''.join(symbol[1]) if len(symbol[1]) > 0 else 'λ'
			rs.append(e1 + '/' + e2)
		else:
			rs.append(symbol)

	return(f'{" ".join(rs)}')

class cWK_CFG:
	def __init__(self, nts: List[tNonTerm], ts: List[tTerm], startSymbol: tNonTerm, rules: List[tRule], relation: List[tRelation]) -> None:
		self.nts = nts
		self.ts = ts
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = relation

		#if not self.is_consistent():
			#raise ValueError

		#TODO make rules compact: A -> (a lambda)(lambda a) == A -> (a a)
		self.ruleDict: dict[tNonTerm, List[tWord]] = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
		for rule in rules:
			self.ruleDict[rule[0]].append(rule[1])

	def is_consistent(self) -> bool:
		if self.startSymbol not in self.nts:
			return False

		for t in self.ts:
			if t in self.nts:
				return False

		for rule in self.rules:
			if rule[0] not in self.nts:
				return False
			for symbol in rule[1]:
				if symbol not in self.nts and symbol not in self.ts:
					return False

		for r in self.relation:
			if r[0] not in self.ts or r[1] not in self.ts:
				return False

		return True

	def printPath(self, wordStatus: cWordStatus) -> None:
		currentWordStatus: Optional[cWordStatus] = wordStatus
		while currentWordStatus:
			print(f' >>> {wordToStr(currentWordStatus.word)}')
			currentWordStatus = currentWordStatus.parent


	def can_generate(self, upperStr: str) -> int:
		initStatus = cWordStatus([self.startSymbol], 0, 0, 1, None)
		openQueue: List[cWordStatus] = [initStatus]
		openSet: Set[int] = set()
		openSet.add(initStatus.hashNo)
		closedSet: Set[int] = set()
		cnt = 0

		while openQueue:
			if cnt == 150000:
				print('taking too long')
				return -1
			else:
				cnt += 1
			print(f'cnt: {cnt}')
			currentWordStatus = openQueue.pop(0)
			closedSet.add(currentWordStatus.hashNo)

			for nextWordStatus in self.get_all_next_states(currentWordStatus, len(upperStr)):
				if self.is_result(nextWordStatus.word, upperStr):
					self.printPath(nextWordStatus)
					return True
				if nextWordStatus.hashNo not in openSet and nextWordStatus.hashNo not in closedSet:
					openQueue.append(nextWordStatus)
					openSet.add(nextWordStatus.hashNo)

		return False

	def is_result(self, word: tWord, goal: str) -> bool:
		return len(word) == 1 and ''.join(word[0][0]) == goal

	def is_rule_applicable(self, word, ntIdx, rule, maxLen):
		return len(word) + len(rule) <= maxLen

	def get_all_next_states(self, wordStatus: cWordStatus, maxLen: int) -> List[cWordStatus]:
		retLst: List[cWordStatus] = []
		for ntIdx, symbol in enumerate(wordStatus.word):
			if not isinstance(symbol, list) and not isinstance(symbol, tuple): # terminals are tuples so symbol is a non terminal
				for ruleRhs in self.ruleDict[symbol]:
					if self.is_rule_applicable(wordStatus.word, ntIdx, ruleRhs, maxLen):
						newWord = self.apply_rule(wordStatus.word, ntIdx, ruleRhs)

						upperStrLen = wordStatus.upperStrLen + 0
						lowerStrLen = wordStatus.lowerStrLen + 0
						ntLen = wordStatus.ntLen + 0

						retLst.append(cWordStatus(newWord, upperStrLen, lowerStrLen, ntLen, wordStatus))
						#yield cWordStatus(newWord, 0, 0, 1)
		return retLst


	def apply_rule(self, word: tWord, ntIdx: int, ruleRhs: tWord) -> tWord:
		print(f'word: {wordToStr(word)}')
		print(f'ntIdx: {ntIdx}')
		print(ruleRhs)
		print(f'rule: {word[ntIdx] + " -> " + wordToStr(ruleRhs):20}\n')

		isTerm = len(ruleRhs) == 1 and isinstance(ruleRhs[0], tuple)   # rule right side is just a terminal
		mergePrev = ntIdx > 0 and isinstance(word[ntIdx - 1], tuple) # can we merge with the previous terminal
		mergeNext = ntIdx < len(word) - 1 and isinstance(word[ntIdx + 1], tuple) # can we merge with the next terminal

		if isTerm:
			if mergePrev and mergeNext:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1] + word[ntIdx + 1][1]
				return word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			elif mergePrev:
				mergedUpper = word[ntIdx - 1][0] + ruleRhs[0][0]
				mergedLower = word[ntIdx - 1][1] + ruleRhs[0][1]
				return word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 1:]

			elif mergeNext:
				mergedUpper = ruleRhs[0][0] + word[ntIdx + 1][0]
				mergedLower = ruleRhs[0][1] + word[ntIdx + 1][1]
				return word[:ntIdx] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			else:
				return word[:ntIdx] + [ruleRhs[0]] + word[ntIdx + 1:]

		mergePrev = mergePrev and  isinstance(ruleRhs[0], tuple)
		mergeNext = mergeNext and isinstance(ruleRhs[-1], tuple)

		if mergePrev and mergeNext:
			mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
			mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
		elif mergePrev:
			mergedUpperPrev = word[ntIdx - 1][0] + ruleRhs[0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + ruleRhs[0][1]
			return word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + ruleRhs[1:] + word[ntIdx + 1:]
		elif mergeNext:
			mergedUpperNext = ruleRhs[-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = ruleRhs[-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx] + ruleRhs[:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
		else:
			return word[:ntIdx] + ruleRhs + word[ntIdx + 1:]


nts: List[tNonTerm] = ['A']
ts: List[tTerm] = ['a']
startSymbol: tNonTerm = 'A'
rules: List[tRule] = [
	('A', ['A', 'A', 'A']),
	('A', [(['a'], ['a'])])
	#('A', tuplify([[['a'], ['a']]]))
]
relation: List[tRelation] = [('a', 'a')]
g = cWK_CFG(nts, ts, startSymbol, rules, relation)

res = g.can_generate('aaaaaa')
print(f'RESULT: {res}')

#for x in g.get_all_next_states([(['a', 'a'], ['a', 'a']), 'A']):
	#print(f'-----> {wordToStr(x)}\n\n\n')
