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
