# (C) copyright Janotech, LLC - 2024, ...

import math
import ctypes

from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen as _Screen
from kivy.uix.label import Label as _Label
from kivy.uix.button import Button as _Button
from kivy.uix.togglebutton import ToggleButton as _ToggleButton
from kivy.uix.boxlayout import BoxLayout as _BoxLayout
from kivy.uix.gridlayout import GridLayout as _GridLayout
from kivy.uix.floatlayout import FloatLayout as _FloatLayout
from kivy.uix.stacklayout import StackLayout as _StackLayout
from kivy.uix.anchorlayout import AnchorLayout as _AnchorLayout
from kivy.uix.scatterlayout import ScatterLayout as _ScatterLayout
from kivy.uix.relativelayout import RelativeLayout as _RelativeLayout
from kivy.uix.image import Image
from kivy.uix.slider import Slider as _Slider
from kivy.uix.switch import Switch as _Switch
from kivy.uix.textinput import TextInput as _TextInput
from kivy.uix.dropdown import DropDown as _DropDown
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.uix.popup import Popup
from kivy.graphics import Color, Line, Rectangle, RoundedRectangle, Rotate, PushMatrix, PopMatrix, Ellipse
from kivy.properties import NumericProperty, BoundedNumericProperty

class UserInterface:

    bg_image = 'assets/images/bg_normal.png'
    
    default_width = 1000
    default_height = 800

    def __init__(self, **kwargs):
        # setup dpi, scaling, etc.
        # self.Window.borderless = True
        windows_dpi_awareness = kwargs.get('windows_dpi_awareness', None)
        if windows_dpi_awareness != None: ctypes.windll.shcore.SetProcessDpiAwareness(windows_dpi_awareness)
        # if DPI changed window then it needs to be refreshed
        # todo: refresh screen or center sreen
        Window.size = (self.default_width, self.default_height)

    def set_pos(self):
        # parent_pos = self.parent.pos if self.parent is not None else (0, 0)
        if self._x >= 0: self.pos[0] = self._x # + parent_pos[0] 
        if self._y >= 0: self.pos[1] = Window.height - self._y - self.size[1] # + parent_pos[1]

    def make_rgba(c):
        if len(c) == 3: return c + (1.0,)
        return c

class MessageBox(Popup):

    def __init__(self, **kwargs):
        message = kwargs.pop('message', None)
        self.size_hint = (None, None)
        self.layout = BoxLayout(orientation = 'vertical')
        if message != None: self.layout.add_widget(message)
        self.layout.add_widget(Button(text = 'OK', size_hint = (1, .5), on_press = self.dismiss))
        self.content = self.layout
        super(MessageBox, self).__init__(**kwargs)

class ConfirmBox(Popup):

    def __init__(self, **kwargs):
        message = kwargs.pop('message', '')
        self.on_confirm = kwargs.pop('on_confirm', None)
        self.title = kwargs.get('title', 'Confirm')
        self.size_hint = (None, None)
        self.size = (600, 600)
        self.title_size = 20
        self.layout = BoxLayout(orientation = 'vertical')
        self.layout.add_widget(_Label(text = message, font_size = 30))
        self.button_layout = BoxLayout(orientation = 'horizontal')
        self.button_layout.add_widget(Button(text = 'Yes', size_hint = (1, None), size = (0, 50), font_size = 30, on_press = self.on_click))
        self.button_layout.add_widget(Button(text = 'No', size_hint = (1, None), size = (0, 50), font_size = 30, on_press = self.on_click))
        self.layout.add_widget(self.button_layout)
        self.content = self.layout
        super(ConfirmBox, self).__init__(**kwargs)

    def on_click(self, button):
        if button.text == 'Yes': self.on_confirm() 
        self.dismiss()
        pass

class Screen(_Screen):

    def __init__(self, **kwargs):
        self.name = kwargs.pop('name', 'demo')
        super(Screen, self).__init__(**kwargs)
        self.layout = _AnchorLayout()
        super(_Screen, self).add_widget(self.layout)
        self.menu = None

    def add_widget(self, widget):
        self.layout.add_widget(widget)

    def build(self, program_name, globals): # globals = {} # was in new gui
        exec(compile(open(program_name + '.py').read(), program_name + '.py', 'exec'), globals)

