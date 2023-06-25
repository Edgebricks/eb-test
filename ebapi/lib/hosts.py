#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import json

from ebapi.common import utils as eutil
from ebapi.common.logger import elog
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class HostsBase(Token):
    def __init__(self, scope="project"):
        super(HostsBase, self).__init__(scope)
        self.client = RestClient(self.getToken())
        self.apiURL = self.getApiURL()
        self.clusterID = self.getClusterID()
        self.clusterURL = self.apiURL + "/v2/clusters/" + self.clusterID
        self.hostsURL = self.clusterURL + "/hosts"


class Hosts(HostsBase):
    def __init__(self):
        super(Hosts, self).__init__()

    def getHosts(self):
        requestURL = self.apiURL + "/v1/hosts"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get list of hosts: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        hosts = []
        content = json.loads(response.content)
        for host in content:
            hosts.append(host["id"])

        return hosts

    def getHostName(self, hostID):
        requestURL = self.apiURL + "/v1/hosts/" + hostID
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get details for host %s : %s"
                % (eutil.bcolor(hostID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        return content["name"]

    def getHostIPbyName(self, hostName):
        hosts = self.getHosts()
        hostID = None
        for host in hosts:
            hName = self.getHostName(host)
            if hName == hostName:
                hostID = host
                break

        requestURL = self.apiURL + "/v1/hosts/" + hostID
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get details for host %s : %s"
                % (eutil.bcolor(hostID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        return content["zhost_address"]

    def getDependentVMS(self, hostID):
        requestURL = self.hostsURL + "/" + hostID + "/dependent_vms"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get dependent VMS: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        content = json.loads(response.content)

        if not content:
            return None

        vms = []
        for item in content:
            vms.append(item["VM"]["id"])

        return vms

    def getHostStatus(self, hostID):
        requestURL = self.hostsURL + "/" + hostID + "/status"
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get host status: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        status = content["Status"]
        availability = content["NodeAvailability"]
        return status, availability

    def powerOFF(self, hostID):
        requestURL = self.hostsURL + "/" + hostID + "/power_off"
        response = self.client.put(requestURL)
        if not response.ok:
            elog.error(
                "failed to power off host: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return False

        return True

    def powerON(self, hostID):
        requestURL = self.hostsURL + "/" + hostID + "/power_on"
        response = self.client.put(requestURL)
        if not response.ok:
            elog.error(
                "failed to power on host: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return False

        return True
