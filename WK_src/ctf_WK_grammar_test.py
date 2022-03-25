#!/usr/bin/python3

from ctf_WK_grammar import *

RES_OK = '\033[92m' + 'OK' + '\x1b[0m'
RES_FAILED = '\033[91m' + 'FAILED' + '\x1b[0m'

testNo = 1

def runTest(word: tWord, ntIdx: int, ruleRhs: tWord, expected: str) -> None:
	global testNo
	g = cWK_CFG(['A'], [], 'A' , [], [])
	actual = wordToStr(g.apply_rule(word, ntIdx, rule))
	status = RES_OK if actual == expected else RES_FAILED
	#print(f'TEST {cnt:4}       {word:20} | {ntIdx:3} | {rule:20} | {expected:20} | {actual:20}         {status:10}')
	print(f'| TEST {testNo:2}       |    {wordToStr(word):20}    |    {ntIdx:3}    |    {word[ntIdx] + " -> " + wordToStr(rule):20}    |    {expected:20}    |    {actual:20}    | {status:15}   |')
	print(hline)
	testNo += 1

hline = '|---------------|----------------------------|-----------|----------------------------|----------------------------|----------------------------|----------|'

print(hline)

print('|               |           WORD             |   NT IDX  |         RULE               |         EXPECTED           |          ACTUAL            | STATUS   |')
print(hline)
print(hline)

rule: tWord = [(['a'], ['a'])]
runTest(['A'],                                         0, rule, 'a/a')
runTest([(['a'], ['a']), 'A'],                         1, rule, 'aa/aa')
runTest(['A', (['a'], ['a'])],                         0, rule, 'aa/aa')
runTest([(['a'], ['b']), 'A', (['c'], ['d'])],         1, rule, 'aac/bad')
runTest([(['a'], ['a']), 'A', 'B'],                    1, rule, 'aa/aa B')
runTest(['B', 'A', (['b'], ['b'])],                    1, rule, 'B ab/ab')
runTest(['A', 'A', 'B'],                               1, rule, 'A a/a B')

rule = [(['a'], ['a']), 'B', (['c'], ['c'])]
runTest(['A', 'A', 'A'],                               1, rule, 'A a/a B c/c A')
runTest(['A', 'A', 'A'],                               0, rule, 'a/a B c/c A A')
runTest(['A', 'A', (['a'], ['b'])],                    1, rule, 'A a/a B ca/cb')
runTest([(['a'], ['b']), 'A'],                         1, rule, 'aa/ba B c/c')
runTest([(['a'], ['b']), 'A', (['c'], ['d']), 'B'],    1, rule, 'aa/ba B cc/cd B')
runTest([(['a'], []), 'A'],                            1, rule, 'aa/a B c/c')

rule = [([], ['b']), 'A', (['a'], [])]
runTest([(['a'], ['b']), 'A', (['c'], ['d'])],         1, rule, 'a/bb A ac/d')
runTest([(['a'], ['a']), 'A', 'B'],                    1, rule, 'a/ab A a/λ B')

rule = [(['a'], []), 'S']
runTest([(['a'], []), 'S'],                    1, rule, 'aa/λ S')

testNo = 1
def runTest2(grammar: cWK_CFG, inputStr: str, expected: bool):
	global testNo
	actual = grammar.can_generate(inputStr)
	status = RES_OK if actual == expected else RES_FAILED

	print(f'| TEST {testNo:2}       | {g.desc:35} | {inputStr:40} |    {expected:6}    |    {actual:6}  | {status:15}  |')
	#print(hline)
	testNo += 1


hline = '|---------------|-------------------------------------|------------------------------------------|--------------|------------|---------|'
print('\n\n\n')
print(hline)
print('|               |   GRAMMAR                           |        STRING                            |   EXPECTED   |   ACTUAL   | STATUS  |')
print(hline)
print(hline)

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
