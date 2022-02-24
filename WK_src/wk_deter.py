#!/usr/bin/python3

# rule form:
#	q0 (w1 w2) --> q1 : tuple (q0, w1, w2, q1)

class cWKA:
	def __init__(self, alphabet, states, rules, finalStates, startState, complRel):
		self.alphabet = alphabet
		self.states = states
		self.rules = rules
		self.finalStates = finalStates
		self.startState = startState
		self.complRel = complRel

		#TODO - check that the definition of wka is consistent

		#ruleDict - key is stateFrom, value is list of tuples (upperStr, lowerStr, stateTo)
		self.ruleDict = {}
		for state in self.states:
			ruleDict[state] = []

		for rule in self.rules:
			self.ruleDict[rule[0]].append((rule[1], rule[2], rule[3]))

	def relation_is_identity(self):
		for a, b in self.complRel:
			if a != b:
				return False

		for c in self.alphabet:
			if (c, c) not in self.complRel:
				return False
		return True

	def is_weakly_deterministic(self):
		pass

	def is_strongly_deterministic(self):
		return self.is_deterministic() and self.relation_is_identity()

	def is_deterministic(self):
		ruleDict = {}
		for rule in self.rules:
			stateFrom = rule[0]
			if stateFrom in ruleDict:
				 for upperStr, lowerStr in ruleDict[stateFrom]:
					 if (rule[1].startswith(upperStr) or upperStr.startswith(rule[1])) and (rule[2].startswith(lowerStr) or lowerStr.startswith(rule[2])):
						 return False
			else:
				ruleDict[stateFrom] = []

			ruleDict[stateFrom].append((rule[1], rule[2]))

		return True


	def run(self, upperStr):
		if self.is_strongly_deterministic():
			# lowerStr == upperStr - means we don't need the lower at all, just the indexes
			idxU = idxL = 0

			curState = self.startState
			while idxU < len(upperStr) or idxL < len(upperStr):
				chosenRule = None
				for rule in self.ruleDict[curState]:
					if upperStr.startswith(rule[1], idxU) and upperStr.startswith(rule[2], idxL):
						chosenRule = rule
						break

				if chosenRule is None:
					return False

				idxU += len(chosenRule[1])
				idxL += len(chosenRule[2])
				curState = chosenRule[3]

			return curState in self.finalStates










# following automaton is weakly deterministic, but not deterministic
states = ['q0', 'q1', 'q2', 'q3', 'q4']
rules = [
	('q0', 'a', '', 'q1'),
	('q0', '', 'b', 'q2'),
	('q1', 'a', '', 'q1'),
	('q1', 'b', 'a', 'q3'),
	('q3', 'b', 'a', 'q3'),
	('q3', '', 'b', 'q3'),
	('q2', '', 'b', 'q2'),
	('q2', 'b', 'a', 'q4'),
	('q4', 'b', 'a', 'q4'),
	('q4', 'a', '', 'q4')
]
finalStates = ['q3', 'q4']
startState = 'q0'
rel = [('a', 'a'), ('b', 'b')]

wka = cWKA(['a', 'b'], states, rules, finalStates, startState, rel)
print(wka.is_deterministic())
print(wka.is_strongly_deterministic())
