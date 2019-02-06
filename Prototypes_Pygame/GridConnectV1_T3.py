#!/usr/bin/env python

"""

Prototype of grid based neuron viewer
Connect Neuron to neuron ( UI only )

"""

import sys
import pygame
from pygame.locals import *

SCREENSIZE = WIDTH, HEIGHT = 900, 700
#              R    G   B
BLACK     = ( 0,    0,   0)
DARKGREY  = ( 80,  80,   80)
GREY      = (127, 127, 127)
WHITE     = (255, 255, 255)
RED       = (255,   0,   0)

XMARGIN = 60
YMARGIN = 60
GRIDSIZE = 7
GRIDWIDTH = 700
GRIDHEIGHT = 700
STEP = (GRIDWIDTH - (XMARGIN + YMARGIN))/GRIDSIZE

NEURONSIZE = 14
NEURON_LIST = []
CONTROLS = []
PLAY = False
CONNECT = False
DRAGGING = False
DRAGSTART = (0, 0)
FPS = 120

class Neuron():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.place = False
        self._rect = self.draw()
        self.baseNeuroTransmitter = 0.4
        self.ntRelease = 0.1

    def clipRect(self):
        clipRect = self._rect.copy()
        clipRect.height = clipRect.height * (1-self.baseNeuroTransmitter)
        return clipRect


    def updateNeuron(self):
        if PLAY and self.place:
            if (self.baseNeuroTransmitter <= 1):
                self.baseNeuroTransmitter += self.ntRelease
            else:
                self.baseNeuroTransmitter = 0
        self.draw()

    def draw(self):
        if self.place:
            pygame.draw.circle(DISPLAYSURF, GREY, (self.x,self.y), NEURONSIZE)
            pygame.draw.rect(DISPLAYSURF, BLACK, self.clipRect())
            return pygame.draw.circle(DISPLAYSURF, GREY, (self.x,self.y), NEURONSIZE, 1)
        elif not self.place:
            self.baseNeuroTransmitter = 0.4
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


class connectControl():
    def __init__(self):
        self.connect = False
        self.offsetX = GRIDWIDTH
        self.offsetY = YMARGIN
        self._rect = self.draw()

    def draw(self):
        if self.connect:
            pygame.draw.circle( DISPLAYSURF, GREY, ( self.offsetX + 10, self.offsetY + 66 ), 10)
            pygame.draw.circle( DISPLAYSURF, GREY, ( self.offsetX + 50, self.offsetY + 66 ), 10)
            pygame.draw.line( DISPLAYSURF, GREY, ( self.offsetX + 18, self.offsetY + 66 ), ( self.offsetX + 40, self.offsetY + 66 ), 1 )
            pygame.draw.polygon(DISPLAYSURF, GREY, (
            (self.offsetX + 40, self.offsetY + 66),
            (self.offsetX + 30, self.offsetY + 58),
            (self.offsetX + 30, self.offsetY + 74),
            (self.offsetX + 40, self.offsetY + 66)
            ))
        else:
            pygame.draw.rect( DISPLAYSURF, BLACK, ( self.offsetX, self.offsetY + 56, 60, 20 ) )
            pygame.draw.circle( DISPLAYSURF, GREY, ( self.offsetX + 10, self.offsetY + 66 ), 10, 1 )
            pygame.draw.circle( DISPLAYSURF, GREY, ( self.offsetX + 50, self.offsetY + 66 ), 10, 1 )
            pygame.draw.line( DISPLAYSURF, GREY, ( self.offsetX + 18, self.offsetY + 66 ), ( self.offsetX + 30, self.offsetY + 66 ), 1 )
            pygame.draw.polygon(DISPLAYSURF, GREY, (
            (self.offsetX + 40, self.offsetY + 66),
            (self.offsetX + 30, self.offsetY + 58),
            (self.offsetX + 30, self.offsetY + 74),
            (self.offsetX + 40, self.offsetY + 66)
            ), 1)
            return pygame.Rect(self.offsetX, self.offsetY + 56, 60, 20)

def main():
    # Setup...
    global DISPLAYSURF, CLOCK, DRAGSTART
    pygame.init()
    DISPLAYSURF = pygame.display.set_mode(SCREENSIZE)
    pygame.display.set_caption('Grid Place Neuron')
    CLOCK = pygame.time.Clock()

    drawGrid(DARKGREY)
    initControls()
    initNeurons()
    # Run Main Loop
    while True:
        if run() == False:
            break
