import sys
from random import shuffle

class minesweeper:
	def __init__(self, width, height, mines):
		if(width * height - 1 <= mines):
			print "(__init__) Error: too many mines for this board size"
			return

		self.width = width
		self.height = height
		self.mines = mines

		self.board = []
		self.mine = []
		self.explored = []
		self.flagged = []

		for i in range(height):
			self.board.append([0] * width)
			self.mine.append([0] * width)
			self.explored.append([0] * width)
			self.flagged.append([0] * width)

		self.initialised = 0
		self.lose = 0
		self.win = 0
		self.exploredCnt = 0

	def showBoard(self):
		for i in range(self.height):
			for j in range(self.width):
				if(self.explored[i][j] == 0 and self.flagged[i][j] == 0):
					sys.stdout.write("#\t")
				elif(self.flagged[i][j] == 1):
					sys.stdout.write("F\t")
				else:
					sys.stdout.write(str(self.board[i][j]) + "\t")

			sys.stdout.write("\n")

		sys.stdout.write("\n")

	'''
	def showBoardBare(self):
		for i in range(self.height):
			for j in range(self.width):
				sys.stdout.write(str(self.board[i][j]) + "\t")

			sys.stdout.write("\n")

		sys.stdout.write("\n")
	'''

	def layMines(self, x, y, mines):
		mine = [0] * (self.width * self.height - 1 - mines) + [1] * mines
		shuffle(mine)
		c = 0

		for i in range(self.height):
			for j in range(self.width):
				if(i != y or j != x):
					self.mine[i][j] = mine[c]
					c += 1
				else:
					self.mine[i][j] = 0

		for i in range(self.height):
			for j in range(self.width):
				if(self.mine[i][j] == 1):
					self.board[i][j] = -1
				else:
					self.board[i][j] = 0

					if(j > 0):
						self.board[i][j] += self.mine[i][j - 1]
					if(j < self.width - 1):
						self.board[i][j] += self.mine[i][j + 1]

					if(i > 0):
						self.board[i][j] += self.mine[i - 1][j]

						if(j > 0):
							self.board[i][j] += self.mine[i - 1][j - 1]
						if(j < self.width - 1):
							self.board[i][j] += self.mine[i - 1][j + 1]

					if(i < self.height - 1):
						self.board[i][j] += self.mine[i + 1][j]

						if(j > 0):
							self.board[i][j] += self.mine[i + 1][j - 1]
						if(j < self.width - 1):
							self.board[i][j] += self.mine[i + 1][j + 1]

	def flag(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(flag) Error: invalid coordinates"
			return 501

		if(self.explored[y][x] == 1):
			print "(flag) Warning: cell is already explored"
			return 502

		self.flagged[y][x] = 1

		return 0

	def reveal(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(reveal) Error: invalid coordinates"
			return 501

		if(self.explored[y][x] == 1):
			print "(reveal) Warning: cell is already explored"
			return 502

		if(self.flagged[y][x] == 1):
			print "(reveal) Warning: cell is flagged"
			return 503

		self.exploredCnt += 1
		self.explored[y][x] = 1

		if(self.exploredCnt == 1):
			self.layMines(x, y, self.mines)
		elif(self.mine[y][x] == 1):
			self.lose = 1
			print "(reveal) Status: Lost\n"
			return -1
		elif(self.exploredCnt == self.height * self.width - self.mines):
			self.win = 1
			print "(reveal) Status: Won\n"
			return -2

		return 0

	def won(self):
		return self.win

	def lost(self):
		return self.lose

	def getBoard(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(getBoard) Error: invalid coordinates"
			return 501

		if(self.explored[y][x] == 0):
			print "(getBoard) Warning: cell is not explored"
			return 504

		return self.board[y][x]

	def isExplored(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(isExplored) Error: invalid coordinates"
			return 501

		return self.explored[y][x]

	def isFlagged(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(isFlagged) Error: invalid coordinates"
			return 501

		return self.flagged[y][x]

	def flaggedAround(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(flaggedAround) Error: invalid coordinates"
			return 501

		res = 0

		if(x > 0):
			res += self.flagged[y][x - 1]
		if(x < self.width - 1):
			res += self.flagged[y][x + 1]

		if(y > 0):
			res += self.flagged[y - 1][x]

			if(x > 0):
				res += self.flagged[y - 1][x - 1]
			if(x < self.width - 1):
				res += self.flagged[y - 1][x + 1]

		if(y < self.height - 1):
			res += self.flagged[y + 1][x]

			if(x > 0):
				res += self.flagged[y + 1][x - 1]
			if(x < self.width - 1):
				res += self.flagged[y + 1][x + 1]

		return res

	def unexploredAround(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(unexploredAround) Error: invalid coordinates"
			return 501

		res = 0

		if(x > 0):
			if self.isExplored(x - 1, y) == 0 and self.flagged[y][x - 1] == 0:
				res += 1
		if(x < self.width - 1):
			if self.isExplored(x + 1, y) == 0 and self.flagged[y][x + 1] == 0:
				res += 1

		if(y > 0):
			if self.isExplored(x, y - 1) == 0 and self.flagged[y - 1][x] == 0:
				res += 1

			if(x > 0):
				if self.isExplored(x - 1, y - 1) == 0 and self.flagged[y - 1][x - 1] == 0:
					res += 1
			if(x < self.width - 1):
				if self.isExplored(x + 1, y - 1) == 0 and self.flagged[y - 1][x + 1] == 0:
					res += 1

		if(y < self.height - 1):
			if self.isExplored(x, y + 1) == 0 and self.flagged[y + 1][x] == 0:
				res += 1

			if(x > 0):
				if self.isExplored(x - 1, y + 1) == 0 and self.flagged[y + 1][x - 1] == 0:
					res += 1
			if(x < self.width - 1):
				if self.isExplored(x + 1, y + 1) == 0  and self.flagged[y + 1][x + 1] == 0:
					res += 1

		return res

	def revealAround(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(revealAround) Error: invalid coordinates"
			return 501

		if(x > 0):
			if self.isExplored(x - 1, y) == 0 and self.isFlagged(x - 1, y) == 0:
				self.reveal(x - 1, y)
		if(x < self.width - 1):
			if self.isExplored(x + 1, y) == 0 and self.isFlagged(x + 1, y) == 0:
				self.reveal(x + 1, y)

		if(y > 0):
			if self.isExplored(x, y - 1) == 0 and self.isFlagged(x, y - 1) == 0:
				self.reveal(x, y - 1)

			if(x > 0):
				if self.isExplored(x - 1, y - 1) == 0 and self.isFlagged(x - 1, y - 1) == 0:
					self.reveal(x - 1, y - 1)
			if(x < self.width - 1):
				if self.isExplored(x + 1, y - 1) == 0 and self.isFlagged(x + 1, y - 1) == 0:
					self.reveal(x + 1, y - 1)

		if(y < self.height - 1):
			if self.isExplored(x, y + 1) == 0 and self.isFlagged(x, y + 1) == 0:
				self.reveal(x, y + 1)

			if(x > 0):
				if self.isExplored(x - 1, y + 1) == 0 and self.isFlagged(x - 1, y + 1) == 0:
					self.reveal(x - 1, y + 1)
			if(x < self.width - 1):
				if self.isExplored(x + 1, y + 1) == 0 and self.isFlagged(x + 1, y + 1) == 0:
					self.reveal(x + 1, y + 1)

	def flagAround(self, x, y):
		if(x < 0 or y < 0 or x >= self.width or y >= self.height):
			print "(flagAround) Error: invalid coordinates"
			return 501

		if(x > 0):
			if self.isExplored(x - 1, y) == 0:
				self.flag(x - 1, y)
		if(x < self.width - 1):
			if self.isExplored(x + 1, y) == 0:
				self.flag(x + 1, y)

		if(y > 0):
			if self.isExplored(x, y - 1) == 0:
				self.flag(x, y - 1)

			if(x > 0):
				if self.isExplored(x - 1, y - 1) == 0:
					self.flag(x - 1, y - 1)
			if(x < self.width - 1):
				if self.isExplored(x + 1, y - 1) == 0:
					self.flag(x + 1, y - 1)

		if(y < self.height - 1):
			if self.isExplored(x, y + 1) == 0:
				self.flag(x, y + 1)

			if(x > 0):
				if self.isExplored(x - 1, y + 1) == 0:
					self.flag(x - 1, y + 1)
			if(x < self.width - 1):
				if self.isExplored(x + 1, y + 1) == 0:
					self.flag(x + 1, y + 1)