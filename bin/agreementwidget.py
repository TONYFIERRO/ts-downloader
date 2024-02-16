from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox


class Agreement(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(450, 400)

        self.chrome_opener = None

        self.v_layout = QVBoxLayout()
        self.label_agreement = QLabel('Do you agree to respect\n the copyrights of the owner of the video materials?')
        self.checkbox_agree = QCheckBox('I agree')
        self.button_next = QPushButton('Next')

        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.label_agreement)
        self.v_layout.addWidget(self.checkbox_agree)
        self.v_layout.addWidget(self.button_next)

        self.label_agreement.setAlignment(Qt.AlignCenter)
        self.button_next.setEnabled(False)
        self.label_agreement.setStyleSheet('font: bold 16px;')
        self.label_agreement.adjustSize()

        self.define_connections()

    def define_connections(self):
        self.checkbox_agree.clicked.connect(self.handle_checkbox_agree)
        self.button_next.clicked.connect(self.handle_button_next)

    def handle_checkbox_agree(self):
        self.button_next.setEnabled(self.checkbox_agree.isChecked())

    def handle_button_next(self):
        self.close()
        self.chrome_opener.show()

    def show_widget(self):
        self.show()
