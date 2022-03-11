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


def test_create_domain_users_project():
    testConfig       = ConfigParser()
    domainName       = testConfig.getDomainName()
    projectName      = testConfig.getProjectName()
    projectAdmin     = testConfig.getProjectAdmin()
    projectAdminPass = testConfig.getProjectAdminPassword()

    ##### Create Domain ####
    domainObj = Domains()
    global domainID
    domainID = domainObj.createDomain(domainName)
    assert domainID
    testConfig.setDomainID(domainID)

    ##### Create User ####
    userObj = Users()
    global userID  
    userID = userObj.createUser(domainID, projectAdmin, projectAdminPass)
    assert userID

    ##### Get User ####
    adminUserID = ''
    content = userObj.getUsers()
    for user in content['users']:
        if user['name'] == testConfig.getCloudAdmin():
            adminUserID = user['id']
            break

    assert adminUserID
    
    ##### Get Roles ####
    roleObj = Roles()
    content = roleObj.getRoles()
    roleID = ''
    for role in content['roles']:
        if role['name'] == 'admin':
            roleID = role['id']
            break

    assert roleID

    # assign admin role to created user
    assert roleObj.assignRole(domainID, userID, roleID)
    # assert roleObj.assignRole(domainID, adminUserID, roleID)

    ##### Create Project ####
    projObj = Projects(domainName, projectAdmin, projectAdminPass)

    metadata = {
        "templateId": "Large",
        "custom_template": "true"
    }

    compQuota = {
        "cores": 128,
        "injected_file_content_bytes":-1,
        "injected_file_path_bytes":-1,
        "injected_files":-1,
        "instances": 64,
        "key_pairs": -1,
        "metadata_items":-1,
        "ram": 262144
    }

    strQuota = {
        "snapshots": 640,
        "backup_gigabytes":-1,
        "backups":-1,
        "volumes": 640,
        "gigabytes": 25600
    }

    netQuota = {
        "router": 30,
        "subnet":-1,
        "network": 30,
        "port":-1,
        "floatingip": 64,
        "pool":-1
    }

    global projID
    projID = projObj.createProject(projectName, domainID, metadata,
                                   compQuota, strQuota, netQuota)
    assert projID
    testConfig.setProjectID(projID)


def test_delete_domain_users_project():
    testConfig       = ConfigParser()
    domainName       = testConfig.getDomainName()
    projectName      = testConfig.getProjectName()
    projectAdmin     = testConfig.getProjectAdmin()
    projectAdminPass = testConfig.getProjectAdminPassword()

    ##### Delete Project ####    
    projObj = Projects(domainName, projectAdmin, projectAdminPass)
    content = projObj.getProject(userID, domainID)

    projID = ''
    for project in content['projects']:
        if project['name'] == projectName:
            projID = project['id']
            break
    assert projObj.deleteProject(projID)

    ##### Delete Domain ####    
    domainObj = Domains()
    assert domainObj.updateDomain(domainID)
    assert domainObj.deleteDomain(domainID)
