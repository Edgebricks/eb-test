# Author: sweta@edgebricks.com
# (c) 2018 ZeroStack
import pytest
import unittest2 as unittest
import time

from ui_automation.testSetup.pages.loginPage import LoginPage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
from ui_automation.framework.utilities.teststatus import TestStatus
from ui_automation.framework.utilities.util import  Util
from ui_automation.testSetup.pages.dashboardPage import DashboardPage
from ui_automation.testSetup.dataSource.dashboardTemplate import DashboardTemplate

@pytest.mark.usefixtures("oneTimeSetUp")

class Dashboard(unittest.TestCase):
    @pytest.fixture()
    def objectSetUp(self,oneTimeSetUp):
        self.dp   = DashboardPage(self.driver)
        self.ts   = TestStatus(self.driver)
        self.util = Util()
        self.dashboardConfig = DashboardTemplate()
        self.text            = self.dashboardConfig.top5CriticalEventText
        self.overViewText    = self.dashboardConfig.overViewText
        self.buText          = self.dashboardConfig.buText
        self.noOfTabs        = self.dashboardConfig.tabsInMonitoring

    @pytest.mark.usefixtures("objectSetUp")
    def test_pulse(self):
        self.dp.clickPulseViewDetails()
        result = self.dp.verifyClickPulseViewDetails()
        #self.ts.mark(result , "PULSE CLICK VIEW DETAILS VERIFICATION")

        #self.dp.clickPulseShowTop5Button()
        #result1 = self.dp.verifyClickPulseShowTop5button()
        self.ts.mark(result , "PULSE CLICK VIEW DETAILS VERIFICATION")
        #self.ts.markFinal("test_Dashboard_Pulse", result, "PULSE CLICK ON VIEW DETAILS")
        #self.dp.clickPulseHideButton()


    @pytest.mark.usefixtures("objectSetUp")
    def test_planning(self):
        self.dp.clickPlanningViewDetails()
        # since its taking time to load planning page, and we are getting raw storage value wrong
        time.sleep(2)
        result = self.dp.verifyClickPlanningViewDetails(self.overViewText)
        self.ts.mark(result , "PLANNING CLICK VIEW DETAILS VERIFICATION")

        self.dp.clickPlanningStorage()
        result1 = self.dp.verifyClickPlanningStorage()
        self.ts.mark(result1 , "PLANNING STORAGE VERIFICATION")

        self.dp.clickPlanningCPUutil()
        result2 = self.dp.verifyCLickPlanningCPUutil()
        self.ts.mark(result2 , "PLANNING CPU UTILIZATION VERIFICATION")

        self.dp.clickPlanningMemutil()
        result3 = self.dp.verifyCLickPlanningMemutil()
        self.ts.mark(result3 , "PLANNING MEMORY UTILIZATION VERIFICATION")

        self.dp.clickPlanningMemAllocation()
        result4 = self.dp.verifyCLickPlanningMemAllocation()
        self.ts.mark(result4 , "PLANNING MEMORY AllOCATION VERIFICATION")
        #self.ts.markFinal("test_Dashboard_Planning", result4, "PLANNING CLICK ON MEM ALLOCATION")

        result5 = self.dp.checkPlanningBoxMetricsLoaded()
        self.ts.mark(result5 , "PLANNING METRICS(BAR GRAPH) ARE LOADED")

    @pytest.mark.usefixtures("objectSetUp")
    def test_monitoring(self):
        self.dp.clickMonitoringViewDetails()
        result5 = self.dp.verifyClickMonitoringViewDetails(self.noOfTabs)
        self.ts.mark(result5 , "MONITORING CLICK VIEW DETAILS VERIFICATION")
        #self.ts.markFinal("test_Dashboard_Monitoring", result5, "MONITORING VIEW DETAILS VERIFICATION")
        #self.util.sleep(10, "SESSION TO ABORT")

    @pytest.mark.usefixtures("objectSetUp")
    def test_inventory(self):
        self.dp.clickOnInventoryAZs()
        result6 = self.dp.verifyClickInventoryOnAZs()
        self.ts.mark(result6 , "INVENTORY CLICK AZs VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryHosts()
        result7 = self.dp.verifyClickInventoryOnHosts()
        self.ts.mark(result7 , "INVENTORY CLICK HOSTS VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryRawStorage()
        result8 = self.dp.verifyClickInventoryOnRawStorage()
        self.ts.mark(result8 , "INVENTORY CLICK RAW STORAGE VERIFICATION")

        # This feature has been removed
        #time.sleep(2)
        #self.dp.clickOnInventoryGPU()
        #result9 = self.dp.verifyClickInventoryOnGPU()
        #self.ts.mark(result9 , "INVENTORY CLICK GPU VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryCPU()
        result10 = self.dp.verifyClickInventoryOnCPU(self.overViewText)
        self.ts.mark(result10 , "INVENTORY CLICK CPU VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryMemory()
        result11 = self.dp.verifyClickInventoryOnMemory(self.overViewText)
        self.ts.mark(result11 , "INVENTORY CLICK MEMORY VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryBU()
        result12 = self.dp.verifyClickInventoryOnBU(self.buText)
        self.ts.mark(result12 , "INVENTORY CLICK BU VERIFICATION")


        time.sleep(2)
        self.dp.clickOnInventoryProject()
        result13 = self.dp.verifyClickInventoryOnProject()
        self.ts.mark(result13 , "INVENTORY CLICK PROJECT VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryVM()
        result14 = self.dp.verifyClickInventoryOnVM()
        self.ts.mark(result14 , "INVENTORY CLICK VM VERIFICATION")

        # Allocated Storage
        time.sleep(2)
        self.dp.clickOnInventoryAllStorage()
        result15 = self.dp.verifyClickInventoryOnAllStorage()
        self.ts.mark(result15 , "INVENTORY CLICK ALLOCATED STORAGE VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryVmAllVCPUs()
        result16 = self.dp.verifyClickInventoryOnVmAllVCPUS(self.overViewText)
        self.ts.mark(result16 , "INVENTORY CLICK VM ALLOCATED VCPU VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryVmAllMem()
        result17 = self.dp.verifyClickInventoryOnVmAllMem(self.overViewText)
        self.ts.mark(result17 , "INVENTORY CLICK VM ALLOCATED MEMORY VERIFICATION")

        time.sleep(2)
        self.dp.clickOnInventoryTotalAllMem()
        result18 = self.dp.verifyClickInventoryOnTotalAllMem(self.overViewText)
        #self.ts.mark(result18 , "INVENTORY CLICK TOTAL ALLOCATED MEMORY VERIFICATION")


        self.ts.markFinal("test_Dashboard_Inventory", result18, "INVENTORY CLICK ON TOTAL ALLOCATED MEMORY VERIFICATION")

        self.util.sleep(10, "SESSION TO ABORT")
