#!/usr/bin/python3

# all rules must be in a form:
# A -> BC             tuple ('A', 'B', 'C')
# A -> a/lambda       tuple ('A', 'a', '')
# A -> lambda/a       tuple ('A', '', 'a')
# A -> lambda/lambda  tuple ('A', '', '')

#Algoritmus funguje jen pro gramatiku s relaci identity.
#Algoritmus funguje jen pro gramatiku v CNF.
#Slozitost n**6 jen pokud povazujeme pocet pravidel za konstant, jinak n**7.
#Chyba v radku 13 algoritmu (asi nema vliv na vysledek, ale zkousi pocitat nesmysly).

class cWKGrammarCNF:
	def __init__(self, ts, nts, rules, rel):
		self.ts = ts
		self.nts = nts
		self.rules = rules
		self.rel = rel

	def checkRules(self, idx1, idx2, target):
		if idx1 not in self.X or idx2 not in self.X:
			return
		for rule in self.rules:
			if rule[1] in self.X[idx1] and rule[2] in self.X[idx2]:
				self.addToX(target, rule[0])

	def computeSet(self, i, j, k ,l):
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


	def addToX(self, idx, nt):
		if idx not in self.X:
			self.X[idx] = []

		self.X[idx].append(nt)
		print(idx, nt)

	# sentence: tuple('upper', 'lower')
	def can_generate(self, sentence):
		n = len(sentence[0])
		self.X = {}

		for i, word in enumerate(sentence[0]):
			for rule in self.rules:
				if rule[1] == word and rule[2] == '':
					self.addToX((i+1, i+1, 0, 0), rule[0])
		for i, word in enumerate(sentence[1]):
			for rule in self.rules:
				if rule[2] == word and rule[1] == '':
					self.addToX((0, 0, i+1, i+1), rule[0])

		for y in range(2, 2*n+1):
			for beta in range(max(y - n, 0), min(n, y)+1):
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

		return (1, n, 1, n) in self.X and self.nts[0] in self.X[(1, n, 1, n)]


ts = []
nts = ['S']
rules = [
	('S', 'S', 'S'),
	('S', 'Tua', 'Y1'),
	('Y1', 'Tda', 'Y2'),
	('Y2', 'S', 'Y3'),
	('Y3', 'Tub', 'Tdb'),
	('S', 'Tua', 'S'),
	('S', 'Tua', 'A'),
	('A', 'Tub', 'Y4'),
	('Y4', 'Tda', 'A'),
	('A', 'Tub', 'Y5'),
	('Y5', 'Tda', 'B'),
	('A', 'Tub', 'Tda'),
	('B', 'Tdb', 'B'),
	('B', '', 'b'),
	('B', 'B', 'B'),
	('B', 'Tua', 'Y6'),
	('Y6', 'Tda', 'Y7'),
	('Y7', 'S', 'Y8'),
	('Y8', 'Tub', 'Tdb'),
	('B', 'Tua', 'S'),
	('B', 'Tua', 'A'),
	('Tua', 'a', ''),
	('Tub', 'b', ''),
	('Tda', '', 'a'),
	('Tdb', '', 'b')
]
rel = None

g = cWKGrammarCNF(ts, nts, rules, rel)

s = 'abababab'
print(g.can_generate((s, s)))
