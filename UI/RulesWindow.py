from PyQt5.QtWidgets import QDialog

from UI.ui_rules import Ui_Rules


class RulesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Rules()
        self.ui.setupUi(self)
