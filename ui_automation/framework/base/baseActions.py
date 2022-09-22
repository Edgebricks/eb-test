#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import logging
import time
import os

from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *

import ui_automation.framework.utilities.customLogger as cl


class BaseActions():
    """
    Class having basic operations that need to be performed on the web elements
    eg : get element , click etc.
    """
    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        self.driver = driver

    def getTitle(self):
        time.sleep(5) # Wait for the page to load completely
        return self.driver.title

    def getByType(self, locatorType):
        locatorType = locatorType.lower()
        if locatorType == "id":
            return By.ID
        elif locatorType == "name":
            return By.NAME
        elif locatorType == "xpath":
            return By.XPATH
        elif locatorType == "css":
            return By.CSS_SELECTOR
        elif locatorType == "class":
            return By.CLASS_NAME
        elif locatorType == "link":
            return By.LINK_TEXT
        elif locatorType == "partial-link":
            return By.PARTIAL_LINK_TEXT
        else:
            self.log.info("Locator type " + locatorType + " not correct/supported")
        return False

    def getElement(self, locator, locatorType="id"):
        element = None
        try:
            locatorType = locatorType.lower()
            byType = self.getByType(locatorType)
            element = self.driver.find_element(byType, locator)
            self.log.info("Element Found with locator: " + locator +
            " and  locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator +
            " and  locatorType: " + locatorType)
        return element

    def getElements(self, locator, locatorType="id"):
        elements = None
        try:
           locatorType = locatorType.lower()
           byType = self.getByType(locatorType)
           elements = self.driver.find_elements(byType, locator)
           self.log.info("Element Found with locator: " + locator +
           " and  locatorType: " + locatorType)
        except:
            self.log.info("Element not found with locator: " + locator +
            " and  locatorType: " + locatorType)
        return elements

    def elementClick(self, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            #element.click()
            self.driver.execute_script("arguments[0].click()", element)
            self.log.info("Clicked on element with locator: " + locator +
            " locatorType: " + locatorType)
        except:
            self.log.error("Cannot click on the element with locator: "
            + locator +" locatorType: " + locatorType)
            print_stack()

    def sendKeys(self, data, locator, locatorType="id"):
        try:
            element = self.getElement(locator, locatorType)
            element.send_keys(data)
            self.log.info("Sent data on element with locator: " + locator +
            " locatorType: " + locatorType)
        except:
            self.log.error("Cannot send data on the element with locator: "
            + locator +" locatorType: " + locatorType)
            print_stack()

    def isElementPresent(self, locator, locatorType="id"):
        try:
            self.wait   = WebDriverWait(self.driver, 100)
            element = self.wait.until(EC.visibility_of_element_located((locatorType,locator)))
            #element = self.getElement(locator, locatorType)
            if element is not None:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def elementsPresenceCheck(self, locator, byType):
        try:
            elementList = self.driver.find_elements(byType, locator)
            if len(elementList) > 0:
                self.log.info("Element Found")
                return True
            else:
                self.log.info("Element not found")
                return False
        except:
            self.log.info("Element not found")
            return False

    def waitForElement(self, locator, locatorType="id",
                               timeout=10, pollFrequency=0.5):
        element = None
        try:
            byType = self.getByType(locatorType)
            self.log.info("Waiting for maximum :: " + str(timeout) +
                  " :: seconds for element to be clickable")
            wait = WebDriverWait(self.driver, timeout, pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            #element = wait.until(EC.element_to_be_clickable((byType,"stopFilter_stops-0")))
            element = wait.until(EC.element_to_be_clickable((byType,locator)))
            self.log.info("Element appeared on the web page")
        except Exception as e:
            self.log.info("Element not appeared on the web page")
        return element


    def waitForElements(self, locator, locatorType="id",
                               timeout=10, pollFrequency=0.5):
        elements = None
        try:
            byType = self.getByType(locatorType)
            wait = WebDriverWait(self.driver, timeout, pollFrequency,
                                 ignored_exceptions=[NoSuchElementException,
                                                     ElementNotVisibleException,
                                                     ElementNotSelectableException])
            elements = wait.until(EC.visibility_of_all_elements_located((byType,locator)))
            self.log.info("Elements appeared on the web page")
        except Exception as e:
            self.log.info("Elements not appeared on the web page")
        return elements

    def screenShots(self, resultMessage):
        """
        Takes screenshots of the current open web page
        """
        fileName = resultMessage + "." + str(round(time.time() * 1000)) + ".png"
        screenshotsDirectory = "../framework/screenshots/"
        relativeFilename = screenshotsDirectory + fileName
        currentDirectory = os.path.dirname(__file__)
        destinationFile = os .path.join(currentDirectory, relativeFilename)
        destinationDirectory = os.path.join(currentDirectory, screenshotsDirectory)

        try:
           if not os.path.exists(destinationDirectory):
              os.makedirs(destinationDirectory)
           self.driver.save_screenshot(destinationFile)
           self.log.info("Screenshots saved to directory:" +destinationFile)
        except:
           self.log.error("###Exception Occured")
           print_stack()
