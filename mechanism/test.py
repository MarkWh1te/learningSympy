def gen123():
    yield 1
    yield 2
    yield 3
    yield 4

for x in gen123():
    print(x)


a = gen123()
print(next(a))
print(next(a))
print(next(a))
print(next(a))
print(next(a))
