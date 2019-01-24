#!/usr/bin/env python
"""

Prototype of grid based neuron viewerself.
Connect fringe cases.
Remove connections.

"""

import sys
import pygame
from pygame.locals import *
from math import atan2, cos, sin

SCREENSIZE = WIDTH, HEIGHT = 900, 700
#              R    G   B
BLACK = (0, 0, 0)
DARKGREY = (60, 60, 60)
GREY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

XMARGIN = 60
YMARGIN = 60
GRIDSIZE = 7
GRIDWIDTH = 700
GRIDHEIGHT = 700
STEP = (GRIDWIDTH - (XMARGIN + YMARGIN)) / GRIDSIZE
NEURONSIZE = 14

NEURON_LIST = []
CONNECTIONS = []
CONTROLS = []

PLAY = False
CONNECT = False
REMOVECONNECT = False
DRAGGING = False
DRAGSTART = (0, 0)
FROMNEURON = None
TONEURON = None

FPS = 120


class Connection():
    def __init__(self, inputNeuronPos, targetNeuronPos):
        self.markerSize = 3
        self.inputNeuronPos = inputNeuronPos
        self.targetNeuronPos = targetNeuronPos
        # Math.atan2(toY - fromY, toX - fromX);
        self.angle = atan2((targetNeuronPos[1] - inputNeuronPos[1]),
                           (targetNeuronPos[0] - inputNeuronPos[0]))
        # x = a + r cos(θ)
        # y = b + r sin(θ)
        self.fromX = inputNeuronPos[0] + NEURONSIZE * cos(self.angle)
        self.fromY = inputNeuronPos[1] + NEURONSIZE * sin(self.angle)
        self.toX = targetNeuronPos[0] - NEURONSIZE * cos(self.angle)
        self.toY = targetNeuronPos[1] - NEURONSIZE * sin(self.angle)
        self.markerX = int(targetNeuronPos[0] -
                           (NEURONSIZE + self.markerSize) * cos(self.angle))
        self.markerY = int(targetNeuronPos[1] -
                           (NEURONSIZE + self.markerSize) * sin(self.angle))

    def draw(self):
        pygame.draw.line(DISPLAYSURF, GREY, (self.fromX, self.fromY),
                         (self.toX, self.toY), 1)
        pygame.draw.circle(DISPLAYSURF, GREY, (self.markerX, self.markerY),
                           self.markerSize)


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
        clipRect.height = clipRect.height * (1 - self.baseNeuroTransmitter)
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
            pygame.draw.circle(DISPLAYSURF, GREY, (self.x, self.y), NEURONSIZE)
            pygame.draw.rect(DISPLAYSURF, BLACK, self.clipRect())
            return pygame.draw.circle(DISPLAYSURF, GREY, (self.x, self.y),
                                      NEURONSIZE, 1)
        elif not self.place:
            self.baseNeuroTransmitter = 0.4
            return pygame.draw.circle(DISPLAYSURF, BLACK, (self.x, self.y),
                                      NEURONSIZE + 1)


class playControl():
    def __init__(self):
        self.play = False
        self.offsetX = GRIDWIDTH
        self.offsetY = YMARGIN
        self._rect = self.draw()

    def draw(self):
        if self.play:
            pygame.draw.polygon(DISPLAYSURF, GREY,
                                ((self.offsetX, self.offsetY),
                                 (self.offsetX, self.offsetY + 25),
                                 (self.offsetX + 25, self.offsetY + 12.5)))
        else:
            pygame.draw.polygon(DISPLAYSURF, BLACK,
                                ((self.offsetX, self.offsetY),
                                 (self.offsetX, self.offsetY + 25),
                                 (self.offsetX + 25, self.offsetY + 12.5)))
            return pygame.draw.polygon(
                DISPLAYSURF, GREY, ((self.offsetX, self.offsetY),
                                    (self.offsetX, self.offsetY + 25),
                                    (self.offsetX + 25, self.offsetY + 12.5)),
                1)


