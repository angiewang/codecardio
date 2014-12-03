try:
	answer = subprocess.check_output("python basics_exec.py", shell=True)
except:
	print "try again"