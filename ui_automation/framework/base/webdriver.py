#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


"""
@package base

WebDriver class implementation
It creates a webdriver instance based on browser configurations

Example:
    wdf = WebDriver(browser)
    wdf.getWebDriverInstance()
"""
import traceback
import os
import logging

from selenium import webdriver
from ui_automation.testSetup.dataSource.login import Login

import ui_automation.framework.utilities.customLogger as cl
log = cl.customLogger(logging.DEBUG)

class WebDriver():

    def __init__(self, browser):
        self.browser = browser
        self.config = Login()
        self.baseURL = self.config.baseURL

    def getDriverPath(self):
        fpath = os.path.abspath(__file__)
        while True:
              fpath, fname = os.path.split(fpath)
              #if fname == 'zstest':
              if fname == 'eb-test':
                 fpath = os.path.join(fpath, fname)
                 break
        for root, _, files in os.walk(fpath):

            for fname in files:
                if fname == "chromedriver.exe":
                   return os.path.join(root, fname)

        return None


    def getWebDriverInstance(self):
        """
        Get WebDriver Instance based on the browser configuration

        Returns:
            'WebDriver Instance'
        """
        path = self.getDriverPath()
        if self.browser == "iexplorer":
            # Set ie driver
            driver = webdriver.Ie()
        elif self.browser == "firefox":
            driver = webdriver.Firefox()
        elif self.browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--headless")
            driver = webdriver.Chrome(path, options = options)
        else:
            options = webdriver.ChromeOptions()
            options.add_experimental_option('excludeSwitches', ['enable-logging'])
            options.add_argument("--headless")
            driver = webdriver.Chrome(path, options = options)

        # Maximize the window
        driver.maximize_window()

        # Loading browser with App URL
        driver.get(self.baseURL)
        return driver
