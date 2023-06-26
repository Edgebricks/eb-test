#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc

from ebapi.common.config import ConfigParser
from ebapi.lib.keystone import Users, Roles
from ebapi.lib.edgebricks import BUs, Projects


class TestProjectCRUD:
    testConfig = ConfigParser()

    def test_project_crud_001(cls):

        # create BU
        buObj = BUs()
        domainName = cls.testConfig.getDomainName()
        buID = buObj.create(buName=domainName)
        assert buID

        # create admin user
        userObj = Users()
        projectAdmin = cls.testConfig.getProjectAdmin()
        projectAdminPass = cls.testConfig.getProjectAdminPassword()
        userID = userObj.create(buID, projectAdmin, projectAdminPass)
        assert userID

        # get Admin RoleID
        roleID = None
        roleObj = Roles()
        content = roleObj.get()
        for role in content["roles"]:
            if role["name"] == "admin":
                roleID = role["id"]
                break
        assert roleID is not None

        # assign admin role to created user
        roleObj = Roles()
        assert roleObj.assign(buID, userID, roleID)

        # create Project with above created user
        projObj = Projects(domainName, projectAdmin, projectAdminPass)

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
        assert projResp["project"]["name"] == projectName

        # delete project
        assert projObj.delete(projID)

        # delete bu
        assert buObj.delete(buID)
