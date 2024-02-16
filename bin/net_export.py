import json
import os
import re


class NetExport:
    def __init__(self):
        self.urls = []
        with open('chrome-net-export-log.json', 'r') as jsonfile:
            self.log = str(json.loads(jsonfile.read()))

    def parse_log(self):
        self.urls = re.findall(r'https?://\S+/chunklist.m3u8', self.log)

    def get_urls(self):
        return self.urls
