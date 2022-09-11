#! /usr/bin/env python


# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


""""
Implements running oneTimeSetup for Sigining In before start of every test module
and to quit from the browser after  test module is done executing.
"""

import pytest
import logging

from selenium import webdriver
from ui_automation.testSetup.dataSource.login import Login
from ui_automation.testSetup.pages.loginPage import LoginPage
from ui_automation.framework.base.webdriver import WebDriver
import ui_automation.framework.utilities.customLogger as cl

loginConfig = Login()
customerid  =  loginConfig.customerID
businessunit = loginConfig.businessUnit
username = loginConfig.userName
password = loginConfig.password
region   = loginConfig.region

#@pytest.yield_fixture(scope="class")
@pytest.fixture(scope="class")
def oneTimeSetUp(request, browser):
    log = cl.customLogger(logging.DEBUG)
    log.info("Running one time setUp")
    wdf = WebDriver(browser)
    driver = wdf.getWebDriverInstance()

    lp = LoginPage(driver)
    lp.login(customerid,businessunit,username,password, region)

    if request.cls is not None:
       request.cls.driver = driver
    yield driver
    driver.quit()
    log.info("Running one time tearDown")

def pytest_addoption(parser):
    #parser.addoption("--html")
    parser.addoption("--browser")
    #parser.addoption("--osType", help="Type of operating system")

"""
@pytest.fixture(scope="session")
def html(request):
    return request.config.getoption("--html")
"""
@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")
"""
@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")
"""
