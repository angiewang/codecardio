from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random, math

class CodeCardio(EventBasedAnimationClass):
	def __init__(self, winWidth=1000, winHeight=1000):
		self.width = winWidth
		self.height = winHeight
		milliseconds = 1000
		self.timerDelay = 1
		self.tokens = []
		self.players = [Player(500, 600)]
		self.question=""
		self.marginY, self.marginX = 50, 75
		self.moveStep = 5
		self.topBoardLength = winHeight/4
		self.tokenHit = False
		self.timerDelay = 1000

	#when collision occurs, generate random question 
	def checkForCollision(self):
		player = self.players[0]
		for token in self.tokens:
			tx, ty, px, py = token.x, token.y, player.x, player.y
			tr, pr = token.r, player.r
			#there is a collision if the distance between the coordinates
			#are less than the smaller of the two tokens' lengths
			comparison = min(tr, pr)*2
			if abs(px - tx) <= comparison and abs(py - ty) <= comparison:
				print "collision detected"
				self.question = "You hit a coding token! Answer this: what is the complexity of bubble sort?"
		#todo - while question is incorrect, keep generating random questions

	def generateQuestion(self, txt=""):
		self.question = txt

	def onTimerFired(self):
		self.checkForCollision() 
		self.moveTokens()

	def drawPlayers(self):
		for player in self.players:
			self.canvas.create_oval(player.x-player.r, player.y-player.r, 
				player.x+player.r, player.y+player.r, fill=player.color)

	def drawTokens(self):
		for token in self.tokens:
			self.canvas.create_rectangle(token.x-token.r, token.y-token.r, 
				token.x+token.r, token.y+token.r, fill=token.color)

	def moveTokens(self):
		#randomly generate tokens
		t = Token(0, self.topBoardLength)
		x = random.randint(t.r, self.width)
		t.move(x, t.r)
		self.tokens.append(t)
		#then move them
		for token in self.tokens: 
			if token.y <= self.height - token.r:
				token.y += self.moveStep * 10

	def initTopBoard(self):
		self.canvas.create_rectangle(0,0,self.width, self.topBoardLength, fill="peach puff")

	def initAnimation(self):
		#set background and scene
		self.initTopBoard()

	def drawQuestion(self):
		y = self.marginY * 2
		self.canvas.create_text(self.width/2, self.topBoardLength/2 + self.marginY, text=self.question, 
			font="Helvetica 20 bold", fill="black")

	def redrawAll(self):
		self.canvas.delete(ALL)
		#background
		self.canvas.create_rectangle(0, self.topBoardLength, self.width, self.height, fill="black")
		self.generateQuestion(self.question)
		self.drawQuestion()
		self.drawPlayers()
		self.drawTitleGraphics()
		self.drawTokens()

	def onKeyPressed(self,event):
		if event.keysym == "Up": self.players[0].move(0, -5)
		elif event.keysym == "Down": self.players[0].move(0, 5)
		elif event.keysym == "Left": self.players[0].move(-5, 0)
		elif event.keysym == "Right": self.players[0].move(5, 0)
		else: self.redrawAll()

	def drawTitleGraphics(self):
		x, y = self.width/2, self.marginY
		self.canvas.create_text(self.marginX, self.marginY + self.topBoardLength,
		 text="Score: 0", font="Helvetica 30 bold", fill="white")
		if self.tokenHit==True:
			print "token is hit. display something on screen"
		else:
			self.canvas.create_text(self.width/2, self.topBoardLength/2,
				text="CODE CARDIO", font="Helvetica 40 bold")

class Character(object):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.r = 30

	def move(self, dX, dY):
		self.x += dX
		self.y += dY

class Player(Character):
	def __init__(self, x, y):
		super(Player,self).__init__(x, y)
		self.color = "sky blue"

class Token(Character):
	def __init__(self, x, y):
		super(Token, self).__init__(x, y)
		self.color = "yellow"

class ExerciseToken(Token):
	def __init__(self, x, y):
		super(ExerciseToken, self).__init__(x, y)
		self.color = "green"

def playCodeCardio():
	winWidth, winHeight = 1000, 1000
	c = CodeCardio(winWidth, winHeight)
	c.run()
    #instantiate the first player
	player1 = Player(random.randint(0, winWidth), random.randint(0, winHeight))

playCodeCardio()