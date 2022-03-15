#!/usr/bin/python3

#class cWordStatus:
	#def __init__(self, word, upperStrLen, lowerStrLen):
		#self.word = word
		#self.upperStrLen = upperStrLen
		#self.lowerStrLen = lowerStrLen

#class cNonTerminal:
	#def __init__(self, sign)
		#self.sign = sign

#class cTerminal:
	#def __init__(self, sign)
		#self.sign = sign

#class cRule:
	#def __init__(self, lhs, rhs):
		#self.lhs = lhs
		#self.rhs = rhs


class cWK_CFG:
	def __init__(self, nts, ts, startSymbol, rules, relation):
		self.nts = nts
		self.ts = ts
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = relation

		if not self.is_consistent():
			raise ValueError

		#TODO make rules compact: A -> (a lambda)(lambda a) == A -> (a a)
		self.ruleDict = {}
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
		#initStatus = cWordStatus([self.startSymbol], 0, 0)
		#openQueue = [initStatus]
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
		for ntIdx, symbol in enumerate(word):
			if not isinstance(symbol, list): # terminals are tuples so symbol is a non terminal
				for rule in self.ruleDict[symbol]:
					newWord = self.apply_rule(word, ntIdx, rule)
					if newWord:
						yield newWord

	def apply_rule(self, word, ntIdx, rule):
		isTerm = len(rule[1]) == 1 and isinstance(rule[1], list)   # rule right side is just a terminal
		mergePrev = ntIdx > 0 and isinstance(word[ntIdx - 1], list)  # can we merge with the previous terminal
		mergeNext = ntIdx < len(word) - 1 and isinstance(word[ntIdx + 1], list) # can we merge with the next terminal

		if isTerm:
			if mergePrev and mergeNext:
				mergedUpper = word[ntIdx - 1][0] + rule[1][0][0] + word[ntIdx + 1][0]
				mergedLower = word[ntIdx - 1][1] + rule[1][0][1] + word[ntIdx + 1][1]
				return word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			elif mergePrev:
				mergedUpper = word[ntIdx - 1][0] + rule[1][0][0]
				mergedLower = word[ntIdx - 1][1] + rule[1][0][1]
				return word[:ntIdx - 1] + [(mergedUpper, mergedLower)] + word[ntIdx + 1:]

			elif mergeNext:
				mergedUpper = rule[1][0][0] + word[ntIdx + 1][0]
				mergedLower = rule[1][0][1] + word[ntIdx + 1][1]
				return word[:ntIdx] + [(mergedUpper, mergedLower)] + word[ntIdx + 2:]

			else:
				return word[:ntIdx] + [rule[1][0]] + word[ntIdx + 1:]

		mergePrev = mergePrev and isinstance(rule[1][0], list)
		mergeNext = mergeNext and isinstance(rule[1][-1], list)

		if mergePrev and mergeNext:
			mergedUpperPrev = word[ntIdx - 1][0] + rule[1][0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + rule[1][0][1]
			mergedUpperNext = rule[1][-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = rule[1][-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + rule[1][1:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
		elif mergePrev:
			mergedUpperPrev = word[ntIdx - 1][0] + rule[1][0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + rule[1][0][1]
			return word[:ntIdx - 1] + [(mergedUpperPrev, mergedLowerPrev)] + rule[1][1:] + word[ntIdx + 1:]
		elif mergeNext:
			mergedUpperNext = rule[1][-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = rule[1][-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx] + rule[1][:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
		else:
			return word[:ntIdx] + rule[1] + word[ntIdx + 1:]


