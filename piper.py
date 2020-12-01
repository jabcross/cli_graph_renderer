from functools import partial

class Pipe:
    def __ror__(self, other):
        self.data = other
        return self

    def __rxor__(self, other):
        self.data = other
        return self

    def __or__(self, other):
        return other(self.data)

    def __xor__(self, other):
        return other(self.data)

def Map(x):
    return partial(map, x)

def Filter(x):
    return partial(filter, x)

p : Pipe = Pipe()

def tee(f):
    return lambda x: (f(x),x)[1]

def pipe(*args):
    x = args[0]
    for i in range(1,len(args)):
        x = args[i](x)
    return x
