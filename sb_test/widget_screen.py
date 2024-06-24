import json

from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from os.path import exists
from gui import *

class WidgetScreen(Screen):

    def __init__(self, **kwargs):
        self.file_name = kwargs.pop('file_name')
        self.menu_height = kwargs.pop('menu_height', 0)
        super(WidgetScreen, self).__init__(**kwargs)
        #self.screen = kwargs.get('screen')
        self.widgets = []

    def add_widget_from_dict(self, dict):
        try: name = dict['name']
        except: name = ''
        type = dict['type']
        x = dict['x']
        y = dict['y']
        size = dict['size'] # eval(dict['size'])
        instance = eval(type)()
        for prop in dict:
            if prop in [ 'name', 'type' ]: continue
            if prop == 'x':
                instance._x = dict[prop]
                continue
            if prop == 'y':
                instance._y = dict[prop] + self.menu_height
                continue
            if type == 'Slider' and prop == 'text':
                setattr(instance.name_label, prop, dict[prop])
                continue
            if type == 'Knob' and prop == 'text':
                setattr(instance.label, prop, dict[prop])
                continue
            if hasattr(instance, prop):
                #print(prop + ": " + dict[prop])
                if prop in [ "text", "halign", "valign", "font_name", "orientation", "background_normal", "background_down" ]:
                    setattr(instance, prop, dict[prop])
                    if type == "Slider":
                        if prop == "orientation": instance.set_orientation(dict[prop])
                        instance.update_handler()
                elif prop in [ "image" ]:
                    if dict[prop] == 'None': continue
                    if type == "CheckButton": continue
                    image = Image(source = dict[prop])
                    setattr(instance, prop, image)#Image(source = dict[prop]))
                    instance.add_widget(image)
                    # instance.update_handler()
                else:
                    if type == "CheckButton": print(dict[prop])
                    value = dict[prop]
                    if len(value) > 0: value = eval(value)
                    setattr(instance, prop, value)
        self.widgets.append(instance)
        if len(name) > 0: exec('self.' + name + ' = instance')
        #exec('self.screen.add_widget(instance)')
        self.add_widget(instance)

    def build_widgets_screen(self):
        for dict in self.json_widgets:
            #print(dict)
            self.add_widget_from_dict(dict)

    def load_screen(self):
        json_widgets = []
        with open(self.file_name, 'r') as file:
            data = file.read()
        self.json_widgets = json.loads(data)
        self.build_widgets_screen()
