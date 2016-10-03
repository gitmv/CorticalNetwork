import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from CNN.cNeuron import cNeuron


class Ui:

    def __init__(self,cortical_network):
        self.cortical_network=cortical_network
        self.fig = plt.figure()
        self.fig.canvas.toolbar.hide()
        self.ax = self.fig.add_subplot(111, autoscale_on=False, xlim=(0, 60), ylim=(0, 20))
        self.cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.selected_obj=None
        self.buttons=[]

    def add_button(self,id,onclick):
        self.buttons.append([None,id,onclick])

    def onclick(self,event):
        print(event.button)
        if event.xdata != None and event.ydata != None:
            if event.button == 1:
                obj=self.getobject(event.xdata,event.ydata)
                self.selected_obj=obj

                if isinstance(obj,cNeuron):
                    obj.activity=1

                #if isinstance(obj,Synapse):
                #    obj.weight=1

                for btnobj in self.buttons:
                    if obj == btnobj[1]:
                        btnobj[2]()

                #if obj=='Button1':
                #    sa = StateAnalyzer(self.cortical_network)
                #    sa.plotresponses([1, 1, 0, 0])

                #if obj=='Button2':
                #    sa = StateAnalyzer(self.cortical_network)
                #    sa.plotresponses([1, 0, 0, 0])

                #if obj=='Button3':
                #    self.cortical_network.new_iterations(100000,True)

                print(obj)

            #if event.button == 3:



    def initialize(self):
        self.drawbuttons([], [], self.ax, True, 0)
        res,s=self.cortical_network.draw([],[], self.ax, True, 0)
        return res

    def start(self):
        ani = animation.FuncAnimation(self.fig, self.onAnimate, np.arange(0, 100, 0.001), init_func=self.initialize, interval=20, blit=True)
        plt.show()

    def getobject(self,x,y):
        for index,obj in enumerate(self.drawobjects):
            pos=obj.get_data()
            ms=obj.get_markersize()
            if np.abs(pos[0]-x)<0.1 and np.abs(pos[1]-y)<0.1:
                return self.drawsources[index]
        return None

    def drawbuttons(self,objarray,sourcearray,subplot,init,t):
        if init:
            pos=18
            for btnobj in self.buttons:
                btnobj[0],=subplot.plot(pos, 18, 'o', color='green', markersize=20)
                pos-=2
            #self.b1, = subplot.plot(25, 18, 'o', color='green', markersize=20)
            #self.b2, = subplot.plot(25, 16, 'o', color='red', markersize=20)
            #self.b3, = subplot.plot(25, 14, 'o', color='blue', markersize=20)
            #self.text= subplot.text(2, 6, 'Button1', fontsize=15)

        for btnobj in self.buttons:
            objarray.append(btnobj[0])
            sourcearray.append(btnobj[1])

        #objarray.append(self.b1)
        #sourcearray.append('Button1')

        #objarray.append(self.b2)
        #sourcearray.append('Button2')

        #objarray.append(self.b3)
        #sourcearray.append('Button3')

        return objarray,sourcearray


    def onAnimate(self,t):
        self.cortical_network.new_iteration(True)
        self.drawobjects,self.drawsources = self.cortical_network.draw([], [], self.ax, False, t)
        self.drawobjects, self.drawsources = self.drawbuttons(self.drawobjects, self.drawsources, self.ax, False, t)
        return self.drawobjects
