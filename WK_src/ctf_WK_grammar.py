#!/usr/bin/python3

class cWordStatus:
	def __init__(self):
		self.word = None
		self.upperStrLen = None
		self.lowerStrLen = None
		self.ntCnt = None
		self.firstNt = None # is this useful?

class cWK_CFG:
	def __init__(self, nts, ts, startSymbol, rules, relation):
		self.nts = nts
		self.ts = ts
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = relation

		if not self.is_consistent():
			raise ValueError

		self ruleDict = {}
		for nt in self.nts:
			ruleDict[nt] = []
		for rule in rules:
			self.ruleDict[rule[0]].append(rule[1])

	def is_consistent(self):
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

	def can_generate(self, upperStr):
		openQueue = [[self.startSymbol]]
		closedQueue = set()

		while openQueue:
			currentWord = openQueue.pop(0)
			closedQueue.add(currentWord)

			for nextWord in self.get_next_states(currentWord):
				if self.is_result(nextWord, upperStr):
					return True
				if nextWord not in openQueue and nextWord not in closedQueue:
					openQueue.append(nextWord)

		return False

	def is_result(word, goal):
		return len(word) == 1 and word[0] == goal

	def get_all_next_states(self, word):
		ntIdx = None
		for i, s in enumerate(word):
			if s in self.nts:
				ntIdx = i
		if ntIdx is None:
			return

		nt = word[ntIdx]
		for rule in self.ruleDict[nt]:
			newWord = self.apply_rule(word, ntIdx, rule)
			if newWord:
				yield newWord

	def get_NT_idxs(self, word):
		for idx, s in enumerate(word):
			if s in self.nts:
				yield idx

	def apply_rule(self, word, ntIdx, rule):
