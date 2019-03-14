#!/usr/bin/env python
"""
NNV - wip 007, slightly Different Architecture:
Grid as root for neuron widgets

"""

import os
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.properties import BoundedNumericProperty
from kivy.uix.widget import Widget
from kivy.config import Config


# Window :
Config.set('graphics', 'width', '1200')
Config.set('graphics', 'height', '800')

#DEFAULT VARS :
GRIDSIZE = 4
NEURONSIZE = 14
XMARGIN = 60
YMARGIN = 60

class gridWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.gridlayout = BoxLayout(opacity=1)
        # self.layout2 = BoxLayout()
        self.add_widget(self.gridlayout)
        # self.add_widget(self.layout2)

    def draw(self, *args, **kwargs):
        _gridSize = kwargs.get('_gridSize', GRIDSIZE)
        if (_gridSize):
            self._gridSize = _gridSize

        GRIDWIDTH = self.size[0]
        GRIDHEIGHT = self.size[1]
        offsetY = (
            (GRIDWIDTH - (GRIDHEIGHT - (XMARGIN + YMARGIN))) / 2) - YMARGIN
        STEP = (GRIDHEIGHT - (XMARGIN + YMARGIN)) / _gridSize

        with self.canvas.before:
            Color(0.1, 0.1, 0.1, mode='rgb')
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.gridlayout.canvas.clear()
        with self.gridlayout.canvas:
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

class wip007(App):

    # class vars:
    title = "NNV - wip007"
    gridSize = BoundedNumericProperty(GRIDSIZE, min=2, max=20, errorvalue=2)
    grid = gridWidget()

    # class Methods:
    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.grid.draw(_gridSize=self.gridSize - 1)


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
