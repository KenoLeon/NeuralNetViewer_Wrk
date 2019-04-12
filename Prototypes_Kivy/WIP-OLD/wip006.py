#!/usr/bin/env python
"""
NNV - wip 005 :

HAS:
- Layout + canvas
- Increment - Decrement Controls
- Grid
- Circle/Full Circle Examples

NEEDS:
- PLACE OBJECT WIDGET NEURONS

To Do:
- App architecure, where to add neurons.
- Paceholder neurons
"""


import os
from kivy.properties import BoundedNumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
from random import random as r
from kivy.uix.behaviors import ButtonBehavior


# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

#DEFAULT VARS :

GRIDSIZE = 4
NEURONSIZE = 14
XMARGIN = 60
YMARGIN = 60

class neuron(ButtonBehavior,Widget):
    def __init__(self, **kwargs):
        super(neuron, self).__init__(**kwargs)
        with self.canvas:
            Color(1, 0.1, 0.1, mode='rgb')
            Ellipse(pos=(XMARGIN, YMARGIN), size=(NEURONSIZE, NEURONSIZE))
    def on_press(self):
        with self.canvas:
            Color(0.4, 0.4, 0.4, mode='rgb')
            Ellipse(pos=(XMARGIN, YMARGIN), size=(NEURONSIZE, NEURONSIZE))

            # Line(ellipse=(0, 0, 150, 150))
        # self.rect = Rectangle(pos=self.pos, size=self.size)
        # self.bind(pos=self.update_rect)
        # self.bind(size=self.update_rect)

    # def update_rect(self, *args):
    #     self.rect.pos = self.pos
    #     self.rect.size = (self.size[0], self.size[1])
    #     self.draw()
    #
    # def draw(self, **kwargs):
    #     with self.canvas:
    #         Color(0.5, 0.5, 0.5, mode='rgb')



class grid(FloatLayout):

    _gridSize = GRIDSIZE

    def __init__(self, **kwargs):
        super(grid, self).__init__(**kwargs)
        with self.canvas:
            Color(0.1, 0.1, 0.1, mode='rgb')
        self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])
        self.drawGrid(_gridSize=self._gridSize)

    def drawGrid(self, **kwargs):
        _gridSize = kwargs.get('_gridSize', GRIDSIZE)
        if (_gridSize):
            self._gridSize = _gridSize
        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / _gridSize
        self.canvas.clear()
        with self.canvas:
            Color(0.1, 0.1, 0.1, mode='rgb')
            self.rect = Rectangle(pos=self.pos, size=self.size)
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


class wip005(App):

    gridSize = BoundedNumericProperty(GRIDSIZE, min=2, max=20, errorvalue=2)
    grid = grid()
    neuronLayer = FloatLayout()

    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.grid.drawGrid(_gridSize=self.gridSize - 1)

    def initNeurons(self):
        n = neuron()
        self.neuronLayer.add_widget(n)

    # From NMV:
    # def initNeurons():
    #     for i in range(GRIDSIZE + 1):
    #         for ii in range(GRIDSIZE + 1):
    #             n = Neuron(int(XMARGIN + (i * STEP)), int((YMARGIN) + (ii * STEP)))
    #             NEURON_LIST.append(n)


    def build(self):
        root = FloatLayout()
        sideBar = BoxLayout(
            padding=4,
            orientation='vertical',
            size_hint=(None, 1),
            width=200,
            spacing=2,
            pos_hint={'x':0.83, 'y':0})

        UI_1 = Builder.load_file(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'UI_1.kv'))
        sideBar.add_widget(UI_1)
        sideBar.add_widget(Widget())
        root.add_widget(self.grid)
        root.add_widget(self.neuronLayer)
        root.add_widget(sideBar)
        self.initNeurons()
        return root


if __name__ == '__main__':
    wip005().run()
