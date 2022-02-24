#!/usr/bin/python3

statesCnt = 1

class cWKRule:
    def __init__(self, stateFrom, stateTo, upperStr, lowerStr):
        self.stateFrom = stateFrom
        self.stateTo = stateTo
        self.upperStr = upperStr
        self.lowerStr = lowerStr


class cWKStatus:
    def __init__(self, state, upperParsed, lowerParsed):
        self.state = state
        self.upperParsed = upperParsed
        self.lowerParsed = lowerParsed

    def __eq__(self, other):
        self.state == other.state and self.upperParsed == other.upperParsed and self.lowerParsed == other.lowerParsed

    def __hash__(self):
        return hash((self.state, self.upperParsed, self.lowerParsed))


class cWKA:
    def __init__(self, alphabet, complRelation, states, initState, finalStates, rules):
        for a, b in complRelation:
            if a not in alphabet or b not in alphabet:
                raise ValueError

        if initState not in states:
            raise ValueError

        for state in finalStates:
            if state not in states:
                raise ValueError

        for rule in rules:
            if rule.stateFrom not in states or rule.stateTo not in states:
                raise ValueError

            for c in rule.upperStr:
                if c not in alphabet:
                    raise ValueError

            for c in rule.lowerStr:
                if c not in alphabet:
                    raise ValueError

        self.alphabet = alphabet
        self.complRelation = complRelation
        self.states = states
        self.initState = initState
        self.finalStates = finalStates
        self.rules = rules


    def run(self, upperStr):
        openStates = [cWKStatus(self.initState, '', '')]
        closedStates = set()

        while openStates:
            currentState = openStates.pop(0)
            closedStates.add(currentState)

            for newState in self.getNextStates(currentState, upperStr):
                if newState not in openStates and newState not in closedStates:
                    if self.checkIfAccepted(newState, len(upperStr)):
                        print('lower strand:', newState.lowerParsed)
                        return True
                    openStates.append(newState)
        return False


    def getNextStates(self, currentStatus, upperStr):

        for rule in self.rules:
            if rule.stateFrom != currentStatus.state:
                continue

            if not upperStr.startswith(rule.upperStr, len(currentStatus.upperParsed)) or len(currentStatus.lowerParsed) + len(rule.lowerStr) > len(upperStr):
                continue

            upperIdx = len(currentStatus.lowerParsed)
            relationOk = True

            for c1 in rule.lowerStr:
                c2 = upperStr[upperIdx]
                upperIdx += 1
                if (c2, c1) not in self.complRelation:
                    relationOk = False
                    break
            if relationOk:
                yield cWKStatus(rule.stateTo, currentStatus.upperParsed + rule.upperStr, currentStatus.lowerParsed + rule.lowerStr)


    def checkIfAccepted(self, currentStatus, upperStrLen):
        return currentStatus.state in self.finalStates and len(currentStatus.upperParsed) == upperStrLen and len(currentStatus.lowerParsed) == upperStrLen
