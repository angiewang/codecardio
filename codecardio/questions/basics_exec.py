def f(x): return (x**2)/(x%7)
def g(x): return x-1
def h(x, y): return (f(g(x)) % g(f(y)))
print h(9, 13)