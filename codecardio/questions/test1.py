fileLoc = "test.py"
with open(fileLoc, mode="rt") as fin:
	question = fin.read()
	print question
	question = (question) % (2)