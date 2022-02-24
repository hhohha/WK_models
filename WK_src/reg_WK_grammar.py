#!/usr/bin/python3

from random import choice

class cWKRule:
    def __init__(self, leftNT, rightNT, upperStr, lowerStr):
        self.leftNT = leftNT
        self.rightNT = rightNT
        self.upperStr = upperStr
        self.lowerStr = lowerStr

    def __str__(self):
        return str(self.leftNT) + '  ->  <' + str(self.upperStr) + '/' + str(self.lowerStr) + '> ' + ('' if self.rightNT is None else str(self.rightNT))

    __repr__ = __str__

class cWKGrammar:
    def __init__(self, nonTerminals, terminals, startSymbol, rules, complRelation):
        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.startSymbol = startSymbol
        self.rules = rules
        self.complRelation = complRelation
        self.limit = 1000

    def generate(self):
        currentUS = ''
        currentLS = ''
        currentNT = self.startSymbol
        i = 0

        while currentNT is not None:
            if i >= self.limit:
                print('\niteration limit reached\n')
                print(f'{currentUS}\n{"-" * max(len(currentUS), len(currentLS))}\n{currentLS}')
                return False
            i += 1

            rules = self.getValidRules(currentNT, currentUS, currentLS)
            if not rules:
                print('\ngeneration stuck\n')
                print(f'{currentUS}\n{"-" * max(len(currentUS), len(currentLS))}\n{currentLS}')
                return False

            rule = choice(rules)
            print('using rule: ', rule)
            currentUS += rule.upperStr
            currentLS += rule.lowerStr
            currentNT = rule.rightNT

        if len(currentUS) == len(currentLS):
            print('\ngeneration finished successfully\n')
            print(f'{currentUS}\n{"-" * max(len(currentUS), len(currentLS))}\n{currentLS}')
            return True
        else:
            print('\nstrands don\'t match\n')
            print(f'{currentUS}\n{"-" * max(len(currentUS), len(currentLS))}\n{currentLS}')
            return False


    def getValidRules(self, currentNT, currentUS, currentLS):

        rules = []

        for rule in self.rules:
            if rule.leftNT != currentNT:
                continue

            tmpUpper = currentUS + rule.upperStr
            tmpLower = currentLS + rule.lowerStr

            idx = min(len(currentLS), len(currentUS))
            ruleOk = True
            while idx < min(len(tmpUpper), len(tmpLower)):
                if (tmpUpper[idx], tmpLower[idx]) not in self.complRelation:
                    ruleOk = False
                    break
                idx += 1

            if ruleOk:
                rules.append(rule)

        return rules


nonTerms = ['S', 'A']
terms = ['a', 'b']
startSymbol = 'S'
rules = [
    cWKRule('S', 'A', 'a', 'a'),
    cWKRule('S', 'A', 'b', 'a'),
    cWKRule('S', 'A', 'b', 'b'),
    cWKRule('A', 'A', 'aa', 'a'),
    cWKRule('A', 'A', 'a', 'aa'),
    cWKRule('A', 'A', 'a', 'b'),
    cWKRule('A', None, 'b', 'b'),
]
cRel = [
    ('a', 'a'),
    ('b', 'b')
]


grammar = cWKGrammar(nonTerms, terms, startSymbol, rules, cRel)
grammar.generate()
