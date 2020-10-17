from tkinter import *

# Author: Declan Sheehan

# Conway's Game of Life Rules:
# 1. Any live cell with less than 2 living neighbors dies.
#	- if A <  2: DIE
# 2. Any cell with 2 or more living neighbors lives on.
# 	- if A >= 2: LIVE
# 3. Any living cell with more than 3 living neighbors dies.
# 	- if A >  3: DIE
# 4. Any dead cell with exactly 3 living neighbors lives.
# 	- if A == 3: LIVE


class Conway(Frame):
	def __init__(self):
		super().__init__()

		# Class-wide Variables #
		self.gameState = False
		self.loop, self.runButton, self.stopButton, self.gameSpeed = None, None, None, 1000
		self.enableCustom = IntVar()
		self.cell = [[0 for y in range(20)] for x in range(20)]
		self.adjacency = [[0 for y in range(20)] for x in range(20)]

		self.create_UI()

	def create_UI(self):
		conwayLF = LabelFrame(self.master, text='Grid')
		conwayLF.place(x=25, y=10, width=350, height=350)

		for x in range(20):
			for y in range(20):
				self.cell[x][y] = Label(conwayLF, width=2, height=2, bg='white', relief=SUNKEN)
				self.cell[x][y].place(x=x*15+20, y=y*15+10, width=15, height=15)

		controlsLF = LabelFrame(self.master, text='Controls')
		controlsLF.place(x=25, y=375, width=350, height=125)

		changeStateCB = Checkbutton(controlsLF, text='Enable Customization', variable=self.enableCustom, command=self.toggleCustom)
		changeStateCB.place(x=5, y=5)
		self.enableCustom.set(1)
		self.toggleCustom()

		self.runButton = Button(controlsLF, text='Run', command=self.runGame)
		self.runButton.place(x=5, y=35, width=50)

		self.stopButton = Button(controlsLF, text='Stop', command=self.stopGame, state=DISABLED)
		self.stopButton.place(x=75, y=35, width=50)

		self.speedSlider = Scale(controlsLF, label='Game Speed Multiplier:', tickinterval=1.0, from_=1.0, to=10.0, orient=HORIZONTAL, command=self.updateSpeed)
		self.speedSlider.place(x=175, y=5, width=150)

		self.clearButton = Button(controlsLF, text='Reset', command=self.resetGame)
		self.clearButton.place(x=5, y=75, width=50)

	def changeStateEvent(self, event):
		if event.widget['bg'] == 'white':
			event.widget.config(bg = 'black')
		else:
			event.widget.config(bg = 'white')

	def changeState(self, x, y, state):
		if state == 0:
			self.cell[x][y].config(bg = 'white')
		else:
			self.cell[x][y].config(bg = 'black')

	def toggleCustom(self):
		if self.enableCustom.get() == 0:
			for x in range(20):
				for y in range(20):
					self.cell[x][y].unbind('<Button-1>')
					# self.cell[x][y].unbind('<B1-Motion>')
		else:
			for x in range(20):
				for y in range(20):
					self.cell[x][y].bind('<Button-1>', self.changeStateEvent)
					# self.cell[x][y].bind('<Motion>', self.changeStateEvent)

	def updateSpeed(self, speed):
		self.gameSpeed = int(float(1000.0 / float(speed)))

	def getState(self, x, y):
		if self.cell[x][y]['bg'] == 'black':
			return 1
		else:
			return 0

	def resetCount(self):
		for x in range(20):
			for y in range(20):
				self.adjacency[x][y] = 0

	def setNeighborCount(self):
		for x in range(18):
			for y in range(18):
				if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x    ][y + 1]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 1][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				
				if self.cell[x + 1][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y + 1]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;

		for x in range(18):

			y = 0

			for x2 in range(3):
				if self.cell[x + x2][19]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x    ][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 1][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1

			y = 19

			for x2 in range(3):
				if self.cell[x + x2][0]['bg'] == 'black': self.adjacency[x + 1][y] += 1

			if self.cell[x    ][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 1][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1

		for y in range(18):

			x = 0

			for y2 in range(3):
				if self.cell[19][y + y2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			if self.cell[x    ][y]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y + 1]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			x = 19

			for y2 in range(3):
				if self.cell[x][y + y2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			if self.cell[x - 1][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x - 1][y + 1]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x - 1][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

		if self.cell[19][19]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[0 ][1 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[1 ][0 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[1 ][1 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;

		if self.cell[19][0 ]['bg'] == 'black': self.adjacency[0 ][19] += 1;
		if self.cell[0 ][18]['bg'] == 'black': self.adjacency[0 ][19] += 1;
		if self.cell[1 ][18]['bg'] == 'black': self.adjacency[0 ][19] += 1;
		if self.cell[1 ][19]['bg'] == 'black': self.adjacency[0 ][19] += 1;

		if self.cell[0 ][19]['bg'] == 'black': self.adjacency[19][0 ] += 1;
		if self.cell[18][0 ]['bg'] == 'black': self.adjacency[19][0 ] += 1;
		if self.cell[18][1 ]['bg'] == 'black': self.adjacency[19][0 ] += 1;
		if self.cell[19][1 ]['bg'] == 'black': self.adjacency[19][0 ] += 1;

		if self.cell[0 ][0 ]['bg'] == 'black': self.adjacency[19][19] += 1;
		if self.cell[18][18]['bg'] == 'black': self.adjacency[19][19] += 1;
		if self.cell[18][19]['bg'] == 'black': self.adjacency[19][19] += 1;
		if self.cell[19][18]['bg'] == 'black': self.adjacency[19][19] += 1;


	def newGen(self):
		for x in range(20):
			for y in range(20):
				if self.adjacency[x][y] < 2 and self.getState(x, y) == 1:
					self.changeState(x, y, 0)
				elif self.adjacency[x][y] == 2 and self.getState(x, y) == 1:
					self.changeState(x, y, 1)
				elif self.adjacency[x][y] == 3 and self.getState(x, y) == 1:
					self.changeState(x, y, 1)
				elif self.adjacency[x][y] > 3 and self.getState(x, y) == 1:
					self.changeState(x, y, 0)
				elif self.adjacency[x][y] == 3 and self.getState(x, y) == 0:
					self.changeState(x, y, 1)
		self.resetCount()

	def resetGame(self):
		for x in range(20):
			for y in range(20):
				self.cell[x][y].config(bg = 'white')
		self.resetCount()

	def Game(self):
		self.setNeighborCount()
		self.newGen()
		self.loop = self.master.after(self.gameSpeed, self.Game)

	def runGame(self):
		self.gameState = True
		self.runButton.config(state=DISABLED)
		self.stopButton.config(state=ACTIVE)
		self.speedSlider.config(state=DISABLED)
		self.Game()
		
	def stopGame(self):
		self.gameState = False
		self.runButton.config(state=ACTIVE)
		self.stopButton.config(state=DISABLED)
		self.speedSlider.config(state=ACTIVE)
		self.master.after_cancel(self.loop)

def main():
	root = Tk()

	root.title('Conway\'s Game of Life')

	root.geometry('400x525')

	root.resizable(False, False)

	app = Conway()

	root.mainloop()

if __name__ == '__main__':
	main()
