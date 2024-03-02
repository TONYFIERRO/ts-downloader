import os
import shutil

from PyQt5.QtCore import (
    Qt,
    QThread
)
from PyQt5.QtWidgets import (
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QProgressBar,
    QSpacerItem,
    QSizePolicy
)
from PyQt5.QtWidgets import (
    QWidget
)

from bin.chromeconnector import ChromeConnector


class DownloadWidget(QWidget):
    def __init__(self, url, mp3_flag, mp4_flag):
        super().__init__()
        self.setFixedSize(400, 400)
        self.setWindowTitle('Download menu')

        self.url = url
        self.mp3_flag = mp3_flag
        self.mp4_flag = mp4_flag

        self.thread = QThread()

        self.start_recovery()
        self.chrome_connector = ChromeConnector(self.url)
        self.v_layout = QVBoxLayout()
        self.label_icon = QLabel("TS-Downloader")
        self.progress_bar = QProgressBar()
        self.button_start_downloading = QPushButton('Start downloading')

        self.setLayout(self.v_layout)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.addWidget(self.label_icon)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.addWidget(self.progress_bar)
        self.v_layout.addWidget(self.button_start_downloading)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.label_icon.setStyleSheet('font: bold 39pt;')
        self.label_icon.setAlignment(Qt.AlignCenter)

        self.define_connections()

    def define_connections(self):
        self.button_start_downloading.clicked.connect(self.handle_button_start_downloading)

    def handle_button_start_downloading(self):
        self.button_start_downloading.setEnabled(False)

        self.chrome_connector.moveToThread(self.thread)

        self.thread.started.connect(self.chrome_connector.run)
        self.chrome_connector.finished.connect(self.thread.quit)
        # self.chrome_connector.finished.connect(self.chrome_connector.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.chrome_connector.report_progress.connect(self.report_progress)
        self.chrome_connector.finished.connect(self.remove_files)
        self.chrome_connector.crashed.connect(self.open_crash_message)

        self.thread.start()

    @staticmethod
    def start_recovery():
        """
        This is a method that recovers the program after a crash. For example, due to Internet problems.

        """

        tmp_files = [
            'chrome-net-export-log.json',
            'chunklist.m3u8',
        ]

        tmp_dirs = [
            '.tmp_ts'
        ]

        for file in tmp_files:
            if os.path.exists(file):
                os.remove(file)

        for directory in tmp_dirs:
            if os.path.exists(directory):
                shutil.rmtree(directory)

    def report_progress(self, value):
        self.progress_bar.setValue(value)

    def remove_files(self):
        tmp_files = [
            'chrome-net-export-log.json',
            'chunklist.m3u8',
        ]

        curr_time = self.chrome_connector.get_current_time()

        if self.mp3_flag is False:
            tmp_files.append(f'Audio {curr_time}.mp3')
        if self.mp4_flag is False:
            tmp_files.append(f'Video {curr_time}.mp4')

        for file in tmp_files:
            if os.path.exists(file):
                os.remove(file)

        self.report_progress(100)
        self.open_success_message()

    @staticmethod
    def open_success_message():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Downloading is done!")
        msg.exec_()

    @staticmethod
    def open_crash_message():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Error!")
        msg.exec_()

    def show_widget(self):
        self.show()

    def closeEvent(self, event) -> None:
        self.chrome_connector.deleteLater()
