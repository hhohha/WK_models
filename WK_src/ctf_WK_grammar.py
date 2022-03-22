#!/usr/bin/python3

class cWordStatus:
	def __init__(self, word, upperStrLen, lowerStrLen, ntLen):
		self.word = word
		self.upperStrLen = upperStrLen
		self.lowerStrLen = lowerStrLen
		self.ntLen = ntLen

def tuplify(l):
	if type(l) == list:
		return tuple(tuplify(x) for x in l)
	else:
		return l

def wordToStr(word):
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
	def __init__(self, nts, ts, startSymbol, rules, relation):
		self.nts = nts
		self.ts = ts
		self.startSymbol = startSymbol
		self.rules = rules
		self.relation = relation

		#if not self.is_consistent():
			#raise ValueError

		#TODO make rules compact: A -> (a lambda)(lambda a) == A -> (a a)
		self.ruleDict = {}
		for nt in self.nts:
			self.ruleDict[nt] = []
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
		openQueue = [tuple(self.startSymbol)]
		openSet = set(tuple(self.startSymbol))
		closedQueue = set()
		cnt = 0

		while openQueue:
			if cnt == 15000:
				print('taking too long')
				return None
			else:
				cnt += 1
			#print(f'cnt: {cnt}')
			currentWord = openQueue.pop(0)
			closedQueue.add(currentWord)

			for nextWord in self.get_all_next_states(currentWord):
				if self.is_result(nextWord, upperStr):
					return True
				if nextWord not in openSet and nextWord not in closedQueue:
				#if nextWord not in openQueue:
					openQueue.append(nextWord)
					openSet.add(nextWord)

		return False

	def is_result(self, word, goal):
		return len(word) == 1 and ''.join(word[0][0]) == goal

	def is_rule_applicable(self, word, ntIdx, rule):
		return True

	def get_all_next_states(self, word):
		#print(f'{wordToStr(word)}  --->  ')
		for ntIdx, symbol in enumerate(word):
			if not isinstance(symbol, list) and not isinstance(symbol, tuple): # terminals are tuples so symbol is a non terminal
				for rule in self.ruleDict[symbol]:
					if self.is_rule_applicable(word, ntIdx, rule):
						yield self.apply_rule(word, ntIdx, rule)
		#print('\n\n')


	def apply_rule(self, word, ntIdx, rule):
		#print(f'word: {wordToStr(word)}')
		#print(f'ntIdx: {ntIdx}')
		#print(rule)
		#print(f'rule: {word[ntIdx] + " -> " + wordToStr(rule):20}\n')

		isTerm = len(rule) == 1 and (isinstance(rule, list) or isinstance(rule, tuple))   # rule right side is just a terminal
		mergePrev = ntIdx > 0 and (isinstance(word[ntIdx - 1], list) or isinstance(word[ntIdx - 1], tuple)) # can we merge with the previous terminal
		mergeNext = ntIdx < len(word) - 1 and (isinstance(word[ntIdx + 1], list) or isinstance(word[ntIdx + 1], tuple))# can we merge with the next terminal

		if isTerm:
			if mergePrev and mergeNext:
				mergedUpper = word[ntIdx - 1][0] + rule[0][0] + word[ntIdx + 1][0]
				mergedLower = word[ntIdx - 1][1] + rule[0][1] + word[ntIdx + 1][1]
				return word[:ntIdx - 1] + tuple([(mergedUpper, mergedLower)]) + word[ntIdx + 2:]

			elif mergePrev:
				mergedUpper = word[ntIdx - 1][0] + rule[0][0]
				mergedLower = word[ntIdx - 1][1] + rule[0][1]
				return word[:ntIdx - 1] + tuple([(mergedUpper, mergedLower)]) + word[ntIdx + 1:]

			elif mergeNext:
				mergedUpper = rule[0][0] + word[ntIdx + 1][0]
				mergedLower = rule[0][1] + word[ntIdx + 1][1]
				return word[:ntIdx] + tuple([(mergedUpper, mergedLower)]) + word[ntIdx + 2:]

			else:
				return word[:ntIdx] + tuple([rule[0]]) + word[ntIdx + 1:]

		mergePrev = mergePrev and (isinstance(rule[0], list) or isinstance(rule[0], tuple))
		mergeNext = mergeNext and (isinstance(rule[-1], list) or isinstance(rule[-1], tuple))

		if mergePrev and mergeNext:
			mergedUpperPrev = word[ntIdx - 1][0] + rule[0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + rule[0][1]
			mergedUpperNext = rule[-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = rule[-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx - 1] + tuple([(mergedUpperPrev, mergedLowerPrev)]) + rule[1:-1] + [(mergedUpperNext, mergedLowerNext)] + word[ntIdx + 2:]
		elif mergePrev:
			mergedUpperPrev = word[ntIdx - 1][0] + rule[0][0]
			mergedLowerPrev = word[ntIdx - 1][1] + rule[0][1]
			return word[:ntIdx - 1] + tuple([(mergedUpperPrev, mergedLowerPrev)]) + rule[1:] + word[ntIdx + 1:]
		elif mergeNext:
			mergedUpperNext = rule[-1][0] + word[ntIdx + 1][0]
			mergedLowerNext = rule[-1][1] + word[ntIdx + 1][1]
			return word[:ntIdx] + rule[:-1] + tuple([(mergedUpperNext, mergedLowerNext)]) + word[ntIdx + 2:]
		else:
			return word[:ntIdx] + rule + word[ntIdx + 1:]


nts = ['A']
ts = ['a']
startSymbol = 'A'
rules = [
	('A', ('A', 'A')),
	('A', tuplify([[['a'], ['a']]]))
]
relation = [('a', 'a')]
g = cWK_CFG(nts, ts, startSymbol, rules, relation)

res = g.can_generate('aaaaaa')
print(f'RESULT: {res}')

#for x in g.get_all_next_states([(['a', 'a'], ['a', 'a']), 'A']):
	#print(f'-----> {wordToStr(x)}\n\n\n')
