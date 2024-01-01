from copy import deepcopy
from random import choice
from core.Settings import Settings

settings = Settings()


class Tetrominoe:

    def __init__(self, m):
        self.matrix = list(m) or []
        self._x = (settings.cols - len(self.matrix[0])) // 2
        self._y = 0

    def drop(self):
        self._y += 1

    def rotate(self):
        return self.copy(zip(*self.matrix[::-1]), self.x, self.y)

    def shadow_shape(self):
        temp = deepcopy(self)
        temp.matrix = [[8 if val else 0 for val in row] for row in temp.matrix]
        return temp

    def copy(self, mtx, x, y):
        obj = Tetrominoe(mtx)
        obj.x = x
        obj.y = y
        return obj

    @staticmethod
    def create_new_shape():
        return choice(TetrominoeTypes)()

    @property
    def y(self):
        return self._y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @y.setter
    def y(self, value):
        self._y = value

    @staticmethod
    def get_color(num: int):
        return colors[num]


class TShape(Tetrominoe):
    def __init__(self):
        __matrix = [[1, 1, 1], [0, 1, 0]]
        super(TShape, self).__init__(__matrix)


class SShape(Tetrominoe):
    def __init__(self):
        __matrix = [[0, 2, 2], [2, 2, 0]]
        super(SShape, self).__init__(__matrix)


class ZShape(Tetrominoe):
    def __init__(self):
        __matrix = [[3, 3, 0], [0, 3, 3]]
        super(ZShape, self).__init__(__matrix)


class JShape(Tetrominoe):
    def __init__(self):
        __matrix = [[4, 0, 0], [4, 4, 4]]
        super(JShape, self).__init__(__matrix)


class LShape(Tetrominoe):
    def __init__(self):
        __matrix = [[0, 0, 5], [5, 5, 5]]
        super(LShape, self).__init__(__matrix)


class IShape(Tetrominoe):
    def __init__(self):
        __matrix = [[6, 6, 6, 6]]
        super(IShape, self).__init__(__matrix)


class OShape(Tetrominoe):
    def __init__(self):
        __matrix = [[7, 7], [7, 7]]
        super(OShape, self).__init__(__matrix)


colors = {
    1: 'purple',
    2: 'green',
    3: 'red',
    4: 'blue',
    5: 'orange',
    6: 'cyan',
    7: 'yellow',
    8: 'gray'
}

TetrominoeTypes = [
    TShape,
    SShape,
    JShape,
    ZShape,
    LShape,
    IShape,
    OShape
]
'''
class TShape(Tetrominoe):
    def __init__(self):
        __matrix = [[1, 1, 1], [0, 1, 0]]
        super(TShape, self).__init__(__matrix, 'purple')


class SShape(Tetrominoe):
    def __init__(self):
        __matrix = [[0, 2, 2], [2, 2, 0]]
        super(SShape, self).__init__(__matrix, 'green')


class ZShape(Tetrominoe):
    def __init__(self):
        __matrix = [[3, 3, 0], [0, 3, 3]]
        super(ZShape, self).__init__(__matrix, 'red')


class JShape(Tetrominoe):
    def __init__(self):
        __matrix = [[4, 0, 0], [4, 4, 4]]
        super(JShape, self).__init__(__matrix, 'blue')


class LShape(Tetrominoe):
    def __init__(self):
        __matrix = [[0, 0, 5], [5, 5, 5]]
        super(LShape, self).__init__(__matrix, 'orange')


class IShape(Tetrominoe):
    def __init__(self):
        __matrix = [[6, 6, 6, 6]]
        super(IShape, self).__init__(__matrix, 'cyan')


class OShape(Tetrominoe):
    def __init__(self):
        __matrix = [[7, 7], [7, 7]]
        super(OShape, self).__init__(__matrix, 'yellow')
'''
"""
TetrominoeTypes = {
    TShape: 0,
    SShape: 1,
    ZShape: 2,
    JShape: 3,
    LShape: 4,
    IShape: 5,
    OShape: 6
}
"""
