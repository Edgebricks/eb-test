#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack

## by S
from selenium.webdriver.common.by import By
from traceback import print_stack
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
###

import pytest
import logging

from ui_automation.framework.base.basePage import BasePage
import ui_automation.framework.utilities.customLogger as cl

class NavigationPage(BasePage):
      """
      Class contains methods to navigate to the links common for all the pages
      """

      log = cl.customLogger(logging.DEBUG)

      def __init__(self,driver):
          super().__init__(driver)
          self.driver=driver

      #locators
      dashboardLink = "Dashboard"
      infrastructureLink = "Infrastructure"
      #businessUnitLink = "Business Units"
      businessUnitLink = "/html/body/div[1]/nav/ul/li[3]"
      usersLink = "//li/a/span/i[@class='ico ico-users']"
      appsLink  = "//li/a/span/i[@class='ico ico-app-store']"
      costManagementLink = "Cost Management"
      settingsLink = "Settings"
      feedbackLocator = "//div/i[@ng-click='goToFeedbackForm()']"
      zsHelpHandlerIcon = "zsHelpHandler"
      goToCloudServiceIcon = "goToCloudService"
      regionSelectorIcon   = "regionSelector"

      def navigateToDashboard(self):
          self.elementClick(locator= self.dashboardLink, locatorType="link")

      def navigateToInfrastructure(self):
          self.elementClick(locator= self.infrastructureLink,
                            locatorType="link")

      def navigateToBusinessUnit(self):
          #self.elementClick(locator= self.businessUnitLink, locatorType="link")
          self.waitForElement(self.businessUnitLink, locatorType="xpath",
                              timeout=60, pollFrequency=0.2)
          self.elementClick(locator= self.businessUnitLink, locatorType="xpath")


      def navigateToUsers(self):
          self.elementClick(locator= self.usersLink, locatorType="xpath")

      def navigateToApps(self):
          self.waitForElement(self.appsLink, locatorType="xpath",
                              timeout=120, pollFrequency=0.2)

          self.elementClick(locator= self.appsLink, locatorType="xpath")

      def navigateToCostManagement(self):
          self.elementClick(locator= self.costManagementLink, locatorType="link")

      def navigateToSettings(self):
          self.elementClick(locator= self.settingsLink, locatorType="link")

      def navigateToFeedbackForm(self):
          self.elementClick(locator= self.feedbackLocator, locatorType="xpath")

      def navigateToZSHelpHandler(self):
          self.elementClick(locator= zsHelpHandlerIcon)

      def navigateToCloudServiceIcon(self):
          self.elementClick(locator= goToCloudServiceIcon)

      def navigateToRegionSelector(self):
          self.waitForElement(self.regionSelectorIcon, locatorType="id",
                              timeout=60, pollFrequency=0.2)
          self.elementClick(locator= self.regionSelectorIcon, locatorType="id")
          self.log.info(f'Navigation successful')
