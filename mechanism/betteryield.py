def f():
    x = 0
    while True:
        x += 1
        print(x)
        yield x
    return x

a=f()
print(a)
print(next(a))
