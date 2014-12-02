from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random, math, sys, os, subprocess
from random import shuffle
from threading import *

class CodeCardio(EventBasedAnimationClass):
	def __init__(self, winWidth=1000, winHeight=1000):
		self.width = winWidth
		self.height = winHeight
		milliseconds = 1000
		self.timerDelay = 1
		self.tokens = []
		self.players = [Player(500, 600)]
		self.marginY, self.marginX = 50, 75
		self.moveStep = 5
		self.topBoardLength = winHeight/4
		self.tokenHit = False
		self.timerDelay = 1000
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

	def faceDetect(self, arg):
		#the code for face detection is from 
		#https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
		cascPath = sys.argv[1]
		faceCascade = cv2.CascadeClassifier(cascPath)
		video_capture = cv2.VideoCapture(0)

		#face detection code from website
		#https://realpython.com/blog/python/face-detection-in-python-using-a-webcam/
		while True:
		    #playCodeCardio()

		    # Capture frame-by-frame
		    ret, frame = video_capture.read()

		    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		    faces = faceCascade.detectMultiScale(
		        gray,
		        scaleFactor=1.1,
		        minNeighbors=5,
		        minSize=(30, 30),
		        flags=cv2.cv.CV_HAAR_SCALE_IMAGE
		    )

		    # Draw a rectangle around the faces
		    for (x, y, w, h) in faces:
		        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
		        print x, y

		    # Display the resulting frame
		    cv2.imshow('Video', frame)

		    if cv2.waitKey(1) & 0xFF == ord('q'):
		        break

		# When everything is done, release the capture
		video_capture.release()
		cv2.destroyAllWindows()


	def initAnimation(self):
	    #create a new thread 
	    thread = Thread(target=faceDetect, args=(haarcascade_frontalface_default.xml, ))
	    thread.start()
	    self.initTopics()

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

	def testCheckForCollision(): pass

	@staticmethod
	def readFile(filename, mode="rt"):
		with open(filename, mode) as fin:
			return fin.read()

	#generates the question when coding token is hit
	def generateQuestion(self):
		topic = self.topics[self.currentTopic] #ex: Programming basics
		fileLoc = "questions/" + self.filelocs[self.currentTopic]+".py"
		#ex: questions/basics.py
		print fileLoc
		question, answer = "", ""
		if (os.path.exists(fileLoc)):
			with open(fileLoc, mode="rt") as fin:
				question = fin.read()
				print question

				numRepl = question.count("%d")

				low,high = 1,5 
				repl = []
				for randomRepl in xrange(numRepl):
					repl.append(random.randint(low,high))
				
				repl = tuple(repl)
				self.question = question % repl
				#self.question = question
				#run the exec file and return answer 
				
				filename="questions/"+self.filelocs[self.currentTopic]+"_exec.py"
				#get answer
				if (os.path.exists(filename)):
					with open(filename, mode="wt") as fout:
					    fout.write(self.question)
					answer = subprocess.check_output("python "+filename, shell=True)
					
				else:
					print "create exec file for this topic"
				print "answer: " + str(answer)
				self.generateMCAnswers(answer)

				
	def generateMCAnswers(self, answer):
		#create list of answers and shuffle them
		self.correctAnswer = answer
		self.answers = [self.correctAnswer]
		print "self.answers: ", self.answers
		self.ansChoices = ["a", "b", "c", "d"]
		for a in xrange(len(self.ansChoices) - 1):
			if int(answer) == 0:
				uppBound = 20 
			else: uppBound = int(answer)
			newAns = random.randint(0, uppBound-1)
			while newAns in self.answers:
				newAns = random.randint(0, uppBound-1)
			print "ans", newAns
			self.answers.append(newAns)
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
		self.filelocs = ["basics", "loops"]
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
			y += self.marginY*3
			for a in xrange(len(self.answers)):
				y += self.marginY
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
		self.canvas.create_rectangle(0, self.topBoardLength, self.width, self.height, fill="gray10")
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
	winWidth, winHeight = 1000, 1000
	c = CodeCardio(winWidth, winHeight)
	c.run()
    #instantiate the first player
	player1 = Player(random.randint(0, winWidth), random.randint(0, winHeight))

#todo-create 
playCodeCardio()
