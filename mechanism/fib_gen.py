class Fibonacci(object):

    def __iter__(self):
        return FibonacciGenerator()

class FibonacciGenerator(object):

    def __init__(self):
        self.a = 1
        self.b = 0

    def __next__(self):
        result = self.a
        self.a, self.b = self.b, self.a + self.b
        return result

    def __iter__(self):
        return self
def fibnacci():
    a, b = 0, 1
    while 1:
        yield b
        a,b = b, a+b


if __name__ == '__main__':
    fib = Fibonacci()
    for i in fib:
        if i > 10:break
        print(i)
    for i in fibnacci():
        if i > 20:
            break

        print(i)
