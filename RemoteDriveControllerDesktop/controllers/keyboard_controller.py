import keyboard
from settings import KeyboardControls


class KeyboardController:
    """Контроллер клавиатуры"""

    def __init__(self):
        self.current_steering = None
        self.pressed_keys = set()

    def press_key(self, key):
        keyboard.press(key)
        self.pressed_keys.add(key)

    def release_key(self, key):
        keyboard.release(key)
        self.pressed_keys.add(key)

    def turn_left(self):
        if self.current_steering != "left":
            self.release_steering()
            keyboard.press(KeyboardControls.KEY_LEFT)
            self.current_steering = "left"

    def turn_right(self):
        if self.current_steering != "right":
            self.release_steering()
            keyboard.press(KeyboardControls.KEY_RIGHT)
            self.current_steering = "right"

    def center_steering(self):
        self.release_steering()
        self.current_steering = None

    def release_steering(self):
        if self.current_steering == "left":
            keyboard.release(KeyboardControls.KEY_LEFT)
        elif self.current_steering == "right":
            keyboard.release(KeyboardControls.KEY_RIGHT)

    def cleanup(self):
        self.center_steering()
        for key in self.pressed_keys:
            keyboard.release(key)
