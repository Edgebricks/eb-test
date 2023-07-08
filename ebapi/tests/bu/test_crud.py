#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc

import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.edgebricks import BUs


class TestBuCRUD:
    testConfig = ConfigParser()

    def test_bu_crud_001(cls):
        # create bu using config
        buObj = BUs()
        domainName = cls.testConfig.getDomainName()
        buID = buObj.create(buName=domainName)
        assert buID

        # get bu
        buResp = buObj.get(buID)
        assert buResp["name"] == domainName

        # wait for bu to be created
        assert buObj.waitForState(buID, state=BUs.BU_STATE_CREATED)

        # update bu
        # newDesc = "ebtest updated description"
        # updatedBuResp = buObj.update(buID, description=newDesc)
        # assert updatedBuResp['description'] == newDesc

        # delete bu
        assert buObj.delete(buID)

        # wait for bu to be deleted
        assert buObj.waitForState(buID, state=BUs.BU_STATE_DELETED)

    @pytest.mark.parametrize(
        "buNames", ["ebtestDomainNew01", "ebtestDomainNew02", "ebtestDomainNew03"]
    )
    def test_bu_crud_002(cls, buNames):
        # create bu
        buObj = BUs()
        buID = buObj.create(buName=buNames)
        assert buID

        # wait for bu to be created
        assert buObj.waitForState(buID, state=BUs.BU_STATE_CREATED)

        # delete bu
        assert buObj.delete(buID)

        # wait for bu to be deleted
        assert buObj.waitForState(buID, state=BUs.BU_STATE_DELETED)
