#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


from time import sleep

from ebapi.common.config import ConfigParser
from ebapi.lib.keystone import Roles
from ebapi.lib.keystone import Users
from ebapi.lib.edgebricks import BUs, Projects
from ebapi.lib.nova import VMs
from ebapi.lib.nova import Flavors
from ebapi.lib.neutron import Networks
from ebapi.lib.glance import Images


class TestSanity:
    domainID = ""
    adminUserID = ""
    userID = ""
    projID = ""
    roleID = ""
    testConfig = ConfigParser()
    domainName = testConfig.getDomainName()
    projectName = testConfig.getProjectName()
    projectAdmin = testConfig.getProjectAdmin()
    projectAdminPass = testConfig.getProjectAdminPassword()

    def test_sanity_project_001(cls):
        # Create Domain
        domainObj = BUs()
        TestSanity.domainID = domainObj.create(buName=cls.domainName)
        assert TestSanity.domainID
        cls.testConfig.setDomainID(TestSanity.domainID)

        # Create User
        userObj = Users()
        TestSanity.userID = userObj.create(
            TestSanity.domainID, cls.projectAdmin, cls.projectAdminPass
        )
        assert TestSanity.userID

        # Get User
        content = userObj.list()
        for user in content["users"]:
            if user["name"] == cls.testConfig.getCloudAdmin():
                TestSanity.adminUserID = user["id"]
                break
        assert TestSanity.adminUserID

        # Get Roles
        roleObj = Roles()
        content = roleObj.get()
        for role in content["roles"]:
            if role["name"] == "admin":
                TestSanity.roleID = role["id"]
                break
        assert TestSanity.roleID

        # assign admin role to created user
        assert roleObj.assign(TestSanity.domainID, TestSanity.userID, TestSanity.roleID)
        # assert roleObj.assign(domainID, adminUserID, roleID)

        # Create Project
        projObj = Projects(cls.domainName, cls.projectAdmin, cls.projectAdminPass)

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

        TestSanity.projID = projObj.create(
            cls.projectName,
            TestSanity.domainID,
            metadata,
            compQuota,
            strQuota,
            netQuota,
        )
        assert TestSanity.projID
        cls.testConfig.setProjectID(TestSanity.projID)

    def test_sanity_vm_002(cls):
        flavorObj = Flavors(TestSanity.projID)
        matchflavorID = flavorObj.getBestMatchingFlavor(numCPU=2, memMB=4096)

        networkObj = Networks(TestSanity.projID)
        netID = networkObj.createInternalNetwork(
            netName="Auto-Net1", subnetName="Auto-SubNet1"
        )

        imageObj = Images(TestSanity.projID)
        imgDetails = imageObj.getImagesbyOwner(owner=TestSanity.projID)
        actualImageID = imgDetails["images"][0]["id"]
        sleep(20)
        vmObj = VMs(TestSanity.projID)
        vmObj.createVM(
            vmName="AutoVM",
            flavorID=matchflavorID,
            networkID=netID,
            imageID=actualImageID,
        )
        sleep(35)
        content = vmObj.getAllVMs()
        for key, value in content.items():
            if value == "AutoVM":
                vmID = key
                break
        vmObj.deleteVM(vmID)
        sleep(35)
        imageObj.deleteImage(actualImageID)
        sleep(20)
        networkObj.deleteInternalNetwork(netID)
        sleep(20)

    def test_sanity_user_003(cls):
        # Delete Project
        projObj = Projects(cls.domainName, cls.projectAdmin, cls.projectAdminPass)
        content = projObj.list(TestSanity.userID, TestSanity.domainID)
        for project in content["projects"]:
            if project["name"] == cls.projectName:
                TestSanity.projID = project["id"]
                break
        assert projObj.delete(TestSanity.projID)
        sleep(15)

        # Delete Domain
        domainObj = BUs()
        # assert domainObj.update(TestSanity.domainID)
        assert domainObj.delete(TestSanity.domainID)
