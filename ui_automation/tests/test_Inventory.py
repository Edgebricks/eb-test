# Author: sweta@edgebricks.com
# (c) 2018 ZeroStack
import pytest
import unittest2 as unittest
import time

from ui_automation.testSetup.pages.loginPage import LoginPage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
from ui_automation.framework.utilities.teststatus import TestStatus
from ui_automation.framework.utilities.util import  Util
from ui_automation.testSetup.pages.inventoryPage import InventoryPage
from ui_automation.testSetup.dataSource.inventoryTemplate import InventoryTemplate

@pytest.mark.usefixtures("oneTimeSetUp")

class Inventory(unittest.TestCase):
    @pytest.fixture()
    def objectSetUp(self,oneTimeSetUp):
        self.ip   = InventoryPage(self.driver)
        self.ts   = TestStatus(self.driver)
        self.util = Util()

    @pytest.mark.usefixtures("objectSetUp")
    def test_inventory(self):
        self.ip.clickInventory()
        result1 = self.ip.verifyClickInventory()
        self.ts.mark(result1 , "INVENTORY - CLICK ON INVENTORY TAB VERIFICATION")

        self.ip.clickOnVMs()
        result2 = self.ip.verifyClickOnVMs()
        self.ts.mark(result2 , "INVENTORY - CLICK ON VMs TAB VERIFICATION")

        self.ip.clickOnSyncVMs()
        result3 = self.ip.verifyClickOnSyncVMs()
        self.ts.mark(result3 , "INVENTORY - VMs - CLICK ON SYNC VMs VERIFICATION")

        self.ip.clickOnProjectsTab()
        result4 = self.ip.verifyClickOnProjctsTab()
        self.ts.mark(result4 , "INVENTORY - PROJECTS TAB - CLICK ON PROJECTS TAB VERIFICATION")

        self.ts.markFinal("test_Inventory", result4 , "INVENTORY - PROJECTS - CLICK ON PROJECTS TAB VERIFICATION")
