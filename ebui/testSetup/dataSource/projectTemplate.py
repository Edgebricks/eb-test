#! /usr/bin/env python
#
# Author: vikram@edgebricks.com
# (c) 2021 Edgebricks Inc


from ebui.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class ProjectTemplate():
    """
    Class that provides attributes from buQuota section in projectTemplate.json
    """

    def __init__(self):
        self.dataproviderObj = TestCaseDataProvider("projectTemplate.json")

    @property
    def projectName(self):
        return self.dataproviderObj.get("projectTemplate", "projectName")

    @property
    def projectTemplate(self):
        return self.dataproviderObj.get("projectTemplate", "projectTemplate")

    @property
    def cidr(self):
        return self.dataproviderObj.get("projectTemplate", "cidr")
