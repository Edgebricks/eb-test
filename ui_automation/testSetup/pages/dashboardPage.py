import pytest
import logging

from ui_automation.framework.base.basePage import BasePage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
import ui_automation.framework.utilities.customLogger as cl


class DashboardPage(BasePage):
    """
    Class contains all the web elements needed for testing a Dashboard
    """

    log = cl.customLogger(logging.DEBUG)
    retry  = 0
    def __init__(self,driver):
        super().__init__(driver)
        self.driver=driver
        self.np = NavigationPage(driver)

    # locators

    pulseViewDetails            = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[1]/div[1]/a'
    regionElementInSummary      = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div[1]/div'
    dashboardTab                = '/html/body/div[1]/nav/ul/li[1]'
    showTop5                    = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[2]'
    top5CriticalEvents          = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/div'
    planningViewDetails         = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[1]/div[1]/a'
    rawStorageLocator           = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div/div[3]/div[5]/span[1]'
    viewDetailsInShowTop5       = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[1]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/div/div/a'
    planningStorage             = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/div[1]/a'
    # green circle keeps on spinning if data failed to load inside planning box
    planningSpinner             = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[1]/div[2]/div[2]/loader/div'
    utilizationRegionID         = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[2]/div[2]/div/div[2]/div/div[1]/div[2]/a'
    cpuUtilLocator              = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[2]/div[1]/ul/li[1]'
    memUtilLocator              = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[2]/div[1]/ul/li[2]'
    memAllocationLocator        = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[2]/div[2]/div[1]/ul/li[3]'
    planningOverView            = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div/div[1]'
    monitoringViewDetails       = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[3]/div/div[1]/a'
    monitoringNoOfTabs          = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div[1]/ul/li'
    inventoryAZlocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[1]/div[2]/a'
    inventoryHostsLocator       = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[2]/div[2]/a'
    inventoryRawStorageLocator  = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]/a'
    inventoryGPUlocator         = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/a'
    inventoryCPUlocator         = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/div[2]/a'
    inventoryMemoryLocator      = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/div[2]/a'
    inventoryBUlocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/a'
    inventoryProjectLocator     = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/a'
    inventoryVMlocator          = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[2]/div[3]/div[2]/a'
    inventoryAllocatedStrglocator = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/a'
    inventoryVmAllVCPULocator   = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]/div[2]/a'
    inventoryVmAllMemLocator    = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[3]/div[3]/div[2]/a'
    inventoryTotalAllMemLocator = '/html/body/div[1]/div[1]/div[5]/div/div/div/div/div[1]/div[2]/div[2]/div[2]/div[4]/div/div[2]/a'
    # click raw storage in inventory, look for text Storage heading Text element
    storageTextElement          = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div/div[1]/div[1]'
    # click BU in inventory, look for text Business Units text element
    buTextLocator               = '/html/body/div[1]/div[1]/div[5]/div/div/div/div[1]/div[1]'
    azElementLocator            = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div[1]/div[2]/div[1]'
    totalStorageLocator         = '/html/body/div[3]/div[1]/div[5]/div/div[2]/div/div/div[2]/storage-pools-info/div/div[1]/div[2]/div/div/div/span'
    gpuLocator                  = '/html/body/div[1]/div[1]/div[5]/div/div/div[2]/div[2]/div/div[1]'
    syncProjectsLocator         = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[1]/div[1]/div'
    # Create AZ elementText
    createAZLocator             = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div/div[1]/div[2]/button'
    syncVMsLocator              = '/html/body/div[1]/div[1]/div[5]/div/div/div[3]/div/div/div[2]/div[1]/div[1]/div'
    allStorageLocator           = '/html/body/div[1]/div[1]/div[5]/div/div[2]/div/div/div[2]/storage-pools-info/div/div[2]/div[2]/div/div/div/span'

    def clickPulseShowTop5Button(self):
        self.waitForElement(self.showTop5,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.showTop5 , locatorType="xpath")

    def clickPulseHideButton(self):
        self.waitForElement(self.showTop5,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.showTop5 , locatorType="xpath")

    def clickPulseViewDetails(self):

        self.waitForElement(self.pulseViewDetails,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.pulseViewDetails , locatorType="xpath")

    def clickPlanningViewDetails(self):

        self.waitForElement(self.planningViewDetails,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.planningViewDetails , locatorType="xpath")


    def clickPlanningStorage(self):
        self.waitForElement(self.planningStorage,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.planningStorage , locatorType="xpath")

    def clickPlanningCPUutil(self):
        self.waitForElement(self.cpuUtilLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.cpuUtilLocator , locatorType="xpath")

    def clickPlanningMemutil(self):
        self.waitForElement(self.memUtilLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.memUtilLocator , locatorType="xpath")

    def clickPlanningMemAllocation(self):
        self.waitForElement(self.memAllocationLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.memAllocationLocator , locatorType="xpath")

    def navigateToDashboard(self):
        self.waitForElement(self.dashboardTab,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.dashboardTab , locatorType="xpath")

    def clickMonitoringViewDetails(self):

        self.waitForElement(self.monitoringViewDetails,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.monitoringViewDetails , locatorType="xpath")

    def clickOnInventoryAZs(self):
        element = self.waitForElement(self.inventoryAZlocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryAZlocator , locatorType="xpath")


    def clickOnInventoryHosts(self):
        element = self.waitForElement(self.inventoryHostsLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryHostsLocator , locatorType="xpath")

    def clickOnInventoryRawStorage(self):
        element = self.waitForElement(self.storageTextElement,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryRawStorageLocator , locatorType="xpath")

    def clickOnInventoryGPU(self):
        element = self.waitForElement(self.inventoryGPUlocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryGPUlocator, locatorType="xpath")

    def clickOnInventoryCPU(self):
        element = self.waitForElement(self.inventoryCPUlocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryCPUlocator, locatorType="xpath")

    def clickOnInventoryMemory(self):
        element = self.waitForElement(self.inventoryMemoryLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryMemoryLocator, locatorType="xpath")

    def clickOnInventoryBU(self):
        element = self.waitForElement(self.inventoryBUlocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryBUlocator, locatorType="xpath")

    def clickOnInventoryProject(self):
        element = self.waitForElement(self.inventoryProjectLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryProjectLocator, locatorType="xpath")

    def clickOnInventoryVM(self):
        element = self.waitForElement(self.inventoryVMlocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryVMlocator, locatorType="xpath")

    def clickOnInventoryAllStorage(self):
        element = self.waitForElement(self.inventoryAllocatedStrglocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryAllocatedStrglocator, locatorType="xpath")

    def clickOnInventoryVmAllVCPUs(self):
        element = self.waitForElement(self.inventoryVmAllVCPULocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryVmAllVCPULocator, locatorType="xpath")

    def clickOnInventoryVmAllMem(self):
        element = self.waitForElement(self.inventoryVmAllMemLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryVmAllMemLocator, locatorType="xpath")

    def clickOnInventoryTotalAllMem(self):
        element = self.waitForElement(self.inventoryTotalAllMemLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        self.elementClick(self.inventoryTotalAllMemLocator, locatorType="xpath")

    def checkPlanningBoxMetricsLoaded(self):
        elementPresent = self.isElementPresent(self.planningSpinner,
                            locatorType="xpath")
        # if metrics in planning box not loaded and you can a spinner spinning then elementPresent == True
        if elementPresent == False:
            self.log.info("PLANNING -> METRICS(BAR GRAPH) ARE LOADED IN PLANNING BOX")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("PLANNING -> METRICS(BAR GRAPH) ARE NOT LOADED IN PLANNING BOX")
            self.navigateToDashboard()
            return False

    def verifyClickPulseViewDetails(self):

        verifyElement = self.isElementPresent(self.regionElementInSummary,
                            locatorType="xpath")
        if verifyElement == True:
            self.log.info("PULSE -> CLICK VIEW DETAILS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PULSE -> CLICK VIEW DETAILS")
            self.navigateToDashboard()
            return False

    def verifyClickPulseShowTop5button(self):
        element = self.waitForElement(self.viewDetailsInShowTop5,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        verifyElement = self.isElementPresent(self.viewDetailsInShowTop5,
                         locatorType="xpath")
        if verifyElement == True:
           self.elementClick(self.viewDetailsInShowTop5, locatorType="xpath")
           self.log.info("PULSE -> CLICK SHOW TOP 5 BUTTON VERIFIED")
           self.navigateToDashboard()
           return True
        else:
           self.log.error("PULSE -> CLICK SHOW TOP 5 BUTTON NOT VERIFIED")
           self.navigateToDashboard()
           return False

    def verifyClickPlanningViewDetails(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("PLANNING -> CLICK VIEW DETAILS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK VIEW DETAILS")
            self.navigateToDashboard()
            return False

    def verifyClickPlanningStorage(self):
        verifyElement = self.isElementPresent(self.storageTextElement,
                            locatorType="xpath")

        if verifyElement == True:
            self.log.info("PLANNING -> CLICK STORAGE WAS VERIFICATION SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK STORAGE")
            self.navigateToDashboard()
            return False

    def verifyCLickPlanningCPUutil(self):

        verifyElement = self.isElementPresent(self.utilizationRegionID,
                            locatorType="xpath")
        if verifyElement == True:
            self.log.info("PLANNING -> CLICK CPU UTILIZATION VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK CPU UTILIZATION")
            self.navigateToDashboard()
            return False

    def verifyCLickPlanningMemutil(self):
        verifyElement = self.isElementPresent(self.utilizationRegionID,
                            locatorType="xpath")
        if verifyElement == True:
            self.log.info("PLANNING -> CLICK MEMORY UTILIZATION VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK MEMORY UTILIZATION")
            self.navigateToDashboard()
            return False

    def verifyCLickPlanningMemAllocation(self):
        verifyElement = self.waitForElement(self.utilizationRegionID,
                            locatorType="xpath")
        if verifyElement == True:
            self.log.info("PLANNING -> CLICK MEMORY AllOCATION VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK MEMORY AllOCATION")
            self.navigateToDashboard()
            return False

    def verifyClickMonitoringViewDetails(self, tabCount):

        elements = self.waitForElements(self.monitoringNoOfTabs,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        noOfTabs = len(elements)
        if (int(noOfTabs) == int(tabCount)):
            self.log.info("MONITORING -> CLICK VIEW DETAILS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY MONITORING -> CLICK VIEW DETAILS")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnAZs(self):
        verifyElement = self.isElementPresent(self.createAZLocator,
                         locatorType="xpath")

        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK AZs VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK AZs")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnHosts(self):
        verifyElement = self.isElementPresent(self.azElementLocator,
                            locatorType="xpath")
        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK HOSTS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK HOSTS")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnRawStorage(self):
        verifyElement = self.isElementPresent(self.storageTextElement,
                         locatorType="xpath")
        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK RAW STORAGE VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK RAW STORAGE")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnGPU(self):
        element = self.waitForElement(self.gpuLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        verifyElement = self.isElementPresent(self.gpuLocator,
                         locatorType="xpath")
        if verifyElement == True:
           self.log.info("INVENTORY -> CLICK GPU VERIFIED")
           self.navigateToDashboard()
           return True
        else:
           self.log.error("PULSE -> CLICK GPU NOT VERIFIED")
           self.navigateToDashboard()
           return False

    def verifyClickInventoryOnCPU(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("PLANNING -> CLICK VIEW DETAILS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK VIEW DETAILS")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnMemory(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("PLANNING -> CLICK VIEW DETAILS VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK VIEW DETAILS")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnBU(self, text_):
        element = self.waitForElement(self.buTextLocator,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        text = element.text.strip()
        if (text == text_):
            self.log.info("INVENTORY -> CLICK BU VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK BU")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnProject(self):
        verifyElement = self.isElementPresent(self.syncProjectsLocator,
                            locatorType="xpath")
        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK PROJECT VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK PROJECT")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnVM(self):
        verifyElement = self.isElementPresent(self.syncVMsLocator,
                            locatorType="xpath")
        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK VM VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK VM")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnAllStorage(self):
        verifyElement = self.isElementPresent(self.storageTextElement,
                            locatorType="xpath")
        if (verifyElement == True):
            self.log.info("INVENTORY -> CLICK ALLOCATED STORAGE VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY INVENTORY -> CLICK ALLOCATED STORAGE")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnVmAllVCPUS(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("INVENTORY -> CLICK VM ALLOCATED VCPU VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK VM ALLOCATED VCPU")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnVmAllMem(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("INVENTORY -> CLICK VM ALLOCATED MEMORY VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK VM ALLOCATED MEMORY")
            self.navigateToDashboard()
            return False

    def verifyClickInventoryOnTotalAllMem(self, text_):

        element = self.waitForElement(self.planningOverView,
                            locatorType="xpath",timeout=120, pollFrequency=0.2)
        overview = element.text
        if (overview == text_):
            self.log.info("INVENTORY -> CLICK TOTAL ALLOCATED MEMORY VERIFICATION WAS SUCCESSFUL")
            self.navigateToDashboard()
            return True
        else:
            self.log.error("FAILED TO VERIFY PLANNING -> CLICK TOTAL ALLOCATED MEMORY")
            self.navigateToDashboard()
            return False
