# Source: https://github.com/ultrafunkamsterdam/undetected-chromedriver/issues/524
# by user named as sebdelsol, who commented on Mar 3, 2022.

import json
import os
import tempfile
from functools import reduce
from selenium import webdriver


class ChromeWithPrefs(webdriver.Chrome):
    def __init__(self, *args, options=None, **kwargs):
        if options:
            self._handle_prefs(options)

        super().__init__(*args, options=options, **kwargs)

        self.keep_user_data_dir = False

    @staticmethod
    def _handle_prefs(options):
        if prefs := options.experimental_options.get("prefs"):

            def undot_key(key, value):
                if "." in key:
                    key, rest = key.split(".", 1)
                    value = undot_key(rest, value)
                return {key: value}

            undot_prefs = reduce(
                lambda d1, d2: {**d1, **d2},
                (undot_key(key, value) for key, value in prefs.items()),
            )

            user_data_dir = os.path.normpath(tempfile.mkdtemp())
            options.add_argument(f"--user-data-dir={user_data_dir}")

            default_dir = os.path.join(user_data_dir, "Default")
            os.mkdir(default_dir)

            prefs_file = os.path.join(default_dir, "Preferences")
            with open(prefs_file, encoding="latin1", mode="w") as f:
                json.dump(undot_prefs, f)

            del options.experimental_options["prefs"]
