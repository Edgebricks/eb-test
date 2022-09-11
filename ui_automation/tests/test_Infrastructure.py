# Author: sweta@edgebricks.com
# (c) 2018 ZeroStack
import pytest
import unittest2 as unittest
import time

from ui_automation.testSetup.pages.loginPage import LoginPage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
from ui_automation.framework.utilities.teststatus import TestStatus
from ui_automation.framework.utilities.util import  Util
from ui_automation.testSetup.pages.infrastructurePage import InfrastructurePage
from ui_automation.testSetup.dataSource.infrastructureTemplate import InfrastructureTemplate

@pytest.mark.usefixtures("oneTimeSetUp")

class Infrastructure(unittest.TestCase):
    @pytest.fixture()
    def objectSetUp(self,oneTimeSetUp):
        self.ip   = InfrastructurePage(self.driver)
        self.ts   = TestStatus(self.driver)
        self.util = Util()

        self.infraConfig         = InfrastructureTemplate()
        self.discoveredHostsText = self.infraConfig.discoveredHosts
        self.costAnalysisText    = self.infraConfig.costAnalysis

    @pytest.mark.usefixtures("objectSetUp")
    def test_infrastructure(self):
        self.ip.clickInfrastructure()
        result1 = self.ip.verifyClickInfrastructure()
        self.ts.mark(result1 , "INFRASTRUCTURE - CLICK INFRASTRUCTURE TAB VERIFICATION")

        self.ip.clickUnConfiguredHosts()
        result2 = self.ip.verifyClickUnConfiguredHosts(self.discoveredHostsText)
        self.ts.mark(result2 , "INFRASTRUCTURE - CLICK UN CONFIGURED HOSTS TAB VERIFICATION")

        self.ip.clickRegionsViewDetails()
        result3 = self.ip.verifyClickRegionsViewDetails()
        self.ts.mark(result3 , "INFRASTRUCTURE - REGIONS - CLICK VIEW DETAILS VERIFICATION")

        self.ip.clickRegionsCostDetails()
        result4 = self.ip.verifyClickRegionsCostDetails(self.costAnalysisText)
        #self.ts.mark(result4 , "INFRASTRUCTURE - REGIONS - CLICK COST DETAILS VERIFICATION")

        self.ts.markFinal("test_Infrastructure", result4 , "INFRASTRUCTURE - REGIONS - CLICK COST DETAILS VERIFICATION")
