import random
import numpy as np

class CorticalNetwork:
    def __init__(self,NeuronType):
        self.test = 0
        self.neurons = []
        self.neuronrows = []
        self.rowlabels = []
        self.NeuronType = NeuronType
        self.input_patterns = []
        self.max_x_size = 0
        self.max_y_size = 0



    def new_neuron_row(self,label=""):
        self.neuronrows.append([])
        self.rowlabels.append(label)

    def get_row(self,label):
        for i, l in enumerate(self.rowlabels):
            if l == label:
                return self.neuronrows[i]

    def add_neuron_to_current_row(self):
        x=len(self.neuronrows[-1])
        y=len(self.neuronrows)
        neuron = self.NeuronType([x * 7 + 2, y * 7 + 2])
        self.neurons.append(neuron)
        self.neuronrows[-1].append(neuron)
        self.max_x_size = np.maximum(self.max_x_size, x+1)
        self.max_y_size = np.maximum(self.max_y_size, y)
        return neuron

    def createneurons(self,xsize,ysize):
        for y in range(ysize):
            self.new_neuron_row()
            for x in range(xsize):
                self.add_neuron_to_current_row()

    def connectneurons(self,connectionrad,connectiondensity,inhibitory_connectionrad,inhibitory_connectiondensity,no_y_layer_connection=False):
        for y in range(len(self.neuronrows)):
            for x in range(len(self.neuronrows[y])):

                for yc in range(-connectionrad,connectionrad+1):
                    for xc in range(-connectionrad,connectionrad+1):
                        if x + xc >= 0 and y + yc >= 0 and y + yc < len(self.neuronrows) and x + xc < len(self.neuronrows[y + yc]) and (yc != 0 or xc != 0) and (yc != 0 or not no_y_layer_connection):
                            if random.uniform(0.0, 1.0/connectiondensity)<=1:
                                self.neuronrows[y][x].addDendriteNeuron(neuron=self.neuronrows[y+yc][x+xc])

                #for yc in range(-inhibitory_connectionrad, inhibitory_connectionrad + 1):
                #    for xc in range(-inhibitory_connectionrad, inhibitory_connectionrad + 1):
                #        if x + xc >= 0 and y + yc >= 0 and y + yc < self.max_y_size and x + xc < self.max_x_size and (yc != 0 or xc != 0):
                #            if random.uniform(0.0, 1.0 / inhibitory_connectiondensity) <= 1:
                #                self.neuronrows[y][x].addInhibitionTargetNeuron(neuron=self.neuronrows[y + yc][x + xc])

    def activatePattern(self,pattern):
        for i,p in enumerate(pattern):
            if p!=0:
                if random.uniform(0.0, 1.0 / p) <= 1.0:
                    self.neurons[i].activate()

    def addInputPattern(self,neuron_activation,pattern_possibility):
        self.input_patterns.append([neuron_activation,pattern_possibility])

    def setinput(self):
        for pat_pos_pair in self.input_patterns:
            if random.uniform(0.0, 1.0/pat_pos_pair[1]) <=1.0:
                self.activatePattern(pat_pos_pair[0])

    def new_iterations(self,iterationcount,activate_patterns,plotmod=0):
        for i in range(iterationcount):
            self.new_iteration(activate_patterns)
            if plotmod!=0 and i%plotmod==0:
                print(i)
        #print("Iterations finished")

    def new_iteration(self,activate_patterns):
        if activate_patterns:
            self.setinput()
        for step in self.NeuronType.iterationsteps:
            for n in self.neurons:
                n.new_iteration(step)







#########################################################################################################
###################################################################################################Layout
#########################################################################################################

    def get_draw_objects(self, drawarray, init):
        for n in self.neurons:
            drawarray=n.get_draw_objects(drawarray,init,)
        return drawarray

    def draw(self,objarray,sourcearray,subplot,init,t):
        for n in self.neurons:
            objarray,sourcearray=n.draw(objarray,sourcearray,subplot,init,t)
        return objarray,sourcearray