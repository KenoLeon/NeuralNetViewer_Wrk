import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.uix.widget import Widget
from kivy.metrics import dp
from kivy.core.window import Window

DRAG_START = ()
DRAG_END = ()
DRAGGING = False


class Main(Widget):
    def __init__(self, *args, **kwargs):
        Widget.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.layout1 = BoxLayout(opacity=0.3)
        self.add_widget(self.layout1)

    def draw(self, *args):
        self.layout1.canvas.clear()
        with self.canvas.before:
            Color(0.6, 0.6, 0.6, 1)
            self.bg = Rectangle(pos=self.pos, size=self.size)

    def drawLine(self):
        self.draw()
        print('will draw line')
        # with self.canvas.before:
        #     Color(1, 1, 1, 1)
        #     Line(points=[DRAG_START, 100,100], width=2)


# NOTE : Registers events, but can't call  widget

class ClickDrawLine(App):
    global DRAGGING

    title = "ClickDrawLine"
    linesCanvas = Main()

    def hello():
        print('Hello World')

    def on_motion(self, etype, motionevent):
        if DRAGGING == True:
            print('Dragging')

    def on_touch_down(self, event):
        global DRAGGING
        DRAGGING = True
        DRAG_START = event.pos


    def on_touch_up(self,event):
        global DRAGGING
        DRAGGING = False
        DRAG_END = event.pos


    def build(self):
        root = BoxLayout()
        root.add_widget(self.linesCanvas)
        return root


    Window.bind(on_motion=on_motion)
    Window.bind(on_touch_down=on_touch_down)
    Window.bind(on_touch_up=on_touch_up)


if __name__ == "__main__":
    ClickDrawLine().run()
