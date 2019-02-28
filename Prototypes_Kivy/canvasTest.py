from kivy.app import App
from kivy.graphics import Rectangle
from kivy.graphics import Color
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from random import random as r


class rootCanvas(Widget):
    def __init__(self, **kwargs):
        super(rootCanvas, self).__init__(**kwargs)
        with self.canvas:
            Color(r(), 1, 1, mode='hsv')
            self.rect = Rectangle(pos=self.pos, size=self.size)

        self.bind(pos=self.update_rect)
        self.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = (self.size[0], self.size[1])

    def change_color(self, *args):
        with self.canvas:
            Color(r(), 1, 1, mode='hsv')
            self.rect = Rectangle(pos=self.pos, size=self.size)


class canvasTest(App):
    def build(self):
        root = BoxLayout()
        sideBar = BoxLayout(size=(200, 100), size_hint=(None, 1))
        widget = rootCanvas()
        root.add_widget(widget)
        btn_1 = Button(
            text='Change Canvas Color',
            width=200,
            on_press=widget.change_color)
        sideBar.add_widget(btn_1)
        root.add_widget(sideBar)
        return root


if __name__ == '__main__':
    canvasTest().run()
