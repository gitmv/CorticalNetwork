import sys
sys.path.insert(0, '../../')
import pygame
import random
import numpy as np
from CNN.CorticalNetwork import CorticalNetwork
from CNN.cNeuron import cNeuron
from UI2 import Ui2
from Analytics.StateRecorder import StateRecorder

def rotate_around_point(x,y,rot,mx,my):
    aa=x-mx
    bb=y-my
    cc=np.sqrt(aa*aa+bb*bb)
    if (cc!=0):
        a=np.rad2deg(np.arcsin(aa/cc))
    else:
        a=0
    a=np.deg2rad(a+rot)
    aa=np.sin(a)*cc
    bb=np.cos(a)*cc
    return mx+aa,my+bb

class gameobj(object):
    def __init__(self,x,y,size):
        self.x=x
        self.y=y
        self.size=size

    def getrect(self):
        return [self.x-self.size,self.y-self.size,self.size*2,self.size*2]

    #def getltrb(self):
    #    r=self.getrect()
    #    return [r[0],r[1],r[0]+r[2],r[1]+r[3]]

    def getpos(self):
        return [self.x, self.y]

    def collision(self,gobj):
        #o1ltrb=self.getltrb()
        #o2ltrb=game_obj.getltrb()
        return (self.x - self.size < gobj.x + gobj.size) and (self.y - self.size < gobj.y + gobj.size) and (self.x + self.size > gobj.x - gobj.size) and (self.y + self.size > gobj.y - gobj.size)

class sensor(gameobj):
    def __init__(self, x, y, dist, deg, size, neuron):
        super().__init__(x,y,size)
        self.dist=dist
        self.deg=deg
        self.activated=False
        self.neuron=neuron
        self.basecolor=(0,0,255)

    def on_activate(self,food):
        self.activated=True
        self.neuron.activate()

    def getcolor(self):
        if self.activated:
            self.activated = False
            return (255,255,255)
        else:
            return self.basecolor


    def position(self,moveing_object):
        self.x, self.y = rotate_around_point(moveing_object.x + self.dist, moveing_object.y,
                                             moveing_object.direction - self.deg, moveing_object.x,
                                             moveing_object.y)


class actor(sensor):
    def __init__(self, x, y, dist, deg, size, neuron, directionchange):
        super().__init__(x, y, dist, deg, size, neuron)
        self.directionchange=directionchange
        self.basecolor = (255, 255, 0)

    def apply_action(self,moveing_object):
        if self.neuron.isFireing():
            moveing_object.direction+=self.directionchange#*self.neuron.get_activity()

class moveing_object(gameobj):
    def __init__(self, x, y, speed, direction, size):
        super().__init__(x,y,size)
        self.speed=speed
        self.direction=direction

    def move(self):
        vx,vy=rotate_around_point(self.speed,0,self.direction,0,0)
        self.x += vx
        self.y += vy

class TurtleGame:

    def calculate_iterations(self):
        #sr = StateRecorder()
        for i in range(10000):
            self.timestep()
            #sr.record(self.brain)
        #sr.plot_recordings([0,7,14])

    def __init__(self):
        pygame.init()
        self.showNN=False
        self.screensize = [1200, 600]
        self.screen = pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Turtle Game")
        self.done = False
        self.clock = pygame.time.Clock()
        self.turtle = moveing_object(30, 230, 1, 45, 10)

        self.sensors=[]

        self.brain=CorticalNetwork(NeuronType=cNeuron)
        self.ui = Ui2(self.brain)
        self.ui.add_button('forward', self.calculate_iterations)
        #self.ui.start()

        for dist in range(3,4):
            self.brain.new_neuron_row()
            for deg in range(-3, 4):
                neuron=self.brain.add_neuron_to_current_row()
                self.sensors.append(sensor(30, 230, dist * 15, deg * 20, 5, neuron))

        #self.brain.new_neuron_row()
        #for deg in range(-3, 4):
        #    hidden_neuron = self.brain.add_neuron_to_current_row()

        self.actors=[]

        self.brain.new_neuron_row()
        for deg in range(-2, 3):
            motor_neuron = self.brain.add_neuron_to_current_row()
            self.actors.append(actor(30, 230, -20, deg * 15, 5, motor_neuron,deg))

        self.brain.connectneurons(connectionrad=8, connectiondensity=1, inhibitory_connectionrad=4, inhibitory_connectiondensity=1,no_y_layer_connection=False)

        self.food=[]
        for i in range(200):
            self.food.append(gameobj(random.uniform(0, self.screensize[0]),random.uniform(0, self.screensize[1]),10))

    def timestep(self):
        self.brain.new_iteration(False)
        #self.turtle.direction+=random.uniform(-3,3)
        self.turtle.move()

        for sensor in self.sensors:
            sensor.position(self.turtle)

        for actor in self.actors:
            actor.position(self.turtle)
            actor.apply_action(self.turtle)

        remove = []
        for f in self.food:
            if f.collision(self.turtle):#eat foot
                for n in self.brain.neurons:
                    n.on_reward()
                remove.append(f)

            for sensor in self.sensors:
                if f.collision(sensor):
                    sensor.on_activate(f)

        for r in remove:
            self.food.append(gameobj(random.uniform(0, self.screensize[0]), random.uniform(0, self.screensize[1]), 10))
            self.food.remove(r)

        if self.turtle.x < 0:
            self.turtle.x = self.screensize[0]

        if self.turtle.x > self.screensize[0]:
            self.turtle.x = 0
            self.turtle.y += 20

        if self.turtle.y < 0:
            self.turtle.y = self.screensize[1]

        if self.turtle.y > self.screensize[1]:
            self.turtle.y = 0

    def start(self):
        while not self.done:
            self.clock.tick(100)
            self.screen.fill((0,0,0))

            self.timestep()

            if self.showNN:
                events=self.ui.new_frame()
            else:
                self.onAnimate()
                events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                if event.type == pygame.KEYUP:
                    self.showNN=not self.showNN

            pygame.display.flip()
        pygame.quit()

    def draw(self,obj):
        if obj[1] == '#circle#':
            return pygame.draw.ellipse(self.screen, obj[3], obj[2])
        return None

    def onAnimate(self):

        self.draw([self,'#circle#',self.turtle.getrect(),(0,255,0)])

        for sensor in self.sensors:
            self.draw([self, '#circle#', sensor.getrect(), sensor.getcolor()])

        for actor in self.actors:
            self.draw([self, '#circle#', actor.getrect(), actor.getcolor()])

        for food in self.food:
            self.draw([self, '#circle#', food.getrect(), (255, 0, 0)])


tg=TurtleGame()#
tg.start()