#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import pytest
import logging

from framework.base.basePage import BasePage
import framework.utilities.customLogger as cl


class NavigationPage(BasePage):
    """
      Class contains methods to navigate to the links common for all the pages
      """

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    dashboardLink = "Dashboard"
    infrastructureLink = "Infrastructure"
    businessUnitLink = "Business Units"
    usersLink = "//li/a/span/i[@class='ico ico-users']"
    appsLink = "//li/a/span/i[@class='ico ico-app-store']"
    costManagementLink = "Cost Management"
    settingsLink = "Settings"
    feedbackLocator = "//div/i[@ng-click='goToFeedbackForm()']"
    zsHelpHandlerIcon = "zsHelpHandler"
    goToCloudServiceIcon = "goToCloudService"
    regionSelectorIcon = "regionSelector"

    def navigateToDashboard(self):
        self.elementClick(locator=self.dashboardLink, locatorType="link")

    def navigateToInfrastructure(self):
        self.elementClick(locator=self.infrastructureLink, locatorType="link")

    def navigateToBusinessUnit(self):
        self.elementClick(locator=self.businessUnitLink, locatorType="link")

    def navigateToUsers(self):
        self.elementClick(locator=self.usersLink, locatorType="xpath")

    def navigateToApps(self):
        self.waitForElement(
            self.appsLink, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(locator=self.appsLink, locatorType="xpath")

    def navigateToCostManagement(self):
        self.elementClick(locator=self.costManagementLink, locatorType="link")

    def navigateToSettings(self):
        self.elementClick(locator=self.settingsLink, locatorType="link")

    def navigateToFeedbackForm(self):
        self.elementClick(locator=self.feedbackLocator, locatorType="xpath")

    def navigateToZSHelpHandler(self):
        self.elementClick(locator=zsHelpHandlerIcon)

    def navigateToCloudServiceIcon(self):
        self.elementClick(locator=goToCloudServiceIcon)

    def navigateToRegionSelector(self):
        self.waitForElement(
            self.regionSelectorIcon, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(locator=self.regionSelectorIcon)
