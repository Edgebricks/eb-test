#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import pytest
import unittest2 as unittest
import time

from selenium import webdriver
from ui_automation.testSetup.dataSource.login import Login
from ui_automation.framework.utilities.teststatus import TestStatus
from ui_automation.testSetup.pages.loginPage import LoginPage

@pytest.mark.usefixtures("oneTimeSetUp")

class LoginTest(unittest.TestCase):


  @pytest.fixture()
  def objectSetUp(self,oneTimeSetUp):
      self.lp = LoginPage(self.driver)
      self.ts = TestStatus(self.driver)
      self.loginConfig = Login()
      self.customerid  =  self.loginConfig.customerID
      self.businessunit = self.loginConfig.businessUnit
      self.username = self.loginConfig.userName
      self.password = self.loginConfig.password
      self.region   = self.loginConfig.region

  @pytest.mark.usefixtures("objectSetUp")
  def test_login(self):
      self.lp.logout()
      result1 = self.lp.verifyLoginTitle()
      self.ts.mark(result1,"Title Verification")
      if result1 == False:
         self.driver.quit()
      self.lp.signinAfterLogout(self.customerid, self.businessunit,
                                 self.username, self.password, self.region)
      result2 = self.lp.verifyLoginStatus()
      self.ts.markFinal("test_login", result2, "Login Verification")
      if result2 == False:
         self.driver.quit()
