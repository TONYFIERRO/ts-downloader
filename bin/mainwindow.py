import validators

from PyQt5.QtCore import (
    Qt
)
from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLineEdit,
    QGroupBox,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QLabel,
    QMainWindow,
    QCheckBox,
    QHBoxLayout
)

from bin.aboutwidget import AboutWidget
from bin.downloadwidget import DownloadWidget
from bin.helpwidget import HelpWidget


class MainWindow(QMainWindow):
    """
    The class responsible for the main window.

    """

    def __init__(self) -> None:
        """
        The window initialization and its elements.

        """

        super().__init__()
        self.setWindowTitle("TS-Downloader")
        self.setFixedSize(400, 400)

        self.download_widget = None

        self.about_widget = AboutWidget()
        self.help_widget = HelpWidget()
        self.main_widget = QWidget()
        self.v_layout = QVBoxLayout()
        self.group_box_url = QGroupBox('URL')
        self.group_box_url_layout = QVBoxLayout()
        self.line_edit_url = QLineEdit('')
        self.button_start = QPushButton('Start')
        self.button_how_does_it_work = QPushButton('How does it work?')
        self.button_about = QPushButton('About the program')
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
        self.v_layout.addWidget(self.button_how_does_it_work)
        self.v_layout.addWidget(self.button_about)
        self.group_box_formats.setLayout(self.group_box_formats_layout)
        self.group_box_formats_layout.addWidget(self.checkbox_mp3)
        self.group_box_formats_layout.addWidget(self.checkbox_mp4)

        self.label_icon.setStyleSheet('font: bold 39pt;')
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.button_start.setEnabled(False)
        self.line_edit_url.setPlaceholderText('Example: https://www.google.com/')

        self.define_connections()

    def define_connections(self) -> None:
        """
        This function defines connections between elements in the window.

        """

        self.button_about.clicked.connect(self.handle_button_about)
        self.button_start.clicked.connect(self.handle_button_start)
        self.line_edit_url.textChanged.connect(self.handle_activation_button_start)
        self.checkbox_mp4.clicked.connect(self.handle_activation_button_start)
        self.checkbox_mp3.clicked.connect(self.handle_activation_button_start)
        self.button_how_does_it_work.clicked.connect(self.handle_button_how_does_it_work)

    def handle_button_how_does_it_work(self) -> None:
        """
        This is the handler of 'How does it work?' button that opens a window with the instruction.

        """

        self.help_widget.show_widget()

    def handle_button_about(self) -> None:
        """
        This is the handler of 'About' button that opens a window about the program.

        """

        self.about_widget.show_widget()

    def handle_button_start(self) -> None:
        """
        This is the handler of start button.

        """

        self.download_widget = DownloadWidget(self.line_edit_url.text(),
                                              self.checkbox_mp3.isChecked(),
                                              self.checkbox_mp4.isChecked())
        self.download_widget.show_widget()

    def handle_activation_button_start(self) -> None:
        """
        This is the functions that's responsible for the activation of start button.

        """

        if self.line_edit_url.text() != '' and validators.url(self.line_edit_url.text()):
            if self.checkbox_mp3.isChecked() or self.checkbox_mp4.isChecked():
                self.button_start.setEnabled(True)
            else:
                self.button_start.setEnabled(False)
        else:
            self.button_start.setEnabled(False)
