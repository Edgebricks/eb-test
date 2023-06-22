#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


from time import sleep
import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.keystone import Domains
from ebapi.lib.keystone import Roles
from ebapi.lib.keystone import Users
from ebapi.lib.edgebricks import Projects
from ebapi.lib.nova import VMs
from ebapi.lib.nova import Flavors
from ebapi.lib.neutron import Networks
from ebapi.lib.glance import Images


class TestCreateDeleteBasic:
    domainID         = ''
    adminUserID      = ''
    userID           = ''
    projID           = ''
    roleID           = ''
    testConfig       = ConfigParser()
    domainName       = testConfig.getDomainName()
    projectName      = testConfig.getProjectName()
    projectAdmin     = testConfig.getProjectAdmin()
    projectAdminPass = testConfig.getProjectAdminPassword()

    def test_create_domain_users_project(cls):

        ##### Create Domain ####
        domainObj = Domains()
        TestCreateDeleteBasic.domainID = domainObj.createDomain(cls.domainName)
        assert TestCreateDeleteBasic.domainID
        cls.testConfig.setDomainID(TestCreateDeleteBasic.domainID)

        ##### Create User ####
        userObj = Users()
        TestCreateDeleteBasic.userID = userObj.createUser(
            TestCreateDeleteBasic.domainID, cls.projectAdmin, cls.projectAdminPass)
        assert TestCreateDeleteBasic.userID

        ##### Get User ####
        content = userObj.getUsers()
        for user in content['users']:
            if user['name'] == cls.testConfig.getCloudAdmin():
                TestCreateDeleteBasic.adminUserID = user['id']
                break

        assert TestCreateDeleteBasic.adminUserID

        ##### Get Roles ####
        roleObj = Roles()
        content = roleObj.getRoles()
        for role in content['roles']:
            if role['name'] == 'admin':
                TestCreateDeleteBasic.roleID = role['id']
                break

        assert TestCreateDeleteBasic.roleID

        # assign admin role to created user
        assert roleObj.assignRole(TestCreateDeleteBasic.domainID,
                                  TestCreateDeleteBasic.userID, TestCreateDeleteBasic.roleID)
        # assert roleObj.assignRole(domainID, adminUserID, roleID)

        ##### Create Project ####
        projObj = Projects(cls.domainName, cls.projectAdmin,
                           cls.projectAdminPass)

        metadata = {
            "templateId": "Large",
            "custom_template": "true"
        }

        compQuota = {
            "cores": 128,
            "injected_file_content_bytes": -1,
            "injected_file_path_bytes": -1,
            "injected_files": -1,
            "instances": 64,
            "key_pairs": -1,
            "metadata_items": -1,
            "ram": 262144
        }

        strQuota = {
            "snapshots": 640,
            "backup_gigabytes": -1,
            "backups": -1,
            "volumes": 640,
            "gigabytes": 25600
        }

        netQuota = {
            "router": 30,
            "subnet": -1,
            "network": 30,
            "port": -1,
            "floatingip": 64,
            "pool": -1
        }

        TestCreateDeleteBasic.projID = projObj.createProject(cls.projectName, TestCreateDeleteBasic.domainID, metadata,
                                                             compQuota, strQuota, netQuota)
        assert TestCreateDeleteBasic.projID
        cls.testConfig.setProjectID(TestCreateDeleteBasic.projID)

    def test_create_delete_vm(cls):

        flavorObj = Flavors(TestCreateDeleteBasic.projID)
        matchflavorID = flavorObj.getBestMatchingFlavor(numCPU = 2, memMB = 4096)

        networkObj = Networks(TestCreateDeleteBasic.projID)
        netID = networkObj.createInternalNetwork(netName = "Auto-Net1", subnetName = "Auto-SubNet1")

        imageObj = Images(TestCreateDeleteBasic.projID)
        imgID = imageObj.createCirrosImageByURL(imageName="Auto-Cirros-Image", netID=netID)
        sleep (35)
        imgDetails = imageObj.getImagesbyOwner(owner=TestCreateDeleteBasic.projID)
        actualImageID = imgDetails['images'][0]['id']
        sleep (20)
        vmObj = VMs(TestCreateDeleteBasic.projID)
        vmObj.createVM(vmName = "AutoVM", flavorID = matchflavorID, networkID = netID, imageID = actualImageID)
        sleep (35)
        content = vmObj.getAllVMs()
        for key, value in content.items():
            if value == 'AutoVM':
                vmID = key
                break
        vmObj.deleteVM (vmID)
        sleep (35)
        imageObj.deleteImage(actualImageID)
        sleep (20)
        networkObj.deleteInternalNetwork(netID)
        sleep (20)


    def test_delete_domain_users_project(cls):

        ##### Delete Project ####
        projObj = Projects(cls.domainName, cls.projectAdmin,
                           cls.projectAdminPass)
        content = projObj.getProject(
            TestCreateDeleteBasic.userID, TestCreateDeleteBasic.domainID)
        for project in content['projects']:
            if project['name'] == cls.projectName:
                TestCreateDeleteBasic.projID = project['id']
                break
        assert projObj.deleteProject(TestCreateDeleteBasic.projID)
        sleep (15)

        ##### Delete Domain ####
        domainObj = Domains()
        assert domainObj.updateDomain(TestCreateDeleteBasic.domainID)
        assert domainObj.deleteDomain(TestCreateDeleteBasic.domainID)
