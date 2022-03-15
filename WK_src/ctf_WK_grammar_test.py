#!/usr/bin/python3

from ctf_WK_grammar import cWK_CFG

RES_OK = '\033[92m' + 'OK' + '\x1b[0m'
RES_FAILED = '\033[91m' + 'FAILED' + '\x1b[0m'

def strWord(word):
	rs = []
	for symbol in word:
		if isinstance(symbol, list) or isinstance(symbol, tuple):
			e1 = ''.join(symbol[0]) if len(symbol[0]) > 0 else 'λ'
			e2 = ''.join(symbol[1]) if len(symbol[1]) > 0 else 'λ'
			rs.append(e1 + '/' + e2)
		else:
			rs.append(symbol)

	return(f'{" ".join(rs)}')


def runTest(cnt, word, ntIdx, rule, expected):
	actual = strWord(cWK_CFG.apply_rule(None, word, ntIdx, rule))
	status = RES_OK if actual == expected else RES_FAILED
	#print(f'TEST {cnt:4}       {word:20} | {ntIdx:3} | {rule:20} | {expected:20} | {actual:20}         {status:10}')
	print(f'| TEST {cnt:2}       |    {strWord(word):20}    |    {ntIdx:3}    |    {rule[0] + " -> " + strWord(rule[1]):20}    |    {expected:20}    |    {actual:20}    | {status:15}   |')
	print(hline)

hline = '|---------------|----------------------------|-----------|----------------------------|----------------------------|--------------------------- |----------|'

print(hline)

print('|               |           WORD             |   NT IDX  |         RULE               |         EXPECTED           |          ACTUAL            | STATUS   |')
print(hline)
print(hline)

rule = ('A', [[['a'], ['a']]])
runTest( 1, ['A'],                                         0, rule, 'a/a')
runTest( 2, [[['a'], ['a']], 'A'],                         1, rule, 'aa/aa')
runTest( 3, ['A', [['a'], ['a']]],                         0, rule, 'aa/aa')
runTest( 4, [[['a'], ['b']], 'A', [['c'], ['d']]],         1, rule, 'aac/bad')
runTest( 5, [[['a'], ['a']], 'A', 'B'],                    1, rule, 'aa/aa B')
runTest( 6, ['B', 'A', [['b'], ['b']]],                    1, rule, 'B ab/ab')
runTest( 7, ['A', 'A', 'B'],                               1, rule, 'A a/a B')

rule = ('A', [[['a'], ['a']], 'B', [['c'], ['c']]])
runTest( 8, ['A', 'A', 'A'],                               1, rule, 'A a/a B c/c A')
runTest( 9, ['A', 'A', 'A'],                               0, rule, 'a/a B c/c A A')
runTest(10, ['A', 'A', [['a'], ['b']]],                    1, rule, 'A a/a B ca/cb')
runTest(11, [[['a'], ['b']], 'A'],                         1, rule, 'aa/ba B c/c')
runTest(12, [[['a'], ['b']], 'A', [['c'], ['d']], 'B'],    1, rule, 'aa/ba B cc/cd B')
runTest(13, [[['a'], []], 'A'],                            1, rule, 'aa/a B c/c')

rule = ('A', [[[], ['b']], 'A', [['a'], []]])
runTest(14, [[['a'], ['b']], 'A', [['c'], ['d']]],         1, rule, 'a/bb A ac/d')
runTest(15, [[['a'], ['a']], 'A', 'B'],                    1, rule, 'a/ab A a/λ B')
