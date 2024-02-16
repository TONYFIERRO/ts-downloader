import sys
import datetime
import os
import shutil
import time
import pyautogui
import qdarktheme
import requests
import validators
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from moviepy.editor import VideoFileClip
from PyQt5.QtWidgets import (
    QApplication,
    QWidget
)

from mainwindow import MainWindow
from chrome_with_prefs import ChromeWithPrefs
from net_export import NetExport
from ts_handler import TSHandler

# TODO: create log-file where the program will write names of the files that will be downloaded

if __name__ == "__main__":
    qdarktheme.enable_hi_dpi()
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    window = MainWindow()
    window.show()
    app.exec()

    # prefs_ = {
    #     "download.default_directory": os.getcwd(),
    #     "browser.altClickSave": True
    # }
    #
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_experimental_option("prefs", prefs_)
    # driver = ChromeWithPrefs(options=chrome_options)
    # time.sleep(5)
    #
    # driver.get('chrome://net-export/#')
    # button = driver.find_elements(By.ID, 'start-logging')
    # ActionChains(driver).click(button[0]).perform()
    # pyautogui.press('enter')
    # driver.switch_to.new_window('tab')
    # driver.get("https://trillioner.life/members/login")
    #
    # time.sleep(30)
    # driver.quit()
    # time.sleep(10)

    # net_export = NetExport()
    # net_export.parse_log()
    # url = net_export.get_urls()[0]
    # print(url)
    #
    # chunklist = requests.get(url)
    # with open("chunklist.m3u8", "wb") as downloaded_chunklist:
    #     downloaded_chunklist.write(chunklist.content)
    #
    # TSHandler('chunklist.m3u8')
    #
    # video = VideoFileClip("chunklist.mp4")
    # current_time = datetime.datetime.now()
    # video.audio.write_audiofile(f"Audio{current_time}.mp3")
    #
    # tmp_files = [
    #     "chrome-net-export-log.json",
    #     "chunklist.m3u8",
    #     "chunklist.mp4"
    # ]
    # for file in tmp_files:
    #     if os.path.exists(file):
    #         os.remove(file)
