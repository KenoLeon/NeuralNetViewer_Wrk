#!/usr/bin/env python
"""
NNV - wip 014:

Resizable Grid with neurons, hover and place

"""

from kivy.config import Config
# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '500')

from kivy.core.window import Window
import os
import math
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import *
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors import ButtonBehavior

#DEFAULT/GLOBAL VARS :

XMARGIN = 60
YMARGIN = 60
OUTLINE_WIDTH = 2
NEURON_LIST = []
HOVER = False

# COLORS:
BACKGROUND_COLOR = SOMA_COLOR = [0.1, 0.1, 0.1]
GRID_COLOR = OUTLINE_COLOR = [0.6, 0.6, 0.6]

'''

TODO:

Animate Neurons...
Play/Stop button xxx

Game Loop
Neurotransmitter + box fill

To Connections.
To refinements.
TO next spec.

'''

class Neuron(ButtonBehavior, Widget):

    hovered = False
    baseNTLevel = 0.8

    def __init__(self, **kwargs):
        super(Neuron, self).__init__(**kwargs)
        self.place = False
        self.draw()
        self.bind(pos=self.redraw, size=self.redraw)
        Window.bind(mouse_pos=self.on_mouse_pos)

    # def clipRect(self):
    #     clipRect = self._rect.copy()
    #     clipRect.height = clipRect.height * (1 - self.ntLevel)
    #     return clipRect

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            StencilPush()
            Color(*OUTLINE_COLOR)
            # ADD extra outline ?
            self.outline = Ellipse()
            StencilUse()
            Color(*SOMA_COLOR)
            self.soma = Ellipse()
            Color(*OUTLINE_COLOR)
            self.ntLevel = Rectangle()
            StencilUnUse()
            StencilPop()


    def redraw(self, *args):
        self.soma.pos = self.pos
        self.soma.size = self.size
        self.ntLevel.pos = self.pos
        self.ntLevel.size = [self.size[0], self.size[1] * (1 - self.baseNTLevel)]
        self.outline.pos = [
            self.pos[0] - OUTLINE_WIDTH / 2, self.pos[1] - OUTLINE_WIDTH / 2
        ]
        sizeO = self.size[0] + OUTLINE_WIDTH
        self.outline.size = [sizeO, sizeO]

    def on_mouse_pos(self, *args):

        pos = args[1]
        inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.hovered = inside
        if inside:
            Window.set_system_cursor('hand')
            with self.canvas:
                Color(*OUTLINE_COLOR)
                self.outline = Ellipse()
                Color(*SOMA_COLOR)
                self.soma = Ellipse()
            self.redraw()
        else:
            Window.set_system_cursor('arrow')
            self.draw()
            self.redraw()

    def on_press(self):
        self.place = not self.place

    def on_release(self):
        pass


class gridNeuronsWidget(Widget):
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.gridLayer = BoxLayout(opacity=1)
        self.neuronLayer = Widget(opacity=1)
        self.add_widget(self.gridLayer)
        self.add_widget(self.neuronLayer)
        self._gridSize = 5
        self._neuronSize = 60
        self.initNeurons()

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

    def reInitGrid(self, *args, **kwargs):
        _gridSize = kwargs.get('_gridSize', self._gridSize)
        if (_gridSize):
            self._gridSize = _gridSize
        self.removeNeurons()
        self.initNeurons()
        self.draw()

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
            for i in range(self._gridSize + 1):
                for ii in range(self._gridSize + 1):
                    pos = (int(XMARGIN + (i * STEP) + offsetY -
                               self.neuronSize / 2),
                           int((YMARGIN) + (ii * STEP)) - self.neuronSize / 2)
                    NEURON_LIST[nC].size = [self.neuronSize, self.neuronSize]
                    NEURON_LIST[nC].pos = pos
                    nC += 1


class wip014(App):

    # class vars:
    title = "NNV - wip014"
    grid = gridNeuronsWidget()
    gridSize = BoundedNumericProperty(
        grid._gridSize + 1, min=2, max=20, errorvalue=2)

    # class Methods:
    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.grid.reInitGrid(_gridSize=self.gridSize - 1)


    def playStop(self):
        print('will playStop')


    # The Big enchilada :
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
    wip014().run()




    # def draw(self):
    #     self.canvas.clear()
    #
    #
    #     if not self.place:
    #         with self.canvas:
    #             Color(*SOMA_COLOR)
    #             self.outline = Ellipse()
    #             Color(*SOMA_COLOR)
    #             self.soma = Ellipse()
    #     elif self.place:
    #         with self.canvas:
    #             Color(*OUTLINE_COLOR)
    #             self.outline = Ellipse()
    #             Color(*SOMA_COLOR)
    #             self.soma = Ellipse()
    #             Color(*OUTLINE_COLOR)
    #             self.ntLevel = Rectangle()



        # def redraw(self, *args):
        #     self.soma.pos = self.pos
        #     self.soma.size = self.size
        #     if self.place:
        #         self.ntLevel.pos = self.pos
        #         self.ntLevel.size = [self.size[0], self.size[1] * (1 - self.baseNTLevel)]
        #     self.outline.pos = [
        #         self.pos[0] - OUTLINE_WIDTH / 2, self.pos[1] - OUTLINE_WIDTH / 2
        #     ]
        #     sizeO = self.size[0] + OUTLINE_WIDTH
        #     self.outline.size = [sizeO, sizeO]
