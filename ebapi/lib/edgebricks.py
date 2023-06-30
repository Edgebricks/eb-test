#! /usr/bin/env python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks Inc


import json
from time import sleep

from ebapi.common import utils as eutil
from ebapi.common.config import ConfigParser
from ebapi.common.logger import elog
from ebapi.common.rest import RestClient
from ebapi.lib.keystone import Token


class BUs(Token):
    # BU_STATE_UNKNOWN represents state unknown
    BU_STATE_UNKNOWN = 0
    # BU_STATE_ENABLED represents state enabled
    BU_STATE_ENABLED = 1
    # BU_STATE_DISABLED represents state disabled
    BU_STATE_DISABLED = 2
    # BU_STATE_DELETED represents state deleted
    BU_STATE_DELETED = 3
    # BU_STATE_CREATE_PENDING represents state to be created
    BU_STATE_CREATE_PENDING = 4
    # BU_STATE_CREATING represents state creating
    BU_STATE_CREATING = 5
    # BU_STATE_CREATED represents state created
    BU_STATE_CREATED = 6
    # BU_STATE_DELETE_PENDING represents state to be deleted
    BU_STATE_DELETE_PENDING = 7
    # BU_STATE_DELETING represents state error
    BU_STATE_DELETING = 8
    # BU_STATE_CREATE_ERROR represents state create error
    BU_STATE_CREATE_ERROR = 9
    # BU_STATE_DELETE_ERROR represents state delete error
    BU_STATE_DELETE_ERROR = 10
    # BU_STATE_ERROR represents state error
    BU_STATE_ERROR = 11

    def __init__(self):
        testConfig = ConfigParser()
        cloudAdmin = testConfig.getCloudAdmin()
        cloudAdminPass = testConfig.getCloudAdminPassword()
        self.apiURL = testConfig.getApiURL()
        self.acctID = testConfig.getAcctID()
        self.clusterID = testConfig.getClusterID()

        super(BUs, self).__init__("system", "admin.local", cloudAdmin, cloudAdminPass)
        self.client = RestClient(self.getToken())
        self.clusterURL = self.apiURL + "/v2/clusters/" + self.clusterID
        self.buURL = self.clusterURL + "/domains"

    def create(self, buName=None, userName=None, userPwd=None, desc=None):
        elog.info("creating business unit %s" % eutil.bcolor(buName))

        # prepare create payload
        if buName is None:
            buName = "ebtestdomain"
        if userName is None:
            userName = "ebtest"
        if userPwd is None:
            userPwd = "ebtest"
        if desc is None:
            desc = "created by ebtest"
        payload = {
            "domain": {"name": buName, "description": desc},
            "user": {
                "email": "ebtest@edgebricks.com",
                "enabled": True,
                "name": userName,
                "password": userPwd,
                "provider": "local",
            },
        }

        # send create request
        response = self.client.post(self.buURL, payload)
        if not response.ok:
            elog.error(
                "failed to create business unit %s :: %s"
                % (eutil.rcolor(buName), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        buID = json.loads(response.content)
        elog.info(
            "business unit [%s,%s] create request sent successfully: %s OK"
            % (
                eutil.bcolor(buName),
                eutil.bcolor(buID),
                eutil.gcolor(response.status_code),
            )
        )
        return buID

    def waitForState(self, buID, state=None, timeoutInSec=None, sleepInSec=None):

        elog.info(
            "waiting for business unit %s state to be %s"
            % (eutil.bcolor(buID), eutil.gcolor(state))
        )

        if timeoutInSec is None:
            timeoutInSec = 150  # 2mins 30secs
        if sleepInSec is None:
            sleepInSec = 15  # 15secs

        curIteration = 1
        maxAllowedItr = timeoutInSec / sleepInSec
        while True:
            buRsp = self.get(buID)
            if buRsp is None:
                elog.error("business unit [%s] not found" % eutil.rcolor(buID))
                return None

            buName = buRsp["name"]
            buState = buRsp["domain_state"]
            if buState == state:
                elog.info(
                    "business unit [%s,%s] is in desired state [%s]"
                    % (eutil.bcolor(buName), eutil.bcolor(buID), eutil.gcolor(state))
                )
                break

            # break after maximum allowed iterations and report failure
            if curIteration > maxAllowedItr:
                elog.error(
                    "business unit [%s] failed to get desired state %s"
                    % (eutil.rcolor(buID), eutil.rcolor(state))
                )
                return None

            sleep(10)
            curIteration = curIteration + 1

        return True

    def delete(self, buID):
        elog.info("deleting business unit %s" % eutil.bcolor(buID))

        # send delete request
        response = self.client.delete(self.buURL + "/" + buID)
        if not response.ok:
            elog.error(
                "failed to delete business unit %s :: %s"
                % (eutil.rcolor(buID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "business unit %s delete request submitted successfully: %s OK"
            % (eutil.bcolor(buID), eutil.gcolor(response.status_code))
        )

        return True

    def get(self, buID=""):
        elog.info("fetching business unit %s" % (eutil.bcolor(buID)))

        # send get request
        response = self.client.get(self.buURL + "/" + buID)
        if not response.ok:
            elog.error(
                "failed to get business unit details %s :: %s"
                % (eutil.rcolor(buID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content

    def update(self, buID, desc=None, enabled=True):
        elog.info("updating business unit %s" % eutil.bcolor(buID))

        # prepare update payload
        payload = {"description": desc, "enabled": enabled}

        # send update request
        response = self.client.patch(self.buURL + "/" + buID, payload)
        if not response.ok:
            elog.error(
                "failed to update business unit %s :: %s"
                % (eutil.rcolor(buID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "updating business unit %s: %s OK"
            % (eutil.bcolor(buID), eutil.gcolor(response.status_code))
        )

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content


class Projects(Token):
    # PROJ_STATE_UNKNOWN represents state unknown
    PROJ_STATE_UNKNOWN = 0
    # PROJ_STATE_ENABLED represents state enabled
    PROJ_STATE_ENABLED = 1
    # PROJ_STATE_DISABLED represents state disabled
    PROJ_STATE_DISABLED = 2
    # PROJ_STATE_DELETED represents state deleted
    PROJ_STATE_DELETED = 3
    # PROJ_STATE_ARCHIVED represents state archived
    PROJ_STATE_ARCHIVED = 4
    # PROJ_STATE_CREATE_PENDING represents state to be created
    PROJ_STATE_CREATE_PENDING = 5
    # PROJ_STATE_CREATING represents state creating
    PROJ_STATE_CREATING = 6
    # PROJ_STATE_CREATED represents state created
    PROJ_STATE_CREATED = 7
    # PROJ_STATE_DELETE_PENDING represents state to be deleted
    PROJ_STATE_DELETE_PENDING = 8
    # PROJ_STATE_DELETING represents state error
    PROJ_STATE_DELETING = 9
    # PROJ_STATE_CREATE_ERROR represents state create error
    PROJ_STATE_CREATE_ERROR = 10
    # PROJ_STATE_DELETE_ERROR represents state delete error
    PROJ_STATE_DELETE_ERROR = 11
    # PROJ_STATE_ERROR represents state error
    PROJ_STATE_ERROR = 12

    def __init__(self, buName, projAdmin, projAdminPass):
        super(Projects, self).__init__("domain", buName, projAdmin, projAdminPass)
        self.client = RestClient(self.getToken())
        self.apiURL = self.getApiURL()
        self.clusterID = self.getClusterID()
        self.clusterURL = self.apiURL + "/v2/clusters/" + self.clusterID
        self.projectURL = self.clusterURL + "/projects"
        self.projectNewURL = self.clusterURL + "/projectsnew"

    def create(
        self,
        projName,
        buID,
        metadata="",
        compQuota="",
        strQuota="",
        netQuota="",
        duration=False,
        desc=None,
    ):
        elog.info(
            "creating project %s in business unit %s"
            % (eutil.bcolor(projName), eutil.bcolor(buID))
        )

        # prepare create payload
        if desc is None:
            desc = "created by ebtest"
        payload = {
            "name": projName,
            "domain_id": buID,
            "description": desc,
            "finite_duration": duration,
        }
        if metadata:
            payload["metadata"] = metadata

        if compQuota or strQuota or netQuota:
            payload["quota"] = {}

        if compQuota:
            payload["quota"]["compute_quota"] = compQuota

        if strQuota:
            payload["quota"]["storage_quota"] = strQuota

        if netQuota:
            payload["quota"]["network_quota"] = netQuota

        # send create request
        response = self.client.post(self.projectNewURL, payload)
        if not response.ok:
            elog.error(
                "failed to create project %s :: %s"
                % (eutil.rcolor(projName), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        # parse projID from the received response
        projID = json.loads(response.content)
        elog.info(
            "project [%s,%s] created successfully"
            % (eutil.bcolor(projName), eutil.bcolor(projID))
        )
        return projID

    def waitForState(self, projID, state=None, timeoutInSec=None, sleepInSec=None):

        elog.info(
            "waiting for project %s state to be %s"
            % (eutil.bcolor(projID), eutil.gcolor(state))
        )

        if timeoutInSec is None:
            timeoutInSec = 150  # 2mins 30secs
        if sleepInSec is None:
            sleepInSec = 15  # 15secs

        curIteration = 1
        maxAllowedItr = timeoutInSec / sleepInSec
        while True:
            projRsp = self.get(projID)
            if projRsp is None:
                elog.error("project [%s] not found" % eutil.rcolor(projID))
                return None

            projName = projRsp["name"]
            projState = projRsp["project_state"]
            if projState == state:
                elog.info(
                    "project [%s,%s] is in desired state [%s]"
                    % (
                        eutil.bcolor(projName),
                        eutil.bcolor(projID),
                        eutil.gcolor(state),
                    )
                )
                break

            # break after maximum allowed iterations and report failure
            if curIteration > maxAllowedItr:
                elog.error(
                    "project [%s] failed to get desired state %s"
                    % (eutil.rcolor(projID), eutil.rcolor(state))
                )
                return None

            sleep(10)
            curIteration = curIteration + 1

        return True

    def delete(self, projID):
        elog.info("deleting project %s" % eutil.bcolor(projID))

        # send delete request
        response = self.client.deleteWithPayload(self.projectNewURL + "/" + projID)
        if not response.ok:
            elog.error(
                "failed to delete project %s :: %s"
                % (eutil.rcolor(projID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return False

        elog.info(
            "project %s delete request submitted successfully: %s OK"
            % (eutil.bcolor(projID), eutil.gcolor(response.status_code))
        )
        return True

    def list(self, buID):
        elog.info("fetching projects in business unit %s" % eutil.bcolor(buID))

        # send list request
        requestURL = self.clusterURL + "/domains" + "/%s/projects" % buID
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get projects from business unit %s :: %s"
                % (eutil.rcolor(buID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content

    def get(self, projID):
        elog.info("fetching project %s" % eutil.bcolor(projID))

        # send get request
        requestURL = self.projectURL + "/%s" % projID
        response = self.client.get(requestURL)
        if not response.ok:
            elog.error(
                "failed to get project details %s :: %s"
                % (eutil.rcolor(projID), eutil.rcolor(response.status_code))
            )
            elog.error(response.text)
            return None

        # display received response
        content = json.loads(response.content)
        elog.info(content)
        return content
