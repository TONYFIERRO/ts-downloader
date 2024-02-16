from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QWidget, QLabel, QProgressBar


class ProgressWidget(QThread):
    def __init__(self):
        super().__init__()

        self.widget = QWidget()
        self.label_state = QLabel('State:')
        self.progress_bar = QProgressBar()

    def run(self):
        pass
