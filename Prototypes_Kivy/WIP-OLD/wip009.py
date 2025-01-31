#!/usr/bin/env python
"""
NNV - wip 009:

"""


from kivy.config import Config
# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '400')

from kivy.core.window import Window

import os
import math
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.behaviors import ButtonBehavior


#DEFAULT VARS :
XMARGIN = 60
YMARGIN = 60

NEURON_LIST = []

'''
TODO:
PLACE NEURONS:

- Neuron as Object xxx
- Hover click/focus:
... remove factory, implement at neuron level ?

- Place.

>> To Animate Neuron

'''


class Neuron(Widget):

        hovered = False
        border_point= None

        def __init__(self, **kwargs):
            self.pos = kwargs.get('_pos')
            self.size  = kwargs.get('_size')
            Window.bind(mouse_pos=self.on_mouse_pos)
            super(Neuron, self).__init__()
            with self.canvas:
                Color(0.1, 0.1, 0.1, mode='rgb')
                self.bg = Ellipse(pos = self.pos, size=self.size)

        def on_mouse_pos(self, *args):
            pass
            # if self.collide_point(*args[1]): print (self.to_window(*args[1]))
            # if self.collide_point(*args[1]): print (self.to_parent(*args[1]))
            # if self.collide_point(*args[1]): print (self.to_widget(*args[1]))
            # if self.collide_point(*args[1]): print (self.to_local(*args[1]))

class gridNeuronsWidget(RelativeLayout):
    def __init__(self, *args, **kwargs):
        FloatLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.gridLayer = BoxLayout(opacity=1)
        self.neuronLayer = FloatLayout(opacity=1)
        self.add_widget(self.gridLayer)
        self.add_widget(self.neuronLayer)
        self._gridSize = 1
        self.neuronsInitialized = False


    def initNeurons(self, *args, **kwargs):
        if float(math.log(self._gridSize)) > 0:
            NEURONSIZE = 1 / float(math.log(self._gridSize)) * 40
        else:
            NEURONSIZE = 60
        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / self._gridSize

        print('|-----------------*-----------------|')
        for i in range(self._gridSize + 1):
            for ii in range(self._gridSize + 1):
                n = Neuron(size_hint=(None, None), _pos=(int(XMARGIN + (i * STEP) +
                         offsetY - NEURONSIZE / 2),
                     int((YMARGIN) + (ii * STEP)) - NEURONSIZE / 2),_size=(NEURONSIZE,NEURONSIZE))
                NEURON_LIST.append(n)
                self.neuronLayer.add_widget(n)
                print('Neuron placed at:' + str(n.pos))
                print('With Size:' + str(n.size))
        print('|-----------------*-----------------|')
        self.neuronsInitialized = True


    def updateNeuronPos(self, *args, **kwargs):
        # Note: Ideally neuron pos needs to be binded to neuronLayer
        for neuron in NEURON_LIST:
            self.neuronLayer.remove_widget(neuron)
        self.initNeurons()

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

        if not self.neuronsInitialized:
            self.initNeurons()
        else:
            self.updateNeuronPos()


class wip009(App):

    # class vars:
    title = "NNV - wip007"
    grid = gridNeuronsWidget()
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
    wip009().run()



#
# Neuron placed at:[130, 30.0]
# With Size:[60, 60]
# Neuron placed at:[130, 710.0]
# With Size:[60, 60]
# Neuron placed at:[810, 30.0]
# With Size:[60, 60]
# Neuron placed at:[810, 710.0]
# With Size:[60, 60]
