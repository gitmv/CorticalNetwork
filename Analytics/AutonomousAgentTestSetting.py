from Analytics.TestSetting import AbstractTestSetting
from CNN.CorticalNetwork import CorticalNetwork

class AutonomousAgentTestSetting(AbstractTestSetting):

    def createCorticalNetwork(self):
        self.cortical_network=CorticalNetwork()

    def runTestSession(self):
        super(AbstractTestSetting, self).runTestSession()
        #uiupdate

    def createTestPatterns(self,steps):
        print("not implemented")

    def getTestScore(self):
        print("not implemented")