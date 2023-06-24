#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import json
from time import sleep

from ebapi.common import utils as eutil
from ebapi.common.config import ConfigParser
from ebapi.common.logger import elog
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class BUs(Token):
    def __init__(self):
        testConfig     = ConfigParser()
        cloudAdmin     = testConfig.getCloudAdmin()
        cloudAdminPass = testConfig.getCloudAdminPassword()
        self.apiURL     = testConfig.getApiURL()
        self.acctID     = testConfig.getAcctID()
        self.clusterID  = testConfig.getClusterID()

        super(BUs, self).__init__('system', 'admin.local', cloudAdmin, cloudAdminPass)
        self.client     = RestClient(self.getToken())
        self.clusterURL = self.apiURL + '/v2/clusters/' + self.clusterID
        self.buURL      = self.clusterURL + '/domains'

    def createBU(self, buName, description = None):
        payload = {
            "domain": {
                "name"        : buName,
                "description" : description,
            },
            "user": {
                "email": "ebtest@edgebricks.com",
                "enabled": True,
                "name": "ebtest",
                "password": "ebtest@123",
                "provider": "local"
            },
        }
        elog.info('creating business unit %s' % eutil.bcolor(buName))
        response = self.client.post(self.buURL, payload)
        if not response.ok:
            elog.error('failed to create business unit: %s'
                       % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return None

        buID  = json.loads(response.content)
        elog.info('business unit [%s,%s] create request submitted successfully: %s OK'
                  % (eutil.bcolor(buName), eutil.bcolor(buID), eutil.gcolor(response.status_code)))

        # wait for bu to be created
        elog.info('waiting for business unit %s to be created' % eutil.bcolor(buID))
        while True:
            sleep(10)
            buState = self.getBU(buID)['domain_state']
            if buState == 3:
                break
            # TODO(vikram): break after maximum timeout and report failure

        elog.info('business unit %s created successfully' % (eutil.bcolor(buID)))
        return buID

    def deleteBU(self, buID):
        elog.info('deleting buID %s' % eutil.bcolor(buID))
        response = self.client.delete(self.buURL+ '/' + buID)
        if not response.ok:
            elog.error('failed to delete business unit: %s'
                       % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return False

        elog.info('business unit %s delete request submitted successfully: %s OK'
                    % (eutil.bcolor(buID), eutil.gcolor(response.status_code)))

        # wait for bu to be created
        elog.info('waiting for business unit %s to be deleted' % eutil.bcolor(buID))
        while True:
            sleep(10)
            buState = self.getBU(buID)['domain_state']
            if buState == 8:
                break
            # TODO(vikram): break after maximum timeout and report failure

        elog.info('business unit %s deleted successfully' % (eutil.bcolor(buID)))
        return True

    def getBU(self, buID=''):
        response   = self.client.get(self.buURL+ '/' + buID)
        if not response.ok:
            elog.error('failed to get business unit detail %s: %s'
                       % (eutil.bcolor(buID),
                          eutil.rcolor(response.status_code)))
            elog.error(response.text)
            return None

        elog.info('fetching business unit %s: %s OK'
                  % (eutil.bcolor(buID),
                     eutil.gcolor(response.status_code)))
        content = json.loads(response.content)
        elog.info(content)
        return content

    def updateBU(self, buID, description = None, enabled=True):
        payload = {
            "description" : description,
            "enabled"     : enabled
        }
        elog.info('Updating business unit %s' % eutil.bcolor(buID))
        response = self.client.patch(self.buURL+ '/' + buID, payload)
        if not response.ok:
            elog.error('failed to update business unit: %s'
                       % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return False

        elog.info('updating business unit %s: %s OK'
                  % (eutil.bcolor(buID),
                     eutil.gcolor(response.status_code)))
        content = json.loads(response.content)
        elog.info(content)
        return content


class Projects(Token):
    def __init__(self, buName, projAdmin, projAdminPass):
        super(Projects, self).__init__('domain', buName, projAdmin,
                                       projAdminPass)
        self.client      = RestClient(self.getToken())
        self.apiURL      = self.getApiURL()
        self.clusterID   = self.getClusterID()
        self.clusterURL  = self.apiURL + '/v2/clusters/' + self.clusterID
        self.projectURL  = self.clusterURL + '/projects'
        serviceURL       = self.getServiceURL()
        keystoneVer      = '/keystone/v3'
        self.keystoneURL = serviceURL + keystoneVer

    def createProject(self, projName, buID, metadata='', compQuota='',
                      strQuota='', netQuota='', duration=False):
        payload = {
            "name"           : projName,
            "domain_id"      : buID,
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

        elog.info('creating project %s in business unit %s'
                  % (eutil.bcolor(projName), eutil.bcolor(buID)))

        response = self.client.post(self.projectURL, payload)
        if not response.ok:
            elog.error('failed to create project %s: %s'
                       % (eutil.bcolor(projName),
                          eutil.rcolor(response.status_code)))
            elog.error(response.text)
            return None

        content = json.loads(response.content)
        projID  = content['id']
        elog.info('project %s created: %s'
                  % (eutil.bcolor(projName), eutil.bcolor(projID)))

        return projID

    def deleteProject(self, projID):
        elog.info('deleting project %s' % eutil.bcolor(projID))
        response = self.client.deleteWithPayload(self.projectURL+ '/' + projID)
        if not response.ok:
            elog.error('failed to delete project: %s'
                       % eutil.rcolor(response.status_code))
            elog.error(response.text)
            return False

        elog.info('deleting project %s: %s OK'
                  % (eutil.bcolor(projID),
                     eutil.gcolor(response.status_code)))
        return True

    def getProject(self, userID='', buID=''):
        requestURL = self.keystoneURL + '/users' + '/%s/projects?domain_id=%s' % (userID, buID)
        response   = self.client.get(requestURL)
        if not response.ok:
            elog.error('failed to get projects from business unit %s: %s'
                       % (eutil.bcolor(buID),
                          eutil.rcolor(response.status_code)))
            elog.error(response.text)
            return None

        return json.loads(response.content)
