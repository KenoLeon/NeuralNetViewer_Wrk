import kivy
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.core.window import Window

class rootLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.size = Window.size
        layout1 = BoxLayout(opacity=1)

        def draw():
            with self.canvas.before:
                Color(1,1,.5,1)
                self.bg = Rectangle(pos=self.pos, size=self.size)
                self.bind(pos=draw)
                self.bind(size=draw)


        # with self.canvas.before:
        #     Color(1,1,.5,1)
        #     self.bg = Rectangle(pos=self.pos, size=self.size)
        # self.bind(pos=self.update)
        # self.bind(size=self.update)
        #
        # with layout1.canvas:
        #     Color(1, 0, 0, 1)   # red colour
        #     Line(points=[self.center_x, self.height / 4, self.center_x, self.height * 3/4], width=dp(2))
        #     Line(points=[self.width * 3/ 4, self.center_y, self.width /4, self.center_y], width=dp(2))

        self.add_widget(layout1)
        draw()

    def update(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
        print(self.center_x)



class Overlay_2(App):
    def build(self):
        return rootLayout()


if __name__ == '__main__':
    Overlay_2().run()
