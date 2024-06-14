from kivy.graphics import Color, Line, Rectangle
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.app import App

from kivy.clock import Clock
from kivy.input.providers.mouse import MouseMotionEvent

class Grip(Widget):

    grip_size = 25
    offset = 10

    def __init__(self, **kwargs):
        super(Grip, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (self.grip_size, self.grip_size)

    def draw_grip(self):
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1)
            Rectangle(pos = self.pos, size = self.size)

    def on_touch_down(self, touch):
        pass

    def on_touch_move(self, touch):
        pass

class SelectWidget(Widget):

    snap_size = 20

    def __init__(self, **kwargs):
        self._x = kwargs.pop('x', -1)
        self._y = kwargs.pop('y', -1)
        self.name = kwargs.pop('name', '')
        self.widget = kwargs.pop('widget', None)
        super(SelectWidget, self).__init__(**kwargs)
        self.size_hint = (None, None)
        self.mouse_down = False
        self.grip_selected = False
        self.selected = False
        self.grip_index = 0
        self.set_pos()
        self.widget.pos = self.pos
        #self.widget.size = self.size
        self.size = self.widget.size
        self.add_widget(self.widget)
        self.grips = [Grip(pos = self.pos), Grip(pos = self.pos), Grip(pos = self.pos), Grip(pos = self.pos)]
        for index, grip in enumerate(self.grips):
            self.grips[index].pos = self.get_grip_pos(index)
            self.add_widget(grip)
        Clock.schedule_once(self.dispatch_event, 0)

    def dispatch_event(self, *args):
        touch = MouseMotionEvent(None, 1, self.pos)
        touch.pos = self.pos
        touch.button = 'left'
        touch.x = self.pos[0] + self.size[0] // 2
        touch.y = self.pos[1] + self.size[1] // 2
        self.dispatch('on_touch_down', touch)

    def set_pos(self):        
        self.window_height = Window.height
        if self._x >= 0: self.pos[0] = self._x 
        if self._y >= 0: self.pos[1] = Window.height - self._y - self.size[1]
        self.widget.pos = self.pos

    def update_pos(self, value):
        delta = value[1] - self.window_height
        self.pos[1] += delta
        self.window_height = value[1]
        self.widget.pos = self.pos
        self.update_grip_positions()
        if self.selected:           
            self.canvas.before.clear()
            self.draw_select_box()

    def set_widget_size(self, size):
        self.size = size
        self.widget.size = size
        self.update_grip_positions()
        if self.selected:           
            self.canvas.before.clear()
            self.draw_select_box()

    def set_widget_pos(self, pos):
        self._x = pos[0]
        self._y = pos[1]
        self.set_pos()
        self.update_grip_positions()
        if self.selected:           
            self.canvas.before.clear()
            self.draw_select_box()

    def update_grip_positions(self):
        for index, grip in enumerate(self.grips):
            grip.pos = self.get_grip_pos(index)

    def get_pos_vars(self):
        return self.pos[0], self.pos[1], self.widget.size[0], self.widget.size[1]

    def get_grip_pos(self, index):
        x, y, w, h = self.get_pos_vars()
        if index == 0: return [x - Grip.offset, y - Grip.offset]
        if index == 1: return [x + w - Grip.grip_size + Grip.offset, y - Grip.offset]
        if index == 2: return [x + w - Grip.grip_size + Grip.offset, y + h - Grip.grip_size + Grip.offset]
        if index == 3: return [x - Grip.offset, y + h - Grip.grip_size + Grip.offset]

    def draw_select_box(self):
        x, y, w, h = self.get_pos_vars()
        points = [x, y, x, y + h, x + w, y + h, x + w, y, x, y]
        with self.canvas.before:
            Color(1, 1, 1) # *color, mode='hsv')
            Line(points = points, width = 2)
        for grip in self.grips:
            grip.draw_grip()

    def on_touch_down(self, touch):
        self.mouse_down = True
        color = (1, 1, 1, 1)
        grip_x = touch.x
        grip_y = touch.y
        touch.x = touch.x // self.snap_size * self.snap_size 
        touch.y = touch.y // self.snap_size * self.snap_size
        self.td = [touch.x, touch.y]

        # first see if a grip is selected
        for index, grip in enumerate(self.grips):
            if grip.collide_point(grip_x, grip_y):
                grip.on_touch_down(touch)
                self.grip_selected = True
                self.grip_index = index
                self.selected = True
                return True

        # check if widget is selected
        if App.get_running_app().ctrl == True:
            if self.selected == True: return
        self.selected = self.collide_point(touch.x, touch.y)
        if self.selected == False:
            for grip in self.grips:
                grip.canvas.before.clear()
            self.canvas.before.clear()
            return

        self.draw_select_box()
        # need to deselect all other selected widgets in normal mode
        if App.get_running_app().ctrl == False: self.parent.deselect_all(self)
        class_name = type(self.widget).__name__
        App.get_running_app().build_props_panel(class_name)
        App.get_running_app().init_properties(self, touch.button)

        if App.get_running_app().shift == True: return False
        return True # needed to allow widget inside widget to be selected

    def on_touch_move(self, touch):
        if not self.mouse_down: return
        
        # keep this line - can select and move entire screen
        # if self.selected == False and App.get_running_app().shift == False: return
        if self.selected == False: return

        touch.x = touch.x // self.snap_size * self.snap_size
        touch.y = touch.y // self.snap_size * self.snap_size
        
        if self.grip_index == 0:
            self.pos[0] -= self.td[0] - touch.x
            self.pos[1] -= self.td[1] - touch.y

        if self.grip_index == 1:
            self.pos[1] -= self.td[1] - touch.y

        if self.grip_index == 2:
            pass

        if self.grip_index == 3:
            self.pos[0] -= self.td[0] - touch.x
            pass

        self.widget.pos = self.pos
        self.canvas.before.clear()

        if self.grip_selected:
            if self.grip_index == 0:
                self.size[0] += self.td[0] - touch.x
                self.size[1] += self.td[1] - touch.y
            if self.grip_index == 1:
                self.size[0] += touch.x - self.td[0]
                self.size[1] += self.td[1] - touch.y
            if self.grip_index == 2:
                self.size[0] += touch.x - self.td[0]
                self.size[1] += touch.y - self.td[1]
            if self.grip_index == 3:
                self.size[0] += self.td[0] - touch.x
                self.size[1] += touch.y - self.td[1]
            self.widget.size = self.size

        self.td = [touch.x, touch.y]
        self.update_grip_positions()
        self.draw_select_box()

        App.get_running_app().init_properties(self)

        return # True

    def on_touch_up(self, touch):
        self.mouse_down = False
        self.grip_selected = False
        self.grip_index = 0

    def select(self, widget):
        widget.selected = True
        widget.grip_selected = False
        widget.grip_index = 0
        widget.draw_select_box()

    def deselect(self, widget):
        widget.selected = False
        widget.grip_selected = False
        widget.grip_index = 0
        widget.canvas.before.clear()
        for grip in widget.grips:
            grip.canvas.before.clear()
