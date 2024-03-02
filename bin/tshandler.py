# Source: https://github.com/hankchen1728/py_m3u8_downloader
# by the GitHub user hankchen1728

import glob
import os
import re
import shutil
import subprocess
import time
from datetime import datetime
from functools import partial
from multiprocessing.dummy import Pool
import requests
import tqdm
from requests.models import Response

header = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) "
                  "AppleWebKit/602.4.8 (KHTML, like Gecko) Version"
                  "/10.0.3 Safari/602.4.8"
}


class VideoDecoder(object):
    def __init__(self, x_key: dict, m3u8_http_base: str = ""):
        self.method = x_key["METHOD"] if "METHOD" in x_key.keys() else ""
        self.uri = decode_key_uri(m3u8_http_base + x_key["URI"]) \
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


def decode_key_uri(URI: str):
    uri_req = requests.get(URI, headers=header)
    uri_str = "".join(["{:02x}".format(c) for c in uri_req.content])
    return uri_str


def decode_ext_x_key(key_str: str):
    key_str = key_str.replace('"', '').lstrip("#EXT-X-KEY:")
    v_list = re.findall(r"[^,=]+", key_str)
    key_map = {v_list[i]: v_list[i + 1] for i in range(0, len(v_list), 2)}
    return key_map


def download_ts_file(ts_url: str, store_dir: str, attempts: int = 10):
    ts_fname = ts_url.split('/')[-1]
    ts_dir = os.path.join(store_dir, ts_fname)
    ts_res = None

    for _ in range(attempts):
        try:
            ts_res = requests.get(ts_url, headers=header)
            if ts_res.status_code == 200:
                break
        except requests.exceptions.Timeout:
            pass
        time.sleep(.5)

    if isinstance(ts_res, Response) and ts_res.status_code == 200:
        with open(ts_dir, 'wb+') as f:
            f.write(ts_res.content)
    else:
        print(f"Failed to download streaming file: {ts_fname}.")


class TSHandler:
    def __init__(self, chunklist, output=None):
        self.startTime = datetime.now()

        self.output = output
        self.m3u8_link = chunklist
        self.merged_mp4 = None
        self.m3u8_http_base = ""
        self.m3u8_content = None
        self.video_decoder = None
        self.ts_url_list = []
        self.ts_names = []
        self.directory = None
        self.ts_folder = None

        self.read_m3u8()
        self.parse_m3u8_content()
        self.set_paths()
        self.download_ts()
        self.merge_ts()
        self.remove_downloaded_ts()

        self.endTime = datetime.now()
        print("Finish:", self.endTime)
        print("Time spent:", self.endTime - self.startTime)

    def read_m3u8(self):
        if self.output is not None:
            self.merged_mp4 = self.output
            if not self.merged_mp4.endswith(".mp4"):
                self.merged_mp4 += ".mp4"
        else:
            self.merged_mp4 = self.m3u8_link.split("/")[-1].rstrip('.m3u8') + ".mp4"

        if self.m3u8_link.startswith("http"):
            self.m3u8_content = requests.get(
                self.m3u8_link, headers=header
            ).content.decode("utf-8")
            self.m3u8_http_base = self.m3u8_link.rstrip(self.m3u8_link.split("/")[-1])
        else:
            self.m3u8_content = ""

            with open(self.m3u8_link, 'r') as f:
                self.m3u8_content = f.read()
                if not self.m3u8_content:
                    raise RuntimeError(f"The m3u8 file: {self.m3u8_link} is empty.")

    def parse_m3u8_content(self):
        m3u8 = self.m3u8_content.split('\n')
        self.ts_names = []
        x_key_dict = dict()
        for i_str in range(len(m3u8)):
            line_str = m3u8[i_str]
            if line_str.startswith("#EXT-X-KEY:"):
                x_key_dict = decode_ext_x_key(line_str)
            elif line_str.startswith("#EXTINF"):
                ts_url = m3u8[i_str + 1]
                self.ts_names.append(ts_url.split('/')[-1])
                if not ts_url.startswith("http"):
                    ts_url = self.m3u8_http_base + ts_url
                self.ts_url_list.append(ts_url)
        print("There are", len(self.ts_url_list), "files to download ...")
        self.video_decoder = VideoDecoder(
            x_key=x_key_dict,
            m3u8_http_base=self.m3u8_http_base
        )

    def set_paths(self):
        self.directory = os.getcwd()
        print("MP4 stored in: ", self.directory)
        self.ts_folder = os.path.join(self.directory, ".tmp_ts")
        os.makedirs(self.ts_folder, exist_ok=True)
        os.chdir(self.ts_folder)

    def download_ts(self):
        pool = Pool(20)
        gen = pool.imap(partial(download_ts_file, store_dir='.'), self.ts_url_list)
        for _ in tqdm.tqdm(gen, total=len(self.ts_url_list)):
            pass
        pool.close()
        pool.join()
        time.sleep(1)
        print("Streaming files downloading completed.")

    def merge_ts(self):
        downloaded_ts = glob.glob("*.ts")

        for ts_fname in tqdm.tqdm(
                downloaded_ts, desc="Decoding the *.ts files"
        ):
            self.video_decoder(ts_fname)

        ordered_ts_names = [
            ts_name for ts_name in self.ts_names if ts_name in downloaded_ts
        ]

        if len(ordered_ts_names) > 200:
            mp4_fnames = []
            part_num = len(ordered_ts_names) // 200 + 1
            for _i in range(part_num):
                sub_files_str = "concat:"

                _idx_list = range(200)
                if _i == part_num - 1:
                    _idx_list = range(len(ordered_ts_names[_i * 200:]))
                for ts_idx in _idx_list:
                    sub_files_str += ordered_ts_names[ts_idx + _i * 200] + '|'
                sub_files_str.rstrip('|')

                mp4_fnames.append('part_{}.mp4'.format(_i))
                subprocess.run([
                    'ffmpeg', '-i', sub_files_str, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', 'part_{}.mp4'.format(_i)
                ])

            with open("mylist.txt", 'w') as f:
                for mp4_fname in mp4_fnames:
                    f.write(f"file {mp4_fname}\n")
            subprocess.run([
                'ffmpeg', "-f",
                "concat", "-i", "mylist.txt",
                '-codec', 'copy', self.merged_mp4
            ])
        else:
            files_str = "concat:"
            for ts_filename in ordered_ts_names:
                files_str += ts_filename + '|'
            files_str.rstrip('|')
            subprocess.run([
                'ffmpeg', '-i', files_str, '-c', 'copy', '-bsf:a', 'aac_adtstoasc', self.merged_mp4
            ])

        print("mp4 file merging completed.")

    def remove_downloaded_ts(self):
        mp4_newpath = os.path.join(self.directory, os.path.basename(self.merged_mp4))
        mp4_fullpath = os.path.abspath(self.merged_mp4)
        os.chdir(self.directory)
        shutil.move(mp4_fullpath, mp4_newpath)
        shutil.rmtree(self.ts_folder)
