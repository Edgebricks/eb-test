#! /usr/bin/env python

# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class Login(object):
        """
        Class that provides attributes from buQuota section in buQuota.json
        """

        def __init__(self):
          self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/login.json')


        @property
        def baseURL(self):
          return self.dataproviderObj.get('login', 'baseURL')

        @property
        def customerID(self):
          return self.dataproviderObj.get('login' , 'customerid')

        @property
        def businessUnit(self):
          return self.dataproviderObj.get('login' , 'businessunit')

        @property
        def userName(self):
          return self.dataproviderObj.get('login' , 'username')

        @property
        def password(self):
          return self.dataproviderObj.get('login', 'password')

        @property
        def region(self):
           return self.dataproviderObj.get('login', 'region')