class Panel(_Label):
    default_size = (300, 200)
    default_font_size = 30

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.border_width = kwargs.pop('border_width', 0)
        self.border_color = kwargs.pop('border_color', (1, 1, 1, 1))
        self.size_hint = (None, None)
        self.size = self.default_size
        self.font_size = self.default_font_size
        self.valign = 'top'
        self.halign = 'left'
        self.padding = 30
        self.background_color = kwargs.pop('background_color', Window.clearcolor)
        self.radius = kwargs.pop('radius', [(20, 20), (20, 20), (20, 20), (20, 20)])
        super(Panel, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance = None, value = None):
        self.set_pos()
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba = tuple(UserInterface.make_rgba(self.background_color)))
            RoundedRectangle(pos = self.pos, size = self.size, radius = self.radius)
            radius = self.radius
            rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], radius[0], radius[1], radius[2], radius[3], 100)
            if self.border_width > 0:
                Color(rgba = self.border_color)
                Line(width = self.border_width, rounded_rectangle = rounded_rectangle)

    def set_pos(self):
        UserInterface.set_pos(self)
        self.text_size = (self.size[0], self.size[1])

class AnchorLayout(_AnchorLayout): pass

class BoxLayout(_BoxLayout):
    
    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        super(BoxLayout, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

class FloatLayout(_FloatLayout):
    
    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        super(FloatLayout, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

class StackLayout(_StackLayout):
    
    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        super(StackLayout, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

class GridLayout(_GridLayout):
    
    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        super(GridLayout, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

class Menu(_BoxLayout):#_StackLayout):

    default_height = 100
    color = (.4, .4, .4)

    def __init__(self, **kwargs):
        self._x = 0
        self._y = 0
        self.size_hint = (1, None)
        self.size = (0, self.default_height)
        super(Menu, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgb = Menu.color)#(.4, .4, .4)) # tuple(self.background_color))
            Rectangle(pos = self.pos, size = self.size)

    def set_pos(self):
        UserInterface.set_pos(self)

    def add_item(self, item):
        self.add_widget(item)

class MenuButton(_Button):

    default_font_size = 30

    def __init__(self, **kwargs):
        super(MenuButton, self).__init__(**kwargs)
        self.font_size = self.default_font_size
        self.size_hint = (None, None)
        self.size = (200, Menu.default_height)
        self.background_color = Menu.color
        self.background_normal = ''

class Label(_Label):

    default_size = (200, 200)
    default_font_size = 30

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.size_hint = (None, None)
        #self.size = self.default_size
        self.font_size = self.default_font_size
        super(Label, self).__init__(**kwargs)
        self.valign = kwargs.pop('valign', 'center')
        self.halign = kwargs.pop('halign', 'left')
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)
        self.text_size = (self.size[0], self.size[1])

class TextInput(_TextInput):

    default_size = (400, 60)
    default_font_size = 30

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.size_hint = (None, None)
        kwargs['padding_y'] = 10
        kwargs['size'] = self.default_size
        self.font_size = self.default_font_size
        super(TextInput, self).__init__(**kwargs)
        #self.valign = kwargs.pop('valign', 'center')
        self.halign = kwargs.pop('halign', 'left')

        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)
        self.text_size = (self.size[0], self.size[1])

class Button(_Button):

    default_size = (200, 200)
    default_font_size = 40

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.radius = kwargs.pop('radius', None)#[20, 20, 20, 20])
        self.border_color = kwargs.pop('border_color', (1, 1, 1, .5))
        self.border_width = kwargs.pop('border_width', 0)
        self.size_hint = (None, None)
        self.size = self.default_size
        self.font_size = self.default_font_size
        self.image = None
        self.button_color = kwargs.pop('button_color', { 'normal': [.3, .3, .3, 1], 'down': [.1, .3, .8, 1] })
        self.draw_color = self.button_color['normal']
        super(Button, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance = None, value = None):
        self.set_image_pos()
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)
        if self.radius == None: return
        self.draw_button()

    def set_image_pos(self):
        if self.image == None: return
        self.image.center_x = self.center_x
        self.image.center_y = self.center_y
        self.image.pos = (self.center_x - self.image.size[0] / 2, self.center_y - self.image.size[1] / 2)
        self.image.size = self.size # (self.size[0] / 2, self.size[1] / 2)

    def draw_button(self):
        if self.radius == None: return
        Clock.schedule_once(self.draw, -1)

    def draw(self, *args):
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba = self.draw_color)
            RoundedRectangle(pos = self.pos, size = self.size, radius = self.radius)
            border_color = self.border_color
            border_width = self.border_width
            radius = self.radius
            rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], radius[0], radius[1], radius[2], radius[3], 100)
            if border_width > 0:
                Color(rgba = border_color)
                Line(width = border_width, rounded_rectangle = rounded_rectangle)

    def on_press(self, *args):
        self.draw_color = self.button_color['down']
        self.draw_button()

    def on_release(self, *args):
        self.draw_color = self.button_color['normal']
        self.draw_button()

