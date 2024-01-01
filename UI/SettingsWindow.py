from PyQt5.QtWidgets import QDialog, QDesktopWidget, QDialogButtonBox

from UI.ui_settings import Ui_Dialog


class SettingDialog(QDialog):
    def __init__(self, *, parent=None, settings, signal):
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.center()
        self.settings = settings
        self.ui.buttonBox.accepted.connect(self.applied)
        self.ui.col_edit_frame.setVisible(False)
        self.ui.row_edit_frame.setVisible(False)
        # self.ui.cols_lineEdit.setText(str(settings.cols))
        # self.ui.rows_lineEdit.setText(str(settings.rows))
        self.ui.tile_size_lcd_slider.setValue(self.settings.tile)
        self.signal = signal

    def center(self):
        """
        центрирование окна
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def applied(self):
        # new_rows = int(self.ui.rows_lineEdit.text())
        # new_cols = int(self.ui.cols_lineEdit.text())
        # f1 = self.settings.cols != new_cols
        # f2 = self.settings.rows != new_rows
        # warn = f1 or f2
        # print(warn)
        # self.settings.cols = new_cols
        # self.settings.rows = new_rows
        tile_size = self.ui.tile_size_lcd_slider.value()
        if self.settings.tile != tile_size:
            self.settings.tile = tile_size
            self.signal.emit()
