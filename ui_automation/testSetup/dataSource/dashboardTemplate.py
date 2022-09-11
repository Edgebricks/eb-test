from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class DashboardTemplate(object):

    """
    Class that provides attributes dashboardTemplate.json
    """
    def __init__(self):
        self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/dashboardTemplate.json')

    @property
    def top5CriticalEventText(self):
        return self.dataproviderObj.get('dashboardTemplate', 'top5CriticalEventText')

    @property
    def buText(self):
        return self.dataproviderObj.get('dashboardTemplate', 'buText')

    @property
    def overViewText(self):
        return self.dataproviderObj.get('dashboardTemplate', 'overViewText')

    @property
    def tabsInMonitoring(self):
        return self.dataproviderObj.get('dashboardTemplate', 'tabsInMonitoring')
