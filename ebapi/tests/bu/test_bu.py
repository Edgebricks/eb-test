#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


from time import sleep
import pytest


from ebapi.common.config import ConfigParser
from ebapi.common.logger import elog
from ebapi.lib.edgebricks import BUs


class TestBu:
    buID   = ''
    testConfig = ConfigParser()
    buName = testConfig.getDomainName()

    def test_domain_crud_001(cls):

        # create bu
        buObj = BUs()
        buID = buObj.createBU(cls.buName, description="created by ebtest")
        assert buID
        cls.testConfig.setDomainID(buID)

        # get bu
        buResp = buObj.getBU(buID)
        assert buResp['name'] == cls.buName

        # update bu
        #newDesc = "ebtest updated description"
        #updatedBuResp = buObj.updateBU(buID, description=newDesc)
        #assert updatedBuResp['description'] == newDesc

        # delete bu
        assert buObj.deleteBU(buID)
