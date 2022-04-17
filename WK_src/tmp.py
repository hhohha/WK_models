#!/usr/bin/python3

from ctf_WK_grammar import *


rules = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['+'], ['+'])])
]
g1 = cWK_CFG(['A'], ['+'], 'A', rules, [('+', '+')])


#rules = [
	#cRule('S', ['S', 'S']),
	#cRule('S', [(['a'], []), ([], ['a']), 'S', (['b'], []), ([], ['b'])]),
	#cRule('S', [(['a'], []), 'S']),
	#cRule('S', [(['a'], []), 'A']),
	#cRule('A', [(['b'], []), ([], ['a']), 'A']),
	#cRule('A', [(['b'], []), ([], ['a']), 'B', (['b'], []), ([], ['a'])]),
	#cRule('B', [([], ['b']), 'B']),
	#cRule('B', [([], ['b'])]),
	#cRule('B', ['B', 'B']),
	#cRule('B', [(['a'], []), ([], ['a']), 'S', (['b'], []), ([], ['b'])]),
	#cRule('B', [(['a'], []), 'S']),
	#cRule('B', [(['a'], []), 'A'])
#]

#g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
##print(g.can_generate('ab'))


#rules = [
	#cRule('S', ['S', 'S']),
	#cRule('S', ['Tua', 'Y1']),
	#cRule('Y1', ['Tda', 'Y2']),
	#cRule('Y2', ['S', 'Y3']),
	#cRule('Y3', ['Tub', 'Tdb']),
	#cRule('S', ['Tua', 'S']),
	#cRule('S', ['Tua', 'A']),
	#cRule('A', ['Tub', 'Y4']),
	#cRule('Y4', ['Tda', 'A']),
	#cRule('A', ['Tub', 'Y5']),
	#cRule('Y5', ['Tda', 'B']),
	#cRule('A', ['Tub', 'Tda']),
	#cRule('B', ['Tdb', 'B']),
	#cRule('B', [([], ['b'])]),
	#cRule('B', ['B', 'B']),
	#cRule('B', ['Tua', 'Y6']),
	#cRule('Y6', ['Tda', 'Y7']),
	#cRule('Y7', ['S', 'Y8']),
	#cRule('Y8', ['Tub', 'Tdb']),
	#cRule('B', ['Tua', 'S']),
	#cRule('B', ['Tua', 'A']),
	#cRule('Tua', [(['a'], [])]),
	#cRule('Tub', [(['b'], [])]),
	#cRule('Tda', [([], ['a'])]),
	#cRule('Tdb', [([], ['b'])])
#]

#nts = ['S', 'Y1', 'Y2', 'Y3', 'Y4', 'Y5', 'Y6', 'Y7', 'Y8', 'A', 'B', 'Tua', 'Tub', 'Tda', 'Tdb']
#ts = ['a', 'b']
#rel = [('a', 'a'), ('b', 'b')]

#g = cWK_CFG(nts, ts, 'S', rules, rel)
#print(g.can_generate('ababab'))

# ab - 25
# aabb - 15968
# aaabbb
