#!/usr/bin/python3

from grammars import g1
from ctf_WK_grammar import *
import time
from itertools import product
#import matplotlib.pyplot as plt

g1.to_wk_cnf()

print(g1.termsFromNts)

#print(g1.can_generate('a' * 26))

#timeTaken = 0
#lens, times = [], []
#s = ''
#try:
	#while timeTaken < 50:
		#s += 'aa'
		#start = time.time()
		##res = g1.can_generate(s)
		#res = g1.run_wk_cyk(s)
		#end = time.time()
		#timeTaken = round(end - start, 3)
		#lens.append(len(s))
		#times.append(timeTaken)
		#print(f'{len(s)}   -   {res}   -   {timeTaken}')
#except:
	#pass

#plt.plot(lens, times)
#plt.show()

# standard search
# positive with regex       1001   -   (2501, [1, 0, 0, 500], True)       -   1.18
# positive without regex    1001   -   (3001, [1, 0, 0, 0], True)         -   0.542
# negative with regex        200   -   (20100, [300, 0, 0, 100], False)   -   3.944
# negative without regex     200   -   (20200, [300, 0, 0, 0], False)     -   2.359

# cnf search
# positive with regex       1001   -   (8004, [2, 0, 0, 500], True)       -   2.146
# positive without regex    1001   -   (11501, [4, 0, 0, 0], True)        -   1.914
# negative with regex         14   -   (211084, [58424, 0, 0, 7], False)  -   5.968
# negative without regex      14   -   (211091, [58424, 0, 0, 0], False)  -   4.254

# wk-cyk
# positive                    29   -   True                               -   5.177
# negative                    28   -   False                              -   4.24

# AFTER OPTIMIZATION OF NT CNT   ######################################################################
# standard search
# positive with regex       1001   -   (2499, [3, 0, 0, 500], True)       -   1.167
# positive without regex    1001   -   (2999, [3, 0, 0, 0], True)         -   0.517
# negative with regex        200   -   (10000, [199, 0, 0, 100], False)   -   1.328
# negative without regex     200   -   (10100, [199, 0, 0, 0], False)     -   0.877

# cnf search
# positive with regex       1001   -   (10983, [7, 0, 0, 499], True)      -   2.643
# positive without regex    1001   -   (8500, [5, 0, 0, 0], True)         -   1.445
# negative with regex         14   -   (861, [127, 0, 0, 7], False)       -   0.019
# negative without regex      14   -   (868, [127, 0, 0, 0], False)       -   0.014


#         tree     wk_cyk
######################################
#  24     0.717    1.846
#  26     1.482    2.831
#  28     3.039    4.263
#  30     6.274    6.25
#  32    12.878    9.06
#  34    26.477    12.55
