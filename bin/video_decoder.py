import re
import subprocess

import requests

header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) "
                  "AppleWebKit/602.4.8 (KHTML, like Gecko) Version"
                  "/10.0.3 Safari/602.4.8"
}


class VideoDecoder(object):
    def __init__(self, x_key: dict, m3u8_http_base: str = ""):
        self.method = x_key["METHOD"] if "METHOD" in x_key.keys() else ""
        self.uri = self.decode_key_uri(m3u8_http_base+x_key["URI"]) \
            if "URI" in x_key.keys() else ""
        self.iv = x_key["IV"].lstrip("0x") if "IV" in x_key.keys() else ""

        # print("URI", self.uri)
        # print("IV", self.iv)

    def decode_aes_128(self, video_fname: str):
        subprocess.run([
            "openssl",
            "aes-128-cbc",
            "-d",
            "-in", video_fname,
            "-out", "out" + video_fname,
            "-nosalt",
            "-iv", self.iv,
            "-K", self.uri
        ])
        subprocess.run(["rm", "-f", video_fname])
        subprocess.run(["mv", "out" + video_fname, video_fname])

    def __call__(self, video_fname: str):
        if self.method == "AES-128":
            self.decode_aes_128(video_fname)
        else:
            pass

    @staticmethod
    def decode_key_uri(URI: str):
        uri_req = requests.get(URI, headers=header)
        uri_str = "".join(["{:02x}".format(c) for c in uri_req.content])
        return uri_str


def decode_ext_x_key(key_str: str):
    # TODO: check if there is case with "'"
    key_str = key_str.replace('"', '').lstrip("#EXT-X-KEY:")
    v_list = re.findall(r"[^,=]+", key_str)
    key_map = {v_list[i]: v_list[i+1] for i in range(0, len(v_list), 2)}
    return key_map
