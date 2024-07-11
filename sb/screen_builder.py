from kivy.uix.screenmanager import Screen as _Screen
from kivy.uix.splitter import Splitter
from kivy.core.window import Window
from kivy.graphics import *
from kivy.app import App
from select_widget import *
from os.path import exists
from gui import *

from copy import copy

class ScreenBuilder(_Screen): 

    def __init__(self, **kwargs):
        self.settings = kwargs.pop('settings')
        super(ScreenBuilder, self).__init__(**kwargs)
        UserInterface(windows_dpi_awareness = self.settings.windows_dpi_awareness)
        self.widgets = []
        self.widgets_to_copy = []
        self.external_classes = {}
        self.grid = None
        self.show_grid = False
        self.undo_count = 0
        Window.clearcolor = 'grey'
        Window.size = (self.settings.window_width, self.settings.window_height)
        Window.bind(size = self.resize)
        self.set_init_pos()

    def set_init_pos(self):
        self.x_add = 40
        self.y_add = 140

    def get_index_name(self, type_name):
        for widget in self.settings.widgets:
            if widget['class'] == type_name:
                if 'index' in widget:
                    index = str(widget['index']); widget['index'] += 1
                    return index
        return ''

    def add_gui_widget(self, widget, **kwargs):
        x = kwargs.pop('x', 100)
        y = kwargs.pop('y', 150)
        size = kwargs.pop('size', (100, 100))
        name = kwargs.pop('name', '')
        index = self.get_index_name(type(widget).__name__)
        select_widget = SelectWidget(x = x, y = y, widget = widget, size = size)
        if len(index) > 0 and len(name) > 0: select_widget.name = name + index
        self.add_widget(select_widget)
        self.widgets.append(select_widget)

    def add_widget_by_name(self, class_name, init, name = '', file = ''):
        size = (200, 200)
        if len(file) > 0 and exists(file + '.py'):
            exec("from " + file + " import *")
        widget = eval(init)
        if hasattr(widget, "font_size"): widget.font_size = 30
        if hasattr(widget, "text"): widget.text = class_name
        self.add_gui_widget(widget, x = self.x_add, y = self.y_add, size = size, name = name)
        self.x_add += 40
        self.y_add += 40
        if self.y_add > Window.height:
            self.y_add = 140
            self.x_add = 40

    def add_widget_from_dict(self, dict):
        try: name = dict['name']
        except: name = ''
        type = dict['type']
        x = dict['x']
        y = dict['y'] + self.settings.menu_height
        size = dict['size'] # eval(dict['size'])
        if type in self.external_classes:
            file = self.external_classes[type]
            exec("from " + file + " import *")
        instance = eval(type)()
        for prop in dict:
            if prop in [ 'name', 'type', 'x', 'y' ]: continue
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
                    image = Image(source = dict[prop])
                    setattr(instance, prop, image)#Image(source = dict[prop]))
                    # instance.add_widget(image)
                    # instance.update_handler()
                else:
                    value = dict[prop]
                    # allow any property to be set - for added class properties need to fix this somehow
                    # for instance size will eval('[width, height]') okay but not if just a string ...
                    # so just add try-except for now
                    if len(value) > 0:
                        try:
                            value = eval(value)
                        except:
                            pass
                    setattr(instance, prop, value)
        select_widget = SelectWidget(name = name, x = x, y = y, widget = instance, size = instance.size)
        self.add_widget(select_widget)
        self.widgets.append(select_widget)

    def select_all(self):
        for widget in self.widgets:
            widget.select(widget)

    def deselect_all(self, exclude_widget):
        for widget in self.widgets:
            if widget == exclude_widget: continue
            widget.deselect(widget)

    def resize(self, instance, value):
        if self.show_grid == True:
            if self.grid != None:
                self.remove_widget(self.grid)
            self.grid = Grid(size = self.size)
            self.add_widget(self.grid)#, index = 10000)
        for widget in self.widgets:
            widget.update_pos(value)

    def get_selected_widget(self): # return 1 widget for now
        for widget in self.widgets:
            if widget.selected: return widget
        return None

    def show_widgets(self):
        for widget in self.widgets:
            print(str(type(widget.widget)))

    def bring_widget_to_top(self, selected_widget):
        for widget in self.widgets:
            if widget == selected_widget:
                self.remove_widget(selected_widget)
                self.add_widget(selected_widget)
                self.widgets.remove(selected_widget)
                self.widgets.append(selected_widget)
        # self.show_widgets()

    def send_widget_to_back(self, selected_widget):
        for widget in self.widgets:
            if widget == selected_widget:
                self.remove_widget(selected_widget)
                self.add_widget(selected_widget, index = 9999)
                self.widgets.remove(selected_widget)
                self.widgets.insert(0, selected_widget)
                self.toggle_grid()
                self.toggle_grid()
        # self.show_widgets()

    def toggle_grid(self):
        if self.grid != None: self.remove_widget(self.grid)
        self.show_grid = True if self.show_grid == False else False
        if self.show_grid == False:
            self.remove_widget(self.grid)
            return
        self.grid = Grid(size = self.size)
        self.add_widget(self.grid)#, index = 10000)

    def remove_widgets(self):
        confirm = ConfirmBox(title = 'Clear All Widgets', message = 'Are you sure?', on_confirm = self.clear_widgets)
        confirm.open()

    def clear_widgets(self):        
        for widget in self.widgets:
            self.remove_widget(widget)
        self.widgets = []
        self.undo_count = 0

    def create_copy(self, screen_widget):
        type_name = type(screen_widget).__name__
        for widget in self.settings.widgets:
            if widget['class'] == type_name:
                new_widget = eval(type_name)(size = screen_widget.size)
                for props in widget['properties']:
                    if props['name'] == 'name': continue
                    if props['name'] == 'orientation' and type_name == 'Slider':
                        new_widget.set_orientation(screen_widget.orientation)
                        continue
                    try:
                        setattr(new_widget, props['name'], copy(getattr(screen_widget, props['name'])))
                    except:
                        pass
                # props = [x for x in dir(screen_widget) if not x.startswith('__') and not callable(getattr(screen_widget, x))]
                return new_widget

    def copy(self):
        self.widgets_to_copy = []
        for widget in self.widgets:
            if widget.selected == True:
                self.widgets_to_copy.append(widget)

    def paste(self):
        for widget in self.widgets_to_copy:
            name = type(widget.widget).__name__.lower()
            widget_copy = self.create_copy(widget.widget)
            self.add_gui_widget(widget_copy, x = widget._x, y = widget._y, name = name)
            #self.add_gui_widget(widget_copy, x = widget_copy._x, y = widget_copy._y, name = name)
            self.undo_count += 1

    def undo(self):
        if len(self.widgets) == 0: return
        if self.undo_count == 0: return
        widget = self.widgets[-1]
        self.widgets.pop()
        self.remove_widget(widget.widget)
        self.remove_widget(widget)
        self.undo_count -= 1

class Grid(Widget):

    def __init__(self, **kwargs):
        super(Grid, self).__init__(**kwargs)
        self.draw_grid()
        self.bind(size = self.update_handler)

    def draw_grid(self):
        width = int(self.size[0]) # - App.get_running_app().properties_layout.size[0] 
        height = int(self.size[1])
        self.canvas.before.clear()
        for y in range(height, 0, -40):
            with self.canvas.before:
                Color(0, 0, 0, .5)
                Line(points = (0, y, width, y))
        for x in range(0, width, 40):
            with self.canvas.before:
                Color(0, 0, 0, .5)
                Line(points = (x, height, x, 0))

    def update_handler(self, instance, pos):
        # remove and add widget back again
        self.size = instance.size
        self.draw_grid()