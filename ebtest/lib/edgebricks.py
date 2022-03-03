#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import json

from ebtest.common import utils as eutil
from ebtest.common import logger as elog
from ebtest.common.rest import RestClient
from ebtest.lib.keystone import Token


class Projects(Token):
    def __init__(self, domainName, projAdmin, projAdminPass):
        super(Projects, self).__init__('domain', domainName, projAdmin,
                                       projAdminPass)
        self.client     = RestClient(self.getToken())
        self.apiURL     = self.getApiURL()
        self.clusterID  = self.getClusterID()
        self.clusterURL = self.apiURL + '/v2/clusters/' + self.clusterID
        self.projectURL = self.clusterURL + '/projects'

    def createProject(self, projName, domainID, metadata='', compQuota='',
                      strQuota='', netQuota='', duration=False):
        payload = {
            "name"           : projName,
            "domain_id"      : domainID,
            "description"    : projName,
            "finite_duration": duration
        }

        if metadata:
            payload['metadata'] = metadata

        if compQuota or strQuota or netQuota:
            payload['quota'] = {}

        if compQuota:
            payload['quota']['compute_quota'] = compQuota

        if strQuota:
            payload['quota']['storage_quota'] = strQuota

        if netQuota:
            payload['quota']['network_quota'] = netQuota

        elog.logging.info('creating project %s in domain %s'
                  % (eutil.bcolor(projName), eutil.bcolor(domainID)))

        response = self.client.post(self.projectURL, payload)
        if not response.ok:
            elog.logging.error('failed to create project %s: %s'
                       % (eutil.bcolor(projName),
                          eutil.rcolor(response.status_code)))
            elog.logging.error(response.text)
            return None

        content = json.loads(response.content)
        projID  = content['id']
        elog.logging.info('project %s created: %s'
                  % (eutil.bcolor(projName), eutil.bcolor(projID)))

        return projID
