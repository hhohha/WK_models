#!/usr/bin/python3

from grammars import *

#s = 'b' +  'a'*1900

# grammar 5 #####################################
s = 'c' * 1000 + 'tg'
s = 'ct' + 1000*'g'
s = 500*'c' + 't' + 500*'g'
s = 500*'a' + 'ctg' + 500*'a'


# grammar 6 #####################################

s = 'a'*500
s = 'b'*500
s = 'a' + 'b'*500
s = 'a'*500 + 'b'*499

# grammar 7 #####################################

s = 'a'*1000
s = 'c' + 'a'*1000
s = 10 *'a' + 'c' + 'a'*10
s = 'a'*1000 + 'c'
s = 'a'*1000 + 'c' + 100*'a'


# grammar 8 #####################################

s = 'ab'*200
s += s[::-1]

start = time.time()
statesOpen, statesAll, prunes, result = g8.can_generate(s)
end = time.time()
timeTaken = round(end - start, 4)



print(f'time: {timeTaken}')
print(f'states open: {statesOpen},    states closed: {statesAll - statesOpen}')
print(f'prunes: {list(map(lambda x: x[1], prunes))}')
print(f'result: {result}')
