#!/usr/bin/python3

class cGrammarStatus:
    def __init__(self, word, strand, parsedUS, parsedLS):
        self.word = tuple(word)
        self.strand = tuple(strand)
        self.parsedUS = parsedUS
        self.parsedLS = parsedLS

    def __hash__(self):
        return hash(self.word) + hash(self.strand) + hash(self.parsedUS) + hash(self.parsedLS)

    def __eq__(self, other):
        return self.word == other.word and self.strand == other.strand and self.parsedUS == other.parsedUS and self.parsedLS == other.parsedLS

class cWKRule:
    def __init__(self, NT, result):
        self.NT = NT
        self.result = result

class cWKCFGrammar:
    def __init__(self, nonTerminals, terminals, startSymbol, rules):
        self.nonTerminals = nonTerminals
        self.terminals = terminals
        self.startSymbol = startSymbol
        self.rules = rules

        # we presume the complementary relation to be identity
        #self.complRelation = complRelation

    def contains(self, word):
        startState = cGrammarStatus([self.startSymbol], word, 0, 0)

        qOpen = [startState]  # TODO - use more suitable structure maybe (deque)?
        qClosed = set(startState)

        while qOpen:
            curStatus = qOpen.pop(0)
            for state in self.getAllFollowingStates(curStatus):
                if state not in qClosed:
                    if weAreDone():
                        return True
                    else:
                        qOpen.append(state)
                        qClosed.add(state)

        return False


    def getAllFollowingStates(self, curStatus):

        # get first NT
        NTidx = -1
        for idx, elem in enumerate(curStatus.word):
            if elem in self.nonTerminals:   # TODO - optimize (nonTerminals is now a list)
                NTidx = idx
                break

        if NTidx == -1:
            # no non-terminal - nothing to generate
            return

        for rule in self.rules:
            if self.isRuleSuitable(rule, curStatus, NTidx):
                yield rule

    def isRuleSuitable(self, rule, status, NTidx):
        # TODO - group rules by starting NT to avoid this
        if rule.NT != status.word[NTidx]:
            return False











    # TODO - find better name
    def weAreDone(self):
        # TODO
        return False









word = ''
g = cWKCFGrammar()
g.contains(word)
