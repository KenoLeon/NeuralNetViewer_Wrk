import kivy
from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle


# https://stackoverflow.com/questions/30207707/how-to-fill-canvas-with-an-image-in-kivy

class rootLayout(BoxLayout):
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

class layer1(BoxLayout):
    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        with self.canvas:
            Color(1, 0.1, 0.1, mode='rgb')
            Ellipse(rootl.center_x,rootl.center_y, size=(20,20))
        # self.bind(pos=self.update_ell)
        # self.bind(size=self.update_ell)

    # def update_ell(self, *args):
    #     self.ell.pos = self.pos
    #     self.ell.size = self.size


class layer2(BoxLayout):

    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        with self.canvas:
            Color(0.1, 1, 1, mode='rgb')
            self.circ = Line(circle=(rootl.center_x,rootl.center_y,190))
        # self.bind(pos=self.update_circ)
        # self.bind(size=self.update_circ)

    # def update_circ(self, *args):
    #     self.circ.pos = self.pos
    #     self.circ.size = self.size


class layoutOverlay(App):


    def build(self):
        global rootl
        rootl = rootLayout()
        rootl.add_widget(layer1())
        rootl.add_widget(layer2())
        return rootl


if __name__ == '__main__':
    layoutOverlay().run()
