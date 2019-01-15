#!/usr/bin/env python

"""

 Prototype of grid based neuron viewer
 Adds space for controls
 Adds playControl

"""

import sys
import pygame
from pygame.locals import *

SCREENSIZE = WIDTH, HEIGHT = 900, 700
#              R    G   B
BLACK     = ( 0,    0,   0)
DARKGREY  = ( 10,  10,   10)
GREY      = (127, 127, 127)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)

XMARGIN = 60
YMARGIN = 60
GRIDSIZE = 7
GRIDWIDTH = 700
GRIDHEIGHT = 700
STEP = (GRIDWIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

NEURONSIZE = 15
NEURON_LIST = []
CONTROLS = []

class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.place = False
        self._rect = self.draw()
        self.baseNeuroTransmitter = 0.4

    def clipRect(self):
        clipRect = self._rect.copy()
        clipRect.height = clipRect.height * (1-self.baseNeuroTransmitter)
        return clipRect

    def draw(self):
        if self.place:
            pygame.draw.circle(DISPLAYSURF, GREY, (self.x,self.y), NEURONSIZE)
            pygame.draw.rect(DISPLAYSURF, BLACK, self.clipRect())
            return pygame.draw.circle(DISPLAYSURF, GREY, (self.x,self.y), NEURONSIZE, 1)
        elif not self.place:
            return pygame.draw.circle(DISPLAYSURF, BLACK, (self.x,self.y), NEURONSIZE + 1)


class playControl():
    def __init__(self):
        self.play = False
        self.offsetX = GRIDWIDTH
        self.offsetY = YMARGIN
        self._rect = self.draw()

    def draw(self):

        if self.play:
            pygame.draw.polygon(DISPLAYSURF, GREY, ((self.offsetX,self.offsetY), (self.offsetX, self.offsetY + 25), (self.offsetX + 25 ,self.offsetY + 12.5)))
        else:
            pygame.draw.polygon(DISPLAYSURF, BLACK, ((self.offsetX,self.offsetY), (self.offsetX, self.offsetY + 25), (self.offsetX + 25 ,self.offsetY + 12.5)))
            return pygame.draw.polygon(DISPLAYSURF, GREY, ((self.offsetX,self.offsetY), (self.offsetX, self.offsetY + 25), (self.offsetX + 25 ,self.offsetY + 12.5)), 1)


def main():
    # Setup...
    global DISPLAYSURF, PLAYC
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')

    drawGrid()
    drawControls()
    initNeurons()
    # Run Main Loop
    while True:
        if run() == False:
            break
# Main Loop
def run():
        while True:
            checkEvents()
            pygame.display.update()


def drawControls():
    PLAYC = playControl()
    CONTROLS.append(PLAYC)

def initNeurons():
    for i in range(GRIDSIZE+1):
        for ii in range(GRIDSIZE+1):
            n = Neuron(int(XMARGIN + (i*STEP)), int((YMARGIN) + (ii*STEP)))
            NEURON_LIST.append(n)


def drawGrid():
    for i in range(GRIDSIZE):
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN, YMARGIN + (i*STEP)), ((GRIDWIDTH - YMARGIN), XMARGIN + (i*STEP) ), 1)
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN + (i*STEP), YMARGIN), (YMARGIN + (i*STEP), HEIGHT - XMARGIN ), 1)
    if  i == (GRIDSIZE - 1) :
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN, YMARGIN + ((i + 1)*STEP)), ((GRIDWIDTH - YMARGIN), XMARGIN + ((i + 1)*STEP) ), 1)
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN + ((i + 1)*STEP), YMARGIN), (YMARGIN + ((i + 1)*STEP), GRIDHEIGHT - XMARGIN ), 1)

# Add Click toggle function

def checkEvents():
    hovering = False
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            for neuron in NEURON_LIST:
                if neuron._rect.collidepoint(event.pos):
                    hovering = True
                else:
                    neuron.draw()
            if CONTROLS[0]._rect.collidepoint(event.pos):
                hovering = True


        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for neuron in NEURON_LIST:
                        if neuron._rect.collidepoint(event.pos):
                            neuron.place = not neuron.place
                            neuron.draw()
                        else:
                            neuron.draw()
                    if CONTROLS[0]._rect.collidepoint(event.pos):
                         CONTROLS[0].play = not CONTROLS[0].play
                         CONTROLS[0].draw()


        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

        if hovering == True:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

if __name__ == '__main__': main()
