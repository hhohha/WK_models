#!/usr/bin/python3

import random
from lib.perf_tester import cPerfTester
from grammars import *

def main():
	times = 7
	t = cPerfTester()

	############ grammar 1 #############################################################
	inputStr = 'a' * 801
	t.run_test_suite(g1, inputStr, True, times)

	g1.to_wk_cnf()

	inputStr = 'a' * 501
	t.run_test_suite(g1, inputStr, True, times)

	############ grammar 2 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(500)]) + 'abc'
	t.run_test_suite(g2, inputStr, True, times)

	g2.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'abc'
	t.run_test_suite(g2, inputStr, True, times)

	############ grammar 3 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(300)]) + 'abc'
	t.run_test_suite(g3, inputStr, True, times)

	g3.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(9)]) + 'abc'
	t.run_test_suite(g3, inputStr, True, times)

	############ grammar 4 #############################################################
	inputStr = ''.join([random.choice('abcdefg') for i in range(80)]) + 'a'
	t.run_test_suite(g4, inputStr, True, times)

	g4.to_wk_cnf()

	inputStr = ''.join([random.choice('abcdefg') for i in range(40)]) + 'a'
	t.run_test_suite(g4, inputStr, True, times)

	############ grammar 5 #############################################################
	inputStr = ''.join([random.choice('acgt') for i in range(400)]) + 'ctg'
	t.run_test_suite(g5, inputStr, True, times)

	g5.to_wk_cnf()

	inputStr = ''.join([random.choice('acgt') for i in range(400)]) + 'ctg'
	t.run_test_suite(g5, inputStr, True, times)

	############ grammar 6 #############################################################
	inputStr = 'a'*300 + 'b'*300
	t.run_test_suite(g6, inputStr, True, times)

	g6.to_wk_cnf()

	inputStr = 'a'*300 + 'b'*300
	t.run_test_suite(g6, inputStr, True, times)

	############ grammar 7 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += 'c' + inputStr[::-1]
	t.run_test_suite(g7, inputStr, True, times)

	g7.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(300)])
	inputStr += 'c' + inputStr[::-1]
	t.run_test_suite(g7, inputStr, True, times)

	############ grammar 8 #############################################################
	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += inputStr[::-1]
	t.run_test_suite(g8, inputStr, True, times)

	g8.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(400)])
	inputStr += inputStr[::-1]
	t.run_test_suite(g8, inputStr, True, times)

	############ grammar 9 #############################################################
	inputStr = ''.join([random.choice('01') for i in range(100)]) + '2' + ''.join([random.choice('01') for i in range(101)])
	t.run_test_suite(g9, inputStr, True, times)

	g9.to_wk_cnf()

	inputStr = ''.join([random.choice('01') for i in range(60)]) + '2' + ''.join([random.choice('01') for i in range(61)])
	t.run_test_suite(g9, inputStr, True, times)

	############ grammar 10 ############################################################
	inputStr = 'o0p1s0cp'*7 + '0'
	t.run_test_suite(g10, inputStr, True, times)

	g10.to_wk_cnf()

	inputStr = 'o0p1s0cp'*7 + '0'
	t.run_test_suite(g10, inputStr, True, times)

	############ grammar 11 ############################################################
	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += inputStr + 'a'
	t.run_test_suite(g11, inputStr, True, times)

	g11.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(10)])
	inputStr += inputStr + 'a'
	t.run_test_suite(g11, inputStr, True, times)

	############ grammar 12 ############################################################
	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 100 + 'r' * 100
	t.run_test_suite(g12, inputStr, True, times)

	g12.to_wk_cnf()

	inputStr = 'r' * 100 + 'd' * 100 + 'u' * 100 + 'r' * 100
	t.run_test_suite(g12, inputStr, True, times)

	############ grammar 13 ############################################################
	inputStr = 'a' * 100 + 'c' * 100 + 'b' * 100
	t.run_test_suite(g13, inputStr, True, times)

	g13.to_wk_cnf()

	inputStr = 'a' * 100 + 'c' * 100 + 'b' * 100
	t.run_test_suite(g13, inputStr, True, times)

	############ grammar 14 ############################################################
	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 101
	t.run_test_suite(g14, inputStr, True, times)

	g14.to_wk_cnf()

	inputStr = 'a' * 100 + 'b' * 101 + 'c' * 100 + 'd' * 101
	t.run_test_suite(g14, inputStr, True, times)

	############ grammar 15 ############################################################
	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr
	t.run_test_suite(g15, inputStr, True, times)

	g15.to_wk_cnf()

	inputStr = ''.join([random.choice('ab') for i in range(100)])
	inputStr += 'c' + inputStr
	t.run_test_suite(g15, inputStr, True, times)

	############ grammar 16 ############################################################
	inputStr = 'a' * 100 + 'b' * 200 + 'a' * 100
	t.run_test_suite(g16, inputStr, True, times)

	g16.to_wk_cnf()

	inputStr = 'a' * 50 + 'b' * 100 + 'a' * 50
	t.run_test_suite(g16, inputStr, True, times)

	############ grammar 17 ############################################################
	inputStr = ''
	for i in range(10, 1, -1):
		inputStr += 'a'*i + 'b'*i
	t.run_test_suite(g17, inputStr, True, times)

	g17.to_wk_cnf()

	inputStr = ''
	for i in range(7, 1, -1):
		inputStr += 'a'*i + 'b'*i
	t.run_test_suite(g17, inputStr, True, times)

	############ grammar 18 ############################################################
	inputStr = ''
	for i in range(15, 1, -1):
		inputStr += 'l' * i + 'r' * i
	t.run_test_suite(g18, inputStr, True, times)

	g18.to_wk_cnf()

	inputStr = ''
	for i in range(15, 1, -1):
		inputStr += 'l' * i + 'r' * i
	t.run_test_suite(g18, inputStr, True, times)

	############ grammar 19 ############################################################
	inputStr = 'a' * 100 + 'c' * 200 + 'b' * 100
	t.run_test_suite(g19, inputStr, True, times)

	g19.to_wk_cnf()

	inputStr = 'a' * 50 + 'c' * 20 + 'b' * 50
	t.run_test_suite(g19, inputStr, True, times)

	############ grammar 20 ############################################################
	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 110
	t.run_test_suite(g20, inputStr, True, times)

	g20.to_wk_cnf()

	inputStr = 'a' * 100 + 'b' * 90 + 'c' * 80 + 'd' * 110
	t.run_test_suite(g20, inputStr, True, times)

	print(t.timeouts)
	print(t.timesTaken)


if __name__ == "__main__":
	main()
