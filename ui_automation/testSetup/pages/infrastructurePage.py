import pytest
import logging

from ui_automation.framework.base.basePage import BasePage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
import ui_automation.framework.utilities.customLogger as cl


class InfrastructurePage(BasePage):
    """
    Class contains all the web elements needed for testing a Infrastructure Page
    """

    log = cl.customLogger(logging.DEBUG)
    retry  = 0
    def __init__(self,driver):
        super().__init__(driver)
        self.driver=driver
        self.np = NavigationPage(driver)

    # locators
    infraTabLocator        = '/html/body/div[1]/nav/ul/li[2]'
    # Region element under Regions Tab
    regionLocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div/div[1]/div/div[1]/div[1]'
    unConfiguredHostsTab   = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[2]'
    discoveredHostsLocator = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div[1]/div[1]/div'
    regionsViewDetails     = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div/div[1]/div/div[1]/div[2]/button'
    summaryRegionLocator   = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div[1]/div'
    regionsCostDetails     = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div/div[1]/div/div[2]/div[8]/div[1]/a'
    costAnalysisLocator    = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div[1]/div[1]'

    def clickInfrastructure(self):
        self.waitForElement(self.infraTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.infraTabLocator , locatorType="xpath")

    def clickUnConfiguredHosts(self):
        self.waitForElement(self.unConfiguredHostsTab,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.unConfiguredHostsTab , locatorType="xpath")

    def clickRegionsViewDetails(self):
        self.waitForElement(self.regionsViewDetails,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.regionsViewDetails , locatorType="xpath")

    def clickRegionsCostDetails(self):
        self.waitForElement(self.regionsCostDetails,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.regionsCostDetails , locatorType="xpath")

    def verifyClickInfrastructure(self):
        verifyElement = self.isElementPresent(self.regionLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INFRASTRUCTURE - CLICK ON INFRASTRUCTURE TAB VERIFIED")
           return True
        else:
           self.log.error("INFRASTRUCTURE - CLICK ON INFRASTRUCTURE TAB NOT VERIFIED")
           return False

    def verifyClickUnConfiguredHosts(self, text_):
        element = self.waitForElement(self.discoveredHostsLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        elementText = element.text
        if elementText == text_:
            self.log.info("INFRASTRUCTURE - CLICK ON UN CONFIGURED HOSTS TAB VERIFIED")
            self.clickInfrastructure()
            return True
        else:
            self.log.error("INFRASTRUCTURE - CLICK ON UN CONFIGURED HOSTS TAB NOT VERIFIED")
            self.clickInfrastructure()
            return False

    def verifyClickRegionsViewDetails(self):
        verifyElement = self.isElementPresent(self.summaryRegionLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INFRASTRUCTURE - REGIONS - CLICK ON VIEW DETAILS VERIFIED")
           self.clickInfrastructure()
           return True
        else:
           self.log.error("INFRASTRUCTURE - REGIONS - CLICK ON VIEW DETAILS NOT VERIFIED")
           self.clickInfrastructure()
           return False

    def verifyClickRegionsCostDetails(self, text_):
        element = self.waitForElement(self.costAnalysisLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        elementText = element.text
        if elementText == text_:
            self.log.info("IINFRASTRUCTURE - REGIONS - CLICK COST DETAILS VERIFIED")
            self.clickInfrastructure()
            return True
        else:
            self.log.error("INFRASTRUCTURE - REGIONS - CLICK COST DETAILS NOT VERIFIED")
            self.clickInfrastructure()
            return False
