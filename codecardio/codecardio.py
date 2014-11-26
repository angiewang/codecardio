from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random, math, sys, os

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
		self.codingTokenHit = False
		self.exerciseTokenHit = False
		self.exercise = "" #represents the current workout when token is hit
		self.currentTopic = ""

	def initAnimation(self): pass

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
				#print "collision detected"
				if type(token)==Token:
					self.codingTokenHit = True
					self.generateQuestion()
				else:
					self.exerciseTokenHit = True
					self.generateExercise()
		#todo - while question is incorrect, keep generating random questions

	#generates the question when coding token is hit
	def generateQuestion(self): pass
		#get current topic
		#then display the contents of the file. 
		#value of the topics dictionary: file location of question

	def getCurrentTopic(self): pass
	#store a dictionary of topics and a list of the files of all their 
	#return the file location of the 

	#generates the workout when exercise token is hit
	def generateExercise(self):
		numberOfExercises = [5, 10, 20]
		num = numberOfExercises[random.randint(0, len(numberOfExercises)-1)]
		exercises = ["PUSHUPS", "SITUPS", "JUMPING JACKS", "SQUATS", "LUNGES"]
		exercise = exercises[random.randint(0, len(exercises)-1)]
		self.exercise = "DO %d %s" % (num, exercise)

	def drawCurrentExercise(self):
		margin = self.marginX
		if self.codingTokenHit:	
			y = self.marginY * 2
			self.canvas.create_text(self.width/2, self.topBoardLength/2 + self.marginY, 
				text="Answer the following question", 
			font="Helvetica 20 bold", fill="black")
			self.canvas.create_rectangle(0+margin, self.topBoardLength+margin, 
				self.width-margin, self.height-margin, fill="white")
		elif self.exerciseTokenHit:
			self.canvas.create_rectangle(0+margin, self.topBoardLength+margin, 
				self.width-margin, self.height-margin, fill="white")
			self.canvas.create_text(self.width/2, self.height/2, text=self.exercise,
				font="Helvetica 40 bold")

	def answerQuestion(self, event):
		print "answer question"
		
	def onTimerFired(self):
		if self.codingTokenHit==False and self.exerciseTokenHit==False:
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
		#first generate coding token
		t = Token(0, self.topBoardLength)
		x = random.randint(t.r, self.width) 
		t.move(x, t.r)
		self.tokens.append(t)

		#then generate exercise token
		#TODO-need to check that they don't overlap
		et = ExerciseToken(0, self.topBoardLength)
		ex = random.randint(et.r, self.width)
		et.move(ex, et.r)
		self.tokens.append(et)

		#then move them
		for token in self.tokens: 
			if token.y <= self.height - token.r:
				scale = 10
				step = self.moveStep * scale
				token.y += step
			else: self.tokens.remove(token) #reaches bottom of screen: remove

	def initTopBoard(self):
		self.canvas.create_rectangle(0,0,self.width, self.topBoardLength, fill="light cyan")

	def redrawAll(self):
		self.canvas.delete(ALL)
		self.initTopBoard()
		#set scene background
		self.canvas.create_rectangle(0, self.topBoardLength, self.width, self.height, fill="black")
		if not self.codingTokenHit and not self.exerciseTokenHit:
			self.drawPlayers()
			self.drawTokens()
		else:
			self.drawCurrentExercise()
		self.drawTitleGraphics()
		
	def onKeyPressed(self,event):
		move = self.moveStep
		if event.keysym == "Left": self.players[0].move(-1 * move, 0)
		elif event.keysym == "Right": self.players[0].move(move, 0)
		if self.codingTokenHit:
			self.answerQuestion(event)
		else: self.redrawAll()

	def drawTitleGraphics(self):
		if not self.codingTokenHit and not self.exerciseTokenHit:
			displayText = "CODE CARDIO"
			directions = "Dodge the falling tokens"
			self.canvas.create_text(self.width/2, self.topBoardLength/2+self.marginY,
			text=directions, font="Didot 25")
		elif self.codingTokenHit == True:
			displayText = "YOU HIT A CODING TOKEN"
			title = "Current topic: " + self.currentTopic
			self.canvas.create_text(self.width/2, self.marginY+self.topBoardLength,
		 text=title, font="Palatino 30 bold", fill="white")
		elif self.exerciseTokenHit == True:
			displayText = "YOU HIT AN EXERCISE TOKEN"
		self.canvas.create_text(self.width/2, self.topBoardLength/2,
				text=displayText, font="Andale\ Mono 60 bold")

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
		self.color = "cyan"

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