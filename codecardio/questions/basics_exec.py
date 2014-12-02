def f(x): return (x**4)
def g(x): return x-4
def h(x, y): return (f(g(x)) % g(f(y)))
print h(1, 4)