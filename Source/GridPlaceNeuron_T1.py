#!/usr/bin/env python

"""
Prototype of grid for placing neurons objects T1, no objects
"""

import sys
import pygame
from pygame.locals import *


SCREENSIZE = WIDTH, HEIGHT = 700, 700
#              R    G   B
BLACK     = (  0,   0,   0)
DARKGREY  = (  10,   10,   10)
GREY      = (127, 127, 127)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)

XMARGIN = 80
YMARGIN = 80
GRIDSIZE = 5
NEURONSIZE = 20

STEP = (WIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

def main():
    # Setup...
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')
    # Run Main Loop
    while True:
        if run() == False:
            break
# Main Loop
def run():
        while True:
            checkForQuit()
            drawGrid()
            neuron = drawNeuron()

            # TODO:  Turn to neuron lists
            # TODO:  Objectify

            if neuron.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.circle(DISPLAYSURF, GREY, (XMARGIN,YMARGIN), NEURONSIZE)
                pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                if pygame.mouse.get_pressed()[0]:
                    pygame.draw.circle(DISPLAYSURF, RED, (XMARGIN,YMARGIN), NEURONSIZE)
            else:
                pygame.mouse.set_cursor(*pygame.cursors.arrow)
            pygame.display.update()

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

def drawNeuron():
    neuron = pygame.draw.circle(DISPLAYSURF, BLACK, (XMARGIN,YMARGIN), NEURONSIZE)
    return neuron

def checkForQuit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()


if __name__ == '__main__': main()
