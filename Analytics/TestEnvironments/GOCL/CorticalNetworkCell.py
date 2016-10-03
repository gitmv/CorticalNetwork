import sys
sys.path.insert(0, '../../../')
from CNN.CorticalNetwork import CorticalNetwork
from CNN.cNeuron import cNeuron
from UI2 import Ui2
from StateSaver import StateSaver
import numpy as np
import random

options=['move','clone','infuse','stay','fight']#'wall'

class CorticalNetworkCell:

    def __init__(self):
        self.startBrainInstance=CorticalNetwork(NeuronType=cNeuron)


    def onNewIteration(self,state,N,cells,neighbors,secondneighbors,dec):
        #print("============================")

        #print(neighbors)
        for n in range(N):
            cell_neightbours=neighbors[n]
            #print("{} cell".format(n))
            #print(cell_neightbours)

            cmd_found=False

            for i,neigh in enumerate(cell_neightbours):
                if neigh[3]>10 and neigh[1]!='CNC_CELL':
                    dec[n, 0] = 'fight'
                    dec[n, 1] = i
                    cmd_found=True

            if cmd_found==False:
                dec[n, 0] = random.choice(options)
                dec[n, 1] = np.random.randint(0,len(neighbors[0]))
        return dec
