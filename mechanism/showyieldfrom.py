def chain1(*iterables):
    for it in iterables:
        for i in it:
            yield i

def chain2(*iterables):
    for i in iterables:
        yield from i

a = ['a','b','c']
b = range(3)

print(list(chain1(a,b)))
print(list(chain2(a,b)))
print(chain1(a,b)==chain2(a,b))
