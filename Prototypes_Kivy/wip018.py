#!/usr/bin/env python
"""
NNV - wip 018:

Resizable Grid with neurons, hover,place and Animation

"""

from kivy.config import Config
# Window :
Config.set('graphics','window_state', 'maximized')
# Debug :
# Config.set('graphics', 'width', '1200')
# Config.set('graphics', 'height', '600')


from kivy.core.window import Window
import os
import math
from math import atan2, cos, sin
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, BooleanProperty, ObjectProperty, NumericProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock

#DEFAULT/GLOBAL VARS :

XMARGIN = 60
YMARGIN = 60
OUTLINE_WIDTH = 2


# COLORS:
BACKGROUND_COLOR = SOMA_COLOR = [0.1, 0.1, 0.1]
GRID_COLOR = OUTLINE_COLOR = [0.6, 0.6, 0.6]

# TEST COLORS:
RED = [1, 0, 0]

# GLOBALS
PLACE = True
CONNECT = False
DRAGGING = False
DRAG_START = ()
DRAG_END = ()

FROMNEURON = None
TARGETNEURON = None
NEURON_LIST = []
CONNECTION_LIST = []

'''

Connections.
# TODO ( week 3 ):

 - Add Marker
 - Affect neurons.
 - Clear all
 - Remove Connection



BUGS:
- Connections list called while empty ?
- After grid resize, go back to place neurons.

DONE:
- Outside to Outside Line XXX
- Connection is made if cancelled DRAG. XXX
- Connection is made when no target neuron. XXX
- on Click without neurons crash. XXX
- Don't connect if self or not place. XXX
- On gridSize remove connections. XXX
- on_release if target neuron, add Connection XXX
- from Neuron target Neuron XXX
- Get Object XXX
- DRAGSTART center of neuron XXX
- Button toggles are buggy :( XXX
- New connection object XXX
- Resize methods. XXX
- Draw all connections, loop logic in grid. XXX

To refinements.
To next spec.

'''


class Connection(Widget):
    def __init__(self,**kwargs):
        self.fromNeuron = kwargs.get('fromNeuron')
        self.targetNeuron = kwargs.get('targetNeuron')
        self.neuronSize = self.fromNeuron.width

        super(Connection, self).__init__()
        self.draw()
        print('neuronSize' + str(self.neuronSize) )


    # self.markerSize = 3
    # self.inputNeuronPos = inputNeuronPos
    # self.targetNeuronPos = targetNeuronPos
    # self.fromNeuron = fromNeuron
    # self.toNeuron = toNeuron

    # self.angle = atan2((targetNeuronPos[1] - inputNeuronPos[1]),
    #                    (targetNeuronPos[0] - inputNeuronPos[0]))
    # self.fromX = inputNeuronPos[0] + NEURONSIZE * cos(self.angle)
    # self.fromY = inputNeuronPos[1] + NEURONSIZE * sin(self.angle)
    # self.toX = targetNeuronPos[0] - NEURONSIZE * cos(self.angle)
    # self.toY = targetNeuronPos[1] - NEURONSIZE * sin(self.angle)

# self.markerX = int(targetNeuronPos[0] -
#                    (NEURONSIZE + self.markerSize) * cos(self.angle))
# self.markerY = int(targetNeuronPos[1] -
#                    (NEURONSIZE + self.markerSize) * sin(self.angle))
# self._rect = pygame.draw.line(DISPLAYSURF, GREY,
#                               (self.fromX, self.fromY),
#                               (self.toX, self.toY), 3)


    def draw(self, *args):

        fromNeuron = self.fromNeuron.center
        targetNeuron = self.targetNeuron.center
        neuronSize = (self.fromNeuron.width/2)+2

        angle = atan2((targetNeuron[1] - fromNeuron[1]),
                           (targetNeuron[0] - fromNeuron[0]))
        fromX = fromNeuron[0] + neuronSize * cos(angle)
        fromY = fromNeuron[1] + neuronSize * sin(angle)
        toX = targetNeuron[0] - neuronSize * cos(angle)
        toY = targetNeuron[1] - neuronSize * sin(angle)



        # for arg in args:
        #     print("another arg through *argv:", args)
        self.canvas.clear()
        with self.canvas:
            Color(*RED)
            Line(points=[(fromX,fromY),(toX, toY)], width=0.8)


