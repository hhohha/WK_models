#!/usr/bin/python3

from ctf_WK_grammar import *


rules: List[cRule] = [
	cRule('S', ['S', 'S']),
	cRule('S', [(['a'], ['a']), 'S', (['b'], ['b'])]),
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], ['a']), 'A']),
	cRule('A', [(['b'], ['a']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], [])]),
	cRule('B', ['S']),
	cRule('C', ['C', 'D'])
]

g = cWK_CFG(['S', 'A', 'B', 'C'], ['a', 'b'], 'S', rules, [])


#for rule in g.rules:
	#print(rule)
#print('\n\n')
#g.remove_unit_rules()

g.remove_lambda_rules()
g.remove_unit_rules()
g.remove_useless_rules()

for rule in g.rules:
	print(rule)

print(g.nts)
print(g.ts)
