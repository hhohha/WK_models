#!/usr/bin/python3

from lib.perf_tester import cPerfTester
from lib.grammars import *

def main():
	times = 1
	t = cPerfTester()

	############ grammar 1 #############################################################
	t.run_speed_test(g1, input_gen_func(501, 100, True), True, times)
	t.run_speed_test(g1, input_gen_func(100, 20, False), False, times)

	g1.to_wk_cnf()

	t.run_speed_test(g1, input_gen_func(100, 20, True), True, times)
	t.run_speed_test(g1, input_gen_func(10, 2, False), False, times)

	############ grammar 2 #############################################################
	t.run_speed_test(g2, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g2, input_gen_func(200, 100, False), False, times)

	g2.to_wk_cnf()

	t.run_speed_test(g2, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g2, input_gen_func(100, 50, False), False, times)

	############ grammar 3 #############################################################
	t.run_speed_test(g3, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g3, input_gen_func(200, 100, False), False, times)

	g3.to_wk_cnf()

	t.run_speed_test(g3, input_gen_func(3, 1, True), True, times)
	t.run_speed_test(g3, input_gen_func(3, 1, False), False, times)

	############ grammar 4 #############################################################

	t.run_speed_test(g4, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g4, input_gen_func(100, 50, False), False, times)

	g4.to_wk_cnf()

	t.run_speed_test(g4, input_gen_func(10, 10, True), True, times)
	t.run_speed_test(g4, input_gen_func(5, 3, False), False, times)

	############ grammar 5 #############################################################

	############ grammar 6 #############################################################

	t.run_speed_test(g6, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g6, input_gen_func(100, 50, False), False, times)

	g6.to_wk_cnf()

	t.run_speed_test(g6, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g6, input_gen_func(100, 50, False), False, times)

	############ grammar 7 #############################################################

	t.run_speed_test(g7, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g7, input_gen_func(200, 100, False), False, times)

	g7.to_wk_cnf()

	t.run_speed_test(g7, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g7, input_gen_func(200, 100, False), False, times)

	############ grammar 8 #############################################################

	t.run_speed_test(g8, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g8, input_gen_func(200, 100, False), False, times)

	g8.to_wk_cnf()

	t.run_speed_test(g8, input_gen_func(200, 50, True), True, times)
	t.run_speed_test(g8, input_gen_func(200, 50, False), False, times)

	############ grammar 9 #############################################################

	t.run_speed_test(g9, input_gen_func(100, 20, True), True, times)
	t.run_speed_test(g9, input_gen_func(50, 20, False), False, times)

	g9.to_wk_cnf()

	t.run_speed_test(g9, input_gen_func(50, 10, True), True, times)
	t.run_speed_test(g9, input_gen_func(20, 10, False), False, times)

	############ grammar 10 ############################################################

	t.run_speed_test(g10, input_gen_func(50, 10, True), True, times)
	t.run_speed_test(g10, input_gen_func(20, 10, False), False, times)

	g10.to_wk_cnf()

	t.run_speed_test(g10, input_gen_func(40, 10, True), True, times)
	t.run_speed_test(g10, input_gen_func(30, 5, False), False, times)

	############ grammar 11 ############################################################

	t.run_speed_test(g11, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g11, input_gen_func(50, 5, False), False, times)

	g11.to_wk_cnf()

	t.run_speed_test(g11, input_gen_func(6, 2, True), True, times)
	t.run_speed_test(g11, input_gen_func(6, 2, False), False, times)

	############ grammar 12 ############################################################

	t.run_speed_test(g12, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g12, input_gen_func(200, 100, False), False, times)

	g12.to_wk_cnf()

	t.run_speed_test(g12, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g12, input_gen_func(200, 100, False), False, times)

	############ grammar 13 ############################################################

	t.run_speed_test(g13, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g13, input_gen_func(200, 100, False), False, times)

	g13.to_wk_cnf()

	t.run_speed_test(g13, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g13, input_gen_func(200, 100, False), False, times)

	############ grammar 14 ############################################################

	t.run_speed_test(g14, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g14, input_gen_func(200, 100, False), False, times)

	g14.to_wk_cnf()

	t.run_speed_test(g14, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g14, input_gen_func(200, 100, False), False, times)

	############ grammar 15 ############################################################

	t.run_speed_test(g15, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g15, input_gen_func(100, 50, False), False, times)

	g15.to_wk_cnf()

	t.run_speed_test(g15, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g15, input_gen_func(100, 50, False), False, times)

	############ grammar 16 ############################################################

	t.run_speed_test(g16, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g16, input_gen_func(100, 50, False), False, times)

	g16.to_wk_cnf()

	t.run_speed_test(g16, input_gen_func(50, 30, True), True, times)
	t.run_speed_test(g16, input_gen_func(50, 30, False), False, times)

	############ grammar 17 ############################################################

	t.run_speed_test(g17, input_gen_func(10, 2, True), True, times)
	t.run_speed_test(g17, input_gen_func(10, 2, False), False, times)

	g17.to_wk_cnf()

	t.run_speed_test(g17, input_gen_func(10, 2, True), True, times)
	t.run_speed_test(g17, input_gen_func(10, 2, False), False, times)

	############ grammar 18 ############################################################

	t.run_speed_test(g18, input_gen_func(200, 100, True), True, times)
	t.run_speed_test(g18, input_gen_func(80, 30, False), False, times)

	g18.to_wk_cnf()

	t.run_speed_test(g18, input_gen_func(100, 20, True), True, times)
	t.run_speed_test(g18, input_gen_func(80, 30, False), False, times)

	############ grammar 19 ############################################################

	t.run_speed_test(g19, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g19, input_gen_func(100, 20, False), False, times)

	g19.to_wk_cnf()

	t.run_speed_test(g19, input_gen_func(100, 30, True), True, times)
	t.run_speed_test(g19, input_gen_func(50, 5, False), False, times)

	############ grammar 20 ############################################################

	t.run_speed_test(g20, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g20, input_gen_func(100, 50, False), False, times)

	g20.to_wk_cnf()

	t.run_speed_test(g20, input_gen_func(100, 50, True), True, times)
	t.run_speed_test(g20, input_gen_func(100, 50, False), False, times)

	print(t.tests)

if __name__ == "__main__":
	main()
