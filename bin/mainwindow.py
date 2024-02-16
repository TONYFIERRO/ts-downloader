import validators
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QGroupBox, QPushButton, QSpacerItem, QSizePolicy, QLabel, \
    QMainWindow, QCheckBox, QHBoxLayout

from bin.aboutwidget import About
from bin.agreementwidget import Agreement
from bin.chromeopener import ChromeOpener


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("TS-Downloader")
        self.setFixedSize(400, 400)

        self.about_widget = About()
        self.agreement_widget = Agreement()
        self.chrome_opener = ChromeOpener()
        self.main_widget = QWidget()
        self.v_layout = QVBoxLayout()
        self.group_box_url = QGroupBox('URL')
        self.group_box_url_layout = QVBoxLayout()
        self.line_edit_url = QLineEdit('')
        self.button_start = QPushButton('Start')
        self.button_about = QPushButton('About')
        self.label_icon = QLabel("TS-Downloader")
        self.group_box_formats = QGroupBox('Output Format')
        self.group_box_formats_layout = QHBoxLayout()
        self.checkbox_mp3 = QCheckBox('MP3 (Audio)')
        self.checkbox_mp4 = QCheckBox('MP4 (Video)')

        self.setCentralWidget(self.main_widget)
        self.main_widget.setLayout(self.v_layout)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.addWidget(self.label_icon)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.addWidget(self.group_box_url)
        self.group_box_url.setLayout(self.group_box_url_layout)
        self.group_box_url_layout.addWidget(self.line_edit_url)
        self.v_layout.addWidget(self.group_box_formats)
        self.v_layout.addWidget(self.button_start)
        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.v_layout.addWidget(self.button_about)
        self.group_box_formats.setLayout(self.group_box_formats_layout)
        self.group_box_formats_layout.addWidget(self.checkbox_mp3)
        self.group_box_formats_layout.addWidget(self.checkbox_mp4)

        self.label_icon.setStyleSheet('font: bold 39pt;')
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.button_start.setEnabled(False)
        self.line_edit_url.setPlaceholderText('Example: https://www.google.com/')

        self.define_connections()

    def define_connections(self):
        self.button_about.clicked.connect(self.handle_button_about)
        self.button_start.clicked.connect(self.handle_button_start)
        self.line_edit_url.textChanged.connect(self.handle_activation_button_start)
        self.checkbox_mp4.clicked.connect(self.handle_activation_button_start)
        self.checkbox_mp3.clicked.connect(self.handle_activation_button_start)

    def handle_button_about(self):
        self.about_widget.show_widget()

    def handle_button_start(self):
        self.hide()
        self.chrome_opener.url = self.line_edit_url.text()
        self.chrome_opener.mp3_flag = self.checkbox_mp3.isChecked()
        self.chrome_opener.mp4_flag = self.checkbox_mp4.isChecked()
        self.agreement_widget.chrome_opener = self.chrome_opener
        self.agreement_widget.show_widget()

    def handle_activation_button_start(self):
        if self.line_edit_url.text() != '' and validators.url(self.line_edit_url.text()):
            if self.checkbox_mp3.isChecked() or self.checkbox_mp4.isChecked():
                self.button_start.setEnabled(True)
            else:
                self.button_start.setEnabled(False)
        else:
            self.button_start.setEnabled(False)
