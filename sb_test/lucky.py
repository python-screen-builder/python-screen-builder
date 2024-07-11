from gui import *
from kivy.app import App
from widget_screen import WidgetScreen

import random
from kivy.clock import Clock

class LuckySquare(WidgetScreen):

    def __init__(self, **kwargs):
        super(LuckySquare, self).__init__(**kwargs)
        self.load_screen()
        self.panel.size_hint = (.8, .8)
        self.stack.size_hint = (.5, .5)
        self.stack.spacing = 10
        self.buttons = []
        self.max_squares = 35
        for i in range(self.max_squares):
            b = Button(text = str(i), size = (100, 100))
            b.id = i
            self.stack.add_widget(b)
            b.bind(on_press = self.on_press)
            self.buttons.append(b)
        self.lucky_number = random.randint(0, self.max_squares - 1)
        self.time = 10
        self.win = False
        self.lose = False
        Clock.schedule_interval(self.on_clock, 1)

    def on_press(self, button):
        if button.id == self.lucky_number:
            button.background_color = 'lightgreen'
            if self.lose == True: return            
            self.panel.text = 'You Win!'
            self.win = True
            return
        button.opacity = .2 if button.opacity == 1 else 1#True
        #self.stack.remove_widget(button)

    def on_clock(self, x):
        if self.lose == True: return
        if self.win == True: return
        if self.time <= 0:
            self.panel.text = 'You Lose!'
            self.lose = True
            self.show_winner()
        self.clock.text = str(self.time)
        self.time -= 1
        pass

    def show_winner(self):
        print(self.lucky_number)
        for b in self.buttons:
            if b.id != self.lucky_number: b.opacity = .2
            else: b.background_color = 'lightgreen'

class TestApp(App):

    def build(self):
        Window.clearcolor = 'steelblue'
        self.test_screen = LuckySquare(file_name = 'lucky.json')
        return self.test_screen

if __name__ == '__main__':
    TestApp().run()
