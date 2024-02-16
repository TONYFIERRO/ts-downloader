import datetime
import os
import time

import pyautogui
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QPushButton, QGroupBox, QProgressBar
from PyQt5.QtWidgets import (
    QWidget
)
from moviepy.video.io.VideoFileClip import VideoFileClip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from bin.chrome_with_prefs import ChromeWithPrefs
from bin.net_export import NetExport
from bin.ts_handler import TSHandler


class ChromeOpener(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(470, 250)

        self.url = None
        self.mp3_flag = None
        self.mp4_flag = None

        self.prefs = {
            "download.default_directory": os.getcwd(),
            "browser.altClickSave": True
        }
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("prefs", self.prefs)
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = None

        self.v_layout = QVBoxLayout()
        self.label_instruction = QLabel('Google Chrome will be opened when you click the button "Open".\n'
                                        'Choose the video that you want to download and play it.\n'
                                        'Then click the button "Start downloading".')
        self.button_open = QPushButton('Open')
        self.button_start_downloading = QPushButton('Start downloading')
        self.groupbox_instruction = QGroupBox('Instruction')
        self.groupbox_instruction_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()

        self.setLayout(self.v_layout)
        self.v_layout.addWidget(self.groupbox_instruction)
        self.groupbox_instruction_layout.addWidget(self.label_instruction)
        self.v_layout.addWidget(self.button_open)
        self.v_layout.addWidget(self.button_start_downloading)
        self.v_layout.addWidget(self.progress_bar)
        self.groupbox_instruction.setLayout(self.groupbox_instruction_layout)

        self.button_start_downloading.setEnabled(False)
        self.label_instruction.setAlignment(Qt.AlignCenter)
        self.progress_bar.setVisible(False)

        self.define_connections()

    def define_connections(self):
        self.button_open.clicked.connect(self.handle_button_open)
        self.button_start_downloading.clicked.connect(self.handle_button_start_downloading)

    def handle_button_open(self):
        self.button_open.setEnabled(False)
        self.button_start_downloading.setEnabled(True)

        self.driver = ChromeWithPrefs(options=self.chrome_options)
        self.driver.get('chrome://net-export/#')
        button = self.driver.find_elements(By.ID, 'start-logging')
        ActionChains(self.driver).click(button[0]).perform()
        pyautogui.press('enter')
        self.driver.switch_to.new_window('tab')
        self.driver.get(self.url)

    def handle_button_start_downloading(self):
        self.button_start_downloading.setEnabled(False)
        self.progress_bar.setVisible(True)

        self.driver.quit()
        net_export = NetExport()
        net_export.parse_log()
        urls = net_export.get_urls()
        self.progress_bar.setValue(20)
        if len(urls) > 0:
            url = urls[0]
            chunklist = requests.get(url)
            with open('chunklist.m3u8', 'wb') as downloaded_chunklist:
                downloaded_chunklist.write(chunklist.content)
            self.progress_bar.setValue(40)

            current_time = datetime.datetime.now()
            TSHandler('chunklist.m3u8', f'Video {current_time}')
            self.progress_bar.setValue(60)

            video = VideoFileClip(f'Video {current_time}.mp4')
            video.audio.write_audiofile(f'Audio {current_time}.mp3')
            self.progress_bar.setValue(80)

            tmp_files = [
                'chrome-net-export-log.json',
                'chunklist.m3u8',
            ]

            if self.mp3_flag is False:
                tmp_files.append(f'Audio {current_time}.mp3')
            if self.mp4_flag is False:
                tmp_files.append(f'Video {current_time}.mp4')

            for file in tmp_files:
                if os.path.exists(file):
                    os.remove(file)
            self.progress_bar.setValue(100)
        else:
            print('URL with a chunklist is not found!')

        self.button_open.setEnabled(True)

    def show_widget(self):
        self.show()
