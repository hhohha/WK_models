#!/usr/bin/python3

import time, sys
sys.path.append("../")

from lib.ctf_WK_grammar import *

RES_TIMEOUT = '\033[93m' + 'TIMEOUT' + '\x1b[0m'
RES_OK = '\033[92m' + 'OK' + '\x1b[0m'
RES_FAILED = '\033[91m' + 'FAILED' + '\x1b[0m'

totalTime = 0
statesO, statesC = 0, 0

hline = '|---------------|-------------------------------------|------------------------------------------|--------------|------------|-----------------------|--------------|---------|'
testNo = 1

print(hline)
print('|               |   GRAMMAR                           |        STRING                            |   EXPECTED   |   ACTUAL   | STATES  (OPEN/CLOSED) | TIME TAKEN   | STATUS  |')
print(hline)
print(hline)

def runTest(grammar: cWK_CFG, inputStr: str, expected: bool):
	global testNo, totalTime, statesO, statesC

	#grammar.to_wk_cnf()

	start = time.time()
	openStates, closedStates, prunes, actual = grammar.run_tree_search(inputStr)
	statesO += openStates
	statesC += closedStates
	#openStates, closedStates, actual = 0, 0, grammar.run_wk_cyk(inputStr)
	end = time.time()
	timeTaken = round(end - start, 8)
	totalTime += timeTaken

	if actual is None:
		status = RES_TIMEOUT
		actual = ''
	else:
		status = RES_OK if actual == expected else RES_FAILED

	print(f'| TEST {testNo:2}       | {g.desc:35} | {inputStr:40} |    {expected:6}    |    {actual:6}  | {openStates:10}/{closedStates:10} | {timeTaken:12} | {status:16} |')
	#print(hline)
	testNo += 1

############################ GRAMMAR 1:   a(aa)*      #####################################################################################

rules: List[cRule] = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['a'], ['a'])])
]
g = cWK_CFG(['A'], ['a'], 'A', rules, [('a', 'a')])
g.desc = 'a(aa)*'

runTest(g, '', False)
runTest(g, 'a', True)
runTest(g, 'aa', False)
runTest(g, 'aaa', True)
runTest(g, 'aaaaaaaaaaa', True)
runTest(g, 'aaaaaaaaaaaa', False)

############################ GRAMMAR 2:   a^n b^n (n>0)    ################################################################################
rules  = [
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], ['a']), 'A']),
	cRule('A', [(['b'], ['a']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], ['b'])])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g.desc = 'a^n b^n (n>0)'

runTest(g, 'ab', True)
runTest(g, 'aaabbb', True)
runTest(g, 'aaabb', False)
runTest(g, 'abab', False)
runTest(g, '', False)
runTest(g, 'aabb', True)
runTest(g, 'abc', False)

############################ GRAMMAR 3:   r^n d^n u^n r^n    ##############################################################################
rules = [
	cRule('S', [(['r'], []), 'S']),
	cRule('S', [(['r'], []), 'A']),
	cRule('A', [(['d'], ['r']), 'A']),
	cRule('A', [(['d'], ['r']), 'B']),
	cRule('B', [(['u'], ['d']), 'B']),
	cRule('B', [(['u'], ['d']), 'C']),
	cRule('C', [(['r'], ['u']), 'C']),
	cRule('C', [(['r'], ['u']), 'D']),
	cRule('D', [([], ['r']), 'D']),
	cRule('D', [([], ['r'])])
]

g = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['r', 'd', 'u'], 'S', rules, [('r', 'r'), ('d', 'd'), ('u', 'u')])
g.desc = 'r^n d^n u^n r^n'

runTest(g, 'rdur', True)
runTest(g, 'rrrrrrdddddduuuuuurrrrrr', True)
runTest(g, 'rrrrrrdddddduuuuuuurrrrrr', False)
runTest(g, 'rrrrrrddddduuuuuurrrrrr', False)

############################ GRAMMAR 4:   a^n c^n b^n    ##################################################################################

rules = [
	cRule('S', [(['a'], []), 'S', (['b'], [])]),
	cRule('S', [(['a'], []), 'A', (['b'], [])]),
	cRule('A', [(['c'], ['a']), 'A']),
	cRule('A', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], [])])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g.desc = 'a^n c^n b^n'

runTest(g, 'aaaaaaaaaaaaccccccccccccbbbbbbbbbbbb', True)
runTest(g, 'aaaaaaaaaaaccccccccccccbbbbbbbbbbbb', False)

############################ GRAMMAR 5:   a^n b^m c^n d^m     ##############################################################################

rules = [
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], []), 'A']),
	cRule('A', [(['b'], []), 'B']),
	cRule('B', [(['c'], ['a']), 'B']),
	cRule('B', [(['c'], ['a']), 'C']),
	cRule('C', [(['d'], ['b']), 'C']),
	cRule('C', [(['d'], ['b']), 'D']),
	cRule('D', [([], ['c']), 'D']),
	cRule('D', [([], ['d']), 'D']),
	cRule('D', [([], [])])
]

g = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['a', 'b', 'c', 'd'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
g.desc = 'a^n b^m c^n d^m'

runTest(g, 'aaaabbbbbbbccccddddddd', True)
runTest(g, 'aaaabbbbbbbccccdddddd', False)

############################ GRAMMAR 6:   wcw where w in {a,b }*     ######################################################################

rules = [
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['b'], []), 'S']),
	cRule('S', [(['c'], []), 'A']),
	cRule('A', [(['a'], ['a']), 'A']),
	cRule('A', [(['b'], ['b']), 'A']),
	cRule('A', [([], ['c']), 'B']),
	cRule('B', [([], ['a']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], [])]),
]

g = cWK_CFG(['S', 'A', 'B', 'C'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g.desc = 'wcw where w in {a,b }*'

runTest(g, 'abbabacabbaba', True)
runTest(g, 'abbabacababa', False)

############################ GRAMMAR 7:   a^n b^m a^n where 2n <= m <= 3n   ###############################################################
rules = [
	cRule('S', [(['a'], []), 'S', (['a'], ['a'])]),
	cRule('S', [(['a'], []), 'A', (['a'], ['a'])]),
	cRule('A', [(['b', 'b'], ['a']), 'A']),
	cRule('A', [(['b', 'b', 'b'], ['a']), 'A']),
	cRule('A', [([], ['b']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], [])])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g.desc = 'a^n b^m a^n where 2n <= m <= 3n'

for m, n in [(m, n) for m in range(1, 7) for n in range (1, 7)]:
	runTest(g, 'a'*n + 'b'*m + 'a'*n, 2*n <= m and m <= 3*n)

print(hline)

print(f'\n\ntotal time taken: {totalTime},     states open: {statesO},   states closed: {statesC}')
