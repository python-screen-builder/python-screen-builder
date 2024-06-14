from kivy.core.window import Window
from kivy.uix.widget import Widget

class Keyboard(Widget):

    def __init__(self, **kwargs):
        super(Keyboard, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        if self._keyboard.widget: pass
        self._keyboard.bind(on_key_down = self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down = self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print(keycode, ' pressed')
        # print(' - text is %r' % text)
        # print(' - modifiers are %r' % modifiers)

        # Keycode is composed of an integer + a string
        # If we hit escape, release the keyboard
        # if keycode[1] == 'escape':
        #     keyboard.release()

        # Return True to accept the key. Otherwise, it will be used by
        # the system.
        return True
