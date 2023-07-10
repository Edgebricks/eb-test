#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import logging

from framework.base.basePage import BasePage
import framework.utilities.customLogger as cl


class BUSummaryPage(BasePage):
    """
    Class contains the links which can be used for navigating to
    BU summary
    BU Projects
    BU Configuration
    """

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    summaryLink = "//li[contains(@ui-sref,'app.BU.details.summary')]"
    projectsLink = "//li[contains(@ui-sref,'app.BU.details.projects')]"
    configurationLink = "//li[contains(@ui-sref,'app.BU.details.configuration')]"

    def navigateToSummary(self):
        self.waitForElement(
            self.summaryLink, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(locator=self.summaryLink, locatorType="xpath")

    def navigateToProjects(self):
        self.waitForElement(
            self.projectsLink, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(locator=self.projectsLink, locatorType="xpath")

    def navigateToConfiguration(self):
        self.waitForElement(
            self.configurationLink, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(locator=self.configurationLink, locatorType="xpath")