# Main Loop
def run():
        while True:
            clearScreen()
            drawGrid(DARKGREY)
            drawControls()
            updateNeurons()
            checkEvents()
            redraw()
            CLOCK.tick(FPS)

def initControls():
    PLAYC = playControl()
    CONNECTC = connectControl()
    CONTROLS.append(PLAYC)
    CONTROLS.append(CONNECTC)


def redraw():
        pygame.display.update()


def drawControls():
    CONTROLS[0].draw()
    CONTROLS[1].draw()


def clearGrid():
    # Rect(left, top, width, height)
    pygame.draw.rect( DISPLAYSURF, BLACK, ( XMARGIN - NEURONSIZE, YMARGIN - NEURONSIZE, (GRIDSIZE*STEP) + NEURONSIZE*2, (GRIDSIZE*STEP) + NEURONSIZE*2 ))


def clearScreen():
    DISPLAYSURF.fill(BLACK)

def updateNeurons():
    for neuron in NEURON_LIST:
            neuron.updateNeuron()


def initNeurons():
    for i in range(GRIDSIZE+1):
        for ii in range(GRIDSIZE+1):
            n = Neuron(int(XMARGIN + (i*STEP)), int((YMARGIN) + (ii*STEP)))
            NEURON_LIST.append(n)

    # Place full grid
    # for neuron in NEURON_LIST:
    #     neuron.place = not neuron.place

def drawGrid(color):
    for i in range(GRIDSIZE):
        pygame.draw.line(DISPLAYSURF, color,
        (XMARGIN, YMARGIN + (i*STEP)), ((GRIDWIDTH - YMARGIN), XMARGIN + (i*STEP) ), 1)
        pygame.draw.line(DISPLAYSURF, color,
        (XMARGIN + (i*STEP), YMARGIN), (YMARGIN + (i*STEP), HEIGHT - XMARGIN ), 1)
    if  i == (GRIDSIZE - 1) :
        pygame.draw.line(DISPLAYSURF, color,
        (XMARGIN, YMARGIN + ((i + 1)*STEP)), ((GRIDWIDTH - YMARGIN), XMARGIN + ((i + 1)*STEP) ), 1)
        pygame.draw.line(DISPLAYSURF, color,
        (XMARGIN + ((i + 1)*STEP), YMARGIN), (YMARGIN + ((i + 1)*STEP), GRIDHEIGHT - XMARGIN ), 1)


def checkEvents():
    global PLAY, CONNECT, DRAGGING, DRAGSTART
    hovering = False
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            for neuron in NEURON_LIST:
                if neuron._rect.collidepoint(event.pos):
                    hovering = True
            if CONTROLS[0]._rect.collidepoint(event.pos) or CONTROLS[1]._rect.collidepoint(event.pos):
                hovering = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # Place neuron
                    if not CONNECT:
                        for neuron in NEURON_LIST:
                            if neuron._rect.collidepoint(event.pos):
                                neuron.place = not neuron.place
                                neuron.draw()
                            else:
                                neuron.draw()
                   # Controls:
                   # PLAY
                    if CONTROLS[0]._rect.collidepoint(event.pos):
                        CONTROLS[0].play = not CONTROLS[0].play
                        CONTROLS[0].draw()
                        PLAY = not PLAY
                    # CONNECT
                    if CONTROLS[1]._rect.collidepoint(event.pos):
                        CONTROLS[1].connect = not CONTROLS[1].connect
                        CONTROLS[1].draw()
                        CONNECT = not CONNECT

                    if CONNECT and not DRAGGING and not CONTROLS[1]._rect.collidepoint(event.pos) and not CONTROLS[0]._rect.collidepoint(event.pos):
                        for neuron in NEURON_LIST:
                            if neuron._rect.collidepoint(event.pos):
                                DRAGSTART = (neuron.x, neuron.y)
                        DRAGGING = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                DRAGGING = False

        # quit, cursors
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()

        if hovering == True:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
        else:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
    # Out of the event loop:
    if DRAGGING and DRAGSTART != (0,0) :
        dragEnd = pygame.mouse.get_pos()
        # mouseX = dragEnd[0]
        # mouseY = dragEnd[1]
        pygame.draw.line(DISPLAYSURF, WHITE, DRAGSTART,dragEnd, 1)
        pygame.draw.circle(DISPLAYSURF, WHITE,dragEnd,4)


if __name__ == '__main__': main()