class connectControl():
    def __init__(self):
        self.connect = False
        self.offsetX = GRIDWIDTH
        self.offsetY = YMARGIN
        self._rect = self.draw()

    def draw(self):
        if self.connect:
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 10, self.offsetY + 66), 10)
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 50, self.offsetY + 66), 10)
            pygame.draw.line(DISPLAYSURF, GREY,
                             (self.offsetX + 18, self.offsetY + 66),
                             (self.offsetX + 40, self.offsetY + 66), 1)
            pygame.draw.polygon(DISPLAYSURF, GREY,
                                ((self.offsetX + 40, self.offsetY + 66),
                                 (self.offsetX + 30, self.offsetY + 58),
                                 (self.offsetX + 30, self.offsetY + 74),
                                 (self.offsetX + 40, self.offsetY + 66)))
        else:
            pygame.draw.rect(DISPLAYSURF, BLACK,
                             (self.offsetX, self.offsetY + 56, 60, 20))
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 10, self.offsetY + 66), 10, 1)
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 50, self.offsetY + 66), 10, 1)
            pygame.draw.line(DISPLAYSURF, GREY,
                             (self.offsetX + 18, self.offsetY + 66),
                             (self.offsetX + 30, self.offsetY + 66), 1)
            pygame.draw.polygon(DISPLAYSURF, GREY,
                                ((self.offsetX + 40, self.offsetY + 66),
                                 (self.offsetX + 30, self.offsetY + 58),
                                 (self.offsetX + 30, self.offsetY + 74),
                                 (self.offsetX + 40, self.offsetY + 66)), 1)
            return pygame.Rect(self.offsetX, self.offsetY + 56, 60, 20)


class connectRemoveControl():
    def __init__(self):
        self.removeConnect = False
        self.offsetX = GRIDWIDTH
        self.offsetY = YMARGIN
        self._rect = self.draw()


    def draw(self):
        if self.removeConnect:
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 10, self.offsetY + 96), 10)
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 50, self.offsetY + 96), 10)
            pygame.draw.line(DISPLAYSURF, GREY, (self.offsetX + 18, self.offsetY + 96),
                             (self.offsetX + 40, self.offsetY + 96), 1)

            pygame.draw.line(DISPLAYSURF, RED,
            (self.offsetX + 24, self.offsetY + 91),
            (self.offsetX + 36, self.offsetY + 101), 2)
            pygame.draw.line(DISPLAYSURF, RED,
            (self.offsetX + 36, self.offsetY + 91),
            (self.offsetX + 24, self.offsetY + 101), 2)

        else:
            pygame.draw.rect(DISPLAYSURF, BLACK,
                             (self.offsetX, self.offsetY + 96, 60, 20))
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 10, self.offsetY + 96), 10, 1)
            pygame.draw.circle(DISPLAYSURF, GREY,
                               (self.offsetX + 50, self.offsetY + 96), 10, 1)
            pygame.draw.line(DISPLAYSURF, GREY, (self.offsetX + 18, self.offsetY + 96),
                             (self.offsetX + 40, self.offsetY + 96), 1)

            pygame.draw.line(DISPLAYSURF, GREY,
            (self.offsetX + 24, self.offsetY + 91),
            (self.offsetX + 36, self.offsetY + 101), 2)
            pygame.draw.line(DISPLAYSURF, GREY,
            (self.offsetX + 36, self.offsetY + 91),
            (self.offsetX + 24, self.offsetY + 101), 2)
            return pygame.Rect(self.offsetX, self.offsetY + 96, 60, 20)

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
        drawConnections()
        checkEvents()
        redraw()
        CLOCK.tick(FPS)


def initControls():
    PLAYC = playControl()
    CONNECTC = connectControl()
    REMOVECONNECTC = connectRemoveControl()
    CONTROLS.append(PLAYC)
    CONTROLS.append(CONNECTC)
    CONTROLS.append(REMOVECONNECTC)


def redraw():
    pygame.display.update()


def drawControls():
    CONTROLS[0].draw()
    CONTROLS[1].draw()
    CONTROLS[2].draw()


