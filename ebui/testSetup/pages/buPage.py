#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import pytest
import logging

from framework.base.basePage import BasePage
from testSetup.pages.navigationPage import NavigationPage
import framework.utilities.customLogger as cl

class BUPage(BasePage):
  """
  Class contains all the web elements needed for creating a BU
  """

  log = cl.customLogger(logging.DEBUG)
  def __init__(self,driver):
      super().__init__(driver)
      self.driver=driver
      self.np = NavigationPage(driver)

  #locators
  createBusinessUnitLocator = "//div[text()='Create Business Unit']"
  businessUnitNameLocator = "domainName"
  noQuotaLimitRadiobutton = "//label/span[text()='No Quota Limits']"
  quotaLimitRadiobutton = "//label/span[text()='Quota Limits']"
  buLocalRadiobutton = "//label/span[text()='Local']"
  buAd_ldap_Radiobutton = "//label/span[text()='AD/LDAP']"
  username = "//input[@name='userName']"
  email ="//input[@name='email']"
  password ="//input[@name='password']"
  confirmPassword ="//input[@name='confirmPassword']"
  doneButton = "//button[text()='Done']"
  cancelButton = "//button[text()='Cancel']"
  buLocator = "//div[@class='title ng-binding' and text()= '{}']"
  searchBUlocator = "//input[@placeholder='Search Business Units']"

  def createBusinessUnit(self):
      self.waitForElement(self.createBusinessUnitLocator,
                         locatorType="xpath",timeout=120, pollFrequency=0.2)

      self.elementClick(self.createBusinessUnitLocator,
                       locatorType="xpath")

  def enterBusinessUnitName(self, businessUnitName):
      self.waitForElement(self.businessUnitNameLocator,
                          locatorType="xpath",timeout=120, pollFrequency=0.2)

      self.sendKeys(businessUnitName, self.businessUnitNameLocator)

  def enterUserName(self, username):
      self.waitForElement(self.username, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.sendKeys(username, self.username, locatorType="xpath")

  def enterEmail(self, email):
      self.waitForElement(self.email ,locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.sendKeys(email, self.email, locatorType="xpath")

  def enterPassword(self, password):
      self.waitForElement(self.password , locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.sendKeys(password, self.password , locatorType="xpath")

  def enterPasswordAgain(self, confirmpassword):
      self.waitForElement(self.confirmPassword ,
                          locatorType="xpath",timeout=120, pollFrequency=0.2)

      self.sendKeys(confirmpassword, self.confirmPassword,
                   locatorType="xpath")

  def selectNoQuotaLimits(self):
      self.waitForElement(self.noQuotaLimitRadiobutton
                          , locatorType="xpath",timeout=120, pollFrequency=0.2)

      self.elementClick(self.noQuotaLimitRadiobutton , locatorType="xpath")

  def selectQuotalimits(self):
      self.waitForElement(self.quotaLimitRadiobutton, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(self.quotaLimitRadiobutton , locatorType="xpath")

  def selectBULocalRadiobutton(self):
      self.waitForElement(self.buLocalRadiobutton, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(self.buLocalRadiobutton , locatorType="xpath")

  def selectBULdapRadiobutton(self):
      self.waitForElement(self.buAd_ldap_Radiobutton, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(self.buAd_ldap_Radiobutton , locatorType="xpath")

  def clickDone(self):
      self.waitForElement(self.doneButton , locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(self.doneButton, locatorType="xpath")

  def clickCancel(self):
       self.waitForElement(self.cancelButton, locatorType="xpath",
                           timeout=120, pollFrequency=0.2)

       self.elementClick(self.cancelButton, locatorType="xpath")

  def searchBU(self, businessUnitName):
      self.waitForElement(self.searchBUlocator, locatorType="xpath",
                          timeout=120, pollFrequency=0.2)

      self.elementClick(self.searchBUlocator, locatorType="xpath")
      self.sendKeys( businessUnitName, self.searchBUlocator,
                     locatorType="xpath")

  def verifyBUCreated(self, businessUnitName):
      self.searchBU(businessUnitName)
      verifyBUlocator = self.buLocator.format(businessUnitName)
      verifyElement = self.isElementPresent(verifyBUlocator,
                       locatorType="xpath")

      if verifyElement == True:
         self.elementClick(verifyBUlocator, locatorType="xpath")
         self.log.info("BU CREATION WAS SUCCESSFUL")
      else:
         self.log.error("FAILED TO VERIFY BU CREATION")


  def createLocalBuWithNoQuota(self, businessUnitName, username, email,
     			       password, confirmpassword):

      self.np.navigateToBusinessUnit()
      self.createBusinessUnit()
      self.enterBusinessUnitName(businessUnitName)
      self.selectNoQuotaLimits()
      self.selectBULocalRadiobutton()
      self.enterUserName(username)
      self.enterEmail(email)
      self.enterPassword(password)
      self.enterPasswordAgain(confirmpassword)
      self.clickDone()
