from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random

class CodeCardio(EventBasedAnimationClass):
	def __init__(self, winWidth=1000, winHeight=1000):
		self.width = winWidth
		self.height = winHeight
		milliseconds = 1000
		self.timerDelay = milliseconds
		self.tokens = [Token(300, 600)]#, Token(400, 400), Token (500, 700)]
		self.players = [Player(200, 700)]
		self.question=""
		self.marginY = 100

	#when collision occurs, generate random question 
	def checkForCollision(self):
		for player in self.players:
			for token in self.tokens:
				#first check x constraint
				if (player.x + player.r >= token.x - token.r):
					if (player.y + player.r <= token.y + token.r
					or player.y + player.r >= token.y - token.r):
						print "collision"
						self.question = "question"
				elif player.x - player.r <= token.x + token.r:
					if (player.y + player.r <= token.y + token.r
					or player.y + player.r >= token.y - token.r):
						print "collision"
						self.question = "question"
		#todo - while question is incorrect, keep generating random questions

	def generateQuestion(self, txt):
		self.question = txt

	def onTimerFired(self):
		self.checkForCollision() 

	def drawPlayers(self):
		for player in self.players:
			self.canvas.create_oval(player.x-player.r, player.y-player.r, 
				player.x+player.r, player.y+player.r, fill=player.color)

	def drawTokens(self):
		for token in self.tokens:
			self.canvas.create_rectangle(token.x-token.r, token.y-token.r, 
				token.x+token.r, token.y+token.r, fill=token.color)

	def drawQuestion(self):
		self.canvas.create_text(self.width/2, self.marginY, text=self.question, 
			font="Helvetica 20 bold")

	def redrawAll(self):
		self.canvas.delete(ALL)
		self.generateQuestion(self.question)
		self.drawQuestion()
		#instantiate players
		self.drawPlayers()
		#instantiate tokens
		self.drawTokens()

	def onKeyPressed(self,event):
		if event.keysym == "Up": self.players[0].move(0, -5)
		elif event.keysym == "Down": self.players[0].move(0, 5)
		elif event.keysym == "Left": self.players[0].move(-5, 0)
		elif event.keysym == "Right": self.players[0].move(5, 0)
		else: self.redrawAll()

class Character(object):
	def __init__(self, x, y, r=50):
		self.x = x
		self.y = y
		self.r = r

	def move(self, dX, dY):
		self.x += dX
		self.y += dY

class Player(Character):
	def __init__(self, x, y, r=25):
		super(Player,self).__init__(x, y, r)
		self.color = "sky blue"

class Token(Character):
	def __init__(self, x, y, r=25):
		super(Token, self).__init__(x, y, r)
		self.color = "gold"

class ExerciseToken(Character):
	def __init__(self, x, y, r=25):
		super(ExerciseToken, self).__init__(x, y, r):
		self.color = "green"

def playCodeCardio():
	winWidth, winHeight = 1000, 1000
	c = CodeCardio(winWidth, winHeight)
	c.run()
    #instantiate the first player
	player1 = Player(random.randint(0, winWidth), random.randint(0, winHeight))

playCodeCardio()