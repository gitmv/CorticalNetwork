# Import a library of functions called 'pygame'
import numpy as np
import pygame

from CNN.cNeuron import cNeuron


class Ui2:

    def __init__(self,cortical_network):
        self.cortical_network=cortical_network
        self.selected_obj=None
        self.buttons=[]
        self.startbuttonpos=[10,10]
        pygame.init()
        self.screensize = [1200, 600]
        self.screen = pygame.display.set_mode(self.screensize)
        pygame.display.set_caption("Cortical Algorithm 0.2")
        self.done = False
        self.clock = pygame.time.Clock()
        self.minmax = [10000.0, 10000.0, -10000.0, -10000.0]
        self.lt = [0,0]
        self.scale = 1.0
        self.add_button("Export",self.exportimage)
        self.initialized=False

    def exportimage(self):
        pygame.image.save(self.screen, "test.png")

    def add_button(self,id,onclick):
        size=10
        rect=[self.startbuttonpos[0]-size,self.startbuttonpos[1]-size,size*2,size*2]
        self.buttons.append([id,'#button#',rect,(200,200,200),onclick])
        self.startbuttonpos[0]+=200

    def new_frame(self):
        self.screen.fill((0, 0, 0))
        drawobjects = self.onAnimate()
        events=pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                clicked = [s[1] for s in drawobjects if s[0].collidepoint(pos)]
                for clicked_obj in clicked:
                    if isinstance(clicked_obj[0], cNeuron):
                        clicked_obj[0].activity = 1

                    if clicked_obj[1] == '#button#':
                        clicked_obj[4]()
        return events

    def start(self):
        #self.drawarray = self.cortical_network.get_draw_objects([], True)
        while not self.done:
            self.clock.tick(30)

            # start_time = time.time()
            self.cortical_network.new_iteration(True)
            # print "--- {} ms ---".format((time.time() - start_time)*1000)

            self.new_frame()

            pygame.display.flip()
        pygame.quit()

    def draw(self,obj,scale_obj):
        if obj[1] == '#circle#':
            if scale_obj:
                self.minmax[0] = np.minimum(self.minmax[0], obj[2][0]-5)
                self.minmax[1] = np.minimum(self.minmax[1], obj[2][1]-5)
                self.minmax[2] = np.maximum(self.minmax[2], obj[2][0]+5)
                self.minmax[3] = np.maximum(self.minmax[3], obj[2][1]+5)
                obj[2][0] = obj[2][0] * self.scale - self.lt[0]
                obj[2][1] = obj[2][1] * self.scale - self.lt[1]
                obj[2][2] = obj[2][2] * self.scale
                obj[2][3] = obj[2][3] * self.scale
            return pygame.draw.ellipse(self.screen, obj[3], obj[2])

        if obj[1] == '#button#':
            myfont = pygame.font.SysFont("monospace", 15)
            label = myfont.render(obj[0], 1, (0, 0, 0))
            rp=label.get_rect()
            rp[0] += obj[2][0]
            rp[1] += obj[2][1]
            r=pygame.draw.rect(self.screen, obj[3], rp)
            self.screen.blit(label, (obj[2][0],obj[2][1]))
            return r

        return None

    def onAnimate(self):
        result=[]

        for b in self.buttons:
            result.append([self.draw(b, False),b])

        self.drawarray = self.cortical_network.get_draw_objects([], not self.initialized)
        self.initialized=True
        for obj in self.drawarray:
            result.append([self.draw(obj,True),obj])



        self.lt = [self.minmax[0],self.minmax[1]]
        self.scale = np.minimum(self.screensize[0]/(self.minmax[2]-self.minmax[0]), self.screensize[1]/(self.minmax[3]-self.minmax[1]))
        return result

'''

        pygame.draw.line(screen, GREEN, [0, 0], [50, 30], 5)

        # Draw on the screen a GREEN line from (0,0) to (50.75)
        # 5 pixels wide.
        pygame.draw.lines(screen, BLACK, False, [[0, 80], [50, 90], [200, 80], [220, 30]], 5)

        # Draw on the screen a GREEN line from (0,0) to (50.75)
        # 5 pixels wide.
        pygame.draw.aaline(screen, GREEN, [0, 50], [50, 80], True)

        # Draw a rectangle outline
        pygame.draw.rect(screen, BLACK, [75, 10, 50, 20], 2)

        # Draw a solid rectangle
        pygame.draw.rect(screen, BLACK, [150, 10, 50, 20])

        # Draw an ellipse outline, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, RED, [225, 10, 50, 20], 2)

        # Draw an solid ellipse, using a rectangle as the outside boundaries
        pygame.draw.ellipse(screen, RED, [300, 10, 50, 20])

        # This draws a triangle using the polygon command
        pygame.draw.polygon(screen, BLACK, [[100, 100], [0, 200], [200, 200]], 5)

        # Draw an arc as part of an ellipse.
        # Use radians to determine what angle to draw.
        pygame.draw.arc(screen, BLACK, [210, 75, 150, 125], 0, pi / 2, 2)
        pygame.draw.arc(screen, GREEN, [210, 75, 150, 125], pi / 2, pi, 2)
        pygame.draw.arc(screen, BLUE, [210, 75, 150, 125], pi, 3 * pi / 2, 2)
        pygame.draw.arc(screen, RED, [210, 75, 150, 125], 3 * pi / 2, 2 * pi, 2)

        # Draw a circle
        pygame.draw.circle(screen, BLUE, [60, 250], 40)

'''






