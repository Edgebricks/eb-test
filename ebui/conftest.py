#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


""""
Implements running oneTimeSetup for Sigining In before start of
every test module and to quit from the browser after test module
is done executing.
"""

import logging
import pytest

from ebui.testSetup.dataSource.login import Login
from ebui.testSetup.pages.loginPage import LoginPage
from ebui.framework.base.webdriver import WebDriver
import ebui.framework.utilities.customLogger as cl

loginConfig = Login()
customerid = loginConfig.customerID
businessunit = loginConfig.businessUnit
username = loginConfig.userName
password = loginConfig.password


@pytest.yield_fixture(scope="class")
def oneTimeSetUp(request, browser): # pylint: disable=redefined-outer-name
    log = cl.customLogger(logging.DEBUG)
    log.info("Running one time setUp")
    wdf = WebDriver(browser)
    driver = wdf.getWebDriverInstance()

    lp = LoginPage(driver)
    lp.login(customerid, businessunit, username, password)

    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()
    log.info("Running one time tearDown")


def pytest_addoption(parser):
    parser.addoption("--html")
    parser.addoption("--browser")
    parser.addoption("--osType", help="Type of operating system")


@pytest.fixture(scope="session")
def html(request):
    return request.config.getoption("--html")


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def osType(request):
    return request.config.getoption("--osType")