def clearGrid():
    # Rect(left, top, width, height)
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (XMARGIN - NEURONSIZE, YMARGIN - NEURONSIZE,
                      (GRIDSIZE * STEP) + NEURONSIZE * 2,
                      (GRIDSIZE * STEP) + NEURONSIZE * 2))


def clearScreen():
    DISPLAYSURF.fill(BLACK)


def updateNeurons():
    for neuron in NEURON_LIST:
        neuron.updateNeuron()


def drawConnections():
    for connection in CONNECTIONS:
        connection.draw()


def initNeurons():
    for i in range(GRIDSIZE + 1):
        for ii in range(GRIDSIZE + 1):
            n = Neuron(int(XMARGIN + (i * STEP)), int((YMARGIN) + (ii * STEP)))
            NEURON_LIST.append(n)

    # Place full grid
    # for neuron in NEURON_LIST:
    #     neuron.place = not neuron.place


def drawGrid(color):
    for i in range(GRIDSIZE):
        pygame.draw.line(DISPLAYSURF, color, (XMARGIN, YMARGIN + (i * STEP)),
                         ((GRIDWIDTH - YMARGIN), XMARGIN + (i * STEP)), 1)
        pygame.draw.line(DISPLAYSURF, color, (XMARGIN + (i * STEP), YMARGIN),
                         (YMARGIN + (i * STEP), HEIGHT - XMARGIN), 1)
    if i == (GRIDSIZE - 1):
        pygame.draw.line(
            DISPLAYSURF, color, (XMARGIN, YMARGIN + ((i + 1) * STEP)),
            ((GRIDWIDTH - YMARGIN), XMARGIN + ((i + 1) * STEP)), 1)
        pygame.draw.line(DISPLAYSURF, color,
                         (XMARGIN + ((i + 1) * STEP), YMARGIN),
                         (YMARGIN + ((i + 1) * STEP), GRIDHEIGHT - XMARGIN), 1)


def checkEvents():
    global PLAY, CONNECT, REMOVECONNECT, DRAGGING, DRAGSTART, FROMNEURON, TONEURON
    hovering = False
    for event in pygame.event.get():
        # Exit
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEMOTION:
            for neuron in NEURON_LIST:
                if neuron._rect.collidepoint(event.pos):
                    hovering = True
            # Hover controls
            if CONTROLS[0]._rect.collidepoint(
                    event.pos) or CONTROLS[1]._rect.collidepoint(event.pos) or CONTROLS[2]._rect.collidepoint(event.pos):
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
            # REMOVECONNECTC
                if CONTROLS[2]._rect.collidepoint(event.pos):
                    if CONTROLS[1].connect:
                        CONTROLS[1].connect = False
                        CONTROLS[1].draw()
                        CONNECT = False
                    CONTROLS[2].removeConnect = not CONTROLS[2].removeConnect
                    CONTROLS[2].draw()
                    REMOVECONNECT = not REMOVECONNECT

                if CONNECT and not DRAGGING and not CONTROLS[
                        1]._rect.collidepoint(
                            event.pos) and not CONTROLS[0]._rect.collidepoint(
                                event.pos):
                    for neuron in NEURON_LIST:
                        if neuron._rect.collidepoint(event.pos):
                            DRAGSTART = (neuron.x, neuron.y)
                            FROMNEURON = neuron
                    DRAGGING = True

        elif event.type == pygame.MOUSEBUTTONUP and DRAGGING:
            if event.button == 1:
                for neuron in NEURON_LIST:
                    if neuron._rect.collidepoint(
                            event.pos) and neuron.place and (FROMNEURON !=
                                                             neuron):
                        TONEURON = neuron
                        newCon = Connection(DRAGSTART, (neuron.x, neuron.y))
                        CONNECTIONS.append(newCon)
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
    if DRAGGING and DRAGSTART != (0, 0):
        dragEnd = pygame.mouse.get_pos()
        # mouseX = dragEnd[0]
        # mouseY = dragEnd[1]
        pygame.draw.line(DISPLAYSURF, WHITE, DRAGSTART, dragEnd, 1)
        pygame.draw.circle(DISPLAYSURF, WHITE, dragEnd, 4)


if __name__ == '__main__': main()
