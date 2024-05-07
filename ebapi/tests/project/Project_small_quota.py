#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# Copyright (c) 2021-2023 Edgebricks Inc.

import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.edgebricks import BUs, Projects


class TestProjectCRUD:
    testConfig = ConfigParser()
    # initialise bu
    buObj = BUs()
    domainName = testConfig.getDomainName()
    userName = testConfig.getProjectAdmin()
    userPwd = testConfig.getProjectAdminPassword()

    @classmethod
    def setup_class(cls):
        # create BU
        cls.buID = cls.buObj.create(
            buName=cls.domainName, userName=cls.userName, userPwd=cls.userPwd
        )
        assert cls.buID

        # get bu
        buResp = cls.buObj.get(cls.buID)
        assert buResp["name"] == cls.domainName

        # wait for bu to be created
        assert cls.buObj.waitForState(cls.buID, state=BUs.BU_STATE_CREATED)

    @classmethod
    def teardown_class(cls):
        # delete bu
        assert cls.buObj.delete(cls.buID, force_delete="true")

        # wait for bu to be deleted
        assert cls.buObj.waitForState(cls.buID, state=BUs.BU_STATE_DELETED)

    def test_project_crud_001(cls):
        # create Project in the above created bu
        projObj = Projects(cls.domainName, cls.userName, cls.userPwd)
        metadata = {"templateId": "Large", "custom_template": "true"}
        compQuota = {
            "cores": 16,
            "injected_file_content_bytes": -1,
            "injected_file_path_bytes": -1,
            "injected_files": -1,
            "instances": 8,
            "key_pairs": -1,
            "metadata_items": -1,
            "ram": 32144,
        }
        strQuota = {
            "snapshots": 80,
            "backup_gigabytes": -1,
            "backups": -1,
            "volumes": 80,
            "gigabytes": 320,
        }
        netQuota = {
            "router": 10,
            "subnet": -1,
            "network": 10,
            "port": -1,
            "floatingip": 8,
            "pool": -1,
        }

        projectName = cls.testConfig.getProjectName()
        try:
            projID = projObj.create(
                projectName, cls.buID, metadata, compQuota, strQuota, netQuota
            )
            assert projID

            # get project
            projResp = projObj.get(projID)
            assert projResp["name"] == projectName

            # wait for project to be created
            assert projObj.waitForState(projID, state=Projects.PROJ_STATE_CREATED)

            # update project description
            newDesc = "ebtestProject description updated"
            updatedProjectResp = projObj.update(
                cls.buID, projID, projectName, desc=newDesc
            )
            assert updatedProjectResp["description"] == newDesc

        finally:
            # delete project
            assert projObj.delete(projID, force_delete=True)

            # wait for project to be deleted
            assert projObj.waitForState(projID, state=Projects.PROJ_STATE_DELETED)

    @pytest.mark.parametrize(
        "projectNames",
        ["ebtestProjectNew01", "ebtestProjectNew02", "ebtestProjectNew03"],
    )
    def test_project_crud_002(cls, projectNames):
        # create Project in the above created bu
        projObj = Projects(cls.domainName, cls.userName, cls.userPwd)
        metadata = {"templateId": "Large", "custom_template": "true"}
        compQuota = {
            "cores": 64,
            "injected_file_content_bytes": -1,
            "injected_file_path_bytes": -1,
            "injected_files": -1,
            "instances": 32,
            "key_pairs": -1,
            "metadata_items": -1,
            "ram": 128144,
        }
        strQuota = {
            "snapshots": 320,
            "backup_gigabytes": -1,
            "backups": -1,
            "volumes": 320,
            "gigabytes": 1280,
        }
        netQuota = {
            "router": 20,
            "subnet": -1,
            "network": 20,
            "port": -1,
            "floatingip": 32,
            "pool": -1,
        }

        try:
            projID = projObj.create(
                projectNames, cls.buID, metadata, compQuota, strQuota, netQuota
            )
            assert projID

            # get project
            projResp = projObj.get(projID)
            assert projResp["name"] == projectNames

            # wait for project to be created
            assert projObj.waitForState(projID, state=Projects.PROJ_STATE_CREATED)

        finally:
            # delete project
            assert projObj.delete(projID, force_delete=True)

            # wait for project to be deleted
            assert projObj.waitForState(projID, state=Projects.PROJ_STATE_DELETED)
