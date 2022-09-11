from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class InfrastructureTemplate(object):

    """
    Class that provides attributes infrastructureTemplate.json
    """
    def __init__(self):
        self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/infrastructureTemplate.json')

    @property
    def discoveredHosts(self):
        return self.dataproviderObj.get('infrastructureTemplate', 'discoveredHosts')

    @property
    def costAnalysis(self):
        return self.dataproviderObj.get('infrastructureTemplate', 'costAnalysis')
