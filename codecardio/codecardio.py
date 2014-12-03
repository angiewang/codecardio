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
		self.mainGame = False
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
		self.mousePX, self.mousePY = 0,0
		self.timerCounter = 0
		self.movementThreshold = 10
		self.arg = "haarcascade_frontalface_default.xml"

	def onWindowClosed(self):
		self.video_capture.release()
		#cv2.destroyAllWindows()
		self.root.quit()

	def initAnimation(self):
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
		#cascPath = sys.argv[1]

		#moved to init
		# cascPath = arg
		# faceCascade = cv2.CascadeClassifier(cascPath)
		# video_capture = cv2.VideoCapture(0)

		#face detection code from website
		#https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
		#while True:
		    
	    # Capture frame-by-frame
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
		    #cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		    print x, y
		    scale = 100
		    step = self.moveStep * scale
		    if x < self.width/2:
		    	print "move right"
		    	self.players[0].x += step
		    elif x > self.height/2:
		    	print "move left"
		    	self.players[0].x -= step

		    # Display the resulting frame
		   # cv2.imshow('Video', frame)

		    # if cv2.waitKey(1) & 0xFF == ord('q'):
		    #     break

		# When everything is done, release the capture
		#video_capture.release()
		#cv2.destroyAllWindows()

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
		#todo - while question is incorrect, keep trying

	def testCheckForCollision(): pass

	def readFile(self, filename, mode="rt"):
		with open(filename, mode) as fin:
			return fin.read()

	def generateRepl(self,low,high,numRepl, question):
		repl = []
		for randomRepl in xrange(numRepl):
			repl.append(random.randint(low,high))
		repl = tuple(repl)
		self.question = question % repl
		#self.question = question
		#run the exec file and return answer 

	#generates the question when coding token is hit
	def generateQuestion(self):
		topic = self.topics[self.currentTopic] #ex: Programming basics
		fileLoc = "questions/" + self.filelocs[self.currentTopic]+".py"
		#ex: questions/basics.py
		print fileLoc
		question, answer = "", ""
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

	def generateMCAnswers(self, answer):
		#create list of answers and shuffle them
		self.correctAnswer = answer
		self.answers = [self.correctAnswer]
		print "self.answers: ", self.answers
		self.ansChoices = ["a", "b", "c", "d"]
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

	def gameIsOver(self): 
		if self.currentTopic == len(self.topics):
			self.create_text(self.width/2, self.height/2, 
				text-"CONGRATS, game is complete")

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
		if self.startScreen==False and self.codingTokenHit==False and self.exerciseTokenHit==False:
			self.checkForCollision() 
			#self.timerDelay = 1000
			if self.timerCounter >= 0:
				self.timerCounter -= 1
			else:
				self.timerCounter = 20
				self.generateCodingToken()
				self.generateExerciseToken()
			self.moveTokens()

			# print "begin thread"
			# self.thread.start()
			self.faceDetect("haarcascade_frontalface_default")

	def drawPlayers(self): 
		for player in self.players:
			self.canvas.create_oval(player.x-player.r, player.y-player.r, 
				player.x+player.r, player.y+player.r, fill=player.color)

	def drawTokens(self):
		for token in self.tokens:
			self.canvas.create_rectangle(token.x-token.r, token.y-token.r, 
				token.x+token.r, token.y+token.r, fill=token.color)

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
		self.canvas.create_rectangle(0,0,self.width, self.topBoardLength, fill="light cyan")

	def onMousePressedWrapper(self, event):
		self.onMousePressed(event)

	def onMousePressed(self, event):
		self.mousePX, self.mousePY = event.x, event.y

	def mouseMotion(self, event):
		canvas = event.widget
		if self.startScreen:
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
			self.initFaceDetect()
			self.root.protocol("WM_DELETE_WINDOW", lambda: self.onWindowClosed())
		#else:

		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline,width=width)
		self.canvas.create_text(x,y, text="Enter the magical world of 15-112",
			font="Didot 20 bold", fill="blue")
		y+=self.marginY+5

		#create second button
		width,outline = 1,"black"
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width=highlight,4
		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline,width=width)
		self.canvas.create_text(x,y, text="Instructions",
			font="Didot 20 bold", fill="blue")
		y+=self.marginY+5

		#create third button
		width,outline = 1,"black"
		if self.mouseX >= x-rx and self.mouseX <= x+rx and self.mouseY >= y-ry and self.mouseY <= y+ry:
			outline,width=highlight,4
		self.canvas.create_rectangle(x-rx, y-ry, x+rx, y+ry, fill="blanched almond",
			outline=outline, width=width)
		self.canvas.create_text(x,y, text="Settings",
			font="Didot 20 bold", fill="blue")

	def redrawAll(self):
		self.canvas.delete(ALL)
		if (self.startScreen==True):
			self.drawStartScreen()
		else:
			self.initTopBoard()
			#set scene background
			self.canvas.create_rectangle(0, self.topBoardLength, self.width, self.height, fill="gray10")
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
		else: self.redrawAll()

	def drawTitleGraphics(self):
		if not self.codingTokenHit and not self.exerciseTokenHit:
			displayText = "CODE CARDIO"
			self.directions = "Dodge the falling tokens"
			self.canvas.create_text(self.width/2, self.topBoardLength/2+self.marginY,
			text=self.directions, font="Didot 25")
		elif self.codingTokenHit == True:
			displayText = "YOU HIT A CODING TOKEN"
			title = "Current topic: " + self.topics[self.currentTopic]
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
	winWidth, winHeight = 1000, 700
	c = CodeCardio(winWidth, winHeight)
	c.run()
    #instantiate the first player
	player1 = Player(random.randint(0, winWidth), random.randint(0, winHeight))

#todo-create 
playCodeCardio()
