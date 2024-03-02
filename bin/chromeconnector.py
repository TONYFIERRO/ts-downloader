import datetime
import os

from PyQt5.QtCore import (
    QObject,
    pyqtSignal
)
from moviepy.video.io.VideoFileClip import VideoFileClip
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
import pyautogui
import requests

from bin.chromewithprefs import ChromeWithPrefs
from bin.netexport import NetExport
from bin.tshandler import TSHandler


class ChromeConnector(QObject):
    finished = pyqtSignal()
    report_progress = pyqtSignal(int)
    crashed = pyqtSignal()

    def __init__(self, url):
        super().__init__()

        self.url = url
        self.current_time = None

        self.prefs = {
            "download.default_directory": os.getcwd(),
            "browser.altClickSave": True
        }
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("prefs", self.prefs)
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = ChromeWithPrefs(options=self.chrome_options)
        self.driver.get('chrome://net-export/#')
        button = self.driver.find_elements(By.ID, 'start-logging')
        ActionChains(self.driver).click(button[0]).perform()
        pyautogui.press('enter')
        self.driver.switch_to.new_window('tab')
        self.driver.get(self.url)

    def run(self):
        self.driver.quit()
        self.report_progress.emit(0)

        net_export = NetExport('chrome-net-export-log.json')
        net_export.parse_log()
        urls = net_export.get_urls()
        self.report_progress.emit(25)

        if len(urls) > 0:
            url = urls[0]
            chunklist = requests.get(url)
            with open('chunklist.m3u8', 'wb') as downloaded_chunklist:
                downloaded_chunklist.write(chunklist.content)
            self.report_progress.emit(55)

            self.current_time = datetime.datetime.now()
            TSHandler('chunklist.m3u8', f'Video {self.current_time}')
            self.report_progress.emit(75)

            video = VideoFileClip(f'Video {self.current_time}.mp4')
            video.audio.write_audiofile(f'Audio {self.current_time}.mp3')
            self.report_progress.emit(95)
        else:
            file = 'chrome-net-export-log.json'
            if os.path.exists(file):
                os.remove(file)

            self.crashed.emit()

        self.finished.emit()

    def get_current_time(self):
        return self.current_time
