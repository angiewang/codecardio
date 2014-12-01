def f1(n):
    f = lambda x: x%2
    def g(n):
        if (n > 0):
            return (f(n), lambda: g(n/2))
        else:
            return None
    curr = g(n)
    while (curr != None):    
        print curr[0],
        curr = curr[1]()
f1(5)