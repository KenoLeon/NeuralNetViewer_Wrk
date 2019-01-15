#!/usr/bin/env python

"""
Prototype of grid for placing neurons objects
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

XMARGIN = 80
YMARGIN = 80
GRIDSIZE = 5
NEURONSIZE = 18
NEURON_LIST = []

STEP = (WIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self._rect = pygame.draw.circle(DISPLAYSURF, BLACK, (self.x,self.y), NEURONSIZE)
        self.place = False

    # def update():
    #     self._rect = pygame.draw.circle(DISPLAYSURF, BLACK, (self.x,self.y), NEURONSIZE)

def main():
    # Setup...
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')
    drawGrid()
    drawNeurons()

    # Run Main Loop
    while True:
        if run() == False:
            break
# Main Loop
def run():
        while True:
            checkForQuit()
            checkNeurons()
            pygame.display.update()

def checkNeurons():
     hovering = False
     for neuron in NEURON_LIST:
         if neuron._rect.collidepoint(pygame.mouse.get_pos()):
             hovering  = True
             pygame.draw.circle(DISPLAYSURF, GREY, (neuron.x,neuron.y), NEURONSIZE)
             if pygame.mouse.get_pressed()[0]:
                pygame.draw.circle(DISPLAYSURF, RED, (neuron.x,neuron.y), NEURONSIZE)
                neuron.place = not neuron.place
         else:
             pygame.draw.circle(DISPLAYSURF, BLACK, (neuron.x,neuron.y), NEURONSIZE)

     if hovering == True:
         pygame.mouse.set_cursor(*pygame.cursors.broken_x)
     else:
         pygame.mouse.set_cursor(*pygame.cursors.arrow)


def drawNeurons():
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

def checkForQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__': main()