class ToggleButton(_ToggleButton):

    default_size = (200, 200)
    default_font_size = 40

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.radius = kwargs.pop('radius', None)#[20, 20, 20, 20])
        self.border_color = kwargs.pop('border_color', (1, 1, 1, .5))
        self.border_width = kwargs.pop('border_width', 0)
        self.size_hint = (None, None)
        self.size = self.default_size
        self.font_size = self.default_font_size
        self.button_color = kwargs.pop('button_color', { 'normal': [.3, .3, .3, 1], 'down': [.1, .3, .8, 1] })
        self.draw_color = self.button_color['normal']
        super(ToggleButton, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler, on_press = self.button_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)
        if self.radius == None: return
        self.draw_button()

    def draw_button(self):
        if self.radius == None: return
        Clock.schedule_once(self.draw, -1)

    def draw(self, *args):
        self.background_normal = ''
        self.background_down = ''
        self.background_color = (0, 0, 0, 0)
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba = self.draw_color)
            RoundedRectangle(pos = self.pos, size = self.size, radius = self.radius)
            border_color = self.border_color
            border_width = self.border_width
            radius = self.radius
            rounded_rectangle = (self.pos[0], self.pos[1], self.size[0], self.size[1], radius[0], radius[1], radius[2], radius[3], 100)
            if border_width > 0:
                Color(rgba = border_color)
                Line(width = border_width, rounded_rectangle = rounded_rectangle)

    def button_handler(self, button):
        if button.state == 'normal': self.draw_color = self.button_color['normal']
        if button.state == 'down': self.draw_color = self.button_color['down']
        self.draw_button()
        pass

    def on_state(self, button, value):
        if button.state == 'normal': self.draw_color = self.button_color['normal']
        if button.state == 'down': self.draw_color = self.button_color['down']
        self.draw_button()

class ProgramButton(ToggleButton):

    def __init__(self, **kwargs):
        self.key = kwargs.pop('key', None)
        self.class_name = kwargs.pop('class_name', None)
        self.program_name = kwargs.pop('program_name', None)
        if self.program_name != None and len(self.program_name) > 0 and self.class_name == None:
            self.class_name = self.program_name.replace('_', ' ').title().replace(' ', '')
        super(ProgramButton, self).__init__(**kwargs)

class CheckButton(_ToggleButton):

    default_size = (40, 40)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        super(CheckButton, self).__init__(**kwargs)
        self.border = (0, 0, 0, 0)
        self.size = self.default_size
        self.size_hint = (None, None)
        self.pos_hint = { 'center_x': .5, 'center_y': .5 }
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler, on_press = self.on_check)
        self.image = Image(source = 'checkmark.png', size_hint = (None, None), size = self.size)

    def on_check(self, button):
        if (button.state == "down"): self.add_widget(self.image)
        if (button.state == "normal"): self.remove_widget(self.image)

    def update_handler(self, instance, value):
        self.image.center_x = self.center_x
        self.image.center_y = self.center_y
        self.image.pos = instance.pos
        self.image.size = (self.size[0], self.size[1]) # added
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

