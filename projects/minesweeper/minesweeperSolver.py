import minesweeper
import random

def detectTrivial(board):
	changed = 0

	for i in range(board.width):
		for j in range(board.height):
			if(board.isExplored(i, j) == 1 and board.unexploredAround(i, j) != 0):
				if(board.getBoard(i, j) == board.flaggedAround(i, j)):
					board.revealAround(i, j)
					changed = 1
				elif(board.getBoard(i, j) == board.unexploredAround(i, j) + board.flaggedAround(i, j)):
					board.flagAround(i, j)
					changed = 1

	return changed

def randomReveal(board):
	possiblePoints = []

	for i in range(board.width):
		for j in range(board.height):
			if board.isExplored(i, j) == 0 and board.isFlagged(i, j) == 0:
				possiblePoints.append((i, j))

	c = int(random.random() * len(possiblePoints))

	board.reveal(possiblePoints[c][0], possiblePoints[c][1])

def generate_Solve(width, height, mines):
	board = minesweeper.minesweeper(width, height, mines)

	board.reveal(0, 0)						#start from corner
	#board.reveal(width / 2, 0)				#start from edge
	#board.reveal(width / 2, height / 2)	#start from centre
	#board.showBoard()

	while(not board.won() and not board.lost()):
		#board.showBoard()
		changed = detectTrivial(board)

		if changed == 0:
			randomReveal(board)

	return board

cnt = 0

for i in range(10000):
	print i
	if(generate_Solve(16, 31, 99).won() == 1):
		cnt += 1

print cnt