import kivy

kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.widget import Widget

from kivy.lang import Builder

Builder.load_string('''
<TheWidget>:

    TextInput:
        id: inp
        hint_text: "I'm an input box!"
        pos: root.x, (root.height / 2) + 250
        size: 300,50
        color: .10,.9,1,2

    Label:
        id: label
        text: ""
        pos: root.x + 400, 525
        color: 244, 65, 223,1

    Button:
        text: "Submit"
        font_size: 16
        pos: root.x + 310, (root.height / 2) + 250
        size: 100,50
        on_press: inp.text = ""
        on_press: label.text = "Submitted"
''')

class TheWidget(Widget):
    pass
    # def __init__(self, **kwargs):
    #     super(TheWidget, self).__init__(**kwargs)


class WidgetsApp(App):
    # This returns the content we want in the window
    def build(self):
        # Return a the TheWidget Class
        return TheWidget();


if __name__ == "__main__":
    widgetsapp = WidgetsApp()
    widgetsapp.run()