class DropDownButton(_Button):

    text_width = 300
    default_font_size = 30
    default_size = (text_width, 100)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.size_hint = (None, None)
        self.font_size = self.default_font_size
        self.text_size = (self.text_width, None)
        self.size = self.default_size
        self.halign = 'left'
        self.padding = 60
        self.image = None
        super(DropDownButton, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance = None, value = None):
        self.set_image_pos()
        self.set_pos()
        pass

    def set_pos(self):
        UserInterface.set_pos(self)

    def set_image_pos(self):
        if self.image == None: return
        self.image.center_x = self.center_x
        self.image.center_y = self.center_y
        self.image.pos = (self.center_x - self.image.size[0] / 2, self.center_y - self.image.size[1] / 2)
        self.image.size = (self.size[0] / 2, self.size[1] / 2)

class SubMenu(_Button):

    default_font_size = 30
    default_size = (200, 100)

    def __init__(self, **kwargs):
        self.size_hint = (None, None)
        self.font_size = self.default_font_size
        self.size = self.default_size
        self.values = kwargs.pop('values')
        self.background_color = Menu.color
        self.background_normal = ''
        super(SubMenu, self).__init__(**kwargs)
        self.drop_down = _DropDown(auto_width = False, width = DropDownButton.text_width)
        for item in self.values:
            button = DropDownButton(text = item) # Menu.default_height
            button.background_color = Menu.color
            button.background_normal = ''
            button.bind(on_release = self.on_select) # lambda button: self.drop_down.select(button.text))
            self.drop_down.add_widget(button)
        self.bind(on_release = self.drop_down.open)
        self.drop_down.bind(on_select = lambda instance, x: setattr(self, 'text', x))

    def on_select(self, button):
        self.drop_down.select(self.text) # button.text)
        self.handler(button)

class ListBoxOption(SpinnerOption):

    text_width = 500
    default_font_size = 30
    default_size = (text_width, 100)

    def __init__(self, **kwargs):
        self.size_hint = (None, None)
        self.font_size = self.default_font_size
        self.size = self.default_size
        self.text_size = (self.text_width, None)
        self.halign = 'left'
        self.padding = 20
        super(ListBoxOption, self).__init__(**kwargs)

class ListBox(Spinner):

    default_font_size = 30
    default_size = (200, 100)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.size_hint = (None, None)
        self.size = self.default_size
        self.font_size = kwargs.pop('font_size', self.default_font_size)
        ListBoxOption.default_font_size = self.font_size
        self.option_cls = 'ListBoxOption'
        self.sync_height = True
        super(ListBox, self).__init__(**kwargs)
        self.set_pos()
        self.bind(pos = self.update_handler, size = self.update_handler, text = self.on_text)

    def on_text(self, instance, value):
        if len(self.values) == 0: return

    def update_handler(self, instance, value):
        self.set_pos()

    def set_pos(self):
        UserInterface.set_pos(self)

    def set_font_size(self, font_size): # this was added
        dd = self._dropdown
        if not dd: return
        container = dd.container
        if not container: return
        for item in container.children[:]:
            item.font_size = font_size

class Slider(_Slider):

    default_size = (200, 200)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.name = kwargs.pop('name', 'slider')
        self.size_hint = (None, None)
        self.padding = 60
        super(Slider, self).__init__(**kwargs)
        self.name_label = Label(x = self._x, y = self._y, size = self.size, text = self.name, font_size = 25)
        self.value_label = Label(x = self._x, y = self._y, size = self.size, text = str(round(self.value)), font_size = 25)
        self.set_orientation(self.orientation)
        self.set_pos()
        self.add_widget(self.name_label)
        self.add_widget(self.value_label)
        self.bind(pos = self.update_handler, size = self.update_handler, value = self.update_value)

    def update_handler(self, instance = None, value = None):
        self.set_pos()

        self.name_label.size = self.size
        x_adjust = 0 if self.orientation == "vertical" else 80
        self.name_label.pos = (self.pos[0] - x_adjust, self.pos[1])
        self.name_label.text_size = (self.size[0], self.size[1])

        self.value_label.size = self.size
        self.value_label.pos = self.pos
        self.value_label.text_size = (self.size[0], self.size[1])

    def set_pos(self):
        UserInterface.set_pos(self)

    def update_value(self, instance, value):
        self.value_label.text = str(round(value))

    def set_orientation(self, value):
        self.orientation = value
        self.name_label.valign = 'bottom' if self.orientation == 'vertical' else 'center'
        self.name_label.halign = 'center' if self.orientation == 'vertical' else 'left'
        self.value_label.valign = 'top' if self.orientation == 'vertical' else 'center' 
        self.value_label.halign = 'center' if self.orientation == 'vertical' else 'right'

