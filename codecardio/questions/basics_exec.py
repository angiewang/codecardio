def f(x): return (x**5)
def g(x): return x-2
def h(x, y): return (f(g(x)) % g(f(y)))
print h(2, 3)