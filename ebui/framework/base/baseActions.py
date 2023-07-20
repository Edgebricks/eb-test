#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import logging
import time
import os

from traceback import print_stack
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    ElementNotVisibleException,
    ElementNotSelectableException,
)

import ebui.framework.utilities.customLogger as cl


class BaseActions:
    """
    Class having basic operations that need to be performed on the web elements
    eg : get element , click etc.
    """

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def getTitle(self):
        time.sleep(5)  # Wait for the page to load completely
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            by_type = By.ID
        if locatorType == "name":
            by_type = By.NAME
        if locatorType == "xpath":
            by_type = By.XPATH
        if locatorType == "css":
            by_type = By.CSS_SELECTOR
        if locatorType == "class":
            by_type = By.CLASS_NAME
        if locatorType == "link":
            by_type = By.LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
            return False
        return by_type

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info(
                "Element Found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        except BaseException:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        return element

    def getElements(self, locator, locatorType="id"):
        elements = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            elements = self.driver.find_elements(byType, locator)
            self.log.info(
                "Element Found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        except BaseException:
            self.log.info(
                "Element not found with locator: "
                + locator
                + " and  locatorType: "
                + locatorType
            )
        return elements

    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.click()
            self.log.info(
                "Clicked on element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
        except BaseException:
            self.log.error(
                "Cannot click on the element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
            print_stack()

    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info(
                "Sent data on element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
        except BaseException:
            self.log.error(
                "Cannot send data on the element with locator: "
                + locator
                + " locatorType: "
                + locatorType
            )
            print_stack()

    def isElementPresent(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True
            self.log.info("Element not found")
            return False
        except BaseException:
            self.log.info("Element not found")
            return False

    def elementsPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            self.log.info("Element not found")
            return False
        except BaseException:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id", timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info(
                "Waiting for maximum:: "
                + str(timeout)
                + " :: seconds for element to be clickable"
            )
            wait = WebDriverWait(
                self.driver,
                timeout=timeout,
                poll_frequency=pollFrequency,
                ignored_exceptions=[
                    NoSuchElementException,
                    ElementNotVisibleException,
                    ElementNotSelectableException,
                ],
            )
            element = wait.until(EC.element_to_be_clickable((byType, locator)))
            self.log.info("Element appeared on the web page")
        except BaseException:
            self.log.info("Element not appeared on the web page")
        return element

    def screenShots(self, resultMessage):
        """
        Takes screenshots of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotsDirectory = "../framework/screenshots/"
        relativeFilename = screenshotsDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os.path.join(currentDirectory, relativeFilename)
        destinationDirectory = os.path.join(currentDirectory, screenshotsDirectory)

        try:
            if not os.path.exists(destinationDirectory):
                os.makedirs(destinationDirectory)
            self.driver.save_screenshot(destinationFile)
            self.log.info("Screenshots saved to directory:" + destinationFile)
        except BaseException:
            self.log.error("###Exception Occured")
            print_stack()
