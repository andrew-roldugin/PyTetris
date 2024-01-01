import sys

from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QBasicTimer, pyqtSignal
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QMainWindow, QDesktopWidget, QFrame, QWidget
from typing import Tuple

from UI.RulesWindow import RulesDialog
from UI.SettingsWindow import SettingDialog
from core.Settings import Settings
from core.Tetris import Tetris
from core.Tetrominoe import Tetrominoe
from UI.ui_main import Ui_MainWindow

ui = Ui_MainWindow()
settings = Settings()
tetris = Tetris(settings)


class MainWindow(QMainWindow):
    resize_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        ui.setupUi(self)
        self.center()

        self.setWindowTitle("Tetris")

        self.board = Board(self)
        ui.boardContainer.layout().addWidget(self.board)

        self.next_shape_frame = NextShapeFrame(self)
        ui.next_shape_container.addWidget(self.next_shape_frame)

        self._setup_signals()

        ui.game_over_2.setVisible(False)

        self.settings_window = SettingDialog(settings=settings, signal=self.resize_signal)
        self.settings_window.ui.checkBox.setChecked(True)
        self.settings_window.ui.checkBox.stateChanged.connect(self.state_changed)

        self.rules_window = RulesDialog()
        self._setup_menu()

    def _setup_menu(self):
        ui.start_new_game.triggered.connect(self.board.start)
        ui.settings.triggered.connect(self.settings_window.show)
        ui.rules.triggered.connect(self.rules_window.show)
        ui.exit.triggered.connect(quit)

    def _setup_signals(self):
        self.board.repaintSignal.connect(self.next_shape_frame.repaint)
        self.board.scoreSignal.connect(ui.scoresLCD.display)
        self.board.removed_lines_signal.connect(ui.deleted_rows_LCD.display)
        self.board.level_signal.connect(ui.level_LCD.display)
        self.board.record_signal.connect(ui.recordLCD.display)
        self.board.timer_event_signal.connect(self.stop)
        tetris.add_signals(repaintSignal=self.board.repaintSignal, scoreSignal=self.board.scoreSignal,
                           removedLinesSignal=self.board.removed_lines_signal, levelSignal=self.board.level_signal,
                           recordSignal=self.board.record_signal, timerEventSignal=self.board.timer_event_signal
                           )

        self.board.record_signal.emit(Tetris.get_record())

        self.resize_signal.connect(lambda: self.board.resizeEvent(None))

    def center(self):
        """
        центрирование окна
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def stop(self):
        self.board.timer.stop()
        self.board.repaint()
        self.next_shape_frame.repaint()
        ui.boardContainer.setVisible(False)
        ui.game_over_2.setVisible(True)

    def state_changed(self, state):
        self.board.show_shadow_shape = state


class NextShapeFrame(QFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.setMinimumSize(200, 100)

    def paintEvent(self, evt: QtGui.QPaintEvent) -> None:
        shape = tetris.next_shape
        if not shape:
            return
        self.setMinimumSize(len(shape.matrix[0]) * settings.tile, len(shape.matrix) * settings.tile)
        self.move(
            (self.parent().width() - self.minimumWidth()) // 2,
            self.geometry().y()
        )
        Painter.draw_shape(self, shape, (0, 0))


class Board(QFrame):
    repaintSignal: pyqtSignal = pyqtSignal()
    scoreSignal = pyqtSignal(int)
    removed_lines_signal = pyqtSignal(int)
    level_signal = pyqtSignal(int)
    record_signal = pyqtSignal(int)
    timer_event_signal = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.settings = settings
        self.tetris = tetris
        self.timer = QBasicTimer()
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.show_shadow_shape = True

    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.setMinimumSize(self.settings.field_resolution[0] + 10, self.settings.field_resolution[1] + 10)

    def start(self):
        if self.tetris.paused():
            return
        self.parent().setVisible(True)
        ui.game_over_2.setVisible(False)
        self.tetris.start_new_game()
        self.repaintSignal.emit()
        self.timer.start(self.settings.fps, self)

    def paintEvent(self, event):
        Painter.draw_grid(self)
        if not self.tetris.playing():
            return
        shape = tetris.shape
        if shape:
            Painter.draw_shape(self, shape, (shape.x, shape.y))
            if self.show_shadow_shape:
                shadow_shape = shape.shadow_shape()
                while not self.tetris.check_collision(shadow_shape):
                    shadow_shape.drop()
                if shape.y < shadow_shape.y - len(shape.matrix):
                    Painter.draw_shape(self, shadow_shape, (shadow_shape.x, shadow_shape.y - 1))

            Painter.draw_field(self, self.tetris.matrix)

    def keyPressEvent(self, evt: QtGui.QKeyEvent) -> None:
        key = evt.key()
        if key == QtCore.Qt.Key_Left:
            self.tetris.try_move(-1)
        elif key == QtCore.Qt.Key_Right:
            self.tetris.try_move(1)
        elif key == QtCore.Qt.Key_Up:
            self.tetris.try_rotate()
        elif key == QtCore.Qt.Key_Down:
            self.tetris.anim_count = self.tetris.anim_limit + 1
            self.tetris.drop()
        elif key == QtCore.Qt.Key_Escape:
            quit()
        elif key == QtCore.Qt.Key_P:
            self.tetris.toggle_pause()
        elif key == QtCore.Qt.Key_Space:
            self.tetris.instant_drop()
        elif key == QtCore.Qt.Key_S:
            self.start()
        else:
            super(Board, self).keyPressEvent(evt)

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.tetris.drop()
            self.tetris.clear_rows()
            self.repaint()
        else:
            super(Board, self).timerEvent(event)


def quit():
    sys.exit()


class Painter:
    @staticmethod
    def draw_grid(surface: QWidget) -> None:
        """
        Отрисовка сетки
        :param surface: поверхность, на которой будет выполняться рисование
        :return: None
        """
        painter = QPainter(surface)
        rect = surface.contentsRect()
        [
            painter.drawRect(rect.left() + x * settings.tile, rect.top() + y * settings.tile,
                             settings.tile, settings.tile,
                             )
            for x in range(settings.cols) for y in range(settings.rows)
        ]

    @staticmethod
    def draw_field(surface: QWidget, matrix) -> None:
        """
        Функция, отрисовывающая все поле
        :param surface: поверхность, на которой будет выполняться рисование
        :param matrix: матрица игрового поля
        :return: None
        """
        painter = QPainter(surface)
        rect = surface.contentsRect()
        for y, row in enumerate(matrix):
            for x, val in enumerate(row):
                if val > 0:
                    Painter._draw_square(painter,
                                         rect.left() + x * settings.tile,
                                         rect.top() + y * settings.tile,
                                         settings.tile, settings.tile,
                                         QColor(Tetrominoe.get_color(val))
                                         )

    @staticmethod
    def draw_shape(surface: QWidget, shape: Tetrominoe, offsets: Tuple[int, int]) -> None:
        """
        Рисование фигуры
        :param surface: поверхность, на которой будет выполняться рисование
        :param shape: фигура для отрисовки
        :param offsets: смещение (x; y)
        :return: None
        """
        painter = QPainter(surface)
        rect = surface.contentsRect()
        for y, row in enumerate(shape.matrix):
            for x, val in enumerate(row):
                if val > 0:
                    Painter._draw_square(painter,
                                         rect.left() + (x + offsets[0]) * settings.tile,
                                         rect.top() + (y + offsets[1]) * settings.tile,
                                         settings.tile, settings.tile,
                                         QColor(Tetrominoe.get_color(val))
                                         )

    @staticmethod
    def _draw_square(painter, x, y, width, height, color):
        painter.fillRect(x, y, width, height, color)

        painter.setPen(color.lighter())
        painter.drawLine(x, y + settings.tile - 1, x, y)
        painter.drawLine(x, y, x + settings.tile - 1, y)

        painter.setPen(color.darker())
        painter.drawLine(x + 1, y + settings.tile - 1,
                         x + settings.tile - 1, y + settings.tile - 1)
        painter.drawLine(x + settings.tile - 1,
                         y + settings.tile - 1, x + settings.tile - 1, y + 1)