class Neuron(ButtonBehavior, Widget):

    hovered = False
    baseNTLevel = 0.4
    mousePos = []

    def __init__(self, **kwargs):
        super(Neuron, self).__init__(**kwargs)
        self.always_release = True
        self.place = False
        self.draw()
        self.bind(pos=self.redraw, size=self.redraw)
        Window.bind(mouse_pos=self.on_mouse_pos)
        self.ntRelease = 0.1

    def draw(self, **kwargs):
        self.canvas.clear()
        if not self.place:
            with self.canvas:
                Color(*SOMA_COLOR)
                self.outline = Ellipse()
                Color(*SOMA_COLOR)
                self.soma = Ellipse()
        elif self.place:
            with self.canvas:
                StencilPush()
                self.mask = Ellipse()
                StencilUse()
                Color(*OUTLINE_COLOR)
                self.outline = Ellipse()
                Color(*SOMA_COLOR)
                self.soma = Ellipse()
                Color(*OUTLINE_COLOR)
                self.ntLevel = Rectangle()
                StencilUnUse()
                StencilPop()

    def redraw(self, *args):
        sizeO = [self.size[0] + OUTLINE_WIDTH, self.size[0] + OUTLINE_WIDTH]
        posO = [
            self.pos[0] - OUTLINE_WIDTH / 2, self.pos[1] - OUTLINE_WIDTH / 2
        ]

        if self.place:
            self.mask.pos = posO
            self.mask.size = sizeO
            self.ntLevel.pos = self.pos
            self.ntLevel.size = [self.size[0], self.size[1] * self.baseNTLevel]

        self.soma.pos = self.pos
        self.soma.size = self.size
        self.outline.pos = posO
        self.outline.size = sizeO

    def on_mouse_pos(self, *args):
        global TARGETNEURON

        self.mousePos = args[1]
        inside = self.collide_point(*self.to_widget(*self.mousePos))
        if self.hovered == inside:
            return
        self.hovered = inside
        if inside:
            if CONNECT:
                Window.set_system_cursor('crosshair')
            else:
                Window.set_system_cursor('hand')

            if not self.place and not CONNECT:
                with self.canvas:
                    Color(*OUTLINE_COLOR)
                    self.outline = Ellipse()
                    Color(*SOMA_COLOR)
                    self.soma = Ellipse()

            if self.place and CONNECT and DRAGGING:
                TARGETNEURON = self

            self.redraw()
        else:
            TARGETNEURON = None
            Window.set_system_cursor('arrow')
            self.draw()
            self.redraw()

    def on_press(self):
        global DRAGGING, DRAG_START, FROMNEURON, TARGETNEURON
        TARGETNEURON = None
        if PLACE:
            self.place = not self.place
            self.draw()
            self.redraw()
        elif CONNECT and self.place:
            DRAGGING = True
            DRAG_START = self.center
            FROMNEURON = self


    def on_release(self):
        global DRAGGING, DRAG_START
        if CONNECT:
            DRAGGING = False
            self.parent.parent.addConnection()


    def updateNeuron(self):
        if self.place:
            if self.baseNTLevel < 1:
                self.baseNTLevel += self.ntRelease
                self.redraw()
            elif self.baseNTLevel >= 1:
                self.redraw()
                self.baseNTLevel = 0


