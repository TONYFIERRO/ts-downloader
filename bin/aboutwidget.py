from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGroupBox


class About(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 250)

        self.v_layout = QVBoxLayout()
        self.label_description = QLabel('This is a program that downloads .ts-files from a server\n and then'
                                        ' merges them into one .mp3/.mp4-file.')
        self.label_author = QLabel('Author: Shamil Zaripov')
        self.label_email = QLabel('Email: mail@tonyfierro.com')
        self.label_telegram = QLabel('Telegram: @tonyfierro')
        self.label_version = QLabel('Version: 1.0')
        self.groupbox_description = QGroupBox('Description')
        self.groupbox_description_layout = QVBoxLayout()
        self.groupbox_info = QGroupBox('Contacts')
        self.groupbox_info_layout = QVBoxLayout()

        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.groupbox_description)
        self.groupbox_description_layout.addWidget(self.label_description)
        self.groupbox_description.setLayout(self.groupbox_description_layout)
        self.v_layout.addWidget(self.groupbox_info)
        self.groupbox_info.setLayout(self.groupbox_info_layout)
        self.groupbox_info_layout.addWidget(self.label_author)
        self.groupbox_info_layout.addWidget(self.label_email)
        self.groupbox_info_layout.addWidget(self.label_telegram)
        self.groupbox_info_layout.addWidget(self.label_version)

        self.label_description.setAlignment(Qt.AlignCenter)
        self.label_author.setAlignment(Qt.AlignCenter)
        self.label_email.setAlignment(Qt.AlignCenter)
        self.label_telegram.setAlignment(Qt.AlignCenter)
        self.label_version.setAlignment(Qt.AlignCenter)

    def show_widget(self):
        self.show()
