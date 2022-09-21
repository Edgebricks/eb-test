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
    inventoryTabLocator         = '/html/body/div[1]/nav/ul/li[4]'
    activityDateLocator         = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[1]/div[2]/ul/li[1]'
    vmTabLocator                = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[2]'
    # xpath for Sync VMs tab and Sync Projects Tab is same
    syncVMs_or_PrjLocator       = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[1]/div[1]/div'
    # xpath for the pop up element is same - Sync VMs or Sync Projects
    syncVMs_or_PrjPopUpElement  = '/html/body/div[1]/div[1]/div[4]/div[2]/div/div/div[4]'
    projectsTabLocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[1]'
    imagesTabLocator            = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[3]'
    # After clicking on Images tab, look for 'Active' Text on UI for verification
    activeTextLocator           = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div[3]/div[2]/div[3]/span[2]'
    volumesTabLocator           = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[4]'
    #volumesTabLocator           = 'Volumes'
    # After clicking on Images tab, look for 'Available' Text on UI for verification
    availableTextLocator        = '/html/body/div[3]/div[1]/div[5]/div/div/div[3]/div/div[1]/div[2]/div[1]/div[3]/span[2]'
    networksTabLocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/ul/li[5]'
    # After clicking on Images tab, look for 'Public' Text on UI for verification
    publicTextLocator           = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[2]/div[4]/span[2]'
    internalNetworksTabLocator  = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[1]/ul/li[2]'
    privateTextLocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[2]/div[5]/span[2]'


    def clickInventory(self):
        self.waitForElement(self.inventoryTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryTabLocator , locatorType="xpath")

    def clickOnVMs(self):
        self.waitForElement(self.vmTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.vmTabLocator , locatorType="xpath")

    def clickOnSyncVMs(self):
        self.waitForElement(self.syncVMs_or_PrjLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.syncVMs_or_PrjLocator , locatorType="xpath")


    def clickOnProjectsTab(self):
        self.waitForElement(self.projectsTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.projectsTabLocator , locatorType="xpath")


    def clickOnSyncProjects(self):
        self.waitForElement(self.syncVMs_or_PrjLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.syncVMs_or_PrjLocator , locatorType="xpath")

    def clickOnImagesTab(self):
        self.waitForElement(self.imagesTabLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.imagesTabLocator , locatorType="xpath")

    def clickOnVolumesTab(self):
        self.waitForElement(self.volumesTabLocator,
                            locatorType="xpath",timeout=200, pollFrequency=0.2)
        self.elementClick(self.volumesTabLocator , locatorType="xpath")


    def clickOnNetworksTab(self):
        self.waitForElement(self.networksTabLocator,
                            locatorType="xpath",timeout=200, pollFrequency=0.2)
        self.elementClick(self.networksTabLocator , locatorType="xpath")

    def clickOnInternalNetworksTab(self):
        self.clickOnNetworksTab()
        self.waitForElement(self.internalNetworksTabLocator,
                            locatorType="xpath",timeout=200, pollFrequency=0.2)
        self.elementClick(self.internalNetworksTabLocator , locatorType="xpath")

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
        verifyElement = self.isElementPresent(self.syncVMs_or_PrjPopUpElement,
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

    def verifyClickOnSyncProjects(self):
        verifyElement = self.isElementPresent(self.syncVMs_or_PrjPopUpElement,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON SYNC PROJECTS VERIFIED - POP UP PRESENT")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON SYNC PROJECTS VERIFIED NOT VERIFIED - POP UP NOT PRESENT")
           self.clickInventory()
           return False

    def verifyClickOnImagesTab(self):
        verifyElement = self.isElementPresent(self.activeTextLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON IMAGES TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON IMAGES TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False

    def verifyClickOnVolumesTab(self):
        verifyElement = self.isElementPresent(self.availableTextLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON VOLUMES TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON VOLUMES TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False

    def verifyClickOnNetworksTab(self):
        verifyElement = self.isElementPresent(self.publicTextLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON NETWORKS TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON NETWORKS TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False

    def verifyClickOnInternalNetworksTab(self):
        verifyElement = self.isElementPresent(self.privateTextLocator,
                         locatorType="xpath")

        if verifyElement == True:
           self.log.info("INVENTORY - CLICK ON INTERNAL NETWORKS TAB VERIFIED")
           self.clickInventory()
           return True
        else:
           self.log.error("INVENTORY - CLICK ON INTERNAL NETWORKS TAB VERIFIED NOT VERIFIED")
           self.clickInventory()
           return False
