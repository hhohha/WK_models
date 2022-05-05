#!/usr/bin/python3

import random
from lib.perf_tester import cPerfTester
from grammars import *

def main():
	times = 5
	t = cPerfTester()

	############ grammar 1 #############################################################
	inputStr = 'a' * 801
	t.run_prune_test(g1, inputStr, True, times)

	inputStr = 'a' * 80
	t.run_prune_test(g1, inputStr, False, times)

	g1.to_wk_cnf()

	inputStr = 'a' * 501
	t.run_prune_test(g1, inputStr, True, times)

	inputStr = 'a' * 26
	t.run_prune_test(g1, inputStr, False, times)

	############ grammar 2 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(500)]) + 'abc'
	t.run_prune_test(g2, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(500)]) + 'ab'
	t.run_prune_test(g2, inputStr, False, times)

	g2.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'abc'
	t.run_prune_test(g2, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'ab'
	t.run_prune_test(g2, inputStr, False, times)

	############ grammar 3 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'abc'
	t.run_prune_test(g3, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'ab'
	t.run_prune_test(g3, inputStr, False, times)

	g3.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(9)]) + 'abc'
	t.run_prune_test(g3, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(9)]) + 'ab'
	t.run_prune_test(g3, inputStr, False, times)

	############ grammar 4 #############################################################
	inputStr = ''.join([random.choice('abcdefg') for i in range(80)]) + 'a'
	t.run_prune_test(g4, inputStr, True, times)

	inputStr = ''.join([random.choice('abcdefg') for i in range(80)]) + 'b'
	t.run_prune_test(g4, inputStr, False, times)

	g4.to_wk_cnf()

	inputStr = ''.join([random.choice('abcdefg') for i in range(40)]) + 'a'
	t.run_prune_test(g4, inputStr, True, times)

	inputStr = ''.join([random.choice('abcdefg') for i in range(20)]) + 'b'
	t.run_prune_test(g4, inputStr, False, times)

	############ grammar 5 #############################################################
	inputStr = ''.join([random.choice('acgt') for i in range(400)]) + 'ctg'
	t.run_prune_test(g5, inputStr, True, times)

	inputStr = ''.join([random.choice('acg') for i in range(400)])
	t.run_prune_test(g5, inputStr, False, times)

	g5.to_wk_cnf()

	inputStr = ''.join([random.choice('acgt') for i in range(400)]) + 'ctg'
	t.run_prune_test(g5, inputStr, True, times)

	inputStr = ''.join([random.choice('acg') for i in range(400)])
	t.run_prune_test(g5, inputStr, False, times)

	############ grammar 6 #############################################################
	inputStr = 'a'*300 + 'b'*300
	t.run_prune_test(g6, inputStr, True, times)

	inputStr = 'a'*300 + 'b'*301
	t.run_prune_test(g6, inputStr, False, times)

	g6.to_wk_cnf()

	inputStr = 'a'*300 + 'b'*300
	t.run_prune_test(g6, inputStr, True, times)

	inputStr = 'a'*300 + 'b'*301
	t.run_prune_test(g6, inputStr, False, times)

	############ grammar 7 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += 'c' + inputStr[::-1]
	t.run_prune_test(g7, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += 'ca' + inputStr[::-1]
	t.run_prune_test(g7, inputStr, False, times)

	g7.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(300)])
	inputStr += 'c' + inputStr[::-1]
	t.run_prune_test(g7, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(300)])
	inputStr += 'ca' + inputStr[::-1]
	t.run_prune_test(g7, inputStr, False, times)

	############ grammar 8 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += inputStr[::-1]
	t.run_prune_test(g8, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += 'a' + inputStr[::-1]
	t.run_prune_test(g8, inputStr, False, times)

	g8.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += inputStr[::-1]
	t.run_prune_test(g8, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += 'a' + inputStr[::-1]
	t.run_prune_test(g8, inputStr, False, times)

	############ grammar 9 #############################################################
	inputStr = ''.join([random.choice('01') for i in range(100)]) + '2' + ''.join([random.choice('01') for i in range(101)])
	t.run_prune_test(g9, inputStr, True, times)

	inputStr = ''.join([random.choice('01') for i in range(100)]) + '2' + ''.join([random.choice('01') for i in range(100)])
	t.run_prune_test(g9, inputStr, False, times)

	g9.to_wk_cnf()

	inputStr = ''.join([random.choice('01') for i in range(60)]) + '2' + ''.join([random.choice('01') for i in range(61)])
	t.run_prune_test(g9, inputStr, True, times)

	inputStr = ''.join([random.choice('01') for i in range(60)]) + '2' + ''.join([random.choice('01') for i in range(60)])
	t.run_prune_test(g9, inputStr, False, times)

	############ grammar 10 ############################################################
	inputStr = 'o0p1s0cp'*1 + '0'
	t.run_prune_test(g10, inputStr, True, times)

	inputStr = 'o0p1s0cp'*50
	t.run_prune_test(g10, inputStr, False, times)

	g10.to_wk_cnf()

	inputStr = 'o0p1s0cp'*7 + '0'
	t.run_prune_test(g10, inputStr, True, times)

	inputStr = 'o0p1s0cp'*4
	t.run_prune_test(g10, inputStr, False, times)

	############ grammar 11 ############################################################
	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += inputStr + 'a'
	t.run_prune_test(g11, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(70)])
	inputStr += inputStr
	t.run_prune_test(g11, inputStr, False, times)

	g11.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(10)])
	inputStr += inputStr + 'a'
	t.run_prune_test(g11, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(10)])
	inputStr += inputStr
	t.run_prune_test(g11, inputStr, False, times)


	############ grammar 12 ############################################################
	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 100 + 'r' * 100
	t.run_prune_test(g12, inputStr, True, times)

	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 101 + 'r' * 100
	t.run_prune_test(g12, inputStr, False, times)

	g12.to_wk_cnf()

	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 100 + 'r' * 100
	t.run_prune_test(g12, inputStr, True, times)

	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 100 + 'r' * 101
	t.run_prune_test(g12, inputStr, False, times)

	############ grammar 13 ############################################################
	inputStr = 'a' * 100 + 'c' * 100 + 'b' * 100
	t.run_prune_test(g13, inputStr, True, times)

	inputStr = 'a' * 101 + 'c' * 100 + 'b' * 100
	t.run_prune_test(g13, inputStr, False, times)

	g13.to_wk_cnf()

	inputStr = 'a' * 100 + 'c' * 100 + 'b' * 100
	t.run_prune_test(g13, inputStr, True, times)

	inputStr = 'a' * 101 + 'c' * 100 + 'b' * 100
	t.run_prune_test(g13, inputStr, False, times)


	############ grammar 14 ############################################################
	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 101
	t.run_prune_test(g14, inputStr, True, times)

	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 100
	t.run_prune_test(g14, inputStr, False, times)

	g14.to_wk_cnf()

	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 101
	t.run_prune_test(g14, inputStr, True, times)

	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 100
	t.run_prune_test(g14, inputStr, False, times)

	############ grammar 15 ############################################################
	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr
	t.run_prune_test(g15, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr + 'a'
	t.run_prune_test(g15, inputStr, False, times)

	g15.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr
	t.run_prune_test(g15, inputStr, True, times)

	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr + 'a'
	t.run_prune_test(g15, inputStr, False, times)

	############ grammar 16 ############################################################
	inputStr = 'a' * 100 + 'b' * 200 + 'a' * 100
	t.run_prune_test(g16, inputStr, True, times)

	inputStr = 'a' * 100 + 'b' * 199 + 'a' * 100
	t.run_prune_test(g16, inputStr, False, times)

	g16.to_wk_cnf()

	inputStr = 'a' * 50 + 'b' * 100 + 'a' * 50
	t.run_prune_test(g16, inputStr, True, times)

	inputStr = 'a' * 50 + 'b' * 99 + 'a' * 50
	t.run_prune_test(g16, inputStr, False, times)

	############ grammar 17 ############################################################
	inputStr = ''
	for i in range(10, 1, -1):
		inputStr += 'a'*i + 'b'*i
	t.run_prune_test(g17, inputStr, True, times)

	inputStr = ''
	for i in range(4, 1, -1):
		inputStr += 'a'*i + 'b'*i
	inputStr += 'a'
	t.run_prune_test(g17, inputStr, False, times)

	g17.to_wk_cnf()

	inputStr = ''
	for i in range(7, 1, -1):
		inputStr += 'a'*i + 'b'*i
	t.run_prune_test(g17, inputStr, True, times)

	inputStr = ''
	for i in range(3, 1, -1):
		inputStr += 'a'*i + 'b'*i
	inputStr += 'a'
	t.run_prune_test(g17, inputStr, False, times)

	############ grammar 18 ############################################################
	inputStr = ''
	for i in range(15, 1, -1):
		inputStr += 'l' * i + 'r' * i
	t.run_prune_test(g18, inputStr, True, times)

	inputStr = ''
	for i in range(10, 1, -1):
		inputStr += 'l' * i + 'r' * i
	inputStr += 'lllrrr'
	t.run_prune_test(g18, inputStr, False, times)

	g18.to_wk_cnf()

	inputStr = ''
	for i in range(15, 1, -1):
		inputStr += 'l' * i + 'r' * i
	t.run_prune_test(g18, inputStr, True, times)

	inputStr = ''
	for i in range(10, 1, -1):
		inputStr += 'l' * i + 'r' * i
	inputStr += 'lllrrr'
	t.run_prune_test(g18, inputStr, False, times)

	############ grammar 19 ############################################################
	inputStr = 'a' * 100 + 'c' * 200 + 'b' * 100
	t.run_prune_test(g19, inputStr, True, times)

	inputStr = 'a' * 100 + 'c' * 100 + 'b' * 101
	t.run_prune_test(g19, inputStr, False, times)

	g19.to_wk_cnf()

	inputStr = 'a' * 50 + 'c' * 20 + 'b' * 50
	t.run_prune_test(g19, inputStr, True, times)

	inputStr = 'a' * 30 + 'c' * 20 + 'b' * 31
	t.run_prune_test(g19, inputStr, False, times)

	############ grammar 20 ############################################################
	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 110
	t.run_prune_test(g20, inputStr, True, times)

	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 111
	t.run_prune_test(g20, inputStr, False, times)

	g20.to_wk_cnf()

	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 110
	t.run_prune_test(g20, inputStr, True, times)

	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 111
	t.run_prune_test(g20, inputStr, False, times)

	print(t.timeouts)
	print(t.timesTaken)
	print(t.nodes)


if __name__ == "__main__":
	main()
