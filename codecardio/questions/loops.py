def f(x,y):
    m = 0
    for z in xrange(2,x,y):
        if (x%z == m):
            print "A",
            m += 1
        elif (y + z > x):
            print "B",
        print (z if (z%3 == 2) else "C"),
    print
f(12, 4)