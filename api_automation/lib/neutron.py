#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import json

from ebtest.common import utils as eutil
from ebtest.common import logger as elog
from ebtest.common.rest import RestClient
from ebtest.lib.keystone import Token


class NeutronBase(Token):
    def __init__(self, scope='domain'):
        super(NeutronBase, self).__init__(scope)
        self.client     = RestClient(self.getToken())
        self.serviceURL = self.getServiceURL()
        self.neutronURL = self.serviceURL + '/neutron/v2.0'
        self.apiURL     = self.getApiURL()
        self.clusterID  = self.getClusterID()
        self.clusterURL = self.apiURL + '/v2/clusters/' + self.clusterID


class Networks(NeutronBase):
    def __init__(self, projectID):
        super(Networks, self).__init__()
        self.projectID   =  projectID
        self.networksURL =  self.neutronURL + '/networks'
        self.tenantURL   = self.networksURL + '?tenant_id=' + self.projectID

    def getURL(self, filterStr):
        if not filterStr:
            return self.tenantURL
        return self.tenantURL + '&' + filterStr

    def getNetworksByFilter(self, filterStr=''):
        '''
        Returns a list of all networks for a specified filter.
        '''
        requestURL = self.getURL(filterStr)
        return self.client.get(requestURL)

    def _getNetworks(self, response):
        content   = json.loads(response.content)
        lnetworks = []
        for network in content['networks']:
            lnetworks.append(network['id'])

        return lnetworks

    def getInternalNetworks(self):
        response = self.getNetworksByFilter('router:external=False')
        if not response.ok:
            elog.logging.error('failed fetching internal networks: %s'
                       % eutil.rcolor(response.status_code))
            return None

        return self._getNetworks(response)

    def getExternalNetworks(self):
        response = self.getNetworksByFilter('router:external=True')
        if not response.ok:
            elog.logging.error('failed fetching external networks: %s'
                       % eutil.rcolor(response.status_code))
            return None

        return self._getNetworks(response)

    def createInternalNetwork(self, netName = '', subnetName = ''):
        payload = {
            "admin_state_up": True,
            "name": netName,
            "subnets": [
                {
                    "name": subnetName,
                    "enable_dhcp": True,
                    "gateway_ip": "192.168.150.1",
                    "ip_version": 4,
                    "cidr": "192.168.150.0/24",
                    "allocation_pools": [
                        {
                            "start": "192.168.150.2",
                            "end": "192.168.150.254"
                        }
                    ],
                    "dns_nameservers": [
                        "8.8.8.8"
                    ],
                    "tenant_id": self.projectID
                }
            ],
            "tenant_id": self.projectID,
            "visibility": "private",
            "project_id": self.projectID
        }
        elog.logging.info('creating internal private network %s' % eutil.bcolor(netName))
        response = self.client.post(self.clusterURL + '/networks', payload)
        if not response.ok:
            elog.logging.error('failed to create network: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return None

        content  = json.loads(response.content)
        networkID = content['id']
        elog.logging.info('network %s created successfully: %s'
                  % (eutil.bcolor(netName),
                     eutil.bcolor(networkID)))
        return networkID

    def deleteInternalNetwork(self, networkID):
        requestURL = self.clusterURL + '/networks/' + networkID
        response   = self.client.deleteWithPayload(requestURL)
        if not response.ok:
            elog.logging.error('deleting network %s failed: %s'
                       % (eutil.rcolor(networkID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        elog.logging.info('deleting network %s success: %s'
                  % (eutil.bcolor(networkID),
                     eutil.gcolor(response.status_code)))
        return True

    def getNetwork(self, networkID):
        requestURL = self.networksURL + '/' + networkID
        return self.client.get(requestURL)

    def getNetworkByName(self, networkID):
        response = self.getNetwork(networkID)
        if not response.ok:
            elog.logging.error('failed fetching network %s: %s'
                       % (eutil.bcolor(networkID),
                          eutil.rcolor(response.status_code)))
            return None

        content = json.loads(response.content)
        return content['network']['name']


class Subnets(NeutronBase):
    def __init__(self):
        super(Subnets, self).__init__()


class Ports(NeutronBase):
    def __init__(self, projectID):
        super(Ports, self).__init__()
        self.projectID = projectID
        self.portsURL  = self.neutronURL + '/ports'

    def getURL(self, filterStr):
        if not filterStr:
            return self.portsURL
        return self.portsURL + '?' + filterStr

    def getPortsByFilter(self, filterStr=''):
        '''
        Returns a list of all ports for a specified filter.
        '''
        requestURL = self.getURL(filterStr)
        return self.client.get(requestURL)

    def getPorts(self):
        filterStr = 'tenant_id=' + self.projectID
        return self.getPortsByFilter(filterStr)

    def getPortIDByMacAddress(self, macAddress):
        filterStr = 'mac_address=' + macAddress
        response  = self.getPortsByFilter(filterStr)
        if not response.ok:
            elog.logging.error('failed to get fetch ports: %s'
                       % eutil.rcolor(response.status_code))
            return None

        content   = json.loads(response.content)
        try:
            portID    = content['ports'][0]['id']
            return portID
        except:
            return None

    def deletePort(self, portID):
        requestURL = self.portsURL + '/' + portID
        return self.client.delete(requestURL)

    def attachQoSPolicy(self, portID, policyID):
        requestURL = self.portsURL + '/' + portID
        payload    = {
            "port": {
                "qos_policy_id": policyID
            }
        }

        response = self.client.put(requestURL, payload)
        if not response.ok:
            elog.logging.error('failed to attach QoS policy %s to port %s: %s'
                       % (eutil.bcolor(policyID),
                          eutil.bcolor(portID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        content     = json.loads(response.content)
        qosPolicyID = content['port']['qos_policy_id']

        if policyID != qosPolicyID:
            elog.logging.error('mismatch in qos_policy_id: given = %s: set = %s'
                       % (eutil.bcolor(policyID),
                          eutil.bcolor(qosPolicyID)))
            return False

        return True

    def detachQoSPolicy(self, portID):
        requestURL = self.portsURL + '/' + portID
        payload    = {
            "port": {
                "qos_policy_id": None
            }
        }

        response = self.client.put(requestURL, payload)
        if not response.ok:
            elog.logging.error('failed to detach QoS policy from port %s: %s'
                       % (eutil.bcolor(portID),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return False

        content     = json.loads(response.content)
        qosPolicyID = content['port']['qos_policy_id']
        if qosPolicyID:
            elog.logging.error('qos_policy_id is still set. should be empty')
            return False

        return True


class Routers(NeutronBase):
    def __init__(self, projectID):
        super(Routers, self).__init__()
        self.projectID   = projectID
        self.routersURL  = self.neutronURL + '/routers?tenant_id='
        self.routersURL += self.projectID

    def getURL(self, filterStr):
        if not filterStr:
            return self.routersURL
        return self.routersURL + '&' + filterStr

    def getRoutersByFilter(self, filterStr=''):
        '''
        Returns a list of all routers for a specified filter.
        '''
        requestURL = self.getURL(filterStr)
        return self.client.get(requestURL)

    def getAllRouters(self):
        response = self.getRoutersByFilter()
        if not response.ok:
            elog.logging.error('failed to get all routers for project %s: %s'
                       % (eutil.bcolor(self.projectID),
                          eutil.rcolor(response.status_code)))
            return None

        lrouters = []
        content  = json.loads(response.content)

        for router in content['routers']:
            lrouters.append(router['id'])

        return lrouters

    def getRouter(self, routerID):
        requestURL = self.neutronURL + '/routers' + '/' + routerID
        return self.client.get(requestURL)

    def getExternalNetworkIDFromRouter(self, routerID):
        response = self.getRouter(routerID)
        if not response.ok:
            eutil.error('failed getting router %s: %s'
                        % (eutil.bcolor(routerID),
                           eutil.rcolor(response.status_code)))
            return None

        content = json.loads(response.content)
        return content['router']['external_gateway_info']['network_id']


class FloatingIPs(NeutronBase):
    def __init__(self, projectID):
        super(FloatingIPs, self).__init__()
        self.projectID       = projectID
        self.floatingIPsURL  = self.neutronURL + '/floatingips?tenant_id='
        self.floatingIPsURL += self.projectID

    def getURL(self, filterStr):
        if not filterStr:
            return self.floatingIPsURL
        return self.floatingIPsURL + '&' + filterStr

    def getFloatingIPsByFilter(self, filterStr=''):
        '''
        Returns a list of all routers for a specified filter.
        '''
        requestURL = self.getURL(filterStr)
        return self.client.get(requestURL)

    def createFloatingIP(self, floatingNetID, vmPortID):
        payload = {
            "floatingip": {
                "floating_network_id": floatingNetID,
                "tenant_id": self.projectID,
                "port_id": vmPortID
            }
        }
        requestURL = self.neutronURL + '/floatingips'
        return self.client.post(requestURL, payload)

    def deleteFloatingIP(self, floatingIP):
        requestURL = self.neutronURL + '/floatingips/' + floatingIP
        return self.client.delete(requestURL)


class QoS(NeutronBase):
    def __init__(self):
        super(QoS, self).__init__()
        self.policyURL = self.neutronURL + '/qos/policies'

    def createPolicy(self, name, shared=False):
        payload = {
            "policy": {
                "name": name,
                "description": "policy for checking throttling",
                "shared": shared
            }
        }

        response = self.client.post(self.policyURL, payload)
        if not response.ok:
            elog.logging.error('failed to create QoS policy: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return None

        content  = json.loads(response.content)
        return content['policy']['id']

    def createBandwidthLimitRules(self, policyID, maxBurst, maxBandwidth):
        requestURL = self.policyURL + '/' + policyID + '/bandwidth_limit_rules'
        payload    = {
            "bandwidth_limit_rule": {
                "max_burst_kbps": maxBurst,
                "max_kbps": maxBandwidth
            }
        }
        response = self.client.post(requestURL, payload)
        if not response.ok:
            elog.logging.error('failed to create bandwidth limit rule: %s'
                       % eutil.rcolor(response.status_code))
            elog.logging.error(response.text)
            return False

        return True

    def deletePolicy(self, policyID):
        requestURL = self.policyURL + '/' + policyID
        response   = self.client.delete(requestURL)
        if not response.ok:
            elog.logging.error('failed to delete QoS policy: %s'
                       % eutil.rcolor(response.status_code))
            return False

        return True
