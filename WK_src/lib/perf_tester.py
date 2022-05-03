import time, random

class cPerfTester:
	def __init__(self):
		self.testCnt = 0
		self.timesTaken = [[], [], [], [], [], [], [] ,[], [], [], [], []]
		self.timeouts = [[], [], [], [], [], [], [] ,[], [], [], [], []]

	def printHeader(self, grammar, inputStr, shouldAccept):
		if len(inputStr) > 90:
			inputStr = inputStr[:80] + f'... [length {len(inputStr)}]'

		print(f'|{"="*150}|')
		print(f'| TEST {self.testCnt:3}{" "*141}|')
		print(f'|{"="*150}|')
		print(f'| GRAMMAR{" "*35}| {grammar.desc:105}|')
		lengths = f'{len(grammar.rules)} / {len(grammar.nts)} / {len(grammar.ts)}'
		print(f'| RULES / NON-TERMINALS / TERMINALS COUNT   | {lengths:105}|')
		print(f'| INPUT STRING{" "*30}| {inputStr:105}|')
		print(f'| SHOULD ACCEPT{" "*29}| {("Yes" if shouldAccept else "No"):105}|')
		print(f'| TIMEOUT{" "*35}| {str(grammar.timeLimit):105}|')
		print(f'|{"-"*150}|')
		print(f'| STRATEGY{" "*55}| TIME      | STATES QUEUED+CLOSED  | STATES PRUNED (SL, TL, WS, RL, RE)   | ACCEPTED |')
		print(f'|{"-"*150}|')

	def run_test_ntimes(self, grammar, inputStr, shouldAccept, times):
		statesOpenTotal, statesAllTotal, prunesTotal, timeTotal, results = 0, 0, [0, 0, 0, 0, 0], 0, []
		for i in range(times):
			start = time.time()
			statesOpen, statesAll, prunes, result = grammar.can_generate(inputStr)
			end = time.time()
			timeTaken = round(end - start, 4)

			statesOpenTotal += statesOpen
			statesAllTotal += statesAll
			prunesTotal = [a + b[1] for a, b in zip(prunesTotal, prunes)]
			timeTotal += timeTaken
			results.append(result)

		statesOpenTotal = round(statesOpenTotal/times)
		statesAllTotal = round(statesAllTotal/times)
		prunesTotal = list(map(lambda x: round(x/times), prunesTotal))
		timeTotal = round(timeTotal/times, 4)

		finalResult = ('TRUE' if shouldAccept else 'FALSE')
		for r in results:
			if r is None:
				finalResult = 'TIMEOUT'
				break
			elif r != shouldAccept:
				finalResult = 'ERROR'
				break

		return statesOpenTotal, statesAllTotal, prunesTotal, timeTotal, finalResult

	def run_test_suite(self, grammar, inputStr, shouldAccept, times=1):
		for k in grammar.pruningOptions:
			grammar.pruningOptions[k] = True

		self.testCnt += 1
		self.printHeader(grammar, inputStr, shouldAccept)

		timesChart = []
		for idx, t in enumerate(grammar.distance_calc_strategies_list):
			grammar.distance_calc_strategy = idx
			statesOpen, statesAll, prunes, timeTaken, result = self.run_test_ntimes(grammar, inputStr, shouldAccept, times)
			strategy = grammar.distance_calc_strategies_list[idx][0]
			statesStr = str(statesOpen) + ' + ' + str(statesAll-statesOpen)
			prunesStr = str(prunes).replace('[', '').replace(']', '')
			timesChart.append(timeTaken)

			self.timesTaken[idx] += timeTaken

			if result == 'TIMEOUT':
				self.timeouts[idx].append(True)
				self.timesTaken[idx].append(-1)
			else:
				self.timeouts[idx].append(False)
				self.timesTaken[idx].append(timeTaken)

			print(f'| {strategy:63}| {timeTaken:9} | {statesStr:21} | {prunesStr:36} | {result:8} |')

		print(self.timeouts)
		print()
		#print(f'|{"="*150}|')
		#print(f'| PRUNING {" "*55}| TIME      | STATES QUEUED+CLOSED  | STATES PRUNED (SL, TL, WS, RL, RE)   | ACCEPTED |')
		#print(f'|{"-"*150}|')

		#grammar.distance_calc_strategy = 5
		#prevKey = None
		#for key in grammar.pruningOptions:
			#if prevKey is not None:
				#grammar.pruningOptions[prevKey] = True
			#grammar.pruningOptions[key] = False
			#prevKey = key

			#statesOpen, statesAll, prunes, timeTaken, result = self.run_test_ntimes(grammar, inputStr, shouldAccept, times)
			#pruning = key.__name__ + ' OFF'
			#prunesStr = str(prunes).replace('[', '').replace(']', '')
			#statesStr = str(statesOpen) + ' + ' + str(statesAll-statesOpen)
			#print(f'| {pruning:63}| {timeTaken:9} | {statesStr:21} | {prunesStr:36} | {result:8} |')

		## all pruning options off
		#for k in grammar.pruningOptions:
			#grammar.pruningOptions[k] = False
		#statesOpen, statesAll, prunes, timeTaken, result = self.run_test_ntimes(grammar, inputStr, shouldAccept, times)
		#pruning = 'ALL OFF'
		#prunesStr = str(prunes).replace('[', '').replace(']', '')
		#statesStr = str(statesOpen) + ' + ' + str(statesAll-statesOpen)
		#print(f'| {pruning:63}| {timeTaken:9} | {statesStr:21} | {prunesStr:36} | {result:8} |')

		print(f'|{"="*150}|\n\n\n')
