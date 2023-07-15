#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import json
import os


class TestCaseDataProvider():
    """
    Base configuration class that reads/write configuration from
    .json file . Mainly used for persistent test data store.

    """

    def __init__(self, filename):
        self._fname = self._getFile(filename)

    def _getFile(self, filename):
        fpath = os.path.abspath(__file__)
        while True:
            fpath, fname = os.path.split(fpath)
            if fname == "zstest":
                break

        for root, _, files in os.walk(fpath):
            for fname in files:
                if fname == filename:
                    return os.path.join(root, fname)

        return None

    def _get(self):
        with open(self._fname, "r", encoding="UTF-8", errors="ignore") as f:
            return json.load(f)

    def get(self, key, config):
        configs = self._get()
        return configs.get(key, {}).get(config)

    def set(self, key, config, value):
        configs = self._get()
        configs[key][config] = value
        with open(self._fname, "w", encoding="UTF-8", errors="ignore") as f:
            json.dump(configs, f, indent=4)
