#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import pytest
import logging

from framework.base.basePage import BasePage
from testSetup.pages.navigationPage import NavigationPage
import framework.utilities.customLogger as cl


class LoginPage(BasePage):
    """
      Class contains all the elements present on th login page
      """

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver
        self.np = NavigationPage(driver)

    # locators
    customerID = "Customer_Id"
    businessUnit = "Business_Unit"
    userName = "User_Name"
    password = "Password"
    signIn = "//button/span[text()='Sign in']"
    errorPrompt = "//div[@class='alert alert-danger ng-binding ng-scope']"
    loginPageTitle = "Console Login"
    regionSelector = "regionSelector"
    signoutButton = "//button[text()='Sign out from all profiles']"
    removeProfileIcon = "//a[@class='removeProfileIcon']"
    yesForRemoveProfile = "//button[text()='Yes']"

    def verifyLoginTitle(self):
        status = self.verifyPageTitle(self.loginPageTitle)
        return status

    def enterCustomerID(self, customerid):
        self.sendKeys(customerid, self.customerID)

    def enterBusinessUnit(self, businessunit):
        self.sendKeys(businessunit, self.businessUnit)

    def enterUserName(self, username):
        self.sendKeys(username, self.userName)

    def enterPassword(self, password):
        self.sendKeys(password, self.password)

    def clickSignInButton(self):
        self.waitForElement(
            self.signIn, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.signIn, locatorType="xpath")

    def clickRemoveProfileIcon(self):
        self.waitForElement(
            self.removeProfileIcon, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.removeProfileIcon, locatorType="xpath")

    def clickYesForRemoveProfile(self):
        self.waitForElement(
            self.yesForRemoveProfile,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.yesForRemoveProfile, locatorType="xpath")

    def verifyLoginStatus(self):
        self.waitForElement(
            self.regionSelector, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        verifyElement = self.isElementPresent(self.regionSelector)
        if verifyElement:
            return True
        else:
            element = self.getElement(self.errorPrompt, locatorType="xpath")
            errormssg = element.text
            self.log.error(errormssg)
            return False
            self.driver.quit()

    def verifyCustomerID(self):
        self.waitForElement(
            self.customerID, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        verifyElement = self.isElementPresent(self.customerID)
        if verify_element:
            return True
        else:
            return False

    def logout(self):
        self.np.navigateToRegionSelector()
        self.waitForElement(
            self.signoutButton, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.signoutButton, locatorType="xpath")
        self.clickRemoveProfileIcon()
        self.clickYesForRemoveProfile()

    def signinAfterLogout(
        self, customerid="", businessunit="", username="", password=""
    ):

        self.enterBusinessUnit(businessunit)
        self.enterUserName(username)
        self.enterPassword(password)
        self.clickSignInButton()
        self.verifyLoginStatus()

    def login(self, customerid="", businessunit="", username="", password=""):
        self.enterCustomerID(customerid)
        self.enterBusinessUnit(businessunit)
        self.enterUserName(username)
        self.enterPassword(password)
        self.clickSignInButton()
        self.verifyLoginStatus()
