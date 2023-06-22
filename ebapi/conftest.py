#!/usr/bin/env python
#
# Author: Ankit Jain (ankit@edgebricks.com)
# (c) 2022 Edgebricks


import json
import os
import pytest
import requests

from ebapi.common.config import ConfigParser
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


@pytest.fixture(scope='session', autouse=True)
def isDefaultTestConfigsSet():
    notset     = 0
    testConfig = ConfigParser()
    configs    = ['apiURL', 'acctID', 'clusterID', 'domainName',
                  'projectAdmin', 'projectAdminPassword']

    for config in configs:
        if not testConfig.getConfig(config):
            notset = 1

    if notset:
        pytest.skip('default test configs not set')


def getAcctAndClusterID():
    testConfig     = ConfigParser()
    apiURL         = testConfig.getConfig('apiURL')
    custID         = testConfig.getConfig('custID')
    headers        = {"Accept": "application/json",
                      "Content-Type": "application/json;charset=UTF-8"}

    if not apiURL or not custID:
        return None, None

    url      = apiURL + '/v1/account_ops/get_clusters?login_name=' + custID
    response = requests.get(url=url, headers=headers)

    if not response.ok:
        return None, None

    data       = json.loads(response.content)
    acctID     = data['clusters'][0]['acct_id']
    clusterID  = data['clusters'][0]['id']

    return acctID, clusterID

def getReleaseVersion():
    testConfig     = ConfigParser()
    apiURL         = testConfig.getConfig('apiURL')
    acctID         = testConfig.getConfig('acctID')
    clusterID      = testConfig.getConfig('clusterID')
    cloudAdmin     = testConfig.getConfig('cloudAdmin')
    cloudAdminPass = testConfig.getConfig('cloudAdminPassword')

    if not apiURL or not acctID or not clusterID or not cloudAdmin or not cloudAdminPass:
        return None, None

    tokenObj = Token('domain', 'admin.local', cloudAdmin, cloudAdminPass)
    token    = tokenObj.getToken()
    if not token:
        return None, None

    url      = apiURL + '/v1/accounts/%s/version' % acctID
    client   = RestClient(token)
    response = client.get(url)

    if not response.ok:
        return None, None

    data     = json.loads(response.content)
    star     = data['clusters'][0]['star']['short']
    sky      = data['sky_version']['sky']['short']

    return sky, star

def pytest_configure(config):
    """Provide additional environment details to pytest-html report"""
    # add environment details to the pytest-html plugin
    config._metdata     = {}
    config._environment = {}
    # read values passed from the cli as parameters
    _apiURL             = config.getoption("--apiurl")
    _custID             = config.getoption("--custid")
    _cloudAdmin         = config.getoption("--cloudadmin")
    _cloudAdminPass     = config.getoption("--cloudadminpassword")
    testConfig          = ConfigParser()
    if _apiURL is not None:
        testConfig.setApiURL(_apiURL)
    if _custID is not None:
        testConfig.setCustURL(_custID)
    if _cloudAdmin is not None:
        testConfig.setCloudAdmin(_cloudAdmin)
    if _cloudAdminPass is not None:
        testConfig.setCloudAdminPassword(_cloudAdminPass)
    _acctID, _clusterID   = getAcctAndClusterID()
    if _acctID is not None:
        testConfig.setAcctID(_acctID)
    if _clusterID is not None:
        testConfig.setClusterID(_clusterID)
    setup                 = testConfig.getConfig('setupName')
    sky, star             = getReleaseVersion()
    apiURL                = testConfig.getConfig('apiURL')

    if not setup:
        setup = os.environ.get('SETUP_NAME')
        if not setup:
            setup = 'Unknown'

    if not apiURL:
        apiURL = 'Unknown'

    if not sky:
        sky = 'Unknown'

    if not star:
        star = 'Unknown'

    config._metadata['API URL']       = apiURL
    config._metadata['Star Version']  = star
    config._metadata['Setup Name']    = setup
    config._metadata['Sky Version']   = sky


def pytest_addoption(parser):
    """Creates new options to be passed as pytest cli command"""
    parser.addoption(
        "--apiurl",
        action="store",
        default=None,
        help="API URL of the cluster e.g. http://vpn.edgebricks.in:11002"
    )
    parser.addoption(
        "--custid",
        action="store",
        default=None,
        help="Customer ID of the cluster e.g. CPYyNDUmy0"
    )
    parser.addoption(
        "--cloudadmin",
        action="store",
        default=None,
        help="Cloud Admin username e.g. CloudAdmin_iHOZE"
    )
    parser.addoption(
        "--cloudadminpassword",
        action="store",
        default=None,
        help="Cloud Admin password e.g. test123"
    )
