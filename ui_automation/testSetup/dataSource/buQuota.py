#! /usr/bin/env python

# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class BUquota(object):
      """
      Class that provides attributes from buQuota section in buQuota.json
      """

      def __init__(self):
          self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/buQuota.json')

      @property
      def buName(self):
          return self.dataproviderObj.get('buQuota', 'businessUnitName')

      @property
      def username(self):
          return self.dataproviderObj.get('buQuota' , 'username')

      @property
      def email(self):
          return self.dataproviderObj.get('buQuota' , 'email')

      @property
      def password(self):
          return self.dataproviderObj.get('buQuota' , 'password')

      @property
      def confirmpassword(self):
          return self.dataproviderObj.get('buQuota', 'confirmpassword')

      @property
      def cores(self):
          return self.dataproviderObj.get('buQuota', 'cores')

      @property
      def instances(self):
          return self.dataproviderObj.get('buQuota', 'instances')

      @property
      def RAM(self):
          return self.dataproviderObj.get('buQuota', 'RAM')

      @property
      def networks(self):
          return self.dataproviderObj.get('buQuota', 'networks')

      @property
      def routers(self):
          return self.dataproviderObj.get('buQuota', 'routers')

      @property
      def externalIP(self):
          return self.dataproviderObj.get('buQuota', 'externalIP')

      @property
      def storage(self):
          return self.dataproviderObj.get('buQuota', 'storage')

      @property
      def volumes(self):
          return self.dataproviderObj.get('buQuota', 'volumes')

      @property
      def snapshots(self):
          return self.dataproviderObj.get('buQuota', 'snapshots')

      @property
      def SSD(self):
          return self.dataproviderObj.get('buQuota', 'SSD')
