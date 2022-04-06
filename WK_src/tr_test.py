#!/usr/bin/python3

from ctf_WK_grammar import *

#rules: List[cRule] = [
	#cRule('S', [(['a'], ['t']), 'S']),
	#cRule('S', [(['t'], ['a']), 'S']),
	#cRule('S', [(['g'], ['c']), 'S']),
	#cRule('S', [(['c'], ['g']), 'A']),
	#cRule('A', [(['c'], ['g']), 'A']),
	#cRule('A', [(['a'], ['t']), 'S']),
	#cRule('A', [(['g'], ['c']), 'S']),
	#cRule('A', [(['t'], ['a']), 'B']),
	#cRule('B', [(['c'], ['g']), 'A']),
	#cRule('B', [(['a'], ['t']), 'S']),
	#cRule('B', [(['t'], ['a']), 'S']),
	#cRule('B', [(['g'], ['c']), 'C']),
	#cRule('C', [(['a'], ['t']), 'C']),
	#cRule('C', [(['t'], ['a']), 'C']),
	#cRule('C', [(['g'], ['c']), 'C']),
	#cRule('C', [(['c'], ['g']), 'C']),
	#cRule('C', [([], [])])
#]
#g = cWK_CFG(['S', 'A', 'B', 'C'], ['a', 't', 'c', 'g'], 'S', rules, [('a', 't'), ('c', 'g'), ('t', 'a'), ('g', 'c')])
#g.desc = ''



rules = [
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], ['a']), 'A']),
	cRule('A', [(['b'], ['a']), 'B']),
	cRule('B', [(['a'], ['b']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], [])]),
	cRule('B', ['A'])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])

#for rule in g.rules:
	#print(f'{rule}     {rule.upperCnt}, {rule.lowerCnt}, {rule.ntCnt}')


s = 'aabbab'
print(g.can_generate(s))
