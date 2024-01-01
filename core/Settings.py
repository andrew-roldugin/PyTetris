from typing import final

TILE: final = 35  # размер ячейки
COLS: final = 10  # количество столбцов
ROWS: final = 20  # количество строк
FPS: final = 30  # установленный FPS
TITLE: final = "Tetris"


class Settings:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, *, tile_size=TILE, rows=ROWS, cols=COLS, fps=FPS):
        self._fps = fps
        self._cols = cols
        self._rows = rows
        self._tile_size = tile_size
        self._field_resolution = self._cols * self._tile_size, self._rows * self._tile_size

    @property
    def tile(self):
        return self._tile_size

    @tile.setter
    def tile(self, new_value):
        self._tile_size = new_value

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, new_value):
        self._fps = new_value

    @property
    def rows(self):
        return self._rows

    @rows.setter
    def rows(self, new_value):
        self._rows = new_value

    @property
    def cols(self):
        return self._cols

    @cols.setter
    def cols(self, new_value):
        self._cols = new_value

    @property
    def field_resolution(self):
        return self._cols * self._tile_size, self._rows * self._tile_size

    @field_resolution.setter
    def field_resolution(self, value):
        self._field_resolution = value

