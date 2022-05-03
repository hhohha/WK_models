#!/usr/bin/python3

from ctf_WK_grammar import *
import time, random
from itertools import product
import matplotlib.pyplot as plt


timeouts = [0, 0, 2, 2, 2, 0, 0, 1, 1, 1, 1, 3]
times = [34.857099999999996, 32.2831, 57.20819999999999, 72.52019999999997, 56.6824, 23.386200000000002, 22.722800000000007, 40.2755, 41.65160000000001, 40.3583, 41.6919, 100.50800000000002]

names = ['1', '2', '3', '4', '3m', '1+4','2+4','1+3','2+3','1+3m','2+3m','0']

plt.bar(names, times)
plt.show()
