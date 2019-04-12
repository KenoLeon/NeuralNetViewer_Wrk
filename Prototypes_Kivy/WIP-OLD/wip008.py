#!/usr/bin/env python
"""
NNV - wip 008:
"""

import os
import math
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget
from kivy.config import Config
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors import ButtonBehavior

# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

#DEFAULT VARS :
XMARGIN = 60
YMARGIN = 60

NEURON_LIST = []

'''
TODO:
PLACE NEURONS:

- Neuron as Object...
- Hover click/focus
- Place.

>> To Animate Neuron

'''


class Neuron(Widget):
        def __init__(self, **kwargs):
            _pos = kwargs.get('_pos')
            _size = kwargs.get('_size')
            super(Neuron, self).__init__()
            with self.canvas:
                Color(0.1, 0.1, 1, mode='rgb')
                self.bg = Ellipse(pos = _pos, size=_size)

class gridWidget(FloatLayout):
    def __init__(self, *args, **kwargs):
        FloatLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.gridLayer = BoxLayout(opacity=1)
        self.neuronLayer = BoxLayout()
        self.add_widget(self.gridLayer)
        self.add_widget(self.neuronLayer)
        self._gridSize = 4


    def initNeurons(self, *args, **kwargs):
        # print(self._gridSize)
        if float(math.log(self._gridSize)) > 0:
            NEURONSIZE = 1 / float(math.log(self._gridSize)) * 40
        else:
            NEURONSIZE = 60
        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / self._gridSize

        for i in range(self._gridSize + 1):
            for ii in range(self._gridSize + 1):
                n = Neuron(_pos=(int(XMARGIN + (i * STEP) +
                         offsetY - NEURONSIZE / 2),
                     int((YMARGIN) + (ii * STEP)) - NEURONSIZE / 2),_size=(NEURONSIZE,NEURONSIZE))
                self.neuronLayer.add_widget(n)


    def draw(self, *args, **kwargs):
        # method vars :
        _gridSize = kwargs.get('_gridSize', self._gridSize)
        if (_gridSize):
            self._gridSize = _gridSize

        if float(math.log(_gridSize)) > 0:
            NEURONSIZE = 1 / float(math.log(_gridSize)) * 40
        else:
            NEURONSIZE = 60
        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / _gridSize

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, mode='rgb')
            self.bg = Rectangle(pos=self.pos, size=self.size)
        # GRID:
        self.gridLayer.canvas.clear()
        with self.gridLayer.canvas:
            Color(0.6, 0.6, 0.6, mode='rgb')
            for i in range(_gridSize):
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
            if i == (_gridSize - 1):
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


            # Logic:
            # If INIT and not grid change,reposition neurons.
            # If Change Grid Size, remove neurons, deal with init.

            # Alternative 1 :
            # REMOVE WIDGETS  RE INIT

            # Alternative 2:
            # Decouple grid and Neurons

            self.initNeurons()


class wip007(App):

    # class vars:
    title = "NNV - wip007"
    grid = gridWidget()
    gridSize = BoundedNumericProperty(
        grid._gridSize + 1, min=2, max=20, errorvalue=2)

    # class Methods:
    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.grid.draw(_gridSize=self.gridSize - 1)

    # The Big enchilada :
    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(
            padding=4,
            orientation='vertical',
            size_hint=(None, 0.60),
            width=200,
            spacing=2,
            pos_hint={'top': 1})
        UI_1 = Builder.load_file(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'UI_1.kv'))
        sideBar.add_widget(UI_1)
        sideBar.add_widget(Widget())
        root.add_widget(self.grid)
        root.add_widget(sideBar)
        return root


if __name__ == "__main__":
    wip007().run()
