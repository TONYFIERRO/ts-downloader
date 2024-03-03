from PyQt5.QtCore import (
    Qt
)

from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QGroupBox
)


class HelpWidget(QWidget):
    """
    The class responsible for the instruction how to use the program.

    """

    def __init__(self) -> None:
        """
        The window initialization and its elements.

        """

        super().__init__()
        self.setFixedSize(400, 400)
        self.setWindowTitle("Instruction")

        self.v_layout = QVBoxLayout()
        self.label_icon = QLabel("TS-Downloader")
        self.label_icon_text = QLabel('Instruction')
        self.groupbox_steps = QGroupBox('Steps')
        self.groupbox_steps_layout = QVBoxLayout()
        self.label_instruction_1 = QLabel('1. Google Chrome will be opened when you click \nthe button "Start".')
        self.label_instruction_2 = QLabel('2. Choose the video that you want to download \nand play it.')
        self.label_instruction_3 = QLabel('3. Then click the button "Start downloading".')
        self.label_agreement = QLabel('Using this program you automatically agree to respect\n the copyrights of the '
                                      'owner of the video materials.')
        self.button_ok = QPushButton('OK')

        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.label_icon)
        self.v_layout.addWidget(self.label_icon_text)
        self.v_layout.addWidget(self.groupbox_steps)
        self.groupbox_steps.setLayout(self.groupbox_steps_layout)
        self.groupbox_steps_layout.addWidget(self.label_instruction_1)
        self.groupbox_steps_layout.addWidget(self.label_instruction_2)
        self.groupbox_steps_layout.addWidget(self.label_instruction_3)
        self.v_layout.addWidget(self.label_agreement)
        self.v_layout.addWidget(self.button_ok)

        self.label_icon.setStyleSheet('font: bold 39pt;')
        self.label_icon.setAlignment(Qt.AlignCenter)
        self.label_icon_text.setStyleSheet('font: bold 18pt;')
        self.label_icon_text.setAlignment(Qt.AlignCenter)
        self.label_instruction_1.setAlignment(Qt.AlignLeft)
        # self.label_instruction_1.setStyleSheet('font: bold 14px;')
        self.label_instruction_2.setAlignment(Qt.AlignLeft)
        # self.label_instruction_2.setStyleSheet('font: bold 14px;')
        self.label_instruction_3.setAlignment(Qt.AlignLeft)
        # self.label_instruction_3.setStyleSheet('font: bold 14px;')

        self.label_agreement.setAlignment(Qt.AlignCenter)
        # self.label_agreement.setStyleSheet('font: bold 14px;')

        self.define_connections()

    def define_connections(self) -> None:
        """
        This function defines connections between elements in the window.

        """

        self.button_ok.clicked.connect(self.handle_button_ok)

    def handle_button_ok(self) -> None:
        """
        This is the handler of the OK button.

        """

        self.close()

    def show_widget(self) -> None:
        """
        The function that opens the class window.

        """

        self.show()
