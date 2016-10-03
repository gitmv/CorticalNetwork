from CorticalNetwork import CorticalNetwork

from Analytics.StateRecorder import StateRecorder
from CNN.cNeuron import cNeuron
from UI2 import Ui2

cn=CorticalNetwork(NeuronType=cNeuron)
cn.createneurons(xsize=1, ysize=2)
cn.connectneurons(connectionrad=3, connectiondensity=1, inhibitory_connectionrad=3, inhibitory_connectiondensity=1,no_y_layer_connection=True)


cn.addInputPattern([1,0],0.1)
cn.addInputPattern([0,1],0.1)

ui=Ui2(cn)

def button1():
    sr = StateRecorder()
    sr.recordXIterations(cn,1000,1,True)
    sr.plot_recordings()

    #sa = StateAnalyzer(cn)
    #sa.plot_neuron_parameters(cn.neurons[1])

ui.add_button('Button1',button1)
ui.start()