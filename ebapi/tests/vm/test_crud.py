#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# Copyright (c) 2021-2023 Edgebricks Inc.

from time import sleep
import pytest

from ebapi.common.config import ConfigParser
from ebapi.lib.edgebricks import BUs, Projects
from ebapi.lib.nova import VMs
from ebapi.lib.nova import Flavors
from ebapi.lib.neutron import Networks
from ebapi.lib.glance import Images


class TestVMCRUD:
    testConfig = ConfigParser()
    # initialise bu and project
    buObj = BUs()
    domainName = testConfig.getDomainName()
    userName = testConfig.getProjectAdmin()
    userPwd = testConfig.getProjectAdminPassword()
    projectName = testConfig.getProjectName()

    @classmethod
    def setup_class(cls):
        # create bu
        cls.buID = cls.buObj.create(
            buName=cls.domainName, userName=cls.userName, userPwd=cls.userPwd
        )
        assert cls.buID

        # get bu
        buResp = cls.buObj.get(cls.buID)
        assert buResp["name"] == cls.domainName

        # wait for bu to be created
        assert cls.buObj.waitForState(cls.buID, state=BUs.BU_STATE_CREATED)

        # create Project in the above created bu
        cls.projObj = Projects(cls.domainName, cls.userName, cls.userPwd)
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

        cls.projID = cls.projObj.create(
            cls.projectName, cls.buID, metadata, compQuota, strQuota, netQuota
        )
        assert cls.projID

        # get project
        projResp = cls.projObj.get(cls.projID)
        assert projResp["name"] == cls.projectName

        # get vm flavor
        flavorObj = Flavors(cls.projID)
        cls.matchflavorID = flavorObj.getBestMatchingFlavor(numCPU=2, memMB=2048)

        # get vm image
        imageObj = Images(cls.projID)
        imgDetails = imageObj.getImagesbyVisibility(visibility="public")
        for images in imgDetails["images"]:
            if images["os"] == "cirros" and images["status"] == "active":
                cls.actualImageID = images["id"]
            break

        # wait for project to be created
        assert cls.projObj.waitForState(cls.projID, state=Projects.PROJ_STATE_CREATED)
        sleep(30)

    @classmethod
    def teardown_class(cls):
        # delete project
        assert cls.projObj.delete(cls.projID, force_delete=True)

        # wait for project to be deleted
        assert cls.projObj.waitForState(cls.projID, state=Projects.PROJ_STATE_DELETED)

        # delete bu
        assert cls.buObj.delete(cls.buID, force_delete="true")

        # wait for bu to be deleted
        assert cls.buObj.waitForState(cls.buID, state=BUs.BU_STATE_DELETED)

    def test_vm_crud_001(cls):
        try:
            # create internal network
            networkObj = Networks(cls.projID)
            netID = networkObj.createInternalNetwork(
                netName="Auto-Net1",
                subnetName="Auto-SubNet1",
            )

            # create vm
            vmObj = VMs(cls.projID)
            vmName = "ebtestVM"
            vmObj.createVM(
                vmName=vmName,
                flavorID=cls.matchflavorID,
                networkID=netID,
                imageID=cls.actualImageID,
            )
            content = vmObj.getAllVMs()
            for key, value in content.items():
                if value == vmName:
                    vmID = key
                break
            # wait for VM to be created
            assert vmObj.waitForState(vmID, state="ACTIVE")

        finally:
            assert vmObj.deleteVM(vmID)
            assert networkObj.deleteInternalNetwork(netID)
            sleep(5)

    @pytest.mark.parametrize(
        "VMNames",
        [
            "ebtestVMNew01",
            "ebtestVMNew02",
            "ebtestVMNew03",
        ],
    )
    def test_vm_crud_002(cls, VMNames):
        try:
            # create internal network
            networkObj = Networks(cls.projID)
            netID = networkObj.createInternalNetwork(
                netName="Auto-Net2",
                subnetName="Auto-SubNet2",
            )

            # create vm
            vmObj = VMs(cls.projID)
            vmObj.createVM(
                vmName=VMNames,
                flavorID=cls.matchflavorID,
                networkID=netID,
                imageID=cls.actualImageID,
            )
            content = vmObj.getAllVMs()
            for key, value in content.items():
                if value == VMNames:
                    vmID = key
                break
            # wait for VM to be created
            assert vmObj.waitForState(vmID, state="ACTIVE")

        finally:
            vmObj.deleteVM(vmID)
            networkObj.deleteInternalNetwork(netID)
            sleep(5)
