from ui_automation.framework.testDataProvider.testCaseDataProvider import TestCaseDataProvider


class InventoryTemplate(object):

    """
    Class that provides attributes inventoryTemplate.json
    """
    def __init__(self):
        self.dataproviderObj = TestCaseDataProvider('C:/Users/User/eb-test/ui_automation/testData/inventoryTemplate.json')

    @property
    def discoveredHosts(self):
        return self.dataproviderObj.get('inventoryTemplate', 'discoveredHosts')
