#!/usr/bin/python3

from automata import cWKRule, cWKA

def test1():
    # abc
    alphabet = ['a', 'b', 'c', 'd']
    states = ['q0', 'q1', 'q2', 'q3']
    relation = [
        ('a', 'b'),
        ('b', 'c'),
        ('c', 'd'),
        ('d', 'a')
    ]
    firstState = 'q0'
    finalStates = ['q3']
    rules = [
        cWKRule('q0', 'q1', 'a', ''),
        cWKRule('q1', 'q2', 'bc', 'b'),
        cWKRule('q2', 'q3', '', 'cd')
    ]

    wka = cWKA(alphabet, relation, states, firstState, finalStates, rules)

    upperStrand = 'abc'

    result = wka.run(upperStrand)
    print(result)

def test2():
    # a^nb^n or b^na^n

    alphabet = ['a', 'b']
    states = ['q0', 'q1', 'q2', 'q3', 'q4']
    relation = [
        ('a', 'a'),
        ('b', 'b')
    ]
    firstState = 'q0'
    finalStates = ['q3', 'q4']
    rules = [
        cWKRule('q0', 'q1', 'a', ''),
        cWKRule('q0', 'q2', '', 'b'),
        cWKRule('q1', 'q1', 'a', ''),
        cWKRule('q1', 'q3', 'b', 'a'),
        cWKRule('q3', 'q3', 'b', 'a'),
        cWKRule('q3', 'q3', '', 'b'),
        cWKRule('q2', 'q2', '', 'b'),
        cWKRule('q2', 'q4', 'b', 'a'),
        cWKRule('q4', 'q4', 'b', 'a'),
        cWKRule('q4', 'q4', 'a', '')
    ]

    wka = cWKA(alphabet, relation, states, firstState, finalStates, rules)

    upperStrand = 'aaabbb'

    result = wka.run(upperStrand)
    print(result)

def test3():
    # w != w^R

    alphabet = ['a', 'b', 'v', 'w', 'c']
    states = ['q0', 'q1', 'qa', 'qb']
    relation = [
        ('a', 'a'),
        ('a', 'v'),
        ('v', 'a'),
        ('b', 'b'),
        ('b', 'w'),
        ('w', 'b'),
        ('c', 'a'),
        ('a', 'c'),
        ('c', 'b'),
        ('b', 'c'),
    ]
    firstState = 'q0'
    finalStates = ['q1']
    rules = [
        cWKRule('q0', 'q0', '', 'a'),
        cWKRule('q0', 'q0', '', 'b'),
        cWKRule('q0', 'qa', '', 'v'),
        cWKRule('q0', 'qb', '', 'w'),
        cWKRule('qa', 'qa', 'a', 'a'),
        cWKRule('qa', 'qa', 'a', 'b'),
        cWKRule('qa', 'qa', 'b', 'a'),
        cWKRule('qa', 'qa', 'b', 'b'),
        cWKRule('qb', 'qb', 'a', 'a'),
        cWKRule('qb', 'qb', 'a', 'b'),
        cWKRule('qb', 'qb', 'b', 'a'),
        cWKRule('qb', 'qb', 'b', 'b'),
        cWKRule('qa', 'q1', 'ab', 'c'),
        cWKRule('qa', 'q1', 'ba', 'c'),
        cWKRule('qb', 'q1', 'ab', 'c'),
        cWKRule('qb', 'q1', 'ba', 'c'),
        cWKRule('q1', 'q1', 'a', ''),
        cWKRule('q1', 'q1', 'b', '')
    ]

    wka = cWKA(alphabet, relation, states, firstState, finalStates, rules)

    upperStrand = 'aabba'

    result = wka.run(upperStrand)
    print(result)

def test4():
    # a^(2n)b^(2n) or b^(2n)a^(2n)
    alphabet = ['a', 'b']
    states = ['q0']
    relation = [
        ('a', 'a'),
        ('b', 'b')
    ]
    firstState = 'q0'
    finalStates = ['q0']
    rules = [
        cWKRule('q0', 'q0', 'aa', 'a'),
        cWKRule('q0', 'q0', 'b', 'a'),
        cWKRule('q0', 'q0', 'b', 'bb')
    ]

    wka = cWKA(alphabet, relation, states, firstState, finalStates, rules)

    upperStrand = 'aabb'

    result = wka.run(upperStrand)
    print(result)


def main():
    test1()
    test2()
    test3()
    test4()

if __name__ == '__main__':
    main()
