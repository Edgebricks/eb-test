#! /usr/bin/env python

# Author: prem@zerostack.com
# (c) 2017 ZeroStack


import json
import os



class TestCaseDataProvider(object):
    """
    Base configuration class that reads/write configuration from
    .json file . Mainly used for persistent test data store.

    """

    def __init__(self, filename):
        #self._fname   = self._getFile(filename)
        self._fname = filename
    def _getFile(self, filename):
        #fpath = os.path.abspath(__file__)
        #by sweta
        fpath = os.path.abspath(self._fname)

        """
        while True:
            fpath, fname = os.path.split(fpath)
            if fname == 'zstest':
               break
        """
        for root, _, files in os.walk(fpath):
           for fname in files:
                if fname == filename:
                    return os.path.join(root, fname)

        return None

    def _get(self):
        with open(self._fname, 'r') as f:
            return json.load(f)

    def get(self, key, config):
        configs = self._get()
        return configs.get(key, {}).get(config)

    def set(self, key, config, value):
        configs = self._get()
        configs[key][config] = value
        with open(self._fname, 'w') as f:
            json.dump(configs, f, indent=4)
