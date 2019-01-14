#!/usr/bin/env python

"""
 Prototype of grid for placing neurons objects
 Adding Base NeuronTransmiters
"""

import sys
import pygame
from pygame.locals import *

SCREENSIZE = WIDTH, HEIGHT = 700, 700
#              R    G   B
BLACK     = ( 0,    0,   0)
DARKGREY  = ( 10,  10,   10)
GREY      = (127, 127, 127)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)

XMARGIN = 60
YMARGIN = 60
GRIDSIZE = 5
NEURONSIZE = 18
NEURON_LIST = []
STEP = (WIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.place = False
        self._rect = self.draw()
        self.baseNeuroTransmitter = 0.4

    # Rect(left, top, width, height) -> Rect
    # rect(Surface, color, Rect, width=0) -> Rect
    # circle(Surface, color, pos, radius, width=0) -> Rect

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

def main():
    # Setup...
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')

    drawGrid()
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

def updateNeurons():
        for neuron in NEURON_LIST:
            neuron.draw()

def initNeurons():
    for i in range(GRIDSIZE+1):
        for ii in range(GRIDSIZE+1):
            n = Neuron(int(XMARGIN + (i*STEP)), int((YMARGIN) + (ii*STEP)))
            NEURON_LIST.append(n)

def drawGrid():
    for i in range(GRIDSIZE):
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN, YMARGIN + (i*STEP)), ((WIDTH - YMARGIN), XMARGIN + (i*STEP) ), 1)
        pygame.draw.line(DISPLAYSURF, GREY,
        (XMARGIN + (i*STEP), YMARGIN), (YMARGIN + (i*STEP), HEIGHT - XMARGIN ), 1)
        if  i == (GRIDSIZE - 1) :
            pygame.draw.line(DISPLAYSURF, GREY,
            (XMARGIN, YMARGIN + ((i + 1)*STEP)), ((WIDTH - YMARGIN), XMARGIN + ((i + 1)*STEP) ), 1)
            pygame.draw.line(DISPLAYSURF, GREY,
            (XMARGIN + ((i + 1)*STEP), YMARGIN), (YMARGIN + ((i + 1)*STEP), HEIGHT - XMARGIN ), 1)

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
        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for neuron in NEURON_LIST:
                        if neuron._rect.collidepoint(event.pos):
                            neuron.place = not neuron.place
                            neuron.draw()
                        else:
                            neuron.draw()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

        if hovering == True:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

if __name__ == '__main__': main()
