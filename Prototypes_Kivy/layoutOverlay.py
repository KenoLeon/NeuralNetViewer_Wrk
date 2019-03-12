import kivy
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle


# https://stackoverflow.com/questions/30207707/how-to-fill-canvas-with-an-image-in-kivy

class rLayout(BoxLayout):
    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        with self.canvas.before:
            Color(1,1,.5,1)
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_bg)
        self.bind(size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

class layoutOverlay(App):
    def build(self):
        return rLayout()

if __name__ == '__main__':
    layoutOverlay().run()
