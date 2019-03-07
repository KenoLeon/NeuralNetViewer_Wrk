# canvasTest.py...

from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color, Line
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.vector import Vector
from random import random as r


class rootCanvas(Widget):
    def __init__(self, **kwargs):
        super(rootCanvas, self).__init__(**kwargs)
        with self.canvas:
            Color(0.2, 0.2, 0.2, mode='rgb')
            self.rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(size=self.update_rect)
        self.bind(size=self.draw)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])

    def draw(self, *args):
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.2, 0.2, mode='rgb')
            self.rect = Rectangle(pos=self.pos, size=self.size)
            Color(1, 1, 1, mode='rgb')
            self.animRect = Rectangle(pos=(10, 10), size=(100, 100))

    def move(self, *args):
        self.animRect.pos = Vector(1,1) + self.animRect.pos
        print(self.animRect.pos)

    def start(self, *args):
        self.event = Clock.schedule_interval(self.move, 1.0 / 60.0)

    def stop(self, *args):
        self.event.cancel()


class canvasTest(App):
    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(size=(200, 100), size_hint=(None, 1),orientation='vertical')
        widget = rootCanvas()
        root.add_widget(widget)
        btn_1 = Button(text='Start', width=200, on_press=widget.start)
        btn_2 = Button(text='Stop', width=200, on_press=widget.stop)
        sideBar.add_widget(btn_1)
        sideBar.add_widget(btn_2)
        root.add_widget(sideBar)
        return root


if __name__ == '__main__':
    canvasTest().run()
