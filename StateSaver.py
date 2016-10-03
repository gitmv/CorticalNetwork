import pickle

class StateSaver:

    def saveNetwork(self, filename, network):  # filename.pkl
        with open(filename, 'wb') as output:
            pickle.dump(network, output, pickle.HIGHEST_PROTOCOL)


    def loadNetwork(self, filename):
        with open(filename, 'rb') as input:
            network = pickle.load(input)
            return network