from random import randint
import numpy as np

class Synapse:
    def __init__(self, inp, outp, weight):
        self.inp = inp
        self.outp = outp
        self.weight = weight


#########################################################################################################
###################################################################################################Layout
#########################################################################################################

    def get_draw_objects(self,drawarray,init):
        if init:
            op=self.outp.position
            ip = self.inp.position
            self.pos=[op[0]+(ip[0]-op[0])/10.0,op[1]+(ip[1]-op[1])/10.0]
            self.size=0.1
            if self.weight!=-1:
                self.color = (0,255,0)
            else:
                self.color = (255,0,0)
        if self.weight > 0:
            self.size=np.sqrt(self.weight)/1.5

        self.rect=[self.pos[0]-self.size, self.pos[1]-self.size, self.size*2.0, self.size*2.0]
        drawarray.append([self,'#circle#',self.rect,self.color])
        return drawarray

'''
    def draw(self, objarray, sourcearray, subplot, init, t):
        if init:
            self.circle, = subplot.plot([], [], 'o', color='green', markersize=10)
            op=self.outp.position
            ip = self.inp.position
            self.circle.set_data([op[0]+(ip[0]-op[0])/10.0,op[1]+(ip[1]-op[1])/10.0])
            if self.weight!=-1:
                self.circle.set_markersize(4)
                self.circle.set_color('green')
            else:
                self.circle.set_markersize(2)
                self.circle.set_color('red')

        #self.circle.set_color((self.weight, 0, 0))
        if self.weight != -1:
            self.circle.set_markersize(np.sqrt(self.weight)*100)
        objarray.append(self.circle)
        sourcearray.append(self)
        return objarray,sourcearray
'''
