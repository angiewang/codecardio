def f(x,y):
    m = 0
    result = 0
    for z in xrange(2,x,y):
        if (x%z == m):
            result = 1, 
            m += 1
        elif (y + z > x):
            result = 2
        print (z if (z%3 == 2) else 3),
    print result
f(3, 4)