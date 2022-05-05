#!/usr/bin/python3

import random
from lib.perf_tester import cPerfTester
from grammars import *

def main():
	t = cPerfTester()

	############ grammar 1 #############################################################
	g1.to_wk_cnf()

	t.run_wk_cyk_test(g1, g1.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g1, g1.input_gen_func(10, 2, False), False)

	############ grammar 2 #############################################################
	g2.to_wk_cnf()

	t.run_wk_cyk_test(g2, g2.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g2, g2.input_gen_func(10, 2, False), False)

	############ grammar 3 #############################################################
	g3.to_wk_cnf()

	t.run_wk_cyk_test(g3, g3.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g3, g3.input_gen_func(10, 2, False), False)

	############ grammar 4 #############################################################
	g4.to_wk_cnf()

	t.run_wk_cyk_test(g4, g4.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g4, g4.input_gen_func(10, 2, False), False)

	############ grammar 5 #############################################################
	g5.to_wk_cnf()

	t.run_wk_cyk_test(g5, g5.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g5, g5.input_gen_func(10, 2, False), False)

	############ grammar 6 #############################################################
	g6.to_wk_cnf()

	t.run_wk_cyk_test(g6, g6.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g6, g6.input_gen_func(10, 2, False), False)

	############ grammar 7 #############################################################
	g7.to_wk_cnf()

	t.run_wk_cyk_test(g7, g7.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g7, g7.input_gen_func(10, 2, False), False)

	############ grammar 8 #############################################################
	g8.to_wk_cnf()

	t.run_wk_cyk_test(g8, g8.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g8, g8.input_gen_func(10, 2, False), False)

	############ grammar 9 #############################################################
	g9.to_wk_cnf()

	t.run_wk_cyk_test(g9, g9.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g9, g9.input_gen_func(10, 2, False), False)

	############ grammar 10 ############################################################
	g10.to_wk_cnf()

	t.run_wk_cyk_test(g10, g10.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g10, g10.input_gen_func(10, 2, False), False)

	############ grammar 11 ############################################################
	g11.to_wk_cnf()

	t.run_wk_cyk_test(g11, g11.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g11, g11.input_gen_func(10, 2, False), False)

	############ grammar 12 ############################################################
	g12.to_wk_cnf()

	t.run_wk_cyk_test(g12, g12.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g12, g12.input_gen_func(10, 2, False), False)

	############ grammar 13 ############################################################
	g13.to_wk_cnf()

	t.run_wk_cyk_test(g13, g13.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g13, g13.input_gen_func(10, 2, False), False)

	############ grammar 14 ############################################################
	g14.to_wk_cnf()

	t.run_wk_cyk_test(g14, g14.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g14, g14.input_gen_func(10, 2, False), False)

	############ grammar 15 ############################################################
	g15.to_wk_cnf()

	t.run_wk_cyk_test(g15, g15.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g15, g15.input_gen_func(10, 2, False), False)

	############ grammar 16 ############################################################
	g16.to_wk_cnf()

	t.run_wk_cyk_test(g16, g16.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g16, g16.input_gen_func(10, 2, False), False)

	############ grammar 17 ############################################################
	g17.to_wk_cnf()

	t.run_wk_cyk_test(g17, g17.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g17, g17.input_gen_func(10, 2, False), False)

	############ grammar 18 ############################################################
	g18.to_wk_cnf()

	t.run_wk_cyk_test(g18, g18.input_gen_func(10, 2, True), True)
	t.run_wk_cyk_test(g18, g18.input_gen_func(10, 2, False), False)

	print(t.tests)

if __name__ == "__main__":
	main()
