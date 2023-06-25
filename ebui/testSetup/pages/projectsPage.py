#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


import pytest
import time
import logging

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from framework.base.basePage import BasePage
from testSetup.pages.buPage import BUPage
import framework.utilities.customLogger as cl


class ProjectsPage(BasePage):
    """
  Class contains web elements or links needed for creating Projects
  """

    log = cl.customLogger(logging.DEBUG)

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    # locators
    createProjectLocator = "//button[text()='Create Project']"
    projectNameLocator = "//input[@placeholder='Enter Project Name']"
    createDefaultKeypairLocator = (
        "//span[text()='Create Default Key Pair for this project']"
    )
    projectTemplateDropdown = (
        "//a[@class='chosen-single' or @class = 'chosen-single chosen-default']"
    )
    projectTemplateList = (
        "//ul/li[@class='active-result' or @class='active-result result-selected']"
    )
    projectDurationLocator = "//span[text()='Project has finite duration']"
    cancelButton = "//div[@class='btn btn-default ng-binding' and text()='Cancel']"
    customizeProjectButton = "//button[text()='Customize Project']"
    userRoleDropdown = (
        "//a[@class='chosen-single' or @class = 'chosen-single chosen-default']"
    )
    userRolesList = "//div[@class='chosen-search']/following-sibling::ul/li"
    configureNetworksLocator = "//button[@type='submit' and text()='Next: Networks']"
    skipNetworkCreationLocator = "//span[text()='Skip Network Creation']"
    cidrTextboxLocator = "//input[@placeholder='10.1.1.0/24']"
    configureSecurityLocator = "//button[text()='Next: Project Security']"
    projectDetailsLocator = "//button/span[text()='Next: Project Details']"
    doneButton = "//button[@ng-click='close()' and text()='Done']"
    searchProjectTextboxLocator = "//input[@placeholder='Search Projects']"
    projectLocator = "//div[@class='title ng-binding' and text()= '{}']"

    def clickCreateProject(self):
        self.waitForElement(
            self.createProjectLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.createProjectLocator, locatorType="xpath")

    def enterProjectName(self, projectName):
        self.waitForElement(
            self.projectNameLocator, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.sendKeys(projectName, self.projectNameLocator, locatorType="xpath")

    def selectCreateDefaultKeypair(self):
        self.waitForElement(
            self.createDefaultKeypairLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.createDefaultKeypairLocator, locatorType="xpath")

    def selectProjectTemplate(self, projectTemplate):
        self.elementClick(self.projectTemplateDropdown, locatorType="xpath")
        projectTemplatesList = self.getElements(
            self.projectTemplateList, locatorType="xpath"
        )

        for template in projectTemplatesList:
            if template.text == projectTemplate:
                template.click()

    def selectProjectHasFiniteDuration(self):
        # select the checkbox
        self.waitForElement(
            self.projectDurationLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.projectDurationLocator, locatorType="xpath")

    def clickCancelProject(self):
        self.waitForElement(
            self.cancelButton, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.cancelButton, locatorType="xpath")

    def clickCustomizeProject(self):
        self.waitForElement(
            self.customizeProjectButton,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.customizeProjectButton, locatorType="xpath")

    def selectUserRole(self):
        self.waitForElement(
            self.userRoleDropdown, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.userRoleDropdown, locatorType="xpath")
        rolesList = self.getElements(self.userRolesList, locatorType="xpath")
        for role in rolesList:
            if role.text == "Admin":
                role.click()

    def clickNextConfigureNetworks(self):
        self.waitForElement(
            self.configureNetworksLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.configureNetworksLocator, locatorType="xpath")

    def clickSkipNetworkCreation(self):
        self.waitForElement(
            self.skipNetworkCreationLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.skipNetworkCreationLocator, locatorType="xpath")

    def enterCIDR(self, cidr):
        self.waitForElement(
            self.cidrTextboxLocator, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.sendKeys(cidr, self.cidrTextboxLocator, locatorType="xpath")

    def clickNextConfigureSecurity(self):
        self.waitForElement(
            self.configureSecurityLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.configureSecurityLocator, locatorType="xpath")

    def clickNextProjectDetails(self):
        self.waitForElement(
            self.projectDetailsLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.elementClick(self.projectDetailsLocator, locatorType="xpath")

    def clickDone(self):
        self.waitForElement(
            self.doneButton, locatorType="xpath", timeout=120, pollFrequency=0.2
        )

        self.elementClick(self.doneButton, locatorType="xpath")

    def searchProject(self, projectName):
        # Types the project name to be searched
        self.waitForElement(
            self.searchProjectTextboxLocator,
            locatorType="xpath",
            timeout=120,
            pollFrequency=0.2,
        )

        self.sendKeys(
            projectName, self.searchProjectTextboxLocator, locatorType="xpath"
        )

    def verifyProjectCreated(self, projectName):
        # Check the presence of the project
        self.searchProject(projectName)
        verifyProjectLocator = self.projectLocator.format(projectName)
        verifyElement = self.isElementPresent(verifyProjectLocator, locatorType="xpath")

        if verifyElement:
            self.waitForElement(
                verifyProjectLocator,
                locatorType="xpath",
                timeout=120,
                pollFrequency=0.2,
            )

            self.elementClick(verifyProjectLocator, locatorType="xpath")
            self.log.info("PROJECT CREATION WAS SUCCESSFUL")
            return True
        else:
            self.log.error("FAILED TO VERIFY PROJECT CREATION")
            return False

    def createProject(self, projectName, projectTemplate, cidr):
        self.clickCreateProject()
        self.enterProjectName(projectName)
        self.selectCreateDefaultKeypair()
        self.selectProjectTemplate(projectTemplate)
        self.selectProjectHasFiniteDuration()
        self.clickCreateProject()
        self.clickCustomizeProject()
        self.selectUserRole()
        self.clickNextConfigureNetworks()
        # self.clickSkipNetworkCreation()
        self.enterCIDR(cidr)
        self.clickNextConfigureSecurity()
        self.clickNextProjectDetails()
        self.clickDone()
