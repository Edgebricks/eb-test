#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


from time import sleep
import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.keystone import Domains


class TestBu:
    domainID         = ''
    testConfig       = ConfigParser()
    domainName       = testConfig.getDomainName()

    def test_create_duplicate_domain_002(cls):

        domainObj = Domains()
        domainID = domainObj.createDomain(cls.domainName)
        assert domainID
        cls.testConfig.setDomainID(domainID)
        dupDomainID = domainObj.createDomain(cls.domainName)
        assert not dupDomainID

        assert domainObj.updateDomain(domainID)
        assert domainObj.deleteDomain(domainID)

    def test_delete_nonexistant_domain_003(cls):

        domainObj = Domains()
        domainID = cls.testConfig.getDomainID()
        assert not domainObj.updateDomain(domainID)
        assert not domainObj.deleteDomain(domainID)

    @pytest.mark.parametrize("domainNames", ["autodomain1", "autodomain2", "autodomain3", "autodomain4"])
    def test_create_delete_multiple_domains_004(cls, domainNames):

        domainObj = Domains()
        domainID = domainObj.createDomain(domainNames)
        assert domainID
        assert domainObj.updateDomain(domainID)
        assert domainObj.deleteDomain(domainID)

    def test_get_domain_005(cls):

        domainObj = Domains()
        domainID = domainObj.createDomain(cls.domainName)
        assert domainID
        content = domainObj.getDomain(domainID)
        assert content["domain"]["id"]

        assert domainObj.updateDomain(domainID)
        assert domainObj.deleteDomain(domainID)
        content = domainObj.getDomain(domainID)
        assert not content

    def test_create_delete_domain_different_quota_006(cls):

        domainObj = Domains()
        domainID = domainObj.createDomain(cls.domainName)
        assert domainID
        assert domainObj.updateDomainQuota(domainID)
        assert domainObj.updateDomain(domainID)
        assert domainObj.deleteDomain(domainID)
