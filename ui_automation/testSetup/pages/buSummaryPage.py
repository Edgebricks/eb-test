#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import pytest
import logging

from ui_automation.framework.base.basePage import BasePage
import ui_automation.framework.utilities.customLogger as cl

class BUSummaryPage(BasePage):
  """
  Class contains the links which can be used for navigating to
  BU summary
  BU Projects
  BU Configuration
  """

  log = cl.customLogger(logging.DEBUG)
  def __init__(self,driver):
      super().__init__(driver)
      self.driver=driver

  #locators
  #summaryLink = "//li[contains(@ui-sref,'app.BU.details.summary')]"
  summaryLink = "/html/body/div[1]/div[1]/div[5]/div/div/div[1]/ul/li[1]"
  #projectsLink = "//li[contains(@ui-sref,'app.BU.details.projects')]"
  projectsLink = "/html/body/div[1]/div[1]/div[5]/div/div/div[1]/ul/li[2]"
  #configurationLink = "//li[contains(@ui-sref,'app.BU.details.configuration')]"
  configurationLink = "/html/body/div[1]/div[1]/div[5]/div/div/div[1]/ul/li[3]"

  # Added By S
  planningLink = "/html/body/div[1]/div[1]/div[5]/div/div/div[1]/ul/li[4]"
  apiLink      = "/html/body/div[1]/div[1]/div[5]/div/div/div[1]/ul/li[5]"

  def navigateToSummary(self):
      self.waitForElement(self.summaryLink, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(locator= self.summaryLink, locatorType="xpath")

  def navigateToProjects(self):
      self.waitForElement(self.projectsLink, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(locator= self.projectsLink, locatorType="xpath")

  def navigateToConfiguration(self):
      self.waitForElement(self.configurationLink, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(locator= self.configurationLink, locatorType="xpath")

  def navigateToPlanning(self):
      self.waitForElement(self.planningLink, locatorType="xpath",
                         timeout=120, pollFrequency=0.2)

      self.elementClick(locator= self.planningLink, locatorType="xpath")

  def navigateToAPI(self):
      self.waitForElement(self.apiLink, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(locator= self.apiLink, locatorType="xpath")
