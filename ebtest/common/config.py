#! /usr/bin/env python


# Author: ankit@edgebricks.com
# (c) 2022 Edgebricks


from configparser import ConfigParser as CP
import os

from ebtest.common import utils as eutil
from ebtest.common import logger as elog


class ConfigParser(object):
    """
    Config class for getting, setting, deleting test configuration.

    Examples:
        ::

            testConfig = ConfigParser()
            testConfig.setConfig('domainName', value)
            testConfig.getConfig('apiURL')
            testConfig.deleteConfig('apiURL')

            # built-in functions for all default configs in test.conf
            testConfig.getProjectID()
            testConfig.setProjectID('<value>')
    """
    def __init__(self, section='defaults'):
        # sets up a configs dictionary
        self.parser  = CP()
        self.section = section
        self.fname   = self.getConfFile()

    def getConfFile(self):
        fpath = os.path.abspath(__file__)
        while True:
            fpath, fname = os.path.split(fpath)
            if fname == 'ebtest':
                break

        for root, _, files in os.walk(fpath):
            for fname in files:
                if fname == 'test.conf':
                    return os.path.join(root, fname)

        elog.logging.error('test.conf not found')
        return None

    def getConfig(self, config):
        """
        method to get test configuration

        Returns:
            None:   on failure.

            string: value of config.

        Args:
            string: test configuraton parameter.

        Examples:
            ::

                testConfig = ConfigParser()
                testConfig.getConfig('apiURL')
        """
        value  = None
        self.parser.read(self.fname)
        try:
            value = self.parser.get(self.section, config)
        except Exception as e:
            elog.logging.error('%s: no such config in test.conf'
                       % eutil.rcolor(config))
            elog.logging.error(e.message)
            raise

        if not value:
            elog.logging.debug('%s: config %s in test.conf'
                       % (eutil.bcolor(config), (eutil.rcolor('not set'))))
        return value

    def setConfig(self, config, value):
        """
        method to set test configuration

        Returns:
            bool: False on failure, True on success.

        Args:
            config (string): test configuraton parameter to set.

            value  (string): value of test config parameter.

        Examples:
            ::

                testConfig = ConfigParser()
                testConfig.setConfig('domainName', value)
        """
        self.parser.read(self.fname)
        try:
            self.parser.set(self.section, config, value)
        except:
            elog.logging.error('failed to set config %s = %s'
                       % (config, value))
            return False

        with open(self.fname, 'w') as f:
            self.parser.write(f)
        return True

    def deleteConfig(self, config):
        """
        method to delete test configuration

        Returns:
            bool: False on failure, True on success.

        Args:
            config (string): test configuraton parameter to delete.

        Examples:
            ::

                testConfig = ConfigParser()
                testConfig.deleteConfig('domainName')
        """
        self.parser.read(self.fname)
        if not self.parser.remove_option(self.section, config):
            elog.logging.error('failed to delete config %s' % eutil.rcolor(config))
            return False

        with open(self.fname, 'w') as f:
            self.parser.write(f)
        return True

    def getApiURL(self):
        return self.getConfig('apiURL')

    def getAcctID(self):
        return self.getConfig('acctID')

    def getClusterID(self):
        return self.getConfig('clusterID')

    def getServiceURL(self):
        apiURL     = self.getApiURL()
        acctID     = self.getAcctID()
        clusterID  = self.getClusterID()

        if not apiURL or not acctID or not clusterID:
            return None
        serviceURL = "%s/os/%s/regions/%s" % (apiURL, acctID, clusterID)
        return serviceURL

    def getProjectID(self):
        return self.getConfig('projectID')

    def getDomainID(self):
        return self.getConfig('domainID')

    def getDomainName(self):
        return self.getConfig('domainName')

    def getCloudAdmin(self):
        return self.getConfig('cloudAdmin')

    def getCloudAdminPassword(self):
        return self.getConfig('cloudAdminPassword')

    def getProjectName(self):
        return self.getConfig('projectName')

    def getProjectAdmin(self):
        return self.getConfig('projectAdmin')

    def getProjectAdminPassword(self):
        return self.getConfig('projectAdminPassword')

    def getProjectMember(self):
        return self.getConfig('projectMember')

    def getProjectMemberPassword(self):
        return self.getConfig('projectMemberPassword')

    def getProviderID(self):
        return self.getConfig('providerID')

    def setApiURL(self, value):
        return self.setConfig('apiURL', value)

    def setAcctID(self, value):
        return self.setConfig('acctID', value)

    def setClusterID(self, value):
        return self.setConfig('clusterID', value)

    def setProjectID(self, value):
        return self.setConfig('projectID', value)

    def setDomainID(self, value):
        return self.setConfig('domainID', value)

    def setDomainName(self, value):
        return self.setConfig('domainName', value)

    def setCloudAdmin(self, value):
        return self.setConfig('cloudAdmin', value)

    def setCloudAdminPassword(self, value):
        return self.setConfig('cloudAdminPassword', value)

    def setProjectName(self, value):
        return self.setConfig('projectName', value)

    def setProjectAdmin(self, value):
        return self.setConfig('projectAdmin', value)

    def setProjectAdminPassword(self, value):
        return self.setConfig('projectAdminPassword', value)

    def setProjectMember(self, value):
        return self.setConfig('projectMember', value)

    def setProjectMemberPassword(self, value):
        return self.setConfig('projectMemberPassword', value)

    def setProviderID(self, value):
        return self.setConfig('providerID', value)