class NewSlider(_Slider): # new slider control

    default_size = (200, 200)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.name = kwargs.pop('name', 'slider')
        self.size_hint = (None, None)
        self.padding = 60
        self.cursor_size = (80, 26)
        self.cursor_image = "slider.png"
        self.background_width = 10
        #self.value_track = True
        self.value_track_width = 10
        self.value_track_color = [0, 0, 0, 1]
        super(Slider, self).__init__(**kwargs)
        self.name_label = Label(x = self._x, y = self._y, size = self.size, text = self.name, font_size = 25)
        self.value_label = Label(x = self._x, y = self._y, size = self.size, text = str(round(self.value)), font_size = 25)
        self.set_orientation(self.orientation)
        self.set_pos()
        self.add_widget(self.name_label)
        self.add_widget(self.value_label)
        self.bind(pos = self.update_handler, size = self.update_handler, value = self.update_value)

    def update_handler(self, instance = None, value = None):
        self.set_pos()

        self.name_label.size = self.size
        x_adjust = 0 if self.orientation == "vertical" else 80
        self.name_label.pos = (self.pos[0] - x_adjust, self.pos[1])
        self.name_label.text_size = (self.size[0], self.size[1])

        self.value_label.size = self.size
        self.value_label.pos = self.pos
        self.value_label.text_size = (self.size[0], self.size[1])

        if self.orientation == "horizontal":
            self.cursor_image = "slider_horizontal.png"
            self.cursor_size = (30, 60)
        if self.orientation == "vertical":
            self.cursor_image = "slider.png"
            self.cursor_size = (40, 60)#(40, 60)

        self.background_vertical = 'track.png'
        self.background_horizontal = 'track.png'

    def set_pos(self):
        UserInterface.set_pos(self)

    def update_value(self, instance, value):
        self.value_label.text = str(round(value))

    def set_orientation(self, value):
        self.orientation = value
        self.name_label.valign = 'bottom' if self.orientation == 'vertical' else 'center'
        self.name_label.halign = 'center' if self.orientation == 'vertical' else 'left'
        self.value_label.valign = 'top' if self.orientation == 'vertical' else 'center' 
        self.value_label.halign = 'center' if self.orientation == 'vertical' else 'right'

