from kivy.uix.widget import Widget
#from kivy.uix.label import Label
from gui import Label, BoxLayout

class TestClass(Widget):

    def __init__(self, **kwargs):
        super(TestClass, self).__init__(**kwargs)
        self.name = ""
        #self.keys = 88
        #self.label = Label(text = 'TestClass', pos_hint = {'top': 1}, size_hint = (1, 1))
        #self.add_widget(self.label)
        pass

