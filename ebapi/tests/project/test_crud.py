#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc

from ebapi.common.config import ConfigParser

# from ebapi.lib.keystone import Users, Roles
from ebapi.lib.edgebricks import BUs, Projects


class TestProjectCRUD:
    testConfig = ConfigParser()

    @classmethod
    def test_project_crud_001(cls):
        # create BU
        buObj = BUs()
        domainName = cls.testConfig.getDomainName()
        userName = cls.testConfig.getProjectAdmin()
        userPwd = cls.testConfig.getProjectAdminPassword()
        buID = buObj.create(buName=domainName, userName=userName, userPwd=userPwd)
        assert buID

        # get bu
        buResp = buObj.get(buID)
        assert buResp["name"] == domainName

        # wait for bu to be created
        assert buObj.waitForState(buID, state=BUs.BU_STATE_CREATED)

        # create Project in the above bu
        projObj = Projects(domainName, userName, userPwd)
        metadata = {"templateId": "Large", "custom_template": "true"}
        compQuota = {
            "cores": 128,
            "injected_file_content_bytes": -1,
            "injected_file_path_bytes": -1,
            "injected_files": -1,
            "instances": 64,
            "key_pairs": -1,
            "metadata_items": -1,
            "ram": 262144,
        }
        strQuota = {
            "snapshots": 640,
            "backup_gigabytes": -1,
            "backups": -1,
            "volumes": 640,
            "gigabytes": 25600,
        }
        netQuota = {
            "router": 30,
            "subnet": -1,
            "network": 30,
            "port": -1,
            "floatingip": 64,
            "pool": -1,
        }

        projectName = cls.testConfig.getProjectName()
        projID = projObj.create(
            projectName, buID, metadata, compQuota, strQuota, netQuota
        )
        assert projID

        # get project
        projResp = projObj.get(projID)
        assert projResp["name"] == projectName

        # wait for project to be created
        assert projObj.waitForState(projID, state=Projects.PROJ_STATE_CREATED)

        # delete project
        assert projObj.delete(projID)

        # wait for project to be deleted
        assert projObj.waitForState(projID, state=Projects.PROJ_STATE_DELETED)

        # delete bu
        assert buObj.delete(buID)

        # wait for bu to be deleted
        assert buObj.waitForState(buID, state=BUs.BU_STATE_DELETED)

    @classmethod
    def test_project_crud_002(cls):
        assert True
