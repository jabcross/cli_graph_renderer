from typing import NewType, Union

class Vec:
    @staticmethod
    def dim_range(start, stop, stride=None, fixed_vals=()):
        if len(fixed_vals) == len(start):
            yield Vec(fixed_vals)
        else:
            if stride == None:
                stride = tuple([1] * len(start))
            dim = len(fixed_vals)
            for i in range(start[dim],stop[dim],stride[dim]):
                for i in Vec.dim_range(start, stop, stride=stride, fixed_vals=(fixed_vals + (i,))):
                    yield i

    def __init__ (self, *args):
        if len(args) == 1:
            if isinstance(args[0],tuple):
                self.values = list(args[0])
            if isinstance(args[0],list):
                self.values = list(args[0])
            if isinstance(args[0],Vec):
                self.values = list(args[0].values)
        elif len(args) > 1:
            self.values = list(args)
        else:
            assert(False)

    def __iter__(self):
        return iter(self.values)

    # Unary ops

    def __neg__ (self):
        return Vec([-i for i in self])

    # Binary ops

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __add__ (self, other):
        other : Vec = Vec(other)
        rv = Vec(0,0)
        rv.values = [a + b for (a,b) in zip(self, other)]
        return rv

    def __radd__ (self, other):
        return self + other

    def __sub__(self, other):
        return self + (-Vec(other))

    def __rsub__(self, other):
        return -(self - other)

    def __floordiv__(self, other):
        if isinstance(other, int):
            return Vec([i // other for i in self])

    def __pow__(self, other):
        other = Vec(other)
        return Vec([a * b for (a,b) in zip(self, other)])

    def __rpow__(self, other):
        return self ** other

    def __hash__(self):
        return tuple(self.values).__hash__()

    def __repr__(self):
        return tuple(self.values).__repr__()

    def __tuple__(self):
        return tuple(self.values)

    def __list__(self):
        return list(self.values)

    def __getitem__(self, key):
        return self.values[key]

    def __setitem__(self, key, value):
        self.values[key] = value

    def __len__(self):
        return len(self.values)

    def clamp(self, m, M):
        return Vec([clamp(x, _m, _M) for (x, _m, _M) in zip(self, m, M)])

    @property
    def x(self):
        return self.values[0]

    @x.setter
    def x(self, x):
        self.values[0] = x

    @property
    def y(self):
        return self.values[1]

    @y.setter
    def y(self, y):
        self.values[1] = y

    @property
    def z(self):
        return self.values[2]

    @z.setter
    def z(self, z):
        self.values[2] = z

    @property
    def r(self):
        return self.values[0]

    @r.setter
    def r(self, r):
        self.values[0] = r

    @property
    def g(self):
        return self.values[1]

    @g.setter
    def g(self, g):
        self.values[1] = g

    @property
    def b(self):
        return self.values[2]

    @b.setter
    def b(self, b):
        self.values[2] = b

def clamp(x, m, M):
    return max(min(x, M), m)

if __name__ == "__main__":
    for i in Vec.dim_range((0,0), (5,5), stride=(1,1)):
        print(i)
