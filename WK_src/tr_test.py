#!/usr/bin/python3

from grammars import g2
from ctf_WK_grammar import *
import time

l = 300

strinput = 'a'*l + 'b'*l
start = time.time()
res = g2.can_generate(strinput)
end = time.time()
timeTaken = end-start
print(f'{strinput} - {res} in {timeTaken}')

# example from https://www.ccs.neu.edu/home/viola/classes/slides/slides-context-free.pdf
#L = { x2y : x,y in {0,1}* |x| ≠ |y| }
#rules = [
	#cRule('S', ['B', 'L']),
	#cRule('S', ['R', 'B']),
	#cRule('L', ['B', 'L']),
	#cRule('L', ['A']),
	#cRule('R', ['R', 'B']),
	#cRule('R', ['A']),
	#cRule('A', ['B', 'A', 'B']),
	#cRule('A', [(['2'], ['2'])]),
	#cRule('B', [(['0'], ['0'])]),
	#cRule('B', [(['1'], ['1'])])
#]

#nts = set()
#for rule in rules:
	#nts.add(rule.lhs)
#ts = ['0', '1', '2']
#g = cWK_CFG(nts, ts, 'S', rules, [(x, x) for x in ts])

#s = '000101001120001010011'
#print(g.can_generate(s))

# +  :  p
# e  :  Ø
# o  :  (
# c  :  )
# l  :  3
# s  :  *
# d  :  •

# example from: https://jeffe.cs.illinois.edu/teaching/algorithms/models/05-context-free.pdf
# accepts regular expressions with ones and zeros
#rules = [
	#cRule('S', ['T']),
	#cRule('S', ['T', (['p'], ['p']), 'S']),
	#cRule('T', ['F']),
	#cRule('T', ['F', 'T']),
	#cRule('F', [(['e'], ['e'])]),
	#cRule('F', ['W']),
	#cRule('F', [(['o'], ['o']), 'T', (['p'], ['p']), 'S', (['c'], ['c'])]),
	#cRule('F', ['X', (['s'], ['s'])]),
	#cRule('F', [(['o'], ['o']), 'Y', (['c'], ['c']), (['s'], ['s'])]),
	#cRule('X', [(['e'], ['e'])]),
	#cRule('X', [(['l'], ['l'])]),
	#cRule('X', [(['0'], ['0'])]),
	#cRule('X', [(['1'], ['1'])]),
	#cRule('Y', ['T', (['p'], ['p']), 'S']),
	#cRule('Y', ['F', (['d'], ['d']), 'T']),
	#cRule('Y', ['X', (['s'], ['s'])]),
	#cRule('Y', [(['o'], ['o']), 'Y', (['c'], ['c']), (['s'], ['s'])]),
	#cRule('Y', ['Z', 'Z']),
	#cRule('W', [(['l'], ['l'])]),
	#cRule('W', ['Z']),
	#cRule('Z', [(['0'], ['0'])]),
	#cRule('Z', [(['1'], ['1'])]),
	#cRule('Z', ['Z', 'Z'])
#]

#nts = set()
#for rule in rules:
	#nts.add(rule.lhs)

#ts = ['p', 'e', 'o', 'c', 'l', 's', 'd', '0', '1']
#g = cWK_CFG(nts, ts, 'S', rules, [(x, x) for x in ts])


#g.to_wk_cnf()
##s = '1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p1p'
#s = '1p1p1p1p1p1p1p1p1p1p1p1p1pp'

#print(g.can_generate(s))