class Knob(_Label):

    default_font_size = 40
    default_size = (200, 200)
    default_value_color = (.8, .8, .8)

    value = NumericProperty(0)
    #min = NumericProperty(0)
    #max = NumericProperty(100)
    range = BoundedNumericProperty(100)#(min, max)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.name = kwargs.pop('name', 'knob')
        self.value = kwargs.pop('value', .001)
        self.range = kwargs.pop('range', (0, 100))
        self.knob_padding = kwargs.pop('knob_padding', 40)
        self.size_hint = (None, None)
        self.font_size = self.default_font_size
        self.step = 1
        self.angle = 0
        self.min = self.range[0]
        self.max = self.range[1]
        super(Knob, self).__init__(**kwargs)
        self.color = (0, 0, 0) # actual label value color
        self.face_color = Window.clearcolor # color of knob face
        self.bind(pos = self.update_handler, size = self.update_handler)
        self.bind(on_range = self.on_range)
        self.label = Label(x = self._x, y = self._y, size = self.size, font_size = 25, text = self.name)
        self.label.valign = 'bottom'
        self.label.halign = 'center'
        self.set_pos()
        self.add_widget(self.label)
        #self.value = self.min + .00001

    def update_handler(self, instance, value):
        self.set_pos()
        self.draw_knob()
        self.label.pos = self.pos
        self.label.size = self.size
        self.label.text_size = (self.size[0], self.size[1])

    def set_pos(self):
        UserInterface.set_pos(self)
        self.size[0] = self.size[1]

    def on_value(self, instance, value):
        self.value = value
        self.angle = pow((value - self.min) / (self.max - self.min), 1.0) * 270
        Clock.schedule_once(self.update_knob, -1)

    def update_knob(self, *args):        
        self.draw_knob()

    def on_range(self, instance, value):
        self.min = value[0]
        self.max = value[1]
        pass

    def on_touch_down(self, touch):
        knob_size = [self.size[0] - 2 * self.knob_padding, self.size[1] - 2 * self.knob_padding]
        knob_pos = [self.pos[0] + self.knob_padding, self.pos[1] + self.knob_padding]

        if Widget(pos = knob_pos, size = knob_size).collide_point(touch.pos[0], touch.pos[1]):
        # if self.collide_point(*touch.pos):
            self.update_angle(touch)

    def on_touch_move(self, touch):
        knob_size = [self.size[0] - 2 * self.knob_padding, self.size[1] - 2 * self.knob_padding]
        knob_pos = [self.pos[0] + self.knob_padding, self.pos[1] + self.knob_padding]

        if Widget(pos = knob_pos, size = knob_size).collide_point(touch.pos[0], touch.pos[1]):
        # if self.collide_point(*touch.pos):
            self.update_angle(touch)

    def draw_knob(self):
        self.canvas.before.clear()
        self.text = str(round(self.value))
        
        knob_size = [self.size[0] - 2 * self.knob_padding, self.size[1] - 2 * self.knob_padding]
        knob_pos = [self.pos[0] + self.knob_padding, self.pos[1] + self.knob_padding]

        with self.canvas.before:
            PushMatrix()
            Color(rgb = self.default_value_color)    
            Rotate(angle = 90 + 45, origin = self.center)
            Ellipse(pos = knob_pos, size = knob_size, angle_start = 0, angle_end = self.angle)
            Color(0, 0, 0)    
            Ellipse(pos = knob_pos, size = knob_size, angle_start = self.angle, angle_end = 270)
            #PopMatrix()
            #PushMatrix()
            Color(rgb = tuple(self.face_color))
            size = (knob_size[0] - knob_size[0] * .3, knob_size[1] - knob_size[1] * .3)
            pos = (knob_pos[0] + knob_size[0] * .3 / 2, knob_pos[1] + knob_size[1] * .3 / 2)
            Ellipse(pos = pos, size = size, angle_start = 0, angle_end = 0)
            PopMatrix()

    def update_angle(self, touch):
        x_pos = touch.pos[0] - self.center[0]
        y_pos = touch.pos[1] - self.center[1]
    
        if y_pos >= 0: quadrant = 1 if x_pos >= 0 else 4
        else: quadrant = 3 if x_pos <= 0 else 2

        if y_pos == 0: y_pos = 1 # TODO - need to fix this if y_pos is 0
        angle = math.atan(x_pos / y_pos) * (180.0 / math.pi)
        
        if quadrant == 2 or quadrant == 3: angle = 180 + angle
        elif quadrant == 4: angle = 360 + angle

        angle += 90 + 45; angle %= 360

        if angle > 270 + 45: angle = .1
        if angle > 270: angle = 270

        self.angle_step = (self.step * 360) / (self.max - self.min)
        self.angle = angle

        relativeValue = pow((angle / 270.0), 1.0)
        self.value = (relativeValue * (self.max - self.min)) + self.min
        self.draw_knob()

