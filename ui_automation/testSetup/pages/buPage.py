#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import pytest
import logging
import time
from ui_automation.framework.base.basePage import BasePage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
import ui_automation.framework.utilities.customLogger as cl
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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
  #searchBUlocator = "//input[@placeholder='Search Business Units']"
  searchBUlocator = "/html/body/div[1]/div[1]/div[5]/div/div/div/div[1]/div[2]/div[3]/input"
  buCreationSuccessfulPopUpLocator = '/html/body/div[1]/div[1]/div[4]/div[2]/div/div/div[4]'
  templateDropDown  = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[2]/div[2]/div[3]/div/div[1]"
  coresLocator             = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[1]/div[2]/div[1]/input"
  instancesLocator         = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[1]/div[2]/div[2]/input"
  RAMLocator               = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[1]/div[2]/div[3]/input"
  networksLocator          = "/html/body/div[3]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[2]/div[2]/div[1]/input"
  routersLocator           = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[2]/div[2]/div[2]/input"
  externalIPLocator        = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[2]/div[2]/div[3]/input"
  storageLocator           = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[3]/div[2]/div[1]/input"
  volumesLocator           = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[3]/div[2]/div[2]/input"
  snapshotsLocator         = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[3]/div[2]/div[3]/input"
  SSDLocator               = "/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[4]/div[3]/div[3]/div/div/input"



  def createBusinessUnit(self):
      self.waitForElement(self.createBusinessUnitLocator,
                         locatorType="xpath",timeout=120, pollFrequency=0.2)

      self.elementClick(self.createBusinessUnitLocator,
                       locatorType="xpath")

  def enterBusinessUnitName(self, businessUnitName):
      """
      self.waitForElement(self.businessUnitNameLocator,
                          locatorType="xpath",timeout=120, pollFrequency=0.2)
      """
      self.waitForElement(self.businessUnitNameLocator,
                          locatorType="id",timeout=120, pollFrequency=0.2)
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
         # Fixed by Sweta
         return True
      else:
         self.log.error("FAILED TO VERIFY BU CREATION")
         return False

  def selectBUTemplate(self, template):
    self.wait   = WebDriverWait(self.driver, 120)
    drop_down = self.wait.until(EC.visibility_of_element_located(('xpath', self.templateDropDown)))
    drop_down.click()
    time.sleep(2)
    options_list = self.wait.until(EC.visibility_of_all_elements_located(('xpath','/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[2]/div[2]/div[3]/div/div[1]/div/ul/li')))
    i = 1
    while(i < len(options_list)+1):
        path = f'/html/body/div[1]/div[1]/div[5]/div/div/form/div/div[2]/div[4]/bu-quota-info/div[2]/div[2]/div[3]/div/div[1]/div/ul/li[{i}]'
        option = self.driver.find_element(By.XPATH, path)
        attribute = option.text
        if (attribute == template):
            option = self.driver.find_element(By.XPATH, path)
            option.click()
            break
        i += 1

  def enterQuotaValues(self, cores, instances, RAM, networks,
                       routers, externalIP, storage, volumes, snapshots, SSD):
      self.sendKeys(cores, self.coresLocator,
                   locatorType="xpath")
      self.sendKeys(instances, self.instancesLocator,
                   locatorType="xpath")
      self.sendKeys(RAM, self.RAMLocator,
                   locatorType="xpath")
      self.sendKeys(networks, self.networksLocator,
                   locatorType="xpath")
      self.sendKeys(routers, self.routersLocator,
                   locatorType="xpath")
      self.sendKeys(externalIP, self.externalIPLocator,
                   locatorType="xpath")
      self.sendKeys(storage, self.storageLocator,
                   locatorType="xpath")
      self.sendKeys(volumes, self.volumesLocator,
                   locatorType="xpath")
      self.sendKeys(snapshots, self.snapshotsLocator,
                   locatorType="xpath")
      self.sendKeys(SSD, self.SSDLocator,
                   locatorType="xpath")

  def createLocalBuWithNoQuota(self, businessUnitName, username, email,
     			       password, confirmpassword):

      self.np.navigateToBusinessUnit()
      self.createBusinessUnit()
      self.enterBusinessUnitName(businessUnitName)
      self.selectNoQuotaLimits()
      #self.selectBULocalRadiobutton()
      self.enterUserName(username)
      self.enterEmail(email)
      self.enterPassword(password)
      self.enterPasswordAgain(confirmpassword)
      self.clickDone()

  def createLocalBuWithQuotaLarge(self, businessUnitName, username, email,
                     password, confirmpassword):

    self.np.navigateToBusinessUnit()
    self.createBusinessUnit()
    self.enterBusinessUnitName(businessUnitName)
    self.selectQuotalimits()
    self.selectBUTemplate('Large')
    self.enterUserName(username)
    self.enterEmail(email)
    self.enterPassword(password)
    self.enterPasswordAgain(confirmpassword)
    self.clickDone()

  def createLocalBuWithQuotaMedium(self, businessUnitName, username, email,
                   password, confirmpassword):

      self.np.navigateToBusinessUnit()
      self.createBusinessUnit()
      self.enterBusinessUnitName(businessUnitName)
      self.selectQuotalimits()
      self.selectBUTemplate('Medium')
      self.enterUserName(username)
      self.enterEmail(email)
      self.enterPassword(password)
      self.enterPasswordAgain(confirmpassword)
      self.clickDone()

  def createLocalBuWithQuotaSmall(self, businessUnitName, username, email,
                   password, confirmpassword):

      self.np.navigateToBusinessUnit()
      self.createBusinessUnit()
      self.enterBusinessUnitName(businessUnitName)
      self.selectQuotalimits()
      self.selectBUTemplate('Small')
      self.enterUserName(username)
      self.enterEmail(email)
      self.enterPassword(password)
      self.enterPasswordAgain(confirmpassword)
      self.clickDone()

  def createLocalBuWithQuotaCustom(self, businessUnitName, username, email,
                   password, confirmpassword, cores, instances, RAM, networks,
                   routers, externalIP, storage, volumes, snapshots, SSD):

      self.np.navigateToBusinessUnit()
      self.createBusinessUnit()
      self.enterBusinessUnitName(businessUnitName)
      self.selectQuotalimits()
      self.selectBUTemplate('Custom')
      self.enterQuotaValues(cores, instances, RAM, networks,
      routers, externalIP, storage, volumes, snapshots, SSD)
      self.enterUserName(username)
      self.enterEmail(email)
      self.enterPassword(password)
      self.enterPasswordAgain(confirmpassword)
      self.clickDone()