# rules = [
# 	cRule('S', ['9', '14']),             # 0
# 	cRule('9', [(['a'], [])]),           # 1
# 	cRule('14', ['S', '10']),            # 2
# 	cRule('10', [(['b'], [])]),          # 3
# 	cRule('S', ['5', '13']),             # 4
# 	cRule('5', [(['a'], [])]),           # 5
# 	cRule('13', ['A', '6']),             # 6
# 	cRule('6', [(['b'], [])]),           # 7
# 	cRule('A', ['7', 'A']),              # 8
# 	cRule('7', ['18', '8']),             # 9
# 	cRule('18', [([], ['a'])]),          # 10
# 	cRule('8', [(['c'], [])]),           # 11
# 	cRule('A', ['1', '15']),             # 12
# 	cRule('1', [([], ['c'])]),           # 13
# 	cRule('15', ['B', '2']),             # 14
# 	cRule('2', [([], ['b'])]),           # 15
# 	cRule('A', ['19', '4']),             # 16
# 	cRule('19', [([], ['c'])]),          # 17
# 	cRule('4', [([], ['b'])]),           # 18
# 	cRule('B', ['11', '17']),            # 19
# 	cRule('11', [([], ['c'])]),          # 20
# 	cRule('17', ['B', '12']),            # 21
# 	cRule('12', [([], ['b'])]),          # 22
# 	cRule('B', ['16', '3']),             # 23
# 	cRule('3', [([], ['b'])]),           # 24
# 	cRule('16', [([], ['c'])])           # 25
# ]
#
# nts = set()
# for rule in rules:
# 	nts.add(rule.lhs)
#
# g = cWK_CFG(nts, ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])rules = [
# 	cRule('S', ['9', '14']),             # 0
# 	cRule('9', [(['a'], [])]),           # 1
# 	cRule('14', ['S', '10']),            # 2
# 	cRule('10', [(['b'], [])]),          # 3
# 	cRule('S', ['5', '13']),             # 4
# 	cRule('5', [(['a'], [])]),           # 5
# 	cRule('13', ['A', '6']),             # 6
# 	cRule('6', [(['b'], [])]),           # 7
# 	cRule('A', ['7', 'A']),              # 8
# 	cRule('7', ['18', '8']),             # 9
# 	cRule('18', [([], ['a'])]),          # 10
# 	cRule('8', [(['c'], [])]),           # 11
# 	cRule('A', ['1', '15']),             # 12
# 	cRule('1', [([], ['c'])]),           # 13
# 	cRule('15', ['B', '2']),             # 14
# 	cRule('2', [([], ['b'])]),           # 15
# 	cRule('A', ['19', '4']),             # 16
# 	cRule('19', [([], ['c'])]),          # 17
# 	cRule('4', [([], ['b'])]),           # 18
# 	cRule('B', ['11', '17']),            # 19
# 	cRule('11', [([], ['c'])]),          # 20
# 	cRule('17', ['B', '12']),            # 21
# 	cRule('12', [([], ['b'])]),          # 22
# 	cRule('B', ['16', '3']),             # 23
# 	cRule('3', [([], ['b'])]),           # 24
# 	cRule('16', [([], ['c'])])           # 25
# ]
#
# nts = set()
# for rule in rules:
# 	nts.add(rule.lhs)
#
# g = cWK_CFG(nts, ['a', 'b', 'c'], 'S', rules, [('a', 'a'), ('b', 'b'), ('c', 'c')])

#print(g.erasableNts)

######################################
#print('------------')

#g5.to_wk_cnf()
#print(g4.erasableNts)

#print(g5.can_generate('abcd'))


#maxlen = 15
#iters = 30

#lclosed = [0]*maxlen
#ltime = [0]*maxlen

#for it in range(iters):
	#print(f'iteration {it}')
	#for i in range(maxlen):
		#s = i*'a' + i*'c'+i*'b'
		#start = time.time()
		#o, c, res = g.can_generate(s)
		#end = time.time()
		#timeTaken = end-start

		#lclosed[i] += c
		#ltime[i] += timeTaken

		#print(f's: {s}      {o, c, res}')


#for i in range(maxlen):
	#lclosed[i] /=  iters
	#ltime[i] /= iters


##plt.plot(lclosed)
##plt.ylabel('some numbers')
##plt.show()

#plt.plot(ltime)
#plt.ylabel('some numbers')
#plt.show()


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



#rules = [
	#cRule('S', [(['a'], []), 'S']),
	#cRule('S', [(['a'], []), 'A']),
	#cRule('A', [(['b'], ['a']), 'A']),
	#cRule('A', [(['b'], ['a']), 'B']),
	#cRule('B', [(['a'], ['b']), 'B']),
	#cRule('B', [([], ['b']), 'B']),
	#cRule('B', [([], [])]),
	#cRule('B', ['A'])
#]

#g = cWK_CFG(['S', 'A', 'B'], ['a', 'b'], 'S', rules, [('a', 'a'), ('b', 'b')])

##for rule in g.rules:
	##print(f'{rule}     {rule.upperCnt}, {rule.lowerCnt}, {rule.ntCnt}')


#s = 'aabbab'
#print(g.can_generate(s))

#def apply_rules(word, ruleIdxs):
	#print(wordToStr(word))
	#for idx in ruleIdxs:
		#rule = rules[idx]
		#for i, letter in enumerate(word):
			#if isinstance(letter, str) and letter == rule.lhs:
				#res = g4.apply_rule(word, i, rule.rhs)
				#word = res
				#print(f'{idx}   {wordToStr(word)}')
				#break
		#else:
			#print(f'cant apply {rule} (idx {idx})')
			#raise ValueError
	#print(f'\nRESULT: {wordToStr(word)}\n')