class WhiteKeys(_RelativeLayout):
    
    def __init__(self, keyboard_size, **kwargs):
        self.keyboard_size = keyboard_size
        self.rows = 1
        self.cols = keyboard_size
        self.spacing = 5
        self.padding = (1, 1, 1, 1)
        self.keys = []
        super(WhiteKeys, self).__init__(**kwargs)
        self.key_width = self.get_width() // self.keyboard_size
        self.key_height = self.size[1]
        for key in range(self.keyboard_size):
            b = _Button(size_hint = (None, None), size = (self.key_width - 4, self.key_height), background_normal = '', background_color = 'ivory')
            self.add_widget(b)
            self.keys.append(b)
        self.bind(pos = self.update_handler, size = self.update_handler)
        self.draw()

    def draw(self):
        self.key_height = self.size[1]
        for index, b in enumerate(self.keys):
            b.pos = (index * self.key_width + 2, 0)
            b.size = (self.key_width - 4, self.key_height)

    def update_handler(self, instance, value):
        #self.set_pos()
        self.key_width = self.get_width() // self.keyboard_size
        self.draw()

    def get_width(self):
        if self.parent == None: return 100
        if self.parent.size_hint[0] == None: return self.size[0]
        return Window.width

class BlackKeys(_RelativeLayout):
    
    def __init__(self, keyboard_size, **kwargs):
        self.keyboard_size = keyboard_size
        self.rows = 1
        self.cols = self.keyboard_size
        self.spacing = 5
        self.padding = (1, 1, 1, 1)
        self.keys = []
        super(BlackKeys, self).__init__(**kwargs)
        self.key_width = self.get_width() // self.keyboard_size
        self.key_height = self.size[1] * 2 // 3
        for key in range(self.keyboard_size - 1):
            b = _Button(size_hint = (None, None), size = (self.key_width - 12, self.key_height), background_normal = '', background_color = 'grey')
            self.add_widget(b)
            self.keys.append(b)
        self.bind(pos = self.update_handler, size = self.update_handler)
        self.draw()

    def draw(self):
        self.key_height = self.size[1] * 2 // 3
        for index, b in enumerate(self.keys):
            shift = self.key_width // 2
            b.pos = (index * self.key_width + 7 + shift, self.size[1] // 3 + 1)
            b.size = (self.key_width - 12, self.key_height)
            k = index % 7
            if k == 2 or k == 6: b.opacity = 0

    def update_handler(self, instance, value):
        #self.set_pos()
        self.key_width = self.get_width() // self.keyboard_size
        self.draw()

    def get_width(self):
        if self.parent == None: return 100
        if self.parent.size_hint[0] == None: return self.size[0]
        return Window.width

class PianoKeyboard(_RelativeLayout):

    # set instance size_hint = (1, 1) to use non x, y expandable version
    # keyboard_size refers to total number of white keys

    keyboard_size = NumericProperty(0)

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.keyboard_size = kwargs.pop('keyboard_size', 57)
        self.size_hint = (None, None)
        super(PianoKeyboard, self).__init__(**kwargs)
        self.white_keys = WhiteKeys(self.keyboard_size, **kwargs)
        self.black_keys = BlackKeys(self.keyboard_size, **kwargs)
        self.midi_notes = [None] * 128
        self.add_widget(self.white_keys)
        self.add_widget(self.black_keys)
        note = 0
        for index, b in enumerate(self.white_keys.keys):
            self.midi_notes[note] = b
            note += 2
            k = index % 7
            if k == 2 or k == 6:
                note -= 1
        note = 0
        for index, b in enumerate(self.black_keys.keys):
            if b.opacity == 0:
                note += 1
                continue
            self.midi_notes[note + 1] = b            
            note += 2
        self.set_pos()
        self.white_keys.update_handler(self.white_keys, self.size)
        self.black_keys.update_handler(self.black_keys, self.size)
        self.bind(pos = self.update_handler, size = self.update_handler)

    def update_handler(self, instance, value):
        self.set_pos()

    def on_keyboard_size(self, instance, value):
        if self.keyboard_size < 8: return
        self.remove_widget(self.white_keys)
        self.remove_widget(self.black_keys)
        self.white_keys = WhiteKeys(self.keyboard_size)
        self.black_keys = BlackKeys(self.keyboard_size)
        self.add_widget(self.white_keys)
        self.add_widget(self.black_keys)

    def set_pos(self):
        UserInterface.set_pos(self)

    def set_note(self, **kwargs):
        note = kwargs.get('note')
        state = kwargs.get('state', True)
        if state == True: self.midi_notes[note].state = 'down'
        if state == False: self.midi_notes[note].state = 'normal'
