import sys

import qdarktheme
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox
)

from mainwindow import MainWindow

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        window = MainWindow()
        window.show()
        app.exec()

    except requests.exceptions.ConnectionError:
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error! The program crashes due to Internet problems.")
        msg.exec_()
