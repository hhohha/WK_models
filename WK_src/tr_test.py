#!/usr/bin/python3

from ctf_WK_grammar import *


rules: List[cRule] = [
	cRule('S', [(['a'], [])]),
	cRule('S', ['A']),
	cRule('A', ['A', 'B']),
	cRule('B', [(['b'], [])])
]

g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [])


#for rule in g.rules:
	#print(rule)
#print('\n\n')
#g.remove_unit_rules()

g.remove_useless_rules()

