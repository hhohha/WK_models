#!/usr/bin/python3

from ctf_WK_grammar import *

#####################################  GRAMMAR 1  #####################################
# accepted language: a(aa)*

rules = [
	cRule('S', ['S', 'S', 'S']),
	cRule('S', [(['a'], ['a'])])
]
g1 = cWK_CFG(['S'], ['a'], 'S', rules, [('a', 'a')])
g1.desc = 'a(aa)*'

#####################################  GRAMMAR 2  #####################################
# accepted strings: (a+b+c)*abc
# how does the model cope with fixed end? (rules in form xA)

rules = [
	cRule('S', [(['a'], ['a']), 'S']),
	cRule('S', [(['b'], ['b']), 'S']),
	cRule('S', [(['c'], ['c']), 'S']),
	cRule('S', [(['a'], ['a']), (['b'], ['b']), (['c'], ['c'])])
]

g2 = cWK_CFG(['S'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g2.desc = '(a+b+c)*abc'

#####################################  GRAMMAR 3  #####################################
# accepted strings: (a+b+c)*abc
# how does the model cope with fixed end? (rules in form Ax)

rules = [
	cRule('S', ['A', (['a'], ['a']), (['b'], ['b']), (['c'], ['c'])]),
	cRule('A', ['A', (['a'], ['a'])]),
	cRule('A', ['A', (['b'], ['b'])]),
	cRule('A', ['A', (['c'], ['c'])]),
	cRule('A', [([], [])])
]

g3 = cWK_CFG(['S', 'A'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g3.desc = '(a+b+c)*abc'

#####################################  GRAMMAR 4  #####################################
# accepted strings: a?b?c?d?e?f?g? + (a?b?c?d?e?f?g?)*a
# my example, aimed to have a lot of rules after transformation to CNF

rules = [
	cRule('S', ['Q', (['a'], ['a'])]),
	cRule('S', ['A', 'B', 'C', 'D', 'E', 'F', 'G']),
	cRule('Q', ['Q', 'Q']),
	cRule('Q', ['A', 'B', 'C', 'D', 'E', 'F', 'G']),
	cRule('A', [(['a'], ['a'])]),
	cRule('A', [([], [])]),
	cRule('B', [(['b'], ['b'])]),
	cRule('B', [([], [])]),
	cRule('C', [(['c'], ['c'])]),
	cRule('C', [([], [])]),
	cRule('D', [(['d'], ['d'])]),
	cRule('D', [([], [])]),
	cRule('E', [(['e'], ['e'])]),
	cRule('E', [([], [])]),
	cRule('F', [(['f'], ['f'])]),
	cRule('F', [([], [])]),
	cRule('G', [(['g'], ['g'])]),
	cRule('G', [([], [])])
]

ts = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
g4 = cWK_CFG(['S', 'Q', 'A', 'B', 'C', 'D', 'E', 'F', 'G'], ts, 'S', rules, [(x, x) for x in ts])
g4.desc = 'a?b?c?d?e?f?g? + (a?b?c?d?e?f?g?)*a'

##################################### GRAMMAR 5  #####################################
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
g5 = cWK_CFG(['S', 'A', 'B', 'C'], ['a', 't', 'g', 'c'], 'S', rules, [('a', 't'), ('t', 'a'), ('g', 'c'), ('c', 'g')])
g5.desc = '({a,t,c,g}*ctg{a,t,c,g}*)*'

##################################### GRAMMAR 6  #####################################
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

g6 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g6.desc = 'a^n b^n (n>0)'

##################################### GRAMMAR 7 #####################################
rules = [
	cRule('S', [(['a'], ['a']), 'S', (['a'], ['a'])]),
	cRule('S', [(['b'], ['b']), 'S', (['b'], ['b'])]),
	cRule('S', [(['c'], ['c'])])
]
g7 = cWK_CFG(['S'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g7.desc = 'wcw^r'

##################################### GRAMMAR 8  #####################################
# accepted strings: w w^r

rules = [
	cRule('S', [(['a'], ['a']), 'S', (['a'], ['a'])]),
	cRule('S', [(['b'], ['b']), 'S', (['b'], ['b'])]),
	cRule('S', [([], [])])
]
g8 = cWK_CFG(['S'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g8.desc = 'w w^r'

##################################### GRAMMAR 9  #####################################
# accepted string: x2y : x,y in {0,1}* |x| != |y| - adjusted CF grammar
# taken from: https://www.ccs.neu.edu/home/viola/classes/slides/slides-context-free.pdf

rules = [
	cRule('S', ['B', 'L']),
	cRule('S', ['R', 'B']),
	cRule('L', ['B', 'L']),
	cRule('L', ['A']),
	cRule('R', ['R', 'B']),
	cRule('R', ['A']),
	cRule('A', ['B', 'A', 'B']),
	cRule('A', [(['2'], ['2'])]),
	cRule('B', [(['0'], ['0'])]),
	cRule('B', [(['1'], ['1'])])
]
g9 = cWK_CFG(['S', 'L', 'R', 'A', 'B'], ['0', '1', '2'], 'S', rules, [('0', '0'), ('1', '1'), ('2', '2')])
g9.desc = 'x2y : x,y in {0,1}* |x| != |y|'

##################################### GRAMMAR 10 #####################################
# accepted strings: regular expressions with ones and zeros and following symbols
# p  :  +   (plus sign)
# e  :  Ø   (empty set)
# o  :  (   (left parenthesis)
# c  :  )   (right parenthesis)
# l  :  3   (empty string)
# s  :  *   (star)
# d  :  •   (dot / concatenation operator)
# it is adjusted CF grammar
# example from: https://jeffe.cs.illinois.edu/teaching/algorithms/models/05-context-free.pdf

rules = [
	cRule('S', ['T']),
	cRule('S', ['T', (['p'], ['p']), 'S']),
	cRule('T', ['F']),
	cRule('T', ['F', 'T']),
	cRule('F', [(['e'], ['e'])]),
	cRule('F', ['W']),
	cRule('F', [(['o'], ['o']), 'T', (['p'], ['p']), 'S', (['c'], ['c'])]),
	cRule('F', ['X', (['s'], ['s'])]),
	cRule('F', [(['o'], ['o']), 'Y', (['c'], ['c']), (['s'], ['s'])]),
	cRule('X', [(['e'], ['e'])]),
	cRule('X', [(['l'], ['l'])]),
	cRule('X', [(['0'], ['0'])]),
	cRule('X', [(['1'], ['1'])]),
	cRule('Y', ['T', (['p'], ['p']), 'S']),
	cRule('Y', ['F', (['d'], ['d']), 'T']),
	cRule('Y', ['X', (['s'], ['s'])]),
	cRule('Y', [(['o'], ['o']), 'Y', (['c'], ['c']), (['s'], ['s'])]),
	cRule('Y', ['Z', 'Z']),
	cRule('W', [(['l'], ['l'])]),
	cRule('W', ['Z']),
	cRule('Z', [(['0'], ['0'])]),
	cRule('Z', [(['1'], ['1'])]),
	cRule('Z', ['Z', 'Z'])
]
nts = ['S', 'T', 'F', 'X', 'Y', 'W', 'Z']
ts = ['p', 'e', 'o', 'c', 'l', 's', 'd', '0', '1']
g10 = cWK_CFG(nts, ts, 'S', rules, [(x, x) for x in ts])
g10.desc = 'RE with 0 and 1 and operators: p-plus, e-empty set, o-opening par, c-closing par, l-epsilon, s-star, d-dot'

##################################### GRAMMAR 11 #####################################
rules = [
	cRule('S', ['A']),
	cRule('S', ['B']),
	cRule('S', ['A', 'B']),
	cRule('S', ['B', 'A']),
	cRule('A', [(['a'], ['a'])]),
	cRule('A', [(['a'], ['a']), 'A', (['a'], ['a'])]),
	cRule('A', [(['a'], ['a']), 'A', (['b'], ['b'])]),
	cRule('A', [(['b'], ['b']), 'A', (['b'], ['b'])]),
	cRule('A', [(['b'], ['b']), 'A', (['a'], ['a'])]),
	cRule('B', [(['b'], ['b'])]),
	cRule('B', [(['a'], ['a']), 'B', (['a'], ['a'])]),
	cRule('B', [(['a'], ['a']), 'B', (['b'], ['b'])]),
	cRule('B', [(['b'], ['b']), 'B', (['b'], ['b'])]),
	cRule('B', [(['b'], ['b']), 'B', (['a'], ['a'])])
]

g11 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g11.desc = '{a, b}* - ww'

##################################### GRAMMAR 12 #####################################
# accepted strings: r^n d^n u^n r^n
# taken from: On Watson Crick automata

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

g12 = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['r', 'd', 'u'], 'S', rules, [('r', 'r'), ('d', 'd'), ('u', 'u')])
g12.desc = 'r^n d^n u^n r^n'


##################################### GRAMMAR 13 #####################################
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

g13 = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g13.desc = 'a^n c^n b^n'


##################################### GRAMMAR 14 #####################################
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

g14 = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['a', 'b', 'c', 'd'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')])
g14.desc = 'a^n b^m c^n d^m'

##################################### GRAMMAR 15 #####################################
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

g15 = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])
g15.desc = 'wcw where w in {a,b }*'

##################################### GRAMMAR 16 #####################################
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

g16 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g16.desc = 'a^n b^m a^n where 2n <= m <= 3n'


##################################### GRAMMAR 17 #####################################
# accepted strings: cnt(a) == cnt(b) and for any prefix: cnt(a) >= cnt(b)
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

g17 = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])
g17.desc = 'cnt(a) == cnt(b) and for any prefix: cnt(a) >= cnt(b)'

##################################### GRAMMAR 18 #####################################
# accepted strings: (l^n r^n)^k where n does not increase (e.g. accepts llrrlr but not lrllrr)
# taken from: generative power and closure properties of WK grammars (example 31)

rules = [
	cRule('S', [(['l'], []), 'S']),
	cRule('S', [(['l'], []), 'A']),
	cRule('A', [(['r'], ['l']), 'A']),
	cRule('A', [(['r'], ['l']), 'B']),
	cRule('B', [(['l'], ['r']), 'B']),
	cRule('B', [([], ['r']), 'B']),
	cRule('B', [([], [])]),
	cRule('B', ['A'])
]

g18 = cWK_CFG(['S', 'A', 'B'], ['l', 'r'], 'S', rules, [('l', 'l'), ('r', 'r')])
g18.desc = '(l^n r^n)^k where n does not increase'

##################################### GRAMMAR 19 #####################################
# non-bijective complementarity relation
# a^n c^m b^n
rules = [
	cRule('S', [(['a'], []), 'S', (['b'], [])]),
	cRule('S', [(['a'], []), 'A', (['b'], [])]),
	cRule('A', [(['c'], ['a']), 'A']),
	cRule('A', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], ['c']), 'B', ([], ['b'])]),
	cRule('B', [([], [])])
]


g19 = cWK_CFG(['S', 'A', 'B'], ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c'), ('a', 'b'), ('b', 'a'), ('a', 'c'), ('c', 'a')])
g19.desc = 'a^n c^m b^n'

##################################### GRAMMAR 20 #####################################
# non-bijective complementarity relation
# '#a + #b = #c + #d'
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

g20 = cWK_CFG(['S', 'A', 'B', 'C', 'D'], ['a', 'b', 'c', 'd'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd'), ('a', 'b'), ('b', 'a')])
g20.desc = '#a + #b = #c + #d'
