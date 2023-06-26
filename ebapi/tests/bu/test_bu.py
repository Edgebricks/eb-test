#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc

import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.edgebricks import BUs


class TestBu:
    testConfig = ConfigParser()

    def test_single_bu_001(cls):

        # create bu using config
        buObj = BUs()
        domainName = cls.testConfig.getDomainName()
        buID = buObj.createBU(buName=domainName)
        assert buID

        # get bu
        buResp = buObj.getBU(buID)
        assert buResp["name"] == domainName

        # update bu
        # newDesc = "ebtest updated description"
        # updatedBuResp = buObj.updateBU(buID, description=newDesc)
        # assert updatedBuResp['description'] == newDesc

        # delete bu
        assert buObj.deleteBU(buID)

    @pytest.mark.parametrize(
        "buNames", ["ebtestDomain01", "ebtestDomain02", "ebtestDomain03"]
    )
    def test_multiple_bu_002(cls, buNames):

        buObj = BUs()
        buID = buObj.createBU(buName=buNames)
        assert buID
        assert buObj.deleteBU(buID)
