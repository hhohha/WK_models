#!/usr/bin/python3

import time, random
from grammars import g1, g2, g3, g4, g5, g6, g7, g8

class cPerfTester:
	def __init__(self):
		self.testCnt = 0
		self.timeTaken = 0
		self.statesOpen = 0
		self.statesClosed = 0

	def printHeader(self, grammar, inputStr, shouldAccept):
		if len(inputStr) > 90:
			inputStr = inputStr[:80] + f'... [length {len(inputStr)}]'

		print(f'|{"="*150}|')
		print(f'| TEST {self.testCnt:3}{" "*141}|')
		print(f'|{"="*150}|')
		print(f'| GRAMMAR{" "*35}| {grammar.desc:105}|')
		lengths = f'{len(grammar.rules)} / {len(grammar.nts)} / {len(grammar.ts)}'
		print(f'| RULES / NON-TERMINALS / TERMINALS COUNT   | {lengths:105}|')
		print(f'| INPUT STRING{" "*30}| {inputStr:105}|')
		print(f'| SHOULD ACCEPT{" "*29}| {("Yes" if shouldAccept else "No"):105}|')
		print(f'| TIMEOUT{" "*35}| {str(grammar.timeLimit):105}|')
		print(f'|{"-"*150}|')
		print(f'| STRATEGY{" "*87}| TIME TAKEN | STATES (ANALYSED/GENERATED) | ACCEPTED |')
		print(f'|{"-"*150}|')

	def run_test_suite(self, grammar, inputStr, shouldAccept, times=1):
		self.testCnt += 1
		self.printHeader(grammar, inputStr, shouldAccept)

		for idx, t in enumerate(grammar.distance_calc_strategies_list):
			grammar.distance_calc_strategy = idx
			avgTime = 0
			avgStates = 0
			timeouted = False

			for i in range(times):
				start = time.time()
				openStates, closedStates, actual = grammar.can_generate(inputStr)
				end = time.time()
				timeTaken = round(end - start, 5)
				avgTime += timeTaken
				avgStates += openStates
				if actual is None:
					timeouted = True

			avgTime = round(avgTime / times, 5)
			avgStates = round(avgStates / times)

			strategy = grammar.distance_calc_strategies_list[idx][0]  # TODO - ugly, refactor
			if timeouted:
				result = "TIMEOUT"
			elif actual == shouldAccept:
				result = actual
			else:
				result = "ERROR"
			states = str(openStates) + "/" + str(closedStates) + " - " + str(grammar.trimms).replace(' ', '')
			print(f'| {strategy:95}| {avgTime:10} | {avgStates:28}| {result:8} |')
		print(f'|{"-"*150}|')

		grammar.backup()
		grammar.to_wk_cnf()
		lengths = f'{len(grammar.rules)} / {len(grammar.nts)} / {len(grammar.ts)}'
		print(f'| Transformed to WK CNF - RULES / NON-TERMINALS / TERMINALS: {lengths:89} |')
		print(f'|{"-"*150}|')

		for idx, t in enumerate(grammar.distance_calc_strategies_list):
			grammar.distance_calc_strategy = idx
			avgTime = 0
			avgStates = 0
			timeouted = False

			for i in range(times):
				start = time.time()
				openStates, closedStates, actual = grammar.can_generate(inputStr)
				end = time.time()
				timeTaken = round(end - start, 5)
				avgTime += timeTaken
				avgStates += openStates
				if actual is None:
					timeouted = True

			avgTime = round(avgTime / times, 5)
			avgStates = round(avgStates / times)

			strategy = grammar.distance_calc_strategies_list[idx][0]  # TODO - ugly, refactor
			if timeouted:
				result = "TIMEOUT"
			elif actual == shouldAccept:
				result = actual
			else:
				result = "ERROR"
			states = str(openStates) + "/" + str(closedStates) + " - " + str(grammar.trimms).replace(' ', '')
			print(f'| {strategy:95}| {avgTime:10} | {avgStates:28}| {result:8} |')

		print(f'|{"-"*150}|')
		start = time.time()
		actual = grammar.run_wk_cyk(inputStr)
		end = time.time()
		timeTaken = round(end - start, 5)
		strategy = 'wk cyk'
		closedStates = 'N/A'
		if actual is None:
			result = "TIMEOUT"
		elif actual == shouldAccept:
			result = actual
		else:
			result = "ERROR"

		print(f'| {strategy:95}| {timeTaken:10} | N/A{" "*25}| {result:8} |')
		print(f'|{"="*150}|\n\n\n')
		grammar.restore()

t = cPerfTester()
#t.run_test_suite(g1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', True)
#t.run_test_suite(g2, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', True)
#t.run_test_suite(g3, 'rrrrrrrrrrrrrrrrrddddddddddddddddduuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrr', True)
#t.run_test_suite(g4, 'aaaaaaaaaaaaaaaaaaaaccccccccccccccccccccbbbbbbbbbbbbbbbbbbbb', True)
#t.run_test_suite(g5, 'aaaaaaaaaabbbbbbbbbbbbbbbbbbbbccccccccccdddddddddddddddddddd', True)
#t.run_test_suite(g6, 'ababbabababaaababbbabbbbaacababbabababaaababbbabbbbaa', True)
#t.run_test_suite(g7, 'aaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaa', True)

# ------------- LEVEL 2 ---------------
t.run_test_suite(g1, 'a'*401, True)
t.run_test_suite(g2, 'a'*400 + 'b'*400, True)
l = 300
t.run_test_suite(g3, 'r'*l + 'd'*l + 'u'*l + 'r'*l, True)
t.run_test_suite(g4, 'a'*l + 'c'*l + 'b'*l, True)
t.run_test_suite(g5, 'a'*(l+10) + 'b'*l + 'c'*(l+10) + 'd'*l , True)

s = ''.join([random.choice(['a','b']) for i in range(l)])
t.run_test_suite(g6, s + 'c' + s, True)

n, m = 100, 250
t.run_test_suite(g7, 'a'*n + 'b'*m + 'a'*n, True)
t.run_test_suite(g8, 'aaaaaaaaaaaaaabbbbbbbbbbbbbbaabbab', True)

# ------------- NEGATIVE ----------------
#t.run_test_suite(g1, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa', False)
#t.run_test_suite(g2, 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb', False)
#t.run_test_suite(g3, 'rrrrrrrrrrrrrrrrrddddddddddddddddduuuuuuuuuuuuuuuuurrrrrrrrrrrrrrrrrr', False)
#t.run_test_suite(g4, 'aaaaaaaaaaaaaaaaaaaaccccccccccccccccccccbbbbbbbbbbbbbbbbbbbbb', False)
#t.run_test_suite(g5, 'aaaaaaaaaabbbbbbbbbbbbbbbbbbbbccccccccccddddddddddddddddddddd', False)
#t.run_test_suite(g6, 'ababbabababaaababbbabbbbaacababbabababaaababbbabbbbaaa', False)
#t.run_test_suite(g7, 'aaaaaaaaaabbbbbbbbbbbbbbbbbbbbbbbbbaaaaaaaaaaa', False)
#t.run_test_suite(g8, 'aaaaabbbbbb', False)

