#! /usr/bin/env python

# Author: priyanshi@zerostack.com
# (c) 2018 ZeroStack


from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class ProjectTemplate(object):
      """
      Class that provides attributes from buQuota section in projectTemplate.json
      """

      def __init__(self):
          self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/projectTemplate.json')

      @property
      def projectName(self):
          return self.dataproviderObj.get('projectTemplate', 'projectName')

      @property
      def projectTemplate(self):
          return self.dataproviderObj.get('projectTemplate' , 'projectTemplate')

      @property
      def cidr(self):
          return self.dataproviderObj.get('projectTemplate' , 'cidr')
