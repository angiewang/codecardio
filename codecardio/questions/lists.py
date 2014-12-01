import copy

a = [[1],[2],[3]]
(b,c,d) = (a, copy.copy(a), copy.deepcopy(a))
print (a == b), (a == c), (a == d)
print (a is b), (a is c), (a is d)
print (a[0] is b[0]), (a[0] is c[0]), (a[0] is d[0])