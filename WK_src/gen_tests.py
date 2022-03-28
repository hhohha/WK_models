#!/usr/bin/python3

import time
from ctf_WK_grammar import *

RES_OK = '\033[92m' + 'OK' + '\x1b[0m'
RES_FAILED = '\033[91m' + 'FAILED' + '\x1b[0m'

hline = '|---------------|-------------------------------------|------------------------------------------|--------------|------------|-----------------------|--------------|---------|'
testNo = 1

print(hline)
print('|               |   GRAMMAR                           |        STRING                            |   EXPECTED   |   ACTUAL   | STATES  (OPEN/CLOSED) | TIME TAKEN   | STATUS  |')
print(hline)
print(hline)

def runTest2(grammar: cWK_CFG, inputStr: str, expected: bool):
	global testNo

	start = time.time()
	openStates, closedStates, actual = grammar.can_generate(inputStr)
	end = time.time()
	timeTaken = round(end - start, 8)
	status = RES_OK if actual == expected else RES_FAILED

	print(f'| TEST {testNo:2}       | {g.desc:35} | {inputStr:40} |    {expected:6}    |    {actual:6}  | {openStates:10}/{closedStates:10} | {timeTaken:12} | {status:15}  |')
	#print(hline)
	testNo += 1

############################ GRAMMAR 1:   a(aa)*      #####################################################################################

rules: List[cRule] = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['a'], ['a'])])
]
g = cWK_CFG(['A'], ['a'], 'A', rules, [('a', 'a')])
g.desc = 'a(aa)*'

runTest2(g, '', False)
runTest2(g, 'a', True)
runTest2(g, 'aa', False)
runTest2(g, 'aaa', True)
runTest2(g, 'aaaaaaaaaaa', True)
runTest2(g, 'aaaaaaaaaaaa', False)

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

runTest2(g, 'ab', True)
runTest2(g, 'aaabbb', True)
runTest2(g, 'aaabb', False)
runTest2(g, 'abab', False)
runTest2(g, '', False)
runTest2(g, 'aabb', True)
runTest2(g, 'abc', False)

############################ GRAMMAR 3:   r^n d^n u^n r^n    ##############################################################################
rules: List[cRule] = [
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

runTest2(g, 'rdur', True)
runTest2(g, 'rrrrrrdddddduuuuuurrrrrr', True)
runTest2(g, 'rrrrrrdddddduuuuuuurrrrrr', False)
runTest2(g, 'rrrrrrddddduuuuuurrrrrr', False)

############################ GRAMMAR 4:   a^n c^n b^n    ##################################################################################

rules: List[cRule] = [
	cRule('S', [(['a'], []), 'S', (['b'], [])]),
	cRule('S', [(['a'], []), 'A', (['b'], [])]),
	cRule('A', [(['c'], ['a']), 'A']),
	cRule('A', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], [])])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g.desc = 'a^n c^n b^n'

runTest2(g, 'aaaaaaaaaaaaccccccccccccbbbbbbbbbbbb', True)
runTest2(g, 'aaaaaaaaaaaccccccccccccbbbbbbbbbbbb', False)

############################ GRAMMAR 5:   a^n b^m c^n d^m     ##############################################################################

rules: List[cRule] = [
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

runTest2(g, 'aaaabbbbbbbccccddddddd', True)
runTest2(g, 'aaaabbbbbbbccccdddddd', False)

############################ GRAMMAR 6:   wcw where w in {a,b }*     ######################################################################

rules: List[cRule] = [
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

runTest2(g, 'abbabacabbaba', True)
runTest2(g, 'abbabacababa', False)

############################ GRAMMAR 6:   a^n b^m a^n where 2n <= m <= 3n   ###############################################################
rules: List[cRule] = [
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
	runTest2(g, 'a'*n + 'b'*m + 'a'*n, 2*n <= m and m <= 3*n)

print(hline)
