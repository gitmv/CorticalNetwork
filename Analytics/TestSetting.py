from Analytics.StateRecorder import StateRecorder
from CNN.CorticalNetwork import CorticalNetwork


class AbstractTestSetting:
    def __init__(self):
        self.testpatterns=[]
        self.name='AbstractTestSetting'

    def createCorticalNetwork(self):
        print("not implemented")

    def createTestPatterns(self,steps):
        print("not implemented")

    def getTestScore(self):
        print("not implemented")

    def saveState(self,filename):
        self.stateRecorder.save(filename)

    def setNetworkParameters(self,param):
        for n in self.cortical_network.neurons:
            for i, p in enumerate(param):
                n.set_get_Parameter(i,p)

    def initializeTestSession(self,cortical_network):
        self.cortical_network=cortical_network
        self.stateRecorder=StateRecorder()

    def runTestSession(self):
        for pattern in self.testpatterns:
            self.cortical_network.activatePattern(pattern)
            self.cortical_network.new_iteration(False)
            self.stateRecorder.record(self.cortical_network)




class TestSetting1(AbstractTestSetting):

    def createCorticalNetwork(self):
        self.cortical_network=CorticalNetwork()

    def createTestPatterns(self,steps):
        print("not implemented")

    def getTestScore(self):
        print("not implemented")



