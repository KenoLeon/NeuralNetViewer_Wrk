#!/usr/bin/env python
"""
NNV - wip 007, slightly Different Architecture:
Grid as root for neuron widgets

"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp


class gridWidget(BoxLayout):

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.layout1 = BoxLayout(opacity=0.3)
        self.layout2 = BoxLayout()
        self.add_widget(self.layout1)
        self.add_widget(self.layout2)

    def draw(self, *args):
        with self.canvas.before:
            Color(1,1,.5,1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.layout1.canvas.clear()
        with self.layout1.canvas:
            Color(1, 0, 0, 1)   # red colour
            Line(points=[self.center_x, self.height / 4, self.center_x, self.height * 3/4], width=dp(2))
            Line(points=[self.width * 3/ 4, self.center_y, self.width /4, self.center_y], width=dp(2))
        self.layout2.canvas.clear()
        with self.layout2.canvas:
            Color(0, 0, 0, 1)   # black colour
            Line(circle=[self.center_x, self.center_y, 190], width=dp(2))

# TODO: Add SideBar...
# TODO: Integrate Grid...


class wip007(App):
    title = "NNV - wip007"
    grid = gridWidget()
    def build(self):
        root = FloatLayout()
        root.add_widget(self.grid)
        return gridWidget()


if __name__ == "__main__":
    wip007().run()
