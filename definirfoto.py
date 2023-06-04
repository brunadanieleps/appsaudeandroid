from random import random
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.uix.filechooser import FileChooserListView, FileChooserIconView
from kivy.uix.floatlayout import FloatLayout


class MyPaintWidget(Widget):
    def on_touch_down(self, touch):
        color = (random(), random(), random())
        with self.canvas:
            Color(*color)
            d = 30.
            touch.ud['line'] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        touch.ud['line'].points += [touch.x, touch.y]


class MyPaintApp(App):

  def build(self):
        parent = Widget()
        painter = MyPaintWidget()
        Choose = Button(text = 'upload image')
        parent.add_widget(painter)
        parent.add_widget(Choose)


        def chooose_file(obj):
            fc = FileChooserIconView(title="Choose Image")
            image_path = self.fc.selection[0]
            image_name = file_path.split('/')[-1]

            with self.canvas.before:
                Rectangle(
                    size=self.size,
                    pos=self.pos,
                    source=image_name)

        return parent


if __name__ == '__main__':
    MyPaintApp().run()


