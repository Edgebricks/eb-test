#!/usr/bin/env python
#
# Author: Ankit Jain (ankit@edgebricks.com)
# (c) 2022 Edgebricks


import json
import os
import pytest

from ebtest.common.config import ConfigParser
from ebtest.common.rest import RestClient
from ebtest.lib.keystone import Token


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


def getReleaseVersion():
    testConfig     = ConfigParser()
    apiURL         = testConfig.getConfig('apiURL')
    acctID         = testConfig.getConfig('acctID')
    cloudAdmin     = testConfig.getConfig('cloudAdmin')
    cloudAdminPass = testConfig.getConfig('cloudAdminPassword')

    if not apiURL or not acctID or not cloudAdmin or not cloudAdminPass:
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
    platform = data['clusters'][0]['star']['short']
    sky      = data['sky_version']['sky']['short']

    return sky, platform


def pytest_configure(config):
    """Provide additional environment details to pytest-html report"""
    # add environment details to the pytest-html plugin
    config._metdata     = {}
    config._environment = {}
    testConfig          = ConfigParser()
    setup               = testConfig.getConfig('setupName')
    apiURL              = testConfig.getConfig('apiURL')
    sky, platform       = getReleaseVersion()

    if not setup:
        setup = os.environ.get('SETUP_NAME')
        if not setup:
            setup = 'Unknown'

    if not apiURL:
        apiURL = 'Unknown'

    if not sky:
        sky = 'Unknown'

    if not platform:
        platform = 'Unknown'

    config._metadata['API URL']     = apiURL
    config._metadata['Platform']    = platform
    config._metadata['Setup Name']  = setup
    config._metadata['Sky Version'] = sky
