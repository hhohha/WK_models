#!/usr/bin/python3

from ctf_WK_grammar import *

# GRAMMAR 1
# accepted strings: a(aa)*
# my example

rules = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['a'], ['a'])])
]
g1 = cWK_CFG(['A'], ['a'], 'A', rules, [('a', 'a')])
g1.desc = 'a(aa)*'

# GRAMMAR 2
# accepted strings: a^n b^n (n>0)
# taken from: On Watson Crick automata

rules  = [
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], ['a']), 'A']),
	cRule('A', [(['b'], ['a']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], ['b'])])
]

g2 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g2.desc = 'a^n b^n (n>0)'

# GRAMMAR 3
# accepted strings: r^n d^n u^n r^n
# taken from:  On Watson Crick automata

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

g3 = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['r', 'd', 'u'], 'S', rules, [('r', 'r'), ('d', 'd'), ('u', 'u')])
g3.desc = 'r^n d^n u^n r^n'

# GRAMMAR 4
# accepted strings: a^n c^n b^n
# taken from: generative power and closure properties of WK grammars (example 10)

rules = [
	cRule('S', [(['a'], []), 'S', (['b'], [])]),
	cRule('S', [(['a'], []), 'A', (['b'], [])]),
	cRule('A', [(['c'], ['a']), 'A']),
	cRule('A', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], [])])
]

g4 = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g4.desc = 'a^n c^n b^n'

# GRAMMAR 5
# accepted strings: a^n b^m c^n d^m
# taken from: generative power and closure properties of WK grammars  (example 11)

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

g5 = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['a', 'b', 'c', 'd'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
g5.desc = 'a^n b^m c^n d^m'

# GRAMMAR 6
# accepted strings: wcw where w in {a,b }*
# taken from: generative power and closure properties of WK grammars (example 12)

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

g6 = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g6.desc = 'wcw where w in {a,b }*'

# GRAMMAR 7
# accepted strings: a^n b^m a^n where 2n <= m <= 3n
# taken from: generative power and closure properties of WK grammars (lemma 14)

rules = [
	cRule('S', [(['a'], []), 'S', (['a'], ['a'])]),
	cRule('S', [(['a'], []), 'A', (['a'], ['a'])]),
	cRule('A', [(['b', 'b'], ['a']), 'A']),
	cRule('A', [(['b', 'b', 'b'], ['a']), 'A']),
	cRule('A', [([], ['b']), 'B']),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], [])])
]

g7 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g7.desc = 'a^n b^m a^n where 2n <= m <= 3n'

# GRAMMAR 8
# accepted strings: ({a,t,c,g}*ctg{a,t,c,g}*)*
# taken from: generative power and closure properties of WK grammars (chapter 6)
rules = [
	cRule('S', [(['a'], ['t']), 'S']),
	cRule('S', [(['t'], ['a']), 'S']),
	cRule('S', [(['g'], ['c']), 'S']),
	cRule('S', [(['c'], ['g']), 'A']),
	cRule('A', [(['c'], ['g']), 'A']),
	cRule('A', [(['a'], ['t']), 'S']),
	cRule('A', [(['g'], ['c']), 'S']),
	cRule('A', [(['t'], ['a']), 'B']),
	cRule('B', [(['c'], ['g']), 'A']),
	cRule('B', [(['a'], ['t']), 'S']),
	cRule('B', [(['t'], ['a']), 'S']),
	cRule('B', [(['g'], ['c']), 'C']),
	cRule('C', [(['a'], ['t']), 'C']),
	cRule('C', [(['t'], ['a']), 'C']),
	cRule('C', [(['g'], ['c']), 'C']),
	cRule('C', [(['c'], ['g']), 'C']),
	cRule('C', [([], [])])
]

# GRAMMAR 9
# accepted strings:
# taken from: generative power and closure properties of WK grammars (example 31)


# GRAMMAR 10
# accepted strings: |a| == |b| and for any prefix: |a| >= |b|
# taken from: WK cyk paper

rules = [
	cRule('S', ['S', 'S']),
	cRule('S', [(['a'], []), ([], ['a']), 'S', (['b'], []), ([], ['b'])]),
	cRule('S', [(['a'], []), 'S']),
	cRule('S', [(['a'], []), 'A']),
	cRule('A', [(['b'], []), ([], ['a']), 'A']),
	cRule('A', [(['b'], []), ([], ['a']), 'B']),
	cRule('A', [(['b'], []), ([], ['a'])]),
	cRule('B', [([], ['b']), 'B']),
	cRule('B', [([], ['b'])]),
	cRule('B', ['B', 'B']),
	cRule('B', [(['a'], []), ([], ['a']), 'S', (['b'], []), ([], ['b'])]),
	cRule('B', [(['a'], []), 'S']),
	cRule('B', [(['a'], []), 'A'])
]

g8 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g8.desc = '|a| == |b| and for any prefix: |a| >= |b|'
