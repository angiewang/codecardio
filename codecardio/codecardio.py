from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random, math, sys, os, subprocess
from random import shuffle
from threading import *
import cv2
#from pygame import mixer

class CodeCardio(EventBasedAnimationClass):
	def __init__(self, winWidth=1000, winHeight=1000):
		self.width = winWidth
		self.height = winHeight
		self.timerDelay = 1
		self.tokens = []
		self.prevX, self.prevY = 500, 400
		self.players = [Player(500, 400)]
		self.marginY, self.marginX = 50, 75
		self.moveStep = 0.1
		self.topBoardLength = winHeight/4
		self.tokenHit = False
		self.codingTokenHit = False
		self.exerciseTokenHit = False
		self.exercise = "" #represents the current workout when exercise token hit
		self.question= "" #represents current question when coding token hit
		self.currentTopic = 0
		self.topics = []
		self.fileLocs = dict()
		self.questionInstructions = ""
		self.responseToQuestion = ""
		self.answers=[]
		self.correctAnswer = None
		self.ansChoices=dict()
		self.tryAgain = False
		self.directions = ""
		#create a new thread 
		self.thread = Thread(target = self.faceDetect, args=("haarcascade_frontalface_default.xml",))
		self.movementThreshold = 10
		self.arg = "haarcascade_frontalface_default.xml"
		self.pauseGame = False
		
		self.mousePX, self.mousePY =0,0
		self.timerCounter = 0
		self.numCorrect = 0
		self.numIncorrect = 0
		self.mainGameBackground = "main_background.gif"
		self.otherBackground = "other_background.gif"

	def initGameState(self):
		self.faceDetectFeature = False
		self.mainGame = False
		self.instructionScreen = False
		self.settingsScreen = False

	def onWindowClosed(self):
		self.video_capture.release()
		self.root.quit()

	def initAnimation(self):
		self.initGameState()
		self.initStartScreen()
		self.root.bind("<Motion>", lambda event: self.mouseMotion(event))
		self.initTopics()

	def initStartScreen(self):
		#start screen init
		self.startScreen = True
		self.startScreenImage = None
		self.mouseX, self.mouseY = 0,0

	def initFaceDetect(self):
		self.cascPath = self.arg
		self.faceCascade = cv2.CascadeClassifier(self.cascPath)
		self.video_capture = cv2.VideoCapture(0)

	def faceDetect(self,arg):
		#the code for face detection is from 
		#https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
		ret, frame = self.video_capture.read()

		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		faces = self.faceCascade.detectMultiScale(
		    gray,
		    scaleFactor=1.1,
		    minNeighbors=5,
		    minSize=(30, 30),
		    flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		)

		# Draw a rectangle around the faces
		for (x, y, w, h) in faces:
			print faces
			#cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
			print x, y
			scale = 100
			step = self.moveStep * scale
			if x < self.width/2:
				print "move right",
				self.players[0].x += step
			elif x > self.height/2:
				print "move left",
				self.players[0].x -= step

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

	def testCheckForCollision(): pass

	def readFile(self, filename, mode="rt"):
		with open(filename, mode) as fin:
			return fin.read()

	def writeFile(self, filename, contents, mode="wt"):
		with open(filename, mode) as fout:
			fout.write(contents)

	def generateRepl(self,low,high,numRepl, question):
		repl = []
		for randomRepl in xrange(numRepl):
			repl.append(random.randint(low,high))
		repl = tuple(repl)
		self.question = question % repl
		print self.question
		#self.question = question

	#generates the question when coding token is hit
	def generateQuestion(self):
		#get file location of topic
		topic = self.topics[self.currentTopic] #ex: Programming basics
		fileLoc = "questions/" + self.filelocs[self.currentTopic]+".py"
		#ex: questions/basics.py
		print fileLoc
		question = self.readFile(fileLoc)
		print question

		numRepl = question.count("%d")

		if numRepl > 0:
			low,high = 1,5
			self.generateRepl(low, high, numRepl, question)

		#run the exec file and return answer 
		execFile = "questions/" + self.filelocs[self.currentTopic] + "_exec.py"
		self.writeFile(execFile, self.question)

		#get answers
		try:
			answer = subprocess.check_output("python "+execFile, shell=True)
		except:
			print "regenerating repl and answers"
			self.generateRepl(low,high,numRepl, question)
			execFile = "questions/" + self.filelocs[self.currentTopic] + "_exec.py"
			self.writeFile(execFile, self.question)

		ansGen = False
		while ansGen == False:
			try:
				answer = subprocess.check_output("python "+execFile, shell=True)
				ansGen = True
			except:
				ansGen = False
				print "regenerating question because not a valid file"
				#regenerate random numbers
				self.generateRepl(low, high, numRepl, question)
				#re-execute
				self.writeFile(execFile, self.question)

		print "answer", answer
		answer = answer.replace("\n","")
		try:
			answer = int(answer)
		except:
			print "answer is not integer"
		self.generateMCAnswers(answer)

		# if (os.path.exists(fileLoc)):
		# 	with open(fileLoc, mode="rt") as fin:
		# 		question = fin.read()
		# 		print question

		# 		numRepl = question.count("%d")
		# 		if numRepl > 0:
		# 			self.generateRepl(1,5,numRepl,question)
		# 		try:	
		# 			filename="questions/"+self.filelocs[self.currentTopic]+"_exec.py"
		# 		except:
		# 			self.generateRepl(1,5, numRepl,question)
		# 		#get answer
		# 		if (os.path.exists(filename)):
		# 			with open(filename, mode="wt") as fout:
		# 			    fout.write(self.question)
		# 			answer = subprocess.check_output("python "+filename, shell=True)
					
		# 		else:
		# 			print "create exec file for this topic"
		# 		print "answer: " + str(answer)
		# 		self.generateMCAnswers(answer)
		
		# if (os.path.exists(fileLoc)):
		# 	self.readFile()

	def genRandomQuestion(self): pass

	def generateMCAnswers(self, answer):
		#create list of answers and shuffle them
		self.correctAnswer = answer
		self.answers = [self.correctAnswer]
		print "self.answers: ", self.answers
		self.ansChoices = ["a", "b", "c", "d"]
		r = 4
		low, high = answer - r, answer + r
		for a in xrange(len(self.ansChoices)-1):
			newAns = random.randint(low,high)
			while newAns in self.answers:
				newAns = random.randint(low,high)
			self.answers.append(newAns)
		# for a in xrange(len(self.ansChoices) - 1):
		# 	if int(answer) == 0:
		# 		uppBound = 20 
		# 	else: uppBound = int(answer)
		# 	newAns = random.randint(0, uppBound-1)
		# 	while newAns in self.answers:
		# 		newAns = random.randint(0, uppBound-1)
		# 	print "ans", newAns
		# 	self.answers.append(newAns)
		shuffle(self.answers)
		print self.answers
		#randomly generate numeric values to substitute into template

	def initTopics(self):
		self.topics = ["Programming basics", "Conditionals and Loops",
		"Strings", "Lists", #"Efficiency", 
		"Sorting algorithms", "Sets",
		"Maps and dictionaries", "Graphics", "Object oriented programming",
		"Recursion", "Functions redux", "File IO"]
	
		#this represents [filename.py, num of templates]
		self.filelocs = ["basics", "loops", "strings", "lists", #"efficiency",
		"sorting", "sets", "maps","graphics", "oop","recursion",
		"functionsredux","fileio"]
		#todo - count number of replacements in template

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
			x = self.width/2
			y = self.height/2
			if not self.tryAgain:
				self.questionInstructions = "Enter the letter that corresponds to the correct answer."
				self.questionInstructions+= "\nCode tracing: indicate what this program will print"
			self.canvas.create_text(x, self.topBoardLength*3/4, 
				text=self.questionInstructions, 
			font="Helvetica 20 bold")
			self.canvas.create_rectangle(0+margin, self.topBoardLength+margin, 
				self.width-margin, self.height-margin, fill="white")

			self.canvas.create_text(self.width/2, y,
				text=self.question, font="Helvetica 20 bold")
			y += self.marginY*2
			for a in xrange(len(self.answers)):
				y += self.marginY/2
				self.canvas.create_text(x, y, 
					text=self.ansChoices[a] + "): " + str(self.answers[a]),
				font="Helvetica 20 bold")

		elif self.exerciseTokenHit:
			self.canvas.create_rectangle(0+margin, self.topBoardLength+margin, 
				self.width-margin, self.height-margin, fill="white")
			self.canvas.create_text(self.width/2, self.height/2, text=self.exercise,
				font="Palatino 40 bold")
			self.canvas.create_text(self.width/2, self.height/2 + self.marginY, 
				text="Press enter when finished", font="Helvetica 20 bold")

	def answerQuestion(self, event): 
		if event.char in {"a", "b", "c", "d"}:
			self.responseToQuestion = event.char
			#question is answered correctly
			index = self.ansChoices.index(self.responseToQuestion)
			if self.answers[index]==self.correctAnswer:
				#reset
				self.codingTokenHit = False
				self.tokens = []
				self.directions = "Correct!"
				self.tryAgain = False
				self.currentTopic += 1
			#question is incorrect, try again
			else:
				self.tryAgain = True
				self.questionInstructions = "INCORRECT - try again"

	def exerciseResponse(self,event):
		if event.keysym =="Return":
			#reset game
			self.exerciseTokenHit = False
			self.tokens = []
		
	def onTimerFired(self):
		if self.mainGame==True and self.codingTokenHit==False and self.exerciseTokenHit==False:
			self.checkForCollision() 
			#self.timerDelay = 1000
			if self.timerCounter >= 0:
				self.timerCounter -= 1
			else:
				self.timerCounter = 20
				if not self.pauseGame:
					self.generateCodingToken()
					self.generateExerciseToken()
			if not self.pauseGame:
				self.moveTokens()
			if self.faceDetectFeature:
				self.faceDetect("haarcascade_frontalface_default")

	def drawPlayers(self): 
		for player in self.players:
			self.canvas.create_oval(player.x-player.r, player.y-player.r, 
				player.x+player.r, player.y+player.r, fill="white")
			filepathP = "megacat.gif"
			px,py = player.x, player.y
			self.startScreenImage = PhotoImage(file=filepathP)
			self.canvas.create_image(px,py, image=self.startScreenImage)

	def drawTokens(self):
		filepathCT = "dkosbie.gif"
		self.startScreenImageCT = PhotoImage(file=filepathCT)
		filepathET = "exercise_octocat.gif"
		self.startScreenImageET = PhotoImage(file=filepathET)

		for token in self.tokens:
			self.canvas.create_rectangle(token.x-token.r, token.y-token.r, 
				token.x+token.r, token.y+token.r)
			tx, ty = token.x, token.y
			if type(token)==Token:
				self.canvas.create_image(tx,ty, image=self.startScreenImageCT)
			elif type(token)==ExerciseToken:
				self.canvas.create_image(tx, ty, image=self.startScreenImageET)

	def generateExerciseToken(self):
		#randomly generate an exercise token
		#then generate exercise token
		#TODO-need to check that they don't overlap
		et = ExerciseToken(0, self.topBoardLength)
		ex = random.randint(et.r, self.width)
		et.move(ex, et.r)
		self.tokens.append(et)

	def generateCodingToken(self):
		#randomly generate a coding token
		#first generate coding token
		t = Token(0, self.topBoardLength)
		x = random.randint(t.r, self.width) 
		t.move(x, t.r)
		self.tokens.append(t)

	def moveTokens(self):
		for token in self.tokens: 
			if token.y <= self.height - token.r:
				scale = 50
				step = self.moveStep * scale
				token.y += step
			else: self.tokens.remove(token) #reaches bottom of screen: remove

	def initTopBoard(self):
		self.canvas.create_rectangle(0,0,self.width, self.topBoardLength, fill="black")

	def onMousePressedWrapper(self, event):
		self.onMousePressed(event)

	def onMousePressed(self, event):
		self.mousePX, self.mousePY = event.x, event.y

	def mouseMotion(self, event):
		canvas = event.widget
		#if self.startScreen or self.instructionScreen or self.settingsScreen or self.gameIsComplete:
		self.mouseX = event.x
		self.mouseY = event.y
		self.redrawAll()

	def drawStartScreen(self):
		self.canvas.delete(ALL)
		#draw
		filepath = "startscreen.gif"
		x,y = self.width/2, self.height/2
		self.startScreenImage = PhotoImage(file=filepath)
		self.canvas.create_image(x,y, image=self.startScreenImage)
		y=self.height/3

		#create welcome text
		self.canvas.create_text(x,y, text="Welcome to",
			font="Apple\ Chancery 80", fill="papaya whip")
		y+=self.marginY*2
		self.canvas.create_text(x,y, 
			text="CODE CARDIO", font="Didot 60 bold", fill="papaya whip")
		y+=self.marginY*2
		rx = self.marginX*3
		ry = self.marginY/2

		#set default rectangular button width
		width,outline = 1,"black"
		highlight = "cyan"

		#create first button
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width=highlight,4
		elif self.mousePX >= x-rx and self.mousePX <= x+rx and self.mousePY >= y-ry and self.mousePY <= y+ry:
			print "start screen"
			self.startScreen = False
			self.mainGame = True
			self.initFaceDetect()
			self.root.protocol("WM_DELETE_WINDOW", lambda: self.onWindowClosed())

		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline,width=width)
		self.canvas.create_text(x,y, text="Enter the magical world of 15-112",
			font="Didot 20 bold", fill="blue")
		y+=self.marginY+5

		#create second button
		width,outline = 1,"black"
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width=highlight,4
		elif self.mousePX >= x-rx and self.mousePX <= x+rx and self.mousePY >= y-ry and self.mousePY <= y+ry:
			print "instructions"
			self.startScreen = False
			self.instructionScreen = True
		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline,width=width)
		self.canvas.create_text(x,y, text="Instructions",
			font="Didot 20 bold", fill="blue")
		y+=self.marginY+5

		#create third button
		width,outline = 1,"black"
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width=highlight,4
		elif self.mousePX >= x-rx and self.mousePX <= x+rx and self.mousePY >= y-ry and self.mousePY <= y+ry:
			print "settings"
			self.startScreen = False
			self.settingsScreen = True
		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline, width=width)
		self.canvas.create_text(x,y, text="Settings",
			font="Didot 20 bold", fill="blue")

	def drawInstructionsScreen(self):
		filepath = self.otherBackground
		x,y = self.width/2, self.height/2
		self.startScreenImage = PhotoImage(file=filepath)
		self.canvas.create_image(x,y, image=self.startScreenImage)

	def drawPauseButton(self):
		x,y = self.topBoardLength, self.topBoardLength/2
		self.canvas.create_rectangle(0,0,x,y, 
			fill="navy",outline="white")
		self.canvas.create_text(x/2,y/2,text="Pause game", font="Didot 20 bold",fill="white")

	def drawSettingsScreen(self): pass

	def drawCompletedGame(self):
		filepath = self.otherBackground
		x,y = self.width/2, self.height/2
		self.startScreenImage = PhotoImage(file=filepath)
		self.canvas.create_image(x,y, image=self.startScreenImage)
		y = self.topBoardLength
		self.canvas.create_text(x,y, font="Apple\ Chancery 50 bold",
			text="Congratulations!", fill="peach puff")
		y += self.marginY*2
		self.canvas.create_text(x, y, font="Didot 40 bold",
			text="You have completed the Code Cardio game.",
			fill="light cyan")
		y += self.marginY*2
		rx = 150
		ry = 30
		outline = "black"
		width = 1
		highlight = "blanched almond"
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width = highlight, 10
		elif self.mousePX >= x-rx and self.mousePX <= x+rx and self.mousePY >= y-ry and self.mousePY <= y+ry:
			self.mainGame = True
			self.gameIsComplete = False
			self.initAnimation()
			self.reset()
		
		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline,width=width)
		self.canvas.create_text(x, y, text="RETURN TO HOME", font="Didot 30")

	def reset(self):
		self.tokens = []
		resetX, resetY = 500, 400
		for p in self.players:
			p.x, p.y = resetX, resetY
		self.mousePX, self.mousePY =0,0
		self.timerCounter = 0
		self.numCorrect = 0
		self.numIncorrect = 0
		self.currentTopic = 0

	def redrawAll(self):
		self.canvas.delete(ALL)
		if self.startScreen==True:
			self.drawStartScreen()
		elif self.mainGame == True:
			self.drawMainGame()
			#if not self.exerciseTokenHit and not self.codingTokenHit:
				#draw relevant buttons
				#self.drawPauseButton()
		elif self.instructionScreen:
			self.drawInstructionsScreen()
		elif self.settingsScreen:
			self.drawSettingsScreen()
		elif self.gameIsComplete:
			self.drawCompletedGame()

	def drawMainGame(self):
		self.initTopBoard()
		#set scene background
		#self.canvas.create_rectangle(0, self.topBoardLength, self.width, self.height, fill="gray10")
		filepathBG = self.mainGameBackground
		x,y = self.width/2, self.height/2 + self.topBoardLength/2
		self.startScreenImageBG = PhotoImage(file=filepathBG)
		self.canvas.create_image(x,y, image=self.startScreenImageBG)
		if not self.codingTokenHit and not self.exerciseTokenHit:
			self.drawPlayers()
			self.drawTokens()
		else:
			self.drawCurrentExercise()
		self.drawTitleGraphics()
		
	def onKeyPressed(self,event):
		scale = 100
		move = self.moveStep * scale
		if event.keysym == "Left": self.players[0].move(-1 * move, 0)
		elif event.keysym == "Right": self.players[0].move(move, 0)
		if self.codingTokenHit:
			self.responseToQuestion = ""
			self.answerQuestion(event)
		elif self.exerciseTokenHit:
			self.exerciseResponse(event)
		if self.mainGame:
			if event.char == "g":
				self.gameIsComplete = True
				self.mainGame = False
			if self.mainGame and event.char == "p":
				self.pauseGame=True
			if self.mainGame and event.char == "f":
				if self.faceDetectFeature:
					self.faceDetectFeature = False
				else: self.faceDetectFeature = True
		else: self.redrawAll()

	def drawTitleGraphics(self):
		if not self.codingTokenHit and not self.exerciseTokenHit:
			displayText = "CODE CARDIO"
			self.directions = "Dodge the falling tokens"
			self.canvas.create_text(self.width/2, self.topBoardLength/2+self.marginY,
			text=self.directions, font="Didot 25", fill="white")
		elif self.codingTokenHit == True:
			displayText = "YOU HIT A CODING TOKEN"
			title = "Current topic: " + self.topics[self.currentTopic]
			self.canvas.create_text(self.width/2, self.marginY+self.topBoardLength,
		 text=title, font="Palatino 30 bold", fill="white")
		elif self.exerciseTokenHit == True:
			displayText = "YOU HIT AN EXERCISE TOKEN"
		self.canvas.create_text(self.width/2, self.topBoardLength/2,
				text=displayText, font="Andale\ Mono 60 bold",fill="white")

	# def drawProgressBar(self):
	# 	if self.mainGame:

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
	winWidth, winHeight = 1000, 700
	c = CodeCardio(winWidth, winHeight)
	c.run()
    #instantiate the first player
	player1 = Player(random.randint(0, winWidth), random.randint(0, winHeight))

#todo-create 
playCodeCardio()
