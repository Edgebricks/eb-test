import pytest
import logging

from ui_automation.framework.base.basePage import BasePage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
import ui_automation.framework.utilities.customLogger as cl


class InventoryPage(BasePage):
    """
    Class contains all the web elements needed for testing a Inventory Page
    """

    log = cl.customLogger(logging.DEBUG)
    retry  = 0
    def __init__(self,driver):
        super().__init__(driver)
        self.driver=driver
        self.np = NavigationPage(driver)

    # locators
    inventoryTabLocator = '/html/body/div[1]/nav/ul/li[4]'
    activityDateLocator = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[1]/div[2]/ul/li[1]'
    vmTabLocator        = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[2]'
    syncVMsLocator      = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[1]/div[1]/div'
    syncVmPopUpElement  = '/html/body/div[1]/div[1]/div[4]/div[2]/div/div/div[4]'
    projectsTabLocator  = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[1]'

    def clickInventory(self):
        self.waitForElement(self.inventoryTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryTabLocator , locatorType="xpath")

    def clickOnVMs(self):
        self.waitForElement(self.vmTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.vmTabLocator , locatorType="xpath")

    def clickOnSyncVMs(self):
        self.waitForElement(self.syncVMsLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.syncVMsLocator , locatorType="xpath")


    def clickOnProjectsTab(self):
        self.waitForElement(self.projectsTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.projectsTabLocator , locatorType="xpath")

    def verifyClickInventory(self):
        verifyElement = self.isElementPresent(self.activityDateLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON INVENTORY TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON INVENTORY TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False

    def verifyClickOnVMs(self):
        verifyElement = self.isElementPresent(self.activityDateLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON VMs TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON VMs TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False

    def verifyClickOnSyncVMs(self):
        verifyElement = self.isElementPresent(self.syncVmPopUpElement,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON SYNC VMs VERIFIED - POP UP PRESENT")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON SYNC VMs VERIFIED NOT VERIFIED - POP UP NOT PRESENT")
           self.clickInventory()
           return False

    def verifyClickOnProjctsTab(self):
        verifyElement = self.isElementPresent(self.activityDateLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON PROJECTS TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON PROJECTS TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False
