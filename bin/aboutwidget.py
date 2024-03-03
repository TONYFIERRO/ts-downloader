from PyQt5.QtCore import (
    Qt
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QPushButton
)


class AboutWidget(QWidget):
    """
    This class creates the window and provides information about the program.

    """

    def __init__(self) -> None:
        """
        The window initialization and its elements.

        """

        super().__init__()
        self.setFixedSize(400, 420)
        self.setWindowTitle('About the program')

        self.v_layout = QVBoxLayout()
        self.label_name = QLabel('TS-Downloader')
        self.label_version = QLabel('Version 1.2.1')
        self.label_description = QLabel('This is a program that downloads .ts-files from \na server and then'
                                        ' merges them into one \n.mp3/.mp4-file.')
        self.label_author = QLabel('Author: Shamil Zaripov')
        self.label_email = QLabel('Email: mail@tonyfierro.com')
        self.label_telegram = QLabel('Telegram: @tonyfierro')
        self.label_github = QLabel('GitHub: https://github.com/TONYFIERRO')
        self.groupbox_description = QGroupBox('Description')
        self.groupbox_description_layout = QVBoxLayout()
        self.groupbox_info = QGroupBox('Contacts')
        self.groupbox_info_layout = QVBoxLayout()
        self.button_ok = QPushButton('OK')

        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.label_name)
        self.v_layout.addWidget(self.label_version)
        self.v_layout.addWidget(self.groupbox_description)
        self.groupbox_description_layout.addWidget(self.label_description)
        self.groupbox_description.setLayout(self.groupbox_description_layout)
        self.v_layout.addWidget(self.groupbox_info)
        self.groupbox_info.setLayout(self.groupbox_info_layout)
        self.groupbox_info_layout.addWidget(self.label_author)
        self.groupbox_info_layout.addWidget(self.label_email)
        self.groupbox_info_layout.addWidget(self.label_telegram)
        self.groupbox_info_layout.addWidget(self.label_github)
        self.v_layout.addWidget(self.button_ok)

        self.label_name.setStyleSheet('font: bold 39pt;')
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_version.setStyleSheet('font: bold 18pt;')
        self.label_version.setAlignment(Qt.AlignCenter)
        self.label_description.setAlignment(Qt.AlignCenter)
        self.label_author.setAlignment(Qt.AlignLeft)
        self.label_email.setAlignment(Qt.AlignLeft)
        self.label_telegram.setAlignment(Qt.AlignLeft)
        self.label_github.setAlignment(Qt.AlignLeft)

        self.define_connections()

    def define_connections(self) -> None:
        """
        This function defines connections between elements in the window.

        """

        self.button_ok.clicked.connect(self.handle_button_ok)

    def handle_button_ok(self) -> None:
        """
        The function that handles pushing 'OK' button.

        """

        self.close()

    def show_widget(self) -> None:
        """
        This method opens the window.

        """

        self.show()
