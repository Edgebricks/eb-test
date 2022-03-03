#! /usr/bin/python
#
# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


import pytest

from ebtest.common.config import ConfigParser
from ebtest.lib.keystone import Domains
from ebtest.lib.keystone import Roles
from ebtest.lib.keystone import Users
from ebtest.lib.edgebricks import Projects


def test_create_domain_project():
    testConfig       = ConfigParser()
    domainName       = testConfig.getDomainName()
    projectName      = testConfig.getProjectName()
    projectAdmin     = testConfig.getProjectAdmin()
    projectAdminPass = testConfig.getProjectAdminPassword()

    domainObj = Domains()
    domainID  = domainObj.createDomain(domainName)
    assert domainID
    testConfig.setDomainID(domainID)

    userObj = Users()
    userID  = userObj.createUser(domainID, projectAdmin, projectAdminPass)
    assert userID

    adminUserID = ''
    content = userObj.getUsers()
    for user in content['users']:
        if user['name'] == 'admin':
            adminUserID = user['id']
            break

    assert adminUserID

    roleObj = Roles()
    content = roleObj.getRoles()
    roleID = ''
    for role in content['roles']:
        if role['name'] == 'admin':
            roleID = role['id']
            break

    assert roleID

    # assign admin role to user admin
    assert roleObj.assignRole(domainID, userID, roleID)
    assert roleObj.assignRole(domainID, adminUserID, roleID)

    projObj = Projects(domainName, projectAdmin, projectAdminPass)

    metadata = {
        "templateId": "Large",
        "approval_pending": "false",
        "custom_template": "true"
    }
    compQuota = {
        "cores": 128,
        "floating_ips": 64,
        "injected_file_content_bytes": -1,
        "injected_file_path_bytes": -1,
        "injected_files": -1,
        "instances": 64,
        "key_pairs": -1,
        "metadata_items": -1,
        "ram": 262144
    }

    strQuota = {
        "backup_gigabytes": -1,
        "backups": -1,
        "snapshots": 640,
        "volumes": 640,
        "gigabytes": 25600
    }

    netQuota = {
        "subnet": -1,
        "router": 30,
        "port": -1,
        "network": 30,
        "floatingip": 64,
        "vip": -1,
        "pool": -1
    }

    projID = projObj.createProject(projectName, domainID, metadata,
                                   compQuota, strQuota, netQuota)
    assert projID
    testConfig.setProjectID(projID)
