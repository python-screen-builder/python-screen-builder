from kivy.uix.widget import Widget
#from kivy.uix.label import Label
from gui import Label, BoxLayout

class TestClass(Widget):

    def __init__(self, **kwargs):
        super(TestClass, self).__init__(**kwargs)
        self.name = ""

