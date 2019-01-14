#!/usr/bin/env python

"""

 GRID/LAYOUT - DISPLAY Tests

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

GRIDSIZE = 49
GRIDWIDTH = 700
GRIDHEIGHT = 700

STEP = (GRIDWIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

def main():
    # Setup...
    global DISPLAYSURF
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')

    drawGrid()
    while True:
        if run() == False:
            break
# Main Loop
def run():
        while True:
            checkEvents()
            pygame.display.update()

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


def checkEvents():
    hovering = False
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

        if hovering == True:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)

if __name__ == '__main__': main()
