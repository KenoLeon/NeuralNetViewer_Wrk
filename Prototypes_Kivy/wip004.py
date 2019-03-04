#!/usr/bin/env python
"""
NNV - wip 004 :

- Layout + canvas
- Increment - Decrement Controls

To Do:
Grid Background on Canvas
canvas Animation

"""
import os
from kivy.properties import BoundedNumericProperty
from kivy.app import App
from kivy.lang import Builder
from kivy.graphics import Rectangle
from kivy.graphics import Color
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


class rootCanvas(Widget):
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

    def drawGrid(self, *args):
        print('will draw grid')

    def play_stop(self, *args):
        print('will play_stop')


class wip004(App):

    gridSize = BoundedNumericProperty(10, min=0, max=20, errorvalue=0)
    rootCanvas = rootCanvas()

    def updateGrid(self, operation):
        if operation and self.gridSize <= 20:
            self.gridSize += 1
        elif self.gridSize >= 0:
            self.gridSize -= 1
        self.rootCanvas.drawGrid()

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
