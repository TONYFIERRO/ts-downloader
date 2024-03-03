import json
import re


class NetExport:
    """
    The class responsible for parsing .json file in order to find the URL of the chunklist.m3u8 file.

    """

    def __init__(self, filename: str) -> None:
        """
        The constructor of the class: .json file opens here.

        """

        self.urls = []
        with open(filename, 'r') as jsonfile:
            self.log = str(json.loads(jsonfile.read()))

    def parse_log(self) -> None:
        """
        The function parses a text.

        """

        self.urls = re.findall(r'https?://\S+/chunklist.m3u8', self.log)

    def get_urls(self) -> list:
        """
        The function returns a list of found URLs.

        """

        return self.urls
