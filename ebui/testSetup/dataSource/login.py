#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


from framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class Login(object):
      """
      Class that provides attributes from buQuota section in buQuota.json
      """

      def __init__(self):
          self.dataproviderObj = TestCaseDataProvider('login.json')


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

