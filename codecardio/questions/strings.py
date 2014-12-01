def f(s):
    for x in xrange(1,4):
        spec = "%%0.%df" % x
        print spec % float(s), 
f("12.45645")