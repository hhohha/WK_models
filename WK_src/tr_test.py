#!/usr/bin/python3

from grammars import g4
from ctf_WK_grammar import *
import time, random
from itertools import product
#import matplotlib.pyplot as plt

for rule in g4.rules:
	print(rule)

s = 'bgedga'
print(s)
#s = 'abababababababa'
res = g4.can_generate(s)
print(res)
