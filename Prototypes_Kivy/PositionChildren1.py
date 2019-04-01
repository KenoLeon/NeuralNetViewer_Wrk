import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

class circleChild( Widget):
    def __init__(self, **kwargs):
        super(circleChild, self).__init__(**kwargs)
        self.draw()
        self.bind(pos=self.redraw, size=self.redraw)

    def draw(self):
        with self.canvas:
            Color(0.4, 0.6, 0.9, 1)  # ConrflowerBlue
            self.ellipse = Ellipse(width=dp(2))

    def redraw(self, *args):
        # reuse
        self.ellipse.pos = self.pos
        self.ellipse.size = self.size

class RootWidget(Widget):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.draw()
        self.bind(pos=self.redraw, size=self.redraw)

        self.circle1 = circleChild(size=[100, 100])
        self.circle2 = circleChild(size=[100, 100])
        self.circle3 = circleChild(size=[100, 100])
        self.circle4 = circleChild(size=[100, 100])
        for c in (self.circle1, self.circle2, self.circle3, self.circle4):
            self.add_widget(c)

    def draw(self):
        with self.canvas.before:
            Color(.8, .8, .8, 1)  # LightGrey
            self.bg = Rectangle(pos=self.pos, size=self.size)
            Color(0, 0, 0, 1)  # Black
            self.vline = Line(width=dp(2))
            self.hline = Line(width=dp(2))

    def redraw(self, *args):
        # reuse
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.vline.points = [
            self.center_x,
            self.center_y - 200,
            self.center_x,
            self.center_y + 200
        ]
        self.hline.points=[
            self.center_x - 200,
            self.center_y,
            self.center_x + 200,
            self.center_y
        ]
        self.circle1.pos = [self.center_x + 100, self.center_y + 100]
        self.circle1.size = [20, 20]
        self.circle2.pos = [self.center_x + 100, self.center_y - 200]
        self.circle3.pos = [self.center_x - 200, self.center_y + 100]
        self.circle4.pos = [self.center_x - 200, self.center_y - 200]

class PositionChildren(App):
    title = "PositionChildren"

    def build(self):
        return RootWidget(size=(100, 100))

if __name__ == "__main__":
    PositionChildren().run()
