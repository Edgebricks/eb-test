#! /usr/bin/env python
#
# Author: Ankit Jain (ankit@edgebricks.com)
# (c) 2022 Edgebricks Inc

import json
import os
import pytest
import requests

from ebapi.common.logger import elog
from ebapi.common import utils as eutil
from ebapi.common.config import ConfigParser
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


@pytest.fixture(scope="session", autouse=True)
def isDefaultTestConfigsSet():
    notset = 0
    testConfig = ConfigParser()
    configs = [
        "apiURL",
        "acctID",
        "clusterID",
        "domainName",
        "projectAdmin",
        "projectAdminPassword",
    ]

    for config in configs:
        if not testConfig.getConfig(config):
            notset = 1
            elog.warning("config:%s not set" % eutil.bcolor(config))

    if notset:
        pytest.skip("default test configs not set")


def getAcctAndClusterID():
    testConfig = ConfigParser()
    apiURL = testConfig.getConfig("apiURL")
    custID = testConfig.getConfig("custID")
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json;charset=UTF-8",
    }

    if not apiURL or not custID:
        elog.error(
            "make sure apiURL:%s and custID:%s is specified"
            % (eutil.bcolor(apiURL), eutil.bcolor(custID))
        )
        return None, None

    url = apiURL + "/v1/account_ops/get_clusters?login_name=" + custID
    rsp = requests.get(url=url, headers=headers, timeout=10)

    if not rsp.ok:
        elog.error("failed to get cluster:%s" % eutil.rcolor(rsp.status_code))
        elog.error(rsp.text)
        return None, None

    data = json.loads(rsp.content)
    acctID = data["clusters"][0]["acct_id"]
    clusterID = data["clusters"][0]["id"]
    return acctID, clusterID


def getReleaseVersion():
    testConfig = ConfigParser()
    apiURL = testConfig.getConfig("apiURL")
    acctID = testConfig.getConfig("acctID")
    clusterID = testConfig.getConfig("clusterID")
    cloudAdmin = testConfig.getConfig("cloudAdmin")
    cloudAdminPass = testConfig.getConfig("cloudAdminPassword")

    if (
        not apiURL
        or not acctID
        or not clusterID
        or not cloudAdmin
        or not cloudAdminPass
    ):
        elog.error(
            "make sure apiURL:%s and acctID:%s clusterID:%s cloudAdmin:%s "
            "cloudAdminPass:%s is specified"
            % (
                eutil.bcolor(apiURL),
                eutil.bcolor(acctID),
                eutil.bcolor(clusterID),
                eutil.bcolor(cloudAdmin),
                eutil.bcolor(cloudAdminPass),
            )
        )
        return None, None

    tokenObj = Token("domain", "admin.local", cloudAdmin, cloudAdminPass)
    token = tokenObj.getToken()
    if not token:
        elog.error("failed to get token")
        return None, None
    elog.info(
        "successfully got token:%s from %s"
        % (eutil.bcolor(token), eutil.gcolor(apiURL))
    )

    url = apiURL + "/v1/accounts/%s/version" % acctID
    client = RestClient(token)
    rsp = client.get(url)
    if not rsp.ok:
        elog.error("failed to get version:%s" % eutil.rcolor(rsp.status_code))
        elog.error(rsp.text)
        return None, None

    data = json.loads(rsp.content)
    skyVersion = data["sky_version"]["sky"]["short"]
    starVersion = data["clusters"][0]["star"]["short"]

    elog.info(
        "star version:%s, sky version:%s"
        % (eutil.bcolor(starVersion), eutil.bcolor(skyVersion))
    )
    return skyVersion, starVersion


def pytest_configure(config):
    """Provide additional environment details to pytest-html report"""
    # add environment details to the pytest-html plugin
    elog.info("reading configuration...")

    config._metadata = {}
    config._environment = {}
    # read values passed from the cli as parameters
    _apiURL = config.getoption("--apiurl")
    _custID = config.getoption("--custid")
    _cloudAdmin = config.getoption("--cloudadmin")
    _cloudAdminPass = config.getoption("--cloudadminpassword")
    testConfig = ConfigParser()

    if _apiURL is not None:
        testConfig.setApiURL(_apiURL)
    if _custID is not None:
        testConfig.setCustURL(_custID)
    if _cloudAdmin is not None:
        testConfig.setCloudAdmin(_cloudAdmin)
    if _cloudAdminPass is not None:
        testConfig.setCloudAdminPassword(_cloudAdminPass)
    _acctID, _clusterID = getAcctAndClusterID()
    if _acctID is not None:
        testConfig.setAcctID(_acctID)
    if _clusterID is not None:
        testConfig.setClusterID(_clusterID)
    setup = testConfig.getConfig("setupname")
    skyVersion, starVersion = getReleaseVersion()
    apiURL = testConfig.getConfig("apiURL")

    if not setup:
        setup = os.environ.get("SETUP_NAME")
        if not setup:
            setup = "Unknown"

    if not apiURL:
        apiURL = "Unknown"

    if not skyVersion:
        skyVersion = "Unknown"

    if not starVersion:
        starVersion = "Unknown"

    config._metadata["API URL"] = apiURL
    config._metadata["Setup Name"] = setup
    config._metadata["Star Version"] = starVersion
    config._metadata["Sky Version"] = skyVersion
    elog.info("successfully read configuration")


def pytest_addoption(parser):
    """Creates new options to be passed as pytest cli command"""
    parser.addoption(
        "--apiurl",
        action="store",
        default=None,
        help="API URL e.g. https://console.staging.edgebricks.com",
    )
    parser.addoption(
        "--custid",
        action="store",
        default=None,
        help="Customer ID of the cluster e.g. CPYyNDUmy0",
    )
    parser.addoption(
        "--cloudadmin",
        action="store",
        default=None,
        help="Cloud Admin username e.g. CloudAdmin_iHOZE",
    )
    parser.addoption(
        "--cloudadminpassword",
        action="store",
        default=None,
        help="Cloud Admin password e.g. test123",
    )
