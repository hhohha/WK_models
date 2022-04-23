#!/usr/bin/python3

from grammars import g1
from ctf_WK_grammar import *
import time
from itertools import product
import matplotlib.pyplot as plt

results = []
lens = []

g1.to_wk_cnf()
try:
	for i in range(1, 50):
		s = 'a' + 'aa'*i
		start = time.time()
		#res = g1.run_wk_cyk(s)
		x, y, res = g1.can_generate(s)
		end = time.time()
		taken = round(end-start, 3)
		lens.append(i)
		results.append(taken)

		print(f'{s} - {res}     time: {taken}')
except:
	pass

print(results)

plt.plot(lens, results)
plt.show()


#start = time.time()
#accepted = []
#for i in range(1, 13):
	#for t in product('lr', repeat=i):
		#s = ''.join(t)
		##res = g.can_generate(s)
		#res = g.run_wk_cyk(s)
		#print(f'{s} - {res}')
		#if res:
			#accepted.append(s)
#end = time.time()
#print('-------------')
#for s in accepted:
	#print(s)

#print('time taken:', end-start)
