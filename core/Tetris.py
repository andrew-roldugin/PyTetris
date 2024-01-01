from copy import deepcopy
from enum import Enum
from functools import wraps

from core.Settings import Settings
from core.TetrisBoard import TetrisBoard
from core.Tetrominoe import Tetrominoe

scores = {-1: 1, 0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def decorator(func):
    def _impl(self, *args, **kwargs):
        if not (self.shape and self.next_shape):
            temp = []
            for _ in range(2):
                temp.append(func(self, *args, **kwargs))
            self.shape, self.next_shape = temp
        else:
            self.shape, self.next_shape = self.next_shape, func(self, *args, **kwargs)
        return self.shape, self.next_shape

    return _impl


def get_record():
    try:
        with open('../record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('../record', 'w') as f:
            f.write('0')
            return 0


def set_record(record, score):
    rec = max(int(record), score)
    with open('../record', 'w') as f:
        f.write(str(rec))
    return rec


class Tetris:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.state = GameState.BEFORE_START
        self.anim_count = 0
        self.anim_speed = 60
        self.anim_limit = 2000
        self.signals = {}
        self.shape = self.next_shape = None

    def start_new_game(self):
        self.__init_new_game()
        self.state = GameState.PLAYING
        self.shape, self.next_shape = self.create_new_shape()

    def __init_new_game(self):
        self.record = get_record()
        self.cols = self.settings.cols
        self.rows = self.settings.rows
        self.prev_val = self._level = 0
        self.score = 0
        self.deleted_rows = 0
        self.__board = TetrisBoard(rows=self.rows, cols=self.cols)

    def add_score(self, lines=-1):
        self.score += scores[lines]

    def drop(self):
        if self.playing():
            self.anim_count += self.anim_speed
            if self.anim_count > self.anim_limit:
                self.anim_count = 0
                self.shape.drop()
                self.add_score()
                if self.check_collision(self.shape):
                    self.__board += self.shape
                    self.shape, self.next_shape = self.create_new_shape()
                    return True
        return False

    def clear_rows(self):
        # идем по полю снизу
        cleared_rows = 0
        for i, row in enumerate(self.__board.matrix[:-1]):
            # если вся строка заполнена(нет 0)
            if 0 not in row:
                self.__board.remove_row(i)
                cleared_rows += 1

        self.add_score(cleared_rows)
        self.deleted_rows += cleared_rows
        self.level = self._deleted_rows // 10

        if self.prev_val != self.level:
            self.prev_val = self.level
            self.anim_speed *= 1.2

    @decorator
    def create_new_shape(self):
        __new_shape = Tetrominoe.create_new_shape()
        if self.check_collision(__new_shape):
            self.game_over()
            return
        else:
            self.signals['repaintSignal'].emit()
            return __new_shape

    def toggle_pause(self):
        if self.state == GameState.BEFORE_START:
            return
        self.state = GameState.PAUSED if self.state == GameState.PLAYING else GameState.PLAYING

    def try_move(self, dx):
        if self.playing():
            new_x = self.shape.x + dx
            if 0 <= new_x <= self.cols - len(self.shape.matrix[0]):
                temp = deepcopy(self.shape)
                temp.x = new_x
                if not self.check_collision(temp):
                    self.shape = temp
                    return True
        return False

    def try_rotate(self):
        if self.playing():
            temp_shape = self.shape.rotate()
            if self.__board.check_borders(temp_shape) and not self.check_collision(temp_shape):
                self.shape = temp_shape
                return True
        return False

    def game_over(self):
        self.state = GameState.GAME_OVER
        self.shape = self.next_shape = None
        self.record = set_record(self._record, self._score)
        self.signals['timerEventSignal'].emit()

    def instant_drop(self):
        if self.state == GameState.PLAYING:
            while not self.drop():
                pass

    def is_game_over(self):
        return self.state == GameState.GAME_OVER

    def paused(self):
        return self.state == GameState.PAUSED

    def playing(self):
        return self.state == GameState.PLAYING

    @property
    def matrix(self):
        return self.__board.matrix

    def add_signals(self, *args, **kwargs):
        self.signals = kwargs

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, v):
        self._level = v
        self.signals['levelSignal'].emit(self._level)

    @property
    def deleted_rows(self):
        return self._deleted_rows

    @deleted_rows.setter
    def deleted_rows(self, v):
        self._deleted_rows = v
        self.signals['removedLinesSignal'].emit(self._deleted_rows)

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, v):
        self._score = v
        self.signals['scoreSignal'].emit(self._score)

    @property
    def record(self):
        return self._record

    @record.setter
    def record(self, v):
        self._record = v
        self.signals['recordSignal'].emit(self._record)

    @classmethod
    def get_record(cls):
        return int(get_record())

    def check_collision(self, shape):
        return self.__board.check_collision(shape)


class GameState(Enum):
    BEFORE_START = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3
