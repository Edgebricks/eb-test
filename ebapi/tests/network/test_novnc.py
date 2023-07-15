#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import json
import re
from urllib.parse import urlparse
import pytest

from ebapi.common import utils as eutil
from ebapi.common.commands import RemoteMachine
from ebapi.common.config import ConfigParser
from ebapi.common.rest import RestClient
from ebapi.common.logger import elog
from ebapi.lib import keystone
from ebapi.lib import nova


# test settings:
# set password or keyFile, not both
nginxIP = ""
vncPublicIP = ""
vncPublicPort = 26000
# credentials for vncPublicIP server
userName = ""
password = ""
keyFile = ""
testConfig = ConfigParser()
projectID = testConfig.getProjectID()


@pytest.fixture(scope="module")
def setup_test():
    notset = False
    testParams = {
        "nginxIP": nginxIP,
        "userName": userName,
        "vncPublicIP": vncPublicIP,
        "vncPublicPort": vncPublicPort,
    }

    for key, value in testParams.items():
        if not value:
            elog.error("%s not set" % key)
            notset = True

    if notset:
        pytest.skip("test params not set")


def test_privateAccess():
    serverObj = nova.Servers(projectID)
    servers = serverObj.getAllServers()
    assert servers
    elog.info(
        "list of VMS: %s" % eutil.bcolor(json.dumps(servers, sort_keys=True, indent=4))
    )
    serverID = servers.keys().pop()
    vncURL = serverObj.getServerConsole(serverID)
    assert vncURL
    elog.info("server console URL: %s" % eutil.bcolor(vncURL))

    consoleURL = urlparse(vncURL)
    assert consoleURL.port == 26000
    assert consoleURL.hostname == nginxIP
    elog.info("console URL has correct nginxIP and publicPort number")


def test_publicAccess():
    firewall = None
    if password:
        firewall = RemoteMachine(vncPublicIP, userName, password)
    elif keyFile:
        firewall = RemoteMachine(vncPublicIP, userName, keyfile=keyFile)
    else:
        pytest.skip("set test param password or keyFile")

    admin = testConfig.getCloudAdmin()
    adminPass = testConfig.getCloudAdminPassword()
    tokenObj = keystone.Token("domain", "admin.local", admin, adminPass)
    token = tokenObj.getToken()

    apiURL = testConfig.getConfig("apiURL")
    clusterID = testConfig.getConfig("clusterID")
    clusterURL = apiURL + "/v1/regions/" + clusterID + "/azs/" + clusterID
    vncURL = clusterURL + "/setup_publicvncaccess"
    payload = {"vnc_public_ip": vncPublicIP, "vnc_public_port": vncPublicPort}

    client = RestClient(token)
    response = client.put(vncURL, payload, timeout=60)
    if not response.ok:
        elog.error(eutil.rcolor(response.text))
        assert False
    elog.info("setting up public vnc access succeeded")

    rc, out = firewall.run("ip route show | grep default")
    assert rc == 0
    dev = re.findall(r"dev (\S+)", out, re.M)
    dev = dev[0]
    rc, out = firewall.run("ifconfig %s" % dev)
    assert rc == 0
    privateIP = re.findall(r"inet (\S+)", out, re.M)
    privateIP = privateIP[0]

    # port forwarding using iptables
    rule = "iptables -A PREROUTING -t nat -p tcp "
    opts = "-i %s --dport %s -j DNAT --to %s:26000" % (dev, vncPublicPort, nginxIP)
    cmd = rule + opts
    rc, _ = firewall.run(cmd)
    assert rc == 0

    rule = "iptables -A POSTROUTING -t nat -p tcp "
    opts = "-o %s --dport %s -d %s -j SNAT --to-source %s" % (
        dev,
        vncPublicPort,
        nginxIP,
        privateIP,
    )
    cmd = rule + opts
    rc, _ = firewall.run(cmd)
    assert rc == 0

    serverObj = nova.Servers(projectID)
    servers = serverObj.getAllServers()
    elog.info(
        "list of VMS: %s" % eutil.bcolor(json.dumps(servers, sort_keys=True, indent=4))
    )
    serverID = servers.keys().pop()
    vncURL = serverObj.getServerConsole(serverID)
    elog.info("server console URL: %s" % eutil.bcolor(vncURL))

    consoleURL = urlparse(vncURL)
    assert (consoleURL.port == vncPublicPort) and (consoleURL.hostname == vncPublicIP)
    elog.info("console URL has correct publicIP and publicPort number")
