#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import pytest
import unittest2 as unittest

from testSetup.dataSource.login import Login
from framework.utilities.teststatus import TestStatus
from testSetup.pages.loginPage import LoginPage


@pytest.mark.usefixtures("oneTimeSetUp")
class LoginTest(unittest.TestCase):
    @pytest.fixture()
    def objectSetUp(self, oneTimeSetUp):
        self.lp = LoginPage(self.driver)
        self.ts = TestStatus(self.driver)
        self.loginConfig = Login()
        self.customerid = self.loginConfig.customerID
        self.businessunit = self.loginConfig.businessUnit
        self.username = self.loginConfig.userName
        self.password = self.loginConfig.password

    @pytest.mark.usefixtures("objectSetUp")
    def test_login(self):
        self.lp.logout()
        result1 = self.lp.verifyLoginTitle()
        self.ts.mark(result1, "Title Verification")
        if not result1:
            self.driver.quit()
        self.lp.signinAfterLogout(
            self.customerid, self.businessunit, self.username, self.password
        )
        result2 = self.lp.verifyLoginStatus()
        self.ts.markFinal("test_login", result2, "Login Verification")
        if not result2:
            self.driver.quit()
