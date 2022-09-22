#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack
import pytest
import unittest2 as unittest

from ui_automation.testSetup.pages.loginPage import LoginPage
from ui_automation.testSetup.pages.buPage import BUPage
from ui_automation.testSetup.pages.buSummaryPage import BUSummaryPage
from ui_automation.testSetup.pages.projectsPage import ProjectsPage
from ui_automation.testSetup.pages.navigationPage import NavigationPage
from ui_automation.framework.utilities.teststatus import TestStatus
from ui_automation.framework.utilities.util import  Util
from ui_automation.testSetup.dataSource.buQuota import BUquota
from ui_automation.testSetup.dataSource.projectTemplate import ProjectTemplate
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
      #self.projects.createProject(self.projectName, self.projectTemplate, self.cidr)
      self.projects.createProject(self.projectName, self.projectTemplate, self.cidr, self.email)

      # there is no such attribute in ProjectsPage
      #self.projects.customizeProject(self.cidr)

      result = self.projects.verifyProjectCreated(self.projectName)
      self.ts.markFinal("test_create_bu_project", result,
                       "PROJECT CREATION VERIFICATION")

      self.util.sleep(10, "SESSION TO ABORT")
