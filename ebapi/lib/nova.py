#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import json
from time import sleep

from ebapi.common import utils as eutil
from ebapi.common.logger import elog
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class NovaBase(Token):
    def __init__(self, projectID, scope="project"):
        super().__init__(scope)
        self.client = RestClient(self.getToken())
        self.projectID = projectID
        self.apiURL = self.getApiURL()
        self.serviceURL = self.getServiceURL()
        self.novaURL = self.serviceURL + "/nova/v2/" + self.projectID
        self.clusterID = self.getClusterID()
        self.clusterURL = self.apiURL + "/v2/clusters/" + self.clusterID


class VMs(NovaBase):
    def __init__(self, projectID):
        super().__init__(projectID)
        self.vmsURL = self.clusterURL + "/projects"
        self.serversURL = self.novaURL + "/servers"

    def getAllVMs(self):
        response = self.client.get(self.vmsURL + "/" + self.projectID + "/vms")
        if not response.ok:
            elog.error("failed to get VMs: %s" % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        vms = {}
        for vm in content:
            vms[vm["id"]] = vm["name"]

        return vms

    def getVM(self, vmID):
        requestURL = self.clusterURL + "/vms/" + vmID
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get VM details: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content

    def _getVMResourceStatus(self):
        response = self.client.get(
            self.vmsURL + "/" + self.projectID + "/resource_status?type=vm"
        )
        content = json.loads(response.content)
        elog.info(content)

        return content

    def waitForState(self, vmID, state=None, timeoutInSecs=None, sleepInSecs=None):
        elog.info(
            "waiting for VM %s state to be %s"
            % (eutil.bcolor(vmID), eutil.gcolor(state))
        )

        if timeoutInSecs is None:
            timeoutInSecs = 150  # 2mins 30secs
        if sleepInSecs is None:
            sleepInSecs = 15  # 15secs

        curIteration = 1
        maxAllowedItr = timeoutInSecs / sleepInSecs
        while True:
            VMState = self.getStatus(vmID)
            if VMState is None:
                elog.error("VM [%s] not found" % eutil.rcolor(vmID))
                return None

            if VMState == state:
                elog.info(
                    "VM [%s] is in desired state [%s]"
                    % (eutil.bcolor(vmID), eutil.gcolor(state))
                )
                break

            # break after maximum allowed iterations and report failure
            if curIteration > maxAllowedItr:
                elog.error(
                    "VM [%s] failed to get desired state %s"
                    % (eutil.rcolor(vmID), eutil.rcolor(state))
                )
                return None

            sleep(sleepInSecs)
            curIteration = curIteration + 1

        return True

    def getFloatingIPFromVMID(self, vmID):
        requestURL = self.novaURL + "/os-floating-ips"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed fetching VM details for %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            return None

        content = json.loads(response.content)
        for floatingIP in content["floating_ips"]:
            instanceID = floatingIP["instance_id"]
            if instanceID == vmID:
                return floatingIP["ip"]

        elog.error("no floating IP assigned to %s" % eutil.bcolor(vmID))
        return None

    def getVMIDFromFloatingIP(self, fip):
        requestURL = self.novaURL + "/os-floating-ips"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed fetching VM details for %s: %s"
                % (eutil.bcolor(fip), eutil.rcolor(response.status_code))
            )
            return None

        content = json.loads(response.content)
        for floatingIP in content["floating_ips"]:
            ip = floatingIP["ip"]
            if ip == fip:
                return floatingIP["instance_id"]

        elog.error("no VM assigned with floatingIP %s" % eutil.bcolor(fip))
        return None

    def getMacAddrFromIP(self, vmID, ipAddr):
        response = self.getVM(vmID)
        if not response:
            elog.error("fetching vm details for %s failed" % (eutil.bcolor(vmID)))
            elog.error(response)
            return None

        for netname in response["addresses"]:
            for element in response["addresses"][netname]:
                if element["Addr"] == ipAddr:
                    return element["OS-EXT-IPS-MAC:mac_addr"]

        elog.error("no mac address found for %s" % eutil.bcolor(ipAddr))
        return None

    def getVolumesAttached(self, vmID):
        response = self.getVM(vmID)
        if not response:
            elog.error("fetching VM details for %s failed" % (eutil.bcolor(vmID)))
            elog.error(response)
            return None

        lvolumes = []
        for vols in response["volumes"]:
            lvolumes.append(vols["id"])

        return lvolumes

    def getStatus(self, vmID):
        response = self.getVM(vmID)
        if not response:
            elog.error("fetching VM details for %s failed" % (eutil.bcolor(vmID)))
            elog.error(response)
            return None

        return response["vm_state"]

    def getHost(self, vmID):
        response = self.getVM(vmID)
        if not response:
            elog.error("fetching VM details for %s failed" % (eutil.bcolor(vmID)))
            elog.error(response)
            return None

        return response["host"]

    def createVM(self, vmName="", flavorID="", networkID="", imageID=""):
        requestURL = self.vmsURL + "/" + self.projectID + "/vms"
        payload = {
            "name": vmName,
            "resources": {
                "server": {
                    "type": "OS::Nova::Server",
                    "os_req": {
                        "server": {
                            "name": vmName,
                            "flavorRef": flavorID,
                            "block_device_mapping_v2": [
                                {
                                    "device_type": "disk",
                                    "disk_bus": "virtio",
                                    "device_name": "/dev/vda",
                                    "source_type": "volume",
                                    "destination_type": "volume",
                                    "delete_on_termination": True,
                                    "boot_index": "0",
                                    "uuid": "{{.bootVol}}",
                                }
                            ],
                            "networks": [{"uuid": networkID}],
                            "security_groups": [{"name": "default"}],
                        },
                        "os:scheduler_hints": {"volume_id": "{{.bootVol}}"},
                    },
                },
                "bootVol": {
                    "type": "OS::Cinder::Volume",
                    "os_req": {
                        "volume": {
                            "availability_zone": None,
                            "description": None,
                            "size": 1,
                            "name": "bootVolume-" + vmName,
                            "volume_type": "relhighiops_type",
                            "disk_bus": "virtio",
                            "device_type": "disk",
                            "source_type": "image",
                            "device_name": "/dev/vda",
                            "bootable": True,
                            "tenant_id": self.projectID,
                            "imageRef": imageID,
                            "enabled": "true",
                        }
                    },
                },
            },
        }
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "creating vm %s: %s"
                % (eutil.bcolor(vmName), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "creating vm %s: %s OK"
            % (eutil.bcolor(vmName), eutil.gcolor(response.status_code))
        )

        timeoutInSecs = 150  # 2mins 30secs
        sleepInSecs = 15  # 15secs
        curIteration = 1
        maxAllowedItr = timeoutInSecs / sleepInSecs

        while True:
            VMRsp = self._getVMResourceStatus()
            if not VMRsp:
                elog.info("VM %s creation is completed." % (eutil.bcolor(vmName)))
                break

            # break after maximum allowed iterations and report failure
            if curIteration > maxAllowedItr:
                elog.error("VM %s creation failed." % (eutil.rcolor(vmName)))
                return False

            sleep(sleepInSecs)
            curIteration = curIteration + 1
        return True

    def deleteVM(self, vmID):
        requestURL = self.vmsURL + "/" + self.projectID + "/vms/" + vmID
        response = self.client.delete(requestURL)
        if not response.ok:
            elog.error(
                "deleting vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "deleting vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        timeoutInSecs = 150  # 2mins 30secs
        sleepInSecs = 15  # 15secs
        curIteration = 1
        maxAllowedItr = timeoutInSecs / sleepInSecs

        while True:
            VMRsp = self._getVMResourceStatus()
            if not VMRsp:
                elog.info("VM %s deletion is completed." % (eutil.bcolor(vmID)))
                break

            # break after maximum allowed iterations and report failure
            if curIteration > maxAllowedItr:
                elog.error("VM %s deletion failed." % (eutil.rcolor(vmID)))
                return False

            sleep(sleepInSecs)
            curIteration = curIteration + 1
        return True

    def suspendVM(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"suspend": ""}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "suspending vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "suspending vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def resumeVM(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"resume": ""}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "resuming vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "resuming vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def rebootVM(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"reboot": {"type": "SOFT"}}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "reboot vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "reboot vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def powerOffVM(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"os-stop": ""}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "poweroff vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "poweroff vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def powerOnVM(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"os-start": ""}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "poweron vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "poweron vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def migrateVM(self, vmID, doc=False, bm=False, host=None):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {
            "os-migrateLive": {
                "host": host,
                "block_migration": bm,
                "disk_over_commit": doc,
            }
        }
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "migrate vm %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "migrate vm %s: %s OK"
            % (eutil.bcolor(vmID), eutil.gcolor(response.status_code))
        )
        return True

    def getVMConsole(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/action"
        payload = {"os-getVNCConsole": {"type": "novnc"}}
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.error(
                "failed getting console for VM %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        return content["console"]["url"]

    def getOSInterfaces(self, vmID):
        requestURL = self.serversURL + "/" + vmID + "/os-interface"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed getting os-interface info for VM %s: %s"
                % (eutil.bcolor(vmID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        return response

    def getPortIDFromNetID(self, vmID, networkID):
        response = self.getOSInterfaces(vmID)
        if not response:
            return None

        content = json.loads(response.content)

        for interface in content["interfaceAttachments"]:
            if interface["net_id"] == networkID:
                return interface["port_id"]

        return None


class Flavors(NovaBase):
    def __init__(self, projectID):
        super().__init__(projectID)
        self.flavorsURL = self.serviceURL + "/nova/v2.1/" + self.projectID + "/flavors"

    def getFlavorsDetail(self):
        requestURL = self.flavorsURL + "/detail"
        return self.client.get(requestURL)

    def getBestMatchingFlavor(self, numCPU, memMB):
        elog.debug(
            "fetching best matching flavor having cpu=%s, ram=%s" % (numCPU, memMB)
        )
        response = self.getFlavorsDetail()
        if not response.ok:
            elog.error(
                "fetching flavor details failed: %s"
                % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        dflavor = {}
        content = json.loads(response.content)
        for flavors in content["flavors"]:
            dflavor[flavors["id"]] = [flavors["vcpus"], flavors["ram"]]

        if not dflavor:
            return None

        bestMatchFlavor = []
        flavorID = ""
        for key, lvalues in dflavor.items():
            flCPU = lvalues[0]
            flMEM = lvalues[1]
            if numCPU <= flCPU and memMB <= flMEM:
                if (
                    not bestMatchFlavor
                    or flCPU < bestMatchFlavor[0]
                    or flMEM < bestMatchFlavor[1]
                ):
                    bestMatchFlavor = []
                    flavorID = key
                    bestMatchFlavor.append(flCPU)
                    bestMatchFlavor.append(flMEM)

        if bestMatchFlavor:
            return flavorID
        return None
