import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line, Ellipse, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget


class circleChild(Widget):
    def __init__(self, *args, **kwargs):
        self.pos = kwargs.get('_pos')
        self.size = kwargs.get('_size')
        super(circleChild, self).__init__()
        with self.canvas:
            Color(0.4, 0.6, 0.9, 1)  # ConrflowerBlue
            Ellipse(pos=self.pos, size=self.size, width=dp(2))


class RootWidget(BoxLayout):
    def __init__(self, *args, **kwargs):
        BoxLayout.__init__(self, *args, **kwargs)
        self.bind(pos=self.draw)
        self.bind(size=self.draw)
        self.layout1 = BoxLayout()
        self.layout2 = BoxLayout(opacity=0.8)
        self.add_widget(self.layout1)
        self.add_widget(self.layout2)
        self.childrenAdded = False

    def draw(self, *args):
        with self.canvas.before:
            Color(.8, .8, .8, 1)  # LightGrey
            self.bg = Rectangle(pos=self.pos, size=self.size)
        self.layout1.canvas.clear()
        with self.layout1.canvas:
            Color(0, 0, 0, 1)  # Black
            Line(
                points=[
                    self.center_x, self.center_y - 200, self.center_x,
                    self.center_y + 200
                ],
                width=dp(2))
            Line(
                points=[
                    self.center_x - 200, self.center_y, self.center_x + 200,
                    self.center_y
                ],
                width=dp(2))
        if not self.childrenAdded:
            self.addChildren()

    def addChildren(self, *args):
        circle1 = circleChild(
            _pos=[self.center_x + 100, self.center_y + 100], _size=[100, 100])
        circle2 = circleChild(
            _pos=[self.center_x + 100, self.center_y - 200], _size=[100, 100])
        circle3 = circleChild(
            _pos=[self.center_x - 200, self.center_y + 100], _size=[100, 100])
        circle4 = circleChild(
            _pos=[self.center_x - 200, self.center_y - 200], _size=[100, 100])
        self.layout2.add_widget(circle1)
        self.layout2.add_widget(circle2)
        self.layout2.add_widget(circle3)
        self.layout2.add_widget(circle4)
        self.childrenAdded = True


class PositionChildren(App):
    title = "PositionChildren"

    def build(self):
        return RootWidget()


if __name__ == "__main__":
    PositionChildren().run()
