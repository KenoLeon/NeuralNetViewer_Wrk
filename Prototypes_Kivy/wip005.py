#!/usr/bin/env python
"""
NNV - wip 005 :

HAS:
- Layout + canvas
- Increment - Decrement Controls

NEEDS:
- PLACE NEURON
- PLAY  NEURON

To Do:

canvas Animation/Loop


"""
import os
from kivy.properties import BoundedNumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.config import Config
from random import random as r

# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

# VARS :

GRIDSIZE = 4
NEURONSIZE = 14


class rootCanvas(Widget):

    _gridSize = GRIDSIZE

    def __init__(self, **kwargs):
        super(rootCanvas, self).__init__(**kwargs)
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
        # ToDo to local vars

        # GRIDWIDTH =  canvas width
        # GRIDHEIGHT =  canvas heigth

        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        XMARGIN = 80
        YMARGIN = 80
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        print(offsetY)

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

    def play_stop(self, *args):
        print('will play_stop')


class wip004(App):

    gridSize = BoundedNumericProperty(GRIDSIZE, min=1, max=20, errorvalue=1)
    rootCanvas = rootCanvas()

    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.rootCanvas.drawGrid(_gridSize=self.gridSize)

    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(
            padding=4,
            orientation='vertical',
            size_hint=(None, 1),
            width=200,
            spacing=2)
        root.add_widget(self.rootCanvas)
        UI_1 = Builder.load_file(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)), 'UI_1.kv'))
        sideBar.add_widget(UI_1)
        sideBar.add_widget(Widget())
        root.add_widget(sideBar)
        return root


if __name__ == '__main__':
    wip004().run()