class gridNeuronsWidget(Widget):
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        Window.bind(mouse_pos=self.mouse_pos)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.gridLayer = BoxLayout(opacity=1)
        self.neuronLayer = Widget(opacity=1)
        self.drawLayer = Widget(opacity=1)
        self.connectionsLayer = Widget(opacity=1)
        self.add_widget(self.gridLayer)
        self.add_widget(self.neuronLayer)
        self.add_widget(self.drawLayer)
        self.add_widget(self.connectionsLayer)
        self._gridSize = 5
        self._neuronSize = 60
        self.initNeurons()

    def addConnection(self):
        self.drawLayer.canvas.clear()
        if FROMNEURON != TARGETNEURON and TARGETNEURON != None:
            newCon = Connection(fromNeuron = FROMNEURON, targetNeuron = TARGETNEURON)
            CONNECTION_LIST.append(newCon)
            self.connectionsLayer.add_widget(newCon)

    def mouse_pos(self, window, pos):
        if CONNECT and DRAGGING:
            self.drawLine(pos)

    def initNeurons(self):
        for i in range(self._gridSize + 1):
            for ii in range(self._gridSize + 1):
                n = Neuron(size=[100, 100])
                NEURON_LIST.append(n)
                self.neuronLayer.add_widget(n)

    def removeNeurons(self, *args, **kwargs):
        for neuron in NEURON_LIST:
            self.neuronLayer.remove_widget(neuron)
        NEURON_LIST.clear()

    def removeConnections(self, *args, **kwargs):
        for connection in CONNECTION_LIST:
            self.connectionsLayer.remove_widget(connection)
        CONNECTION_LIST.clear()


    def reInitGrid(self, *args, **kwargs):
        _gridSize = kwargs.get('_gridSize', self._gridSize)
        if (_gridSize):
            self._gridSize = _gridSize
        self.removeNeurons()
        self.initNeurons()
        self.removeConnections()
        self.draw()


    def drawLine(self, mPos):
        self.drawLayer.canvas.clear()
        with self.drawLayer.canvas:
            Color(1, 1, 1, 1)
            Line(points=[DRAG_START[0], DRAG_START[1], mPos[0], mPos[1]], width=0.8)


    def draw(self, *args, **kwargs):
        # method vars :
        _gridSize = kwargs.get('_gridSize', self._gridSize)
        if (_gridSize):
            self._gridSize = _gridSize

        if float(math.log(self._gridSize)) > 0:
            self.neuronSize = 1 / float(math.log(self._gridSize)) * 46
        else:
            self.neuronSize = 60
        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / self._gridSize

        with self.canvas.before:
            Color(*BACKGROUND_COLOR)
            self.bg = Rectangle(pos=self.pos, size=self.size)


        # GRID:
        self.gridLayer.canvas.clear()
        with self.gridLayer.canvas:
            Color(*GRID_COLOR)
            for i in range(self._gridSize):
                Line(
                    points=[
                        XMARGIN + offsetY, YMARGIN + (i * STEP),
                        (GRIDHEIGHT - YMARGIN) + offsetY, XMARGIN + (i * STEP)
                    ],
                    width=1)
                Line(
                    points=[
                        XMARGIN + (i * STEP) + offsetY, YMARGIN,
                        YMARGIN + (i * STEP) + offsetY, GRIDHEIGHT - XMARGIN
                    ],
                    width=1)
            if i == (self._gridSize - 1):
                Line(
                    points=[
                        XMARGIN + offsetY, YMARGIN + ((i + 1) * STEP),
                        (GRIDHEIGHT - YMARGIN) + offsetY,
                        XMARGIN + ((i + 1) * STEP)
                    ],
                    width=1)
                Line(
                    points=[
                        XMARGIN + ((i + 1) * STEP) + offsetY, YMARGIN,
                        YMARGIN + ((i + 1) * STEP) + offsetY,
                        GRIDHEIGHT - XMARGIN
                    ],
                    width=1)

            nC = 0
            # Update Neurons:

            for i in range(self._gridSize + 1):
                for ii in range(self._gridSize + 1):
                    pos = (int(XMARGIN + (i * STEP) + offsetY -
                               self.neuronSize / 2),
                           int((YMARGIN) + (ii * STEP)) - self.neuronSize / 2)
                    NEURON_LIST[nC].size = [self.neuronSize, self.neuronSize]
                    NEURON_LIST[nC].pos = pos
                    nC += 1

        # Connections:
        # Draw order is important Grid->Neurons->Connections
        for connection in CONNECTION_LIST:
            connection.draw()
            # connection.draw(int(self.neuronSize))

class wip018(App):
    # APP VARS:
    title = "NNV - wip018"
    grid = gridNeuronsWidget()
    gridSize = BoundedNumericProperty(
        grid._gridSize + 1, min=2, max=20, errorvalue=2)
    _play = False
    _connect = False
    _playStopEvent = None
    _connectEvent = None
    _FPS = BoundedNumericProperty(
        24, min=1, max=120, errorvalue=1)

    # APP Methods:
    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.grid.reInitGrid(_gridSize=self.gridSize - 1)

    def updateFPS(self, operation):
        if operation == True:
            self._FPS += 1
        else:
            self._FPS -= 1

        if self._play == True:
            Clock.unschedule(self._playStopEvent)
            self._playStopEvent = Clock.schedule_interval(self.updateNeurons,
                                                  1 / self._FPS)


    def playStop(self):
        self._play = not self._play
        if self._play == True:
            self._playStopEvent = Clock.schedule_interval(self.updateNeurons,
                                                  1 / self._FPS)
        else:
            Clock.unschedule(self._playStopEvent)

    def updateNeurons(self, *args):
        for neuron in NEURON_LIST:
            neuron.updateNeuron()

    def toggleConnect(self):
        global CONNECT, PLACE
        CONNECT = not CONNECT
        if PLACE == True:
            PLACE = False
        if CONNECT == True:
            Window.set_system_cursor('crosshair')


    def togglePlace(self):
        global CONNECT, PLACE
        PLACE = not PLACE
        if CONNECT == True:
            CONNECT = False
        if PLACE == True:
            Window.set_system_cursor('hand')


    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(
            orientation='vertical',
            size_hint=(None, None),
            width=200,
            spacing=4,
            pos_hint={'top': 1})
        UI_1 = Builder.load_file(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'UI_1.kv'))
        UI_2 = Builder.load_file(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'UI_2.kv'))
        sideBar.add_widget(UI_1)
        sideBar.add_widget(UI_2)

        root.add_widget(self.grid)
        root.add_widget(sideBar)
        return root


if __name__ == "__main__":
    wip018().run()
