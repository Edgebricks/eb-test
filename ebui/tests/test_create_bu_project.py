#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import pytest

from ebui.testSetup.pages.buPage import BUPage
from ebui.testSetup.pages.buSummaryPage import BUSummaryPage
from ebui.testSetup.pages.projectsPage import ProjectsPage
from ebui.testSetup.pages.navigationPage import NavigationPage
from ebui.framework.utilities.teststatus import TestStatus
from ebui.framework.utilities.util import Util
from ebui.testSetup.dataSource.buQuota import BUquota
from ebui.testSetup.dataSource.projectTemplate import ProjectTemplate


@pytest.mark.usefixtures("oneTimeSetUp")
class CreateBUProject:
    @pytest.fixture()
    def __init__(self, driver):
        self.bu = BUPage(driver)
        self.ts = TestStatus(driver)
        self.buSummary = BUSummaryPage(driver)
        self.projects = ProjectsPage(driver)
        self.np = NavigationPage(driver)
        self.util = Util()

        self.buConfig = BUquota()
        self.businessUnitName = self.buConfig.buName
        self.username = self.buConfig.username
        self.email = self.buConfig.email
        self.password = self.buConfig.password
        self.confirmpassword = self.buConfig.confirmpassword

        self.projectConfig = ProjectTemplate()
        self.projectName = self.projectConfig.projectName
        self.projectTemplate = self.projectConfig.projectTemplate
        self.cidr = self.projectConfig.cidr

    @pytest.mark.usefixtures("__init__")
    def test_create_bu_project(self):
        self.bu.createLocalBuWithNoQuota(
            self.businessUnitName,
            self.username,
            self.email,
            self.password,
            self.confirmpassword,
        )

        result = self.bu.verifyBUCreated(self.businessUnitName)
        self.ts.mark(result, "BU CREATION VERIFICATION")
        self.buSummary.navigateToProjects()
        self.projects.createProject(self.projectName, self.projectTemplate, self.cidr)

        result = self.projects.verifyProjectCreated(self.projectName)
        self.ts.markFinal(
            "test_create_bu_project", result, "PROJECT CREATION VERIFICATION"
        )

        self.util.sleep(10, "SESSION TO ABORT")

    @pytest.mark.usefixtures("__init__")
    def test_delete_bu_project(self):
        assert True
