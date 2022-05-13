#!/usr/bin/python3

from ctf_WK_grammar import *
#import time, random
#from itertools import product
#from lib.perf_tester import cPerfTester
from grammars import g1
#import matplotlib.pyplot as plt
##import numpy as np
#lengths = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33]
#times = [0.0, 0.0, 0.0, 0.01, 0.03, 0.07, 0.15, 0.28, 0.52, 0.88, 1.47, 2.3, 3.46, 5.23, 7.55, 10.67]

#fig, axs = plt.subplots(1, 2)

#axs[0].plot(lengths, times, marker='o')
#axs[0].set(xlabel='number of inputs')
#axs[0].set(ylabel='time (sec)')


#axs[1].plot([x**6//1000000 for x in lengths], times, marker='o')
#axs[1].set(xlabel='number of operation (in millions)')
##plt.xlabel("number of inputs")
##plt.ylabel("time (sec)")
##fig = plt.figure()

#plt.show()

#g3.to_wk_cnf()
#g3.timeLimit = 600

#times = []
#opens = []
#alls = []
#lengths = []
#for i in range(20, 21):
	#inputStr = 'a'*i + 'b'
	#start = time.time()
	#openStates, allStates, prunes, res = g3.can_generate(inputStr)
	#end = time.time()
	#timeTaken = end - start

	#times.append(timeTaken)
	#opens.append(openStates)
	#alls.append(allStates)
	#lengths.append(len(inputStr))
	#print(f'input len: {len(inputStr)}, open states: {openStates}, all states: {allStates}, time taken: {timeTaken}:')

#print('----------------------')
#print('times:', times)
#print('opens:', opens)
#print('alls:', alls)
#print('lengths:', lengths)

#g2.to_wk_cnf()
#t.run_wk_cyk_test(g2, g2.input_gen_func(2, 2, True), True)



#for testIdx in [18, 21, 22, 32]:
	#numbers = []
	#for i in range(12):
		#if times[i][testIdx] == -1:
			#numbers.append(10)
		#else:
			#numbers.append(times[i][testIdx])

	##fig = plt.figure(figsize = (10, 5))

	## creating the bar plot
	#plt.bar(labels, numbers, width = 0.4)

	#plt.xlabel(" ")
	#plt.ylabel("time (sec)")
	#plt.title("")
	##plt.savefig('t' + str(testIdx+1) + '.png')
	#plt.show()
	##plt.clf()

#for heur in range(12):
	#passedTests = 0
	#timeTotal = 0
	#for i in range(40):
		#if timeouts[heur][i]:
			#timeTotal += 20
		#else:
			#timeTotal += times[heur][i]
	#totals2.append(round(timeTotal, 2))

## normalization
#for tstIdx in range(40):
	#minTime = 1000
	#for h in range(12):
		#if times[h][tstIdx] < minTime:
			#minTime = times[h][tstIdx]
	#norm = 1 / minTime / 10
	#for h in range(12):
		#times[h][tstIdx] *= norm

#totals = []
#for heur in range(12):
	#passedTests = 0
	#timeTotal = 0
	#for i in range(40):
		#if timeouts[heur][i]:
			#timeTotal += 20
		#else:
			#timeTotal += times[heur][i]
	#totals.append(round(timeTotal, 2))

#x = np.arange(len(labels))  # the label locations
#width = 0.35  # the width of the bars

#fig, ax = plt.subplots()
#rects1 = ax.bar(x - width/2, totals, width, label='Normalized time')
#rects2 = ax.bar(x + width/2, totals2, width, label='Total time (sec)')

## Add some text for labels, title and custom x-axis tick labels, etc.
#ax.set_ylabel('Time')
#ax.set_title('Comparision of heuristic functions')
#ax.set_xticks(x, labels)
#ax.legend()

#ax.bar_label(rects1)
#ax.bar_label(rects2)

#plt.show()




