#! /usr/bin/env python


# Author: priyanshi@zerostack.com
 # (c) 2018 ZeroStack


import pytest

# By S
import logging
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

##
from ui_automation.framework.base.baseActions import BaseActions
from ui_automation.testSetup.pages.navigationPage import NavigationPage
import ui_automation.framework.utilities.customLogger as cl

class LoginPage(BaseActions):
        """
        Class contains all the elements present on th login page
        """
        log = cl.customLogger(logging.DEBUG)

        def __init__(self,driver):
          super().__init__(driver)
          self.driver=driver
          self.np = NavigationPage(self.driver)

        #locators
        customerID   = "Customer_Id"
        businessUnit = "Business_Unit"
        userName = "User_Name"
        password = "Password"
        signIn = "//button/span[text()='Sign in']"
        errorPrompt = "//div[@class='alert alert-danger ng-binding ng-scope']"
        #loginPageTitle = "Console Login"
        loginPageTitle = "Console"
        regionSelector = "regionSelector"
        #signoutButton = "//button[text()='Sign out from all profiles']"
        signoutButton = '//html/body/div[1]/header/div[1]/div[3]/div[2]/region-list/div/div[3]/div[2]/button'
        removeProfileIcon = "//a[@class='removeProfileIcon']"
        yesForRemoveProfile = "//button[text()='Yes']"
        customerIDValue  = '//*[@id="regionSelector"]/div/span[1]'
        signInSelectRegion = '/html/body/div[2]/div/div/div[2]/div[3]/div/form[1]/div[2]/div/div/div[2]/div/div[2]'
        afterSignOutSelectRegion = '/html/body/div[2]/div/div/div[2]/div[3]/div/form[1]/div[2]/div/div/div[2]'


        def verifyPageTitle(self, title):
            return (self.driver.title == title)

        def verifyLoginTitle(self):
            status = self.verifyPageTitle(self.loginPageTitle)
            self.log.info(f'status = {status}')
            return status

        def enterCustomerID(self,customerid):
            self.sendKeys(customerid, self.customerID)

        def enterBusinessUnit(self, businessunit):
            self.sendKeys(businessunit, self.businessUnit)

        def enterUserName(self, username):
            self.sendKeys(username, self.userName)

        def enterPassword(self, password):
            self.sendKeys(password, self.password)


        def selectRegion(self, region, path):
            # region
            self.wait   = WebDriverWait(self.driver, 120)
            drop_down = self.wait.until(EC.visibility_of_element_located(('xpath', path)))
            drop_down.click()
            time.sleep(2)
            options_list = self.wait.until(EC.visibility_of_all_elements_located(('xpath','/html/body/div[2]/div/div/div[2]/div[3]/div/form[1]/div[2]/div/div/div[2]/div[2]/ul/li')))
            i = 1
            while(i < len(options_list)+1):
                path = f'/html/body/div[2]/div/div/div[2]/div[3]/div/form[1]/div[2]/div/div/div[2]/div[2]/ul/li[{i}]'
                option = self.driver.find_element(By.XPATH, path)
                attribute = option.text
                if (attribute == region):
                    option = self.driver.find_element(By.XPATH, path)
                    option.click()
                    break
                i += 1
        def clickSignInButton(self):
            self.waitForElement(self.signIn , locatorType="xpath",
                              timeout=120, pollFrequency=0.2)

            self.elementClick(self.signIn , locatorType="xpath")

        def clickRemoveProfileIcon(self):
            self.waitForElement(self.removeProfileIcon , locatorType="xpath",
                              timeout=120, pollFrequency=0.2)

            self.elementClick(self.removeProfileIcon, locatorType="xpath")

        def clickYesForRemoveProfile(self):
            self.waitForElement(self.yesForRemoveProfile , locatorType="xpath",
                              timeout=120, pollFrequency=0.2)

            self.elementClick(self.yesForRemoveProfile, locatorType="xpath")

        def verifyLoginStatus(self):

            self.waitForElement(self.regionSelector, locatorType="id",
                              timeout=120, pollFrequency= 0.2)
            verifyElement = self.isElementPresent(self.regionSelector)
            if verifyElement == True:
                return True
            else:
                element = self.getElement(self.errorPrompt,
                                         locatorType="xpath")
                errormssg = element.text
                self.log.error(errormssg)
                return False
                self.driver.quit()

        def verifyCustomerID(self):
            self.waitForElement(self.customerID , locatorType="xpath",
                              timeout=120, pollFrequency=0.2)

            verifyElement = self.isElementPresent(self.customerID)
            if verify_element == True:
                return True
            else:
                return False

        def logout(self):
            self.np.navigateToRegionSelector()
            self.waitForElement(self.signoutButton, locatorType="xpath",
                              timeout=120, pollFrequency= 0.2)

            self.elementClick(self.signoutButton, locatorType="xpath")
            #self.clickRemoveProfileIcon()
            #self.clickYesForRemoveProfile()

        def signinAfterLogout(self, customerid="", businessunit="", username=""
                              , password="", region = ""):
            self.selectRegion(region, self.afterSignOutSelectRegion)
            self.enterBusinessUnit(businessunit)
            self.enterUserName(username)
            self.enterPassword(password)
            self.clickSignInButton()
            self.verifyLoginStatus()

        def login(self,customerid="", businessunit="", username="", password="", region=""):
            self.enterCustomerID(customerid)
            self.enterBusinessUnit(businessunit)
            self.enterUserName(username)
            self.enterPassword(password)
            self.selectRegion(region, self.signInSelectRegion)
            self.clickSignInButton()
            self.verifyLoginStatus()
