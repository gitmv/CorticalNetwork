import random

from CNN.Synapse import Synapse


class basicNeuron(object):
    iterationsteps = []

    def __init__(self, position):
        # basic
        self.position = position  # position of the neuron
        self.inp_synapses = []  # list of input synapses
        self.inhibition_targets = []  # list of "output synapses" (for inhibition)
        self.activity = 0.0  # activation value
        self.outside_activation = 0.0  # non synaptic activation
        self.iteration_start_activity = 0.0  # activity value before the current iteration (for synchroneous calculations)
        self.inhibition = 0.0  # inhibition from other neurons to the curren neuron


    def addDendriteNeuron(self, neuron):
        synapse=Synapse(neuron, self, random.uniform(0.0, 0.1))
        self.inp_synapses.append(synapse)
        return synapse

    def addInhibitionTargetNeuron(self, neuron):
        self.inhibition_targets.append(Synapse(self, neuron, -1.0))

    def isFireing(self):
        return False

    def activate(self):
        self.outside_activation = 1

    def get_activity(self):
        return self.iteration_start_activity


            #########################################################################################################
            ###################################################################################################Layout
            #########################################################################################################

    def set_get_Parameter(self, i, value):
        return None

    def getStateValues(self):
        values = []
        labels = []
        return values, labels

    def get_draw_objects(self, drawarray, init):
        if init:
            self.size = 0.5

        for synapse in self.inp_synapses:
            drawarray = synapse.get_draw_objects(drawarray, init)

        #for inh_synapse in self.inhibition_targets:
        #    drawarray = inh_synapse.get_draw_objects(drawarray, init)

        if self.isFireing():
            self.color = (100.0, self.iteration_start_activity * 255, 100.0)
        else:
            self.color = (self.iteration_start_activity * 255, 100.0, 100.0)

        self.rect = [self.position[0] - self.size, self.position[1] - self.size, self.size * 2, self.size * 2]
        drawarray.append([self, '#circle#', self.rect, self.color])
        return drawarray

    '''
    def draw(self,objarray,sourcearray,subplot,init,t):

        if init:
            #self.rectangle=Rectangle((1,1), width=5, height=12)
            self.circle,=subplot.plot([], [], 'o', color='green', markersize=30)
            self.circle.set_data(self.position)
            #self.circle.set_markersize(7+t*100)

        for synapse in self.inp_synapses:
             objarray,sourcearray=synapse.draw(objarray,sourcearray,subplot,init,t)

        for inh_synapse in self.inhibition_targets:
            objarray, sourcearray = inh_synapse.draw(objarray, sourcearray, subplot, init, t)

        if self.isFireing():
            self.circle.set_color((0.0, self.iteration_start_activity, 0.0))
        else:
            self.circle.set_color((self.iteration_start_activity, 0.0, 0.0))

        objarray.append(self.circle)
        sourcearray.append(self)
        return objarray,sourcearray
'''
