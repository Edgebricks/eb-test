#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import json

from ebtest.common import utils as eutil
from ebtest.common import logger as elog
from ebtest.common.rest import RestClient
from ebtest.lib.keystone import Token


class NovaBase(Token):
    def __init__(self, projectID, scope='domain'):
        super(NovaBase, self).__init__(scope)
        self.client     = RestClient(self.getToken())
        self.projectID  = projectID
        self.serviceURL = self.getServiceURL()
        self.novaURL    = self.serviceURL + '/nova/v2/' + self.projectID


class Servers(NovaBase):
    def __init__(self, projectID):
        super(Servers, self).__init__(projectID)
        self.serversURL  = self.novaURL + '/servers'

    def getAllServers(self):
        response = self.client.get(self.serversURL)
        if not response.ok:
            elog.logging.error('failed to get all VMs: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return None

        content = json.loads(response.content)
        servers = {}
        for server in content['servers']:
            servers[server['id']] = server['name']

        return servers

    def getServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID
        return self.client.get(requestURL)

    def getFloatingIPFromVMID(self, vmID):
        requestURL = self.novaURL + '/os-floating-ips'
        response   = self.client.get(requestURL)
        if not response.ok:
            elog.logging.error('failed fetching server details for %s: %s'
                       % (eutil.bcolor(vmID),
                          eutil.rcolor(response.status_code)))
            return None

        content = json.loads(response.content)
        for floatingIP in content['floating_ips']:
            instanceID = floatingIP['instance_id']
            if instanceID == vmID:
                return floatingIP['ip']

        elog.logging.error('no floating IP assigned to %s' % eutil.bcolor(vmID))
        return None

    def getVMIDFromFloatingIP(self, fip):
        requestURL = self.novaURL + '/os-floating-ips'
        response   = self.client.get(requestURL)
        if not response.ok:
            elog.logging.error('failed fetching server details for %s: %s'
                       % (eutil.bcolor(fip),
                          eutil.rcolor(response.status_code)))
            return None

        content = json.loads(response.content)
        for floatingIP in content['floating_ips']:
            ip = floatingIP['ip']
            if ip == fip:
                return floatingIP['instance_id']

        elog.logging.error('no vm assigned with floatingIP %s' % eutil.bcolor(fip))
        return None

    def getMacAddrFromIP(self, vmID, ipAddr):
        response = self.getServer(vmID)
        if not response.ok:
            elog.logging.error('fetching server details for %s: %s'
                       % (eutil.bcolor(vmID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content = json.loads(response.content)
        for netname in content['server']['addresses']:
            for element in content['server']['addresses'][netname]:
                if element['addr'] == ipAddr:
                    return element['OS-EXT-IPS-MAC:mac_addr']

        elog.logging.error('not mac address found for %s' % eutil.bcolor(ipAddr))
        return None

    def getVolumesAttached(self, vmID):
        response = self.getServer(vmID)
        if not response.ok:
            elog.logging.error('fetching server details for %s: %s'
                       % (eutil.bcolor(vmID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content  = json.loads(response.content)
        lvolumes = []
        for vols in content['server']['os-extended-volumes:volumes_attached']:
            lvolumes.append(vols['id'])

        return lvolumes

    def getStatus(self, vmID):
        response = self.getServer(vmID)
        if not response.ok:
            elog.logging.error('fetching server details for %s: %s'
                       % (eutil.bcolor(vmID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content  = json.loads(response.content)
        return content['server']['status']

    def getHost(self, vmID):
        response = self.getServer(vmID)
        if not response.ok:
            elog.logging.error('fetching server details for %s: %s'
                       % (eutil.bcolor(vmID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content  = json.loads(response.content)
        return content['server']['OS-EXT-SRV-ATTR:host']

    def deleteServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID
        response   = self.client.delete(requestURL)
        if not response.ok:
            elog.logging.error('deleting vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('deleting vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def suspendServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"suspend": ""}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('suspending vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('suspending vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def resumeServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"resume": ""}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('resuming vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('resuming vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def rebootServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"reboot":{"type":"SOFT"}}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('reboot vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('reboot vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def powerOffServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"os-stop": ""}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('poweroff vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('poweroff vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def powerOnServer(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"os-start": ""}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('poweron vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('poweron vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def migrateServer(self, serverID, doc=False, bm=False, host=None):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {
            "os-migrateLive": {
                "host"            : host,
                "block_migration" : bm,
                "disk_over_commit": doc
            }
        }
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('migrate vm %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('migrate vm %s: %s OK'
                  % (eutil.bcolor(serverID),
                     eutil.gcolor(response.status_code)))
        return True

    def getServerConsole(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/action'
        payload    = {"os-getVNCConsole": {"type": "novnc"}}
        response   = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('failed getting console for server %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content = json.loads(response.content)
        return content['console']['url']

    def getOSInterfaces(self, serverID):
        requestURL = self.serversURL + '/' + serverID + '/os-interface'
        response   = self.client.get(requestURL)
        if not response.ok:
            elog.logging.error('failed getting os-interface info for server %s: %s'
                       % (eutil.bcolor(serverID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        return response

    def getPortIDFromNetID(self, serverID, networkID):
        response = self.getOSInterfaces(serverID)
        if not response:
            return None

        content = json.loads(response.content)

        for interface in content['interfaceAttachments']:
            if interface['net_id'] == networkID:
                return interface['port_id']

        return None


class Flavors(NovaBase):
    def __init__(self, projectID):
        super(Flavors, self).__init__(projectID)
        self.flavorsURL =  self.novaURL + '/flavors'

    def getFlavorsDetail(self):
        requestURL = self.flavorsURL + '/detail'
        return self.client.get(requestURL)

    def getBestMatchingFlavor(self, numCPU, memMB):
        response = self.getFlavorsDetail()
        if not response.ok:
            elog.logging.error('fetching flavor details: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return None

        dflavor = {}
        content = json.loads(response.content)
        for flavors in content['flavors']:
            dflavor[flavors['id']] = [flavors['vcpus'], flavors['ram']]

        if not dflavor:
            return None

        bestMatchFlavor = []
        flavorID = ''
        for key, lvalues in dflavor.items():
            flCPU = lvalues[0]
            flMEM = lvalues[1]
            if numCPU <= flCPU and memMB <= flMEM:
                if not bestMatchFlavor or flCPU < bestMatchFlavor[0] or \
                        flMEM < bestMatchFlavor[1]:
                    bestMatchFlavor = []
                    flavorID        = key
                    bestMatchFlavor.append(flCPU)
                    bestMatchFlavor.append(flMEM)

        if bestMatchFlavor:
            return flavorID
        else:
            return None
