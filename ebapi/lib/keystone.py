#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import json
import requests

from ebapi.common import utils as eutil
from ebapi.common.config import ConfigParser
from ebapi.common.logger import elog
from ebapi.common.rest import RestClient


class KeystoneBase(ConfigParser):
    """
    class that implements CRUD operation for keystone.
    """

    def __init__(self):
        super().__init__()
        serviceURL = self.getServiceURL()
        keystoneVer = "/keystone/v3"
        self.keystoneURL = serviceURL + keystoneVer
        self.apiURL = self.getApiURL()
        self.clusterID = self.getClusterID()
        self.clusterURL = self.apiURL + "/v2/clusters/" + self.clusterID


class Token(KeystoneBase):
    """
    class that implements CRUD operation for Token.
    """

    def __init__(
        self, scope="system", domainName="", user="", password="", projectName=""
    ):
        super().__init__()
        self.scope = scope
        self.domainName = domainName
        self.projectName = projectName
        self.user = user
        self.password = password

        if not self.domainName:
            self.domainName = self.getDomainName()
        if not self.projectName:
            self.projectName = self.getProjectName()
        if not self.user:
            self.user = self.getProjectAdmin()
        if not self.password:
            self.password = self.getProjectAdminPassword()

        self.tokenURL = self.keystoneURL + "/auth/tokens"
        self.token = self.getToken()

    def getPayloadWithSystemScope(self):
        # return payload with system scope
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {"name": self.domainName},
                            "name": self.user,
                            "password": self.password,
                        }
                    },
                },
                "scope": {"system": {"all": True}},
            }
        }
        return payload

    def getPayloadWithDomainScope(self):
        # return payload with domain scope
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {"name": self.domainName},
                            "name": self.user,
                            "password": self.password,
                        }
                    },
                },
                "scope": {"domain": {"name": self.domainName}},
            }
        }
        return payload

    def getPayloadWithProjectScope(self):
        # return payload with project scope
        payload = {
            "auth": {
                "identity": {
                    "methods": ["password"],
                    "password": {
                        "user": {
                            "domain": {"name": self.domainName},
                            "name": self.user,
                            "password": self.password,
                        }
                    },
                },
                "scope": {
                    "project": {
                        "name": self.projectName,
                        "domain": {"name": self.domainName},
                    }
                },
            }
        }
        return payload

    def getToken(self):
        """
        Returns:
            method that returns a project or domain scope token. default is
            domain scope token.

        Examples:
            domain level scope::

                tokenObj = Token('domain', domainName, userName, userPassword)

            project level scope::

                tokenObj = Token('project', domainName, userName, userPassword,
                                 projectName,)
        """
        payload = ""
        if self.scope == "system":
            payload = self.getPayloadWithSystemScope()
        elif self.scope == "domain":
            payload = self.getPayloadWithDomainScope()
        else:
            payload = self.getPayloadWithProjectScope()

        payload = json.dumps(payload)
        headers = {"Accept": "application/json"}
        elog.debug("token url:%s, paylod:%s", self.tokenURL, payload)
        response = requests.post(
            self.tokenURL, headers=headers, data=payload, timeout=30
        )
        if not response.ok:
            elog.error("failed to fetch token: %s" % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return None

        return response.headers["X-Subject-Token"]


class Roles(Token):
    def __init__(self):
        testConfig = ConfigParser()
        cloudAdmin = testConfig.getCloudAdmin()
        cloudAdminPass = testConfig.getCloudAdminPassword()
        super().__init__("system", "admin.local", cloudAdmin, cloudAdminPass)
        self.client = RestClient(self.getToken())
        self.rolesURL = self.keystoneURL + "/roles"

    def get(self):
        elog.info("fetching roles")

        response = self.client.get(self.rolesURL)
        if not response.ok:
            elog.error("failed to get roles: %s" % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return None

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content

    def assign(self, domainID, userID, roleID):
        elog.info(
            "assigning role %s to user %s in domain %s"
            % (eutil.bcolor(roleID), eutil.bcolor(userID), eutil.bcolor(domainID))
        )

        # send role assign request
        userURL = "/users/" + userID
        roleURL = "/roles/" + roleID
        domainURL = "/domains/" + domainID
        requestURL = self.keystoneURL + domainURL + userURL + roleURL
        response = self.client.put(requestURL)
        if not response.ok:
            elog.error(
                "failed to assign role %s to user %s in domain %s: %s"
                % (
                    eutil.bcolor(roleID),
                    eutil.bcolor(userID),
                    eutil.bcolor(domainID),
                    eutil.rcolor(response.status_code),
                )
            )
            elog.error(response.text)
            return False

        elog.info(
            "assigned role %s to user %s in domain %s"
            % (eutil.bcolor(roleID), eutil.bcolor(userID), eutil.bcolor(domainID))
        )
        return True


class Users(Token):
    def __init__(self):
        testConfig = ConfigParser()
        cloudAdmin = testConfig.getCloudAdmin()
        cloudAdminPass = testConfig.getCloudAdminPassword()
        super().__init__("system", "admin.local", cloudAdmin, cloudAdminPass)
        self.client = RestClient(self.getToken())
        self.usersURL = self.keystoneURL + "/users"

    def create(self, domainID, userName, password):
        elog.info(
            "creating user %s in domain %s with password %s"
            % (eutil.bcolor(userName), eutil.bcolor(domainID), eutil.bcolor(password))
        )

        # prepare create user payload
        payload = {
            "user": {
                "name": userName,
                "email": "%s@%s.com" % (userName, domainID),
                "enabled": True,
                "password": password,
                "domain_id": domainID,
            }
        }

        # send create request
        response = self.client.post(self.usersURL, payload)
        if not response.ok:
            elog.error("failed to create user: %s" % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return None

        # parse userID from the received reponse
        content = json.loads(response.content)
        userID = content["user"]["id"]
        elog.info(
            "user [%s,%s] created successfully"
            % (eutil.bcolor(userName), eutil.bcolor(userID))
        )
        return userID

    def getURL(self, domainID):
        if not domainID:
            return self.usersURL

        return self.usersURL + "?domain_id=%s" % domainID

    def list(self, domainID=""):
        requestURL = self.getURL(domainID)
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get users from domain %s: %s"
                % (eutil.bcolor(domainID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        return json.loads(response.content)

    def delete(self, userID):
        elog.info("deleting user %s" % eutil.bcolor(userID))
        response = self.client.delete(self.usersURL + "/" + userID)
        if not response.ok:
            elog.error("failed to delete user: %s" % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return False

        elog.info(
            "deleting user %s: %s OK"
            % (eutil.bcolor(userID), eutil.gcolor(response.status_code))
        )
        return True


class Domains(Token):
    def __init__(self):
        testConfig = ConfigParser()
        cloudAdmin = testConfig.getCloudAdmin()
        cloudAdminPass = testConfig.getCloudAdminPassword()
        self.acctID = testConfig.getAcctID()
        super().__init__("system", "admin.local", cloudAdmin, cloudAdminPass)
        self.client = RestClient(self.getToken())
        self.domainURL = self.keystoneURL + "/domains"

    def create(self, domainName, description=None):
        payload = {"domain": {"name": domainName, "description": description}}
        elog.info("creating domain %s" % eutil.bcolor(domainName))
        response = self.client.post(self.domainURL, payload)
        if not response.ok:
            elog.error(
                "failed to create domain: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return None

        # while creating a new domain EB automatically assigns admin user
        # with admin role to the domain
        content = json.loads(response.content)
        domainID = content["domain"]["id"]
        elog.info(
            "domain %s created successfully: %s"
            % (eutil.bcolor(domainName), eutil.bcolor(domainID))
        )
        return domainID

    def update(self, domainID, description=None, enabled=False):
        payload = {"domain": {"description": description, "enabled": enabled}}
        elog.info("Updating domain %s" % eutil.bcolor(domainID))
        response = self.client.patch(self.domainURL + "/" + domainID, payload)
        if not response.ok:
            elog.error(
                "failed to update domain: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return False

        elog.info(
            "updating domain %s: %s OK"
            % (eutil.bcolor(domainID), eutil.gcolor(response.status_code))
        )
        return True

    def updateQuota(self, domainID=""):
        payload = {
            "acct_id": self.acctID,
            "cluster_id": self.clusterID,
            "entity_id": domainID,
            "entity_type": "domain",
            "quota_sets": {
                "compute_quota": {
                    "cores": 10,
                    "instances": 10,
                    "ram": 10240,
                    "key_pairs": -1,
                    "fixed_ips": -1,
                },
                "network_quota": {
                    "network": 10,
                    "security_group": -1,
                    "security_group_rule": -1,
                    "router": 10,
                    "floatingip": 10,
                },
                "storage_quota": {
                    "gigabytes": 10,
                    "volumes": 10,
                    "snapshots": 10,
                    "gigabytes_relhighiops_type": 10,
                    "gigabytes_relhighcap_type": 10,
                    "gigabytes_highcap_type": 10,
                    "gigabytes_highiops_type": 10,
                },
                "selectedTemplate": "Custom",
            },
        }
        elog.info("Updating quota of domain %s" % eutil.bcolor(domainID))
        response = self.client.put(
            self.clusterURL + "/domains/" + domainID + "/quotas", payload
        )
        if not response.ok:
            elog.error(
                "failed to update quota of domain: %s"
                % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return False

        elog.info(
            "updating quota of domain %s: %s OK"
            % (eutil.bcolor(domainID), eutil.gcolor(response.status_code))
        )
        return True

    def delete(self, domainID):
        elog.info("deleting domain %s" % eutil.bcolor(domainID))
        response = self.client.delete(self.domainURL + "/" + domainID)
        if not response.ok:
            elog.error(
                "failed to delete domain: %s" % eutil.rcolor(response.status_code)
            )
            elog.error(response.text)
            return False

        elog.info(
            "deleting domain %s: %s OK"
            % (eutil.bcolor(domainID), eutil.gcolor(response.status_code))
        )
        return True

    def get(self, domainID=""):
        response = self.client.get(self.domainURL + "/" + domainID)
        if not response.ok:
            elog.error(
                "failed to get domain detail %s: %s"
                % (eutil.bcolor(domainID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        return json.loads(response.content)
