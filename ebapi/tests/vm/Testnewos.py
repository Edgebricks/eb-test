from time import sleep

from ebapi.common.config import ConfigParser
from ebapi.lib.edgebricks import BUs, Projects
from ebapi.lib.nova import VMs
from ebapi.lib.nova import Flavors
from ebapi.lib.neutron import Networks
from ebapi.lib.glance import Images


class TestVMAction:
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

        # wait for project to be created
        assert cls.projObj.waitForState(cls.projID, state=Projects.PROJ_STATE_CREATED)

        # get vm flavor
        flavorObj = Flavors(cls.projID)
        cls.matchflavorID = flavorObj.getBestMatchingFlavor(numCPU=2, memMB=2048)

        # get vm images
        imageObj = Images(cls.projID)
        imgDetails = imageObj.getImagesbyVisibility(visibility="public")
        cls.image_ids = {}
        for images in imgDetails["images"]:
            if images["os"] in ["arch", "centos-7", "centos-8.4", "freebsd-12", "ubuntu-16", "ubuntu-18", "ubuntu-20", "ubuntu-22.04", "windows-10", "windows-11", "windows-2022"]:
                cls.image_ids[images["os"]] = images["id"]

        sleep(5)

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

    def create_vm(self, vm_name, image_id, network_id):
        vm_obj = VMs(self.projID)
        vm_obj.createVM(
            vmName=vm_name,
            flavorID=self.matchflavorID,
            networkID=network_id,
            imageID=image_id,
        )
        return vm_obj

    def test_vm_creation(self):
        try:
            # create internal network
            networkObj = Networks(self.projID)
            netID = networkObj.createInternalNetwork(
                netName="Auto-Net1",
                subnetName="Auto-SubNet1",
            )

            for os, image_id in self.image_ids.items():
                vm_name = f"test_vm_{os.replace('-', '_')}"
                vm = self.create_vm(vm_name, image_id, netID)
                vm_id = vm.getAllVMs().keys()[0]
                assert vm.waitForState(vm_id, state="ACTIVE")

        finally:
            for os, _ in self.image_ids.items():
                vm_name = f"test_vm_{os.replace('-', '_')}"
                vm = VMs(self.projID)
                vm_id = vm.getVMbyName(vm_name)
                if vm_id:
                    assert vm.deleteVM(vm_id)
            assert networkObj.deleteInternalNetwork(netID)
            sleep(5)
l