from tkinter import *

# Author: Declan Sheehan

# Conway's Game of Life Rules:
# 1. Any live cell with less than 2 living neighbors dies.
#	- if A <  2: DIE
# 2. Any livng cell with 2 or more living neighbors lives on.
# 	- if A >= 2: LIVE
# 3. Any living cell with more than 3 living neighbors dies.
# 	- if A >  3: DIE
# 4. Any dead cell with exactly 3 living neighbors lives.
# 	- if A == 3: LIVE

class Conway(Frame):
	def __init__(self):
		super().__init__()

		# Class-wide Variables #
		self.GS = 20

		self.loop, self.runButton, self.stopButton, self.gameSpeed = None, None, None, 1000
		self.enableCustom = IntVar()
		self.cell = [[0 for y in range(40)] for x in range(40)]
		self.adjacency = [[0 for y in range(40)] for x in range(40)]

		self.create_UI()

	def create_UI(self):
		bar = Menu(self.master)
		presetBar = Menu(bar, tearoff=0)
		sizeBar = Menu(bar, tearoff=0)

		presetBar.add_command(label='X-Box', command=self.presetOne)
		sizeBar.add_command(label='20x20', command=lambda: self.resizeMainFrame(400, 525, 20))
		sizeBar.add_command(label='30x30', command=lambda: self.resizeMainFrame(600, 775, 30))
		sizeBar.add_command(label='40x40', command=lambda: self.resizeMainFrame(750, 1000, 40))

		bar.add_cascade(label='Presets', menu=presetBar)
		bar.add_cascade(label='Size', menu=sizeBar)

		self.master.config(menu=bar)

		self.conwayLF = LabelFrame(self.master, text='Grid')
		self.conwayLF.place(relx=0.0625, rely=0.01904, relwidth=0.875, relheight=0.6667)

		if self.GS == 20:
			for x in range(self.GS):
				for y in range(self.GS):
					self.cell[x][y] = Label(self.conwayLF, width=2, height=2, bg='white', relief=SUNKEN)
					self.cell[x][y].place(x=x*15+22, y=y*15+10, width=15, height=15)

		controlsLF = LabelFrame(self.master, text='Controls')
		controlsLF.place(relx=0.0625, rely=0.71428, relwidth=0.875, relheight=0.238)

		changeStateCB = Checkbutton(controlsLF, text='Enable Customization', variable=self.enableCustom, command=self.toggleCustom)
		changeStateCB.place(relx=0.01428, rely=0.04)
		self.enableCustom.set(1)
		self.toggleCustom()

		self.runButton = Button(controlsLF, text='Run', command=self.runGame)
		self.runButton.place(relx=0.01428, rely=0.28, relwidth=0.1428)

		self.stopButton = Button(controlsLF, text='Stop', command=self.stopGame, state=DISABLED)
		self.stopButton.place(relx=0.2142, rely=0.28, relwidth=0.1428)

		self.speedSlider = Scale(controlsLF, label='Game Speed Multiplier:', tickinterval=1.0, from_=1.0, to=10.0, orient=HORIZONTAL, command=self.updateSpeed)
		self.speedSlider.place(relx=0.5, rely=0.04, relwidth=0.4285)

		self.clearButton = Button(controlsLF, text='Reset', command=self.resetGame)
		self.clearButton.place(relx=0.01428, rely=0.6, relwidth=0.1428)

	def resizeMainFrame(self, x, y, sq):
		size_string = str(x) + 'x' + str(y)
		self.master.geometry(size_string)
		for x in range(self.GS):
			for y in range(self.GS):
				self.cell[x][y].place_forget()
		self.GS = sq
		self.redrawGrid()

	def redrawGrid(self):
		Xscale, Yscale = 0, 0
		if self.GS == 20:
			Xscale = 22
		elif self.GS == 30:
			Xscale = 33
		elif self.GS == 40:
			Xscale = 25
		Yscale = 0.45 * self.GS
		for x in range(self.GS):
			for y in range(self.GS):
				self.cell[x][y] = Label(self.conwayLF, width=2, height=2, bg='white', relief=SUNKEN)
				self.cell[x][y].place(x=x*15+Xscale, y=y*15+Yscale, width=15, height=15)
		self.toggleCustom()

	def presetOne(self):
		for x in range(self.GS):
			for y in range(self.GS):
				if x == y:
					self.cell[x][y].config(bg = 'black')
				elif x + y == self.GS-1:
					self.cell[x][y].config(bg = 'black')
				elif x == 0 and y >= 0:
					self.cell[x][y].config(bg = 'black')
				elif x == self.GS-1 and y >= 0:
					self.cell[x][y].config(bg = 'black')
				elif y == 0 and y >= 0:
					self.cell[x][y].config(bg = 'black')
				elif y == self.GS-1 and y >= 0:
					self.cell[x][y].config(bg = 'black')
				else:
					self.cell[x][y].config(bg = 'white')

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
			for x in range(self.GS):
				for y in range(self.GS):
					self.cell[x][y].unbind('<Button-1>')
					# self.cell[x][y].unbind('<Motion>')
		else:
			for x in range(self.GS):
				for y in range(self.GS):
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
		for x in range(self.GS):
			for y in range(self.GS):
				self.adjacency[x][y] = 0

	def setNeighborCount(self):
		for x in range(self.GS - 2):
			for y in range(self.GS - 2):
				if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x    ][y + 1]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 1][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				
				if self.cell[x + 1][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y + 1]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;
				if self.cell[x + 2][y + 2]['bg'] == 'black': self.adjacency[x + 1][y + 1] += 1;

		for x in range(self.GS - 2):
			y = 0
			for x2 in range(3):
				if self.cell[x + x2][self.GS - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x    ][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 1][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y + 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1

			y = self.GS - 1

			for x2 in range(3):
				if self.cell[x + x2][0]['bg'] == 'black': self.adjacency[x + 1][y] += 1

			if self.cell[x    ][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 1][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y - 1]['bg'] == 'black': self.adjacency[x + 1][y] += 1
			if self.cell[x + 2][y    ]['bg'] == 'black': self.adjacency[x + 1][y] += 1

		for y in range(self.GS - 2):
			x = 0
			for y2 in range(3):
				if self.cell[self.GS - 1][y + y2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			if self.cell[x    ][y]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y + 1]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x + 1][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			x = self.GS - 1

			for y2 in range(3):
				if self.cell[x][y + y2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

			if self.cell[x - 1][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x - 1][y + 1]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x - 1][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y    ]['bg'] == 'black': self.adjacency[x][y + 1] += 1
			if self.cell[x    ][y + 2]['bg'] == 'black': self.adjacency[x][y + 1] += 1

		if self.cell[self.GS-1][self.GS-1]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[0 ][1 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[1 ][0 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;
		if self.cell[1 ][1 ]['bg'] == 'black': self.adjacency[0 ][0 ] += 1;

		if self.cell[self.GS-1][0 ]['bg'] == 'black': self.adjacency[0 ][self.GS-1] += 1;
		if self.cell[0 ][self.GS-2]['bg'] == 'black': self.adjacency[0 ][self.GS-1] += 1;
		if self.cell[1 ][self.GS-2]['bg'] == 'black': self.adjacency[0 ][self.GS-1] += 1;
		if self.cell[1 ][self.GS-1]['bg'] == 'black': self.adjacency[0 ][self.GS-1] += 1;

		if self.cell[0 ][self.GS-1]['bg'] == 'black': self.adjacency[self.GS-1][0 ] += 1;
		if self.cell[self.GS-2][0 ]['bg'] == 'black': self.adjacency[self.GS-1][0 ] += 1;
		if self.cell[self.GS-2][1 ]['bg'] == 'black': self.adjacency[self.GS-1][0 ] += 1;
		if self.cell[self.GS-1][1 ]['bg'] == 'black': self.adjacency[self.GS-1][0 ] += 1;

		if self.cell[0 ][0 ]['bg'] == 'black': self.adjacency[self.GS-1][self.GS-1] += 1;
		if self.cell[self.GS-2][self.GS-2]['bg'] == 'black': self.adjacency[self.GS-1][self.GS-1] += 1;
		if self.cell[self.GS-2][self.GS-1]['bg'] == 'black': self.adjacency[self.GS-1][self.GS-1] += 1;
		if self.cell[self.GS-1][self.GS-2]['bg'] == 'black': self.adjacency[self.GS-1][self.GS-1] += 1;


	def newGen(self):
		for x in range(self.GS):
			for y in range(self.GS):
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
		for x in range(self.GS):
			for y in range(self.GS):
				self.cell[x][y].config(bg = 'white')
		self.resetCount()

	def Game(self):
		self.setNeighborCount()
		self.newGen()
		self.loop = self.master.after(self.gameSpeed, self.Game)

	def runGame(self):
		self.runButton.config(state=DISABLED)
		self.stopButton.config(state=ACTIVE)
		self.speedSlider.config(state=DISABLED)
		self.Game()
		
	def stopGame(self):
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
