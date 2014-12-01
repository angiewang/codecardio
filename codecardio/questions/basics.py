def f(x): return (x**%d)/(x%%%d)
def g(x): return x-%d
def h(x, y): return (f(g(x)) %% g(f(y)))
print h(%d, %d)