#!/usr/bin/python3

import time
from ctf_WK_grammar import *

def run_perf_test(grammar: cWK_CFG, inputStr: str) -> None:

	for idx, t in enumerate(grammar.distance_calc_strategies_list):
		grammar.distance_calc_strategy = idx
		start = time.time()
		openStates, closedStates, actual = grammar.can_generate(inputStr)
		end = time.time()
		print(f'strategy used: {t[0]}     time taken: {end-start}     states analysed: {closedStates}')



rules: List[cRule] = [
	cRule('A', ['A', 'A', 'A']),
	cRule('A', [(['a'], ['a'])])
]
g = cWK_CFG(['A'], ['a'], 'A', rules, [('a', 'a')])
g.desc = 'a(aa)*'

run_perf_test(g, 'aaaaaaaaaaaaaaaaaaa')
