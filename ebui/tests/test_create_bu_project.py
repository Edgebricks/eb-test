#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


import pytest
import unittest2 as unittest

from testSetup.pages.loginPage import LoginPage
from testSetup.pages.buPage import BUPage
from testSetup.pages.buSummaryPage import BUSummaryPage
from testSetup.pages.projectsPage import ProjectsPage
from testSetup.pages.navigationPage import NavigationPage
from framework.utilities.teststatus import TestStatus
from framework.utilities.util import  Util
from testSetup.dataSource.buQuota import BUquota
from testSetup.dataSource.projectTemplate import ProjectTemplate

@pytest.mark.usefixtures("oneTimeSetUp")

class CreateBUProject(unittest.TestCase):


  @pytest.fixture()
  def objectSetUp(self,oneTimeSetUp):
      self.bu = BUPage(self.driver)
      self.ts = TestStatus(self.driver)
      self.buSummary = BUSummaryPage(self.driver)
      self.projects = ProjectsPage(self.driver)
      self.np = NavigationPage(self.driver)
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


  @pytest.mark.usefixtures("objectSetUp")
  def test_create_bu_project(self):
      self.bu.createLocalBuWithNoQuota(self.businessUnitName, self.username,
                                       self.email, self.password,
                                       self.confirmpassword)

      result = self.bu.verifyBUCreated(self.businessUnitName)
      self.ts.mark(result , "BU CREATION VERIFICATION")
      self.buSummary.navigateToProjects()
      self.projects.createProject(self.projectName, self.projectTemplate)
      self.projects.customizeProject(self.cidr)

      result = self.projects.verifyProjectCreated(self.projectName)
      self.ts.markFinal("test_create_bu_project", result,
                       "PROJECT CREATION VERIFICATION")

      self.util.sleep(10, "SESSION TO ABORT")
