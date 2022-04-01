#!/usr/bin/python3

from ctf_WK_grammar import *

rules: List[cRule] = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['a'], ['a'])])
]
g = cWK_CFG(['A'], ['a'], 'A', rules, [('a', 'a')])
g.desc = 'a(aa)*'

#runTest(g, 'aaaaaaaaaaaaccccccccccccbbbbbbbbbbbb', True)



#for rule in g.rules:
	#print(f'{rule}')

print('')

#g.to_wk_cnf()

#for rule in g.rules:
	#print(f'{rule}')


#print(g.run_wk_cyk('aaabb'))

#print(g.can_generate('acb'))
print('aaaaaaaaaaaaa   ', g.can_generate('aaaaaaaaaaaaa'))
