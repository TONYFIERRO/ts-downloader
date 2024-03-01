import os
import sys
import qdarktheme
import requests

from PyQt5.QtWidgets import (
    QApplication
)

from mainwindow import MainWindow

# TODO: create log-file where the program will write names of the files that will be downloaded
# TODO: change net_export names to netexport
# TODO: after starting remove the files, for instance: .ts_files, chrome-net-export, ...
# TODO: deploy project for MacOS and Windows

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        qdarktheme.setup_theme()
        window = MainWindow()
        window.show()
        app.exec()

    except requests.exceptions.ConnectionError:
        tmp_files = [
            'chrome-net-export-log.json',
            'chunklist.m3u8',
            '.tmp_ts'
        ]

        for file in tmp_files:
            if os.path.exists(file):
                os.remove(file)
