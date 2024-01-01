from core.Tetrominoe import Tetrominoe


class TetrisBoard:

    def __init__(self, *, rows, cols):
        self.cols = cols
        self.rows = rows
        self.__board = self.create_new_board()

    def create_new_board(self):
        self.__board = [
            [0 for _ in range(self.cols)]
            for _ in range(self.rows)
        ]
        self.__board.extend([[-1 for _ in range(self.cols)]])
        return self.__board

    def __add__(self, other: Tetrominoe):
        if isinstance(other, Tetrominoe):
            for cy, row in enumerate(other.matrix):
                for cx, val in enumerate(row):
                    if val:
                        self.__board[cy + other.y - 1][cx + other.x] = val
            return self
        else:
            return

    def remove_row(self, row):
        del self.__board[row]
        self.__board.insert(0, [0 for _ in range(self.cols)])

    def check_collision(self, shape):
        for y, row in enumerate(shape.matrix):
            for x, val in enumerate(row):
                # try:
                if 0 <= x <= self.rows and 0 <= y < self.cols:
                    if val and self.__board[y + shape.y][x + shape.x]:
                        return True
            #         return True
            # except IndexError:s
            #     return True
        return False

    def check_borders(self, shape):
        if shape.x < 0 or shape.x + len(shape.matrix[0]) > self.cols:
            return False
        elif shape.y + len(shape.matrix) > self.rows:
            return False
        return True

    @property
    def matrix(self):
        return self.__board
