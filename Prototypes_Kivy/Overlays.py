from kivy.base import runTouchApp
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line
from kivy.metrics import dp

Window.clearcolor = (1, 1, 1, 1)


class Overlays(Screen):

    def __init__(self, **kwargs):
        super(Overlays, self).__init__(**kwargs)
        self.size = Window.size

        layout1 = BoxLayout(opacity=0.5)
        with layout1.canvas:
            Color(1, 0, 0, 1)   # red colour
            Line(points=[self.center_x, self.height / 4, self.center_x, self.height * 3/4], width=dp(2))
            Line(points=[self.width * 3/ 4, self.center_y, self.width /4, self.center_y], width=dp(2))

        layout2 = BoxLayout()
        with layout2.canvas:
            Color(0, 0, 0, 1)   # black colour
            Line(circle=[self.center_x, self.center_y, 190], width=dp(2))

        self.add_widget(layout1)
        self.add_widget(layout2)


if __name__ == "__main__":
    runTouchApp(Overlays())
