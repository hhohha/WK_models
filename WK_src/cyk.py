#!/usr/bin/python3

class cCFG:
	def __init__(self, terminals, nonterminals, rules):
		self.terminals = terminals
		self.nonterminals = nonterminals
		self.rules = rules
		self.start_nt = nonterminals[0]

	def can_generate(self, sentence):
		P = {}
		n  = len(sentence)

		for s, word in enumerate(sentence):
			for rule in rules:
				if rule[1] == word:
					P[(1, s + 1, rule[0])] = True

		for l in range(2, n + 1):
			for s in range(1, n - l + 2):
				for p in range(1, l):
					for rule in rules:
						if (p, s, rule[1]) in P and (l-p, s+p, rule[2]) in P:
							P[(l, s, rule[0])] = True

		#print(P)
		return (n, 1, 'S') in P

ts = ['she', 'eats', 'fish', 'with' 'a', 'fork']
nts = ['S', 'VP', 'PP', 'NP', 'V', 'P', 'N', 'Det']
rules = [
	('S', 'NP', 'VP'),
	('VP', 'VP', 'PP'),
	('VP', 'V', 'NP'),
	('VP', 'eats', ''),
	('PP', 'P', 'NP'),
	('NP', 'Det', 'N'),
	('NP', 'she', ''),
	('V', 'eats', ''),
	('P', 'with', ''),
	('N', 'fish', ''),
	('N', 'fork', ''),
	('Det', 'a', '')
]

myGrammar = cCFG(ts, nts, rules)

#sentence = ['she', 'eats', 'a', 'fish', 'with', 'a', 'fork']
sentence = ['a', 'fish', 'eats', 'she', 'with', 'she']

print(myGrammar.can_generate(sentence))
