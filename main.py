from CNN.CorticalNetwork import CorticalNetwork
from Analytics.StateRecorder import StateRecorder
from CNN.cNeuron import cNeuron
from UI2 import Ui2
from StateSaver import StateSaver

cn=CorticalNetwork(NeuronType=cNeuron)
#cn.createneurons(xsize=8, ysize=2)
#cn.connectneurons(connectionrad=10, connectiondensity=1, inhibitory_connectionrad=3, inhibitory_connectiondensity=1,no_y_layer_connection=True)

cn.createneurons(xsize=8, ysize=2)
cn.connectneurons(connectionrad=8, connectiondensity=1, inhibitory_connectionrad=4, inhibitory_connectiondensity=1,no_y_layer_connection=False)

cn.addInputPattern([1, 0, 1, 0, 1, 0, 1, 0],0.01)
cn.addInputPattern([0, 1, 0, 1, 0, 1, 0, 1],0.01)
#cn.addInputPattern([1, 0, 1, 0],0.01)
#cn.addInputPattern([0, 1, 0, 1],0.01)
#cn.addInputPattern([0.01 for n in cn.neurons],1)
cn.addInputPattern([0.1 for n in range(8)],1)#cn.neurons

#cn.new_iterations(1000000,True)

def button1():
    sr = StateRecorder()
    sr.recordXIterations(cn,1000,1,True)
    #sr.plot_recordings([1,5,9])
    sr.plot_Neuron_Activities([0,2,4,6,8])
    #sa.plotresponses([1, 1, 0, 0])

def button2():
    sr = StateRecorder()
    sr.recordXIterations(cn,1000,100,True)
    sr.plot_recordings([0,8])
    #sr.plot_Neuron_Activities()
    #sa.plotresponses([1, 1, 0, 0])

def button3():
    cn.new_iterations(100000,True,1000)

def button4():
    ss=StateSaver()
    ss.saveNetwork("network.pkl",cn)

def button5():
    ss=StateSaver()
    cn=ss.loadNetwork("network.pkl")
    ui.cortical_network=cn


ui=Ui2(cn)
ui.add_button('Activity hist', button1)
ui.add_button('All', button2)
ui.add_button('100000 it', button3)
ui.add_button('Save Network', button4)
ui.add_button('Load Network', button5)
ui.start()