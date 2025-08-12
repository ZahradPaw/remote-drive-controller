import json
import sys
import os
from settings import KeyboardControls, Settings


def resource_path(relative_path):
    """Получает абсолютный путь к ресурсу"""
    if getattr(sys, 'frozen', False):
        # Если приложение собрано в .exe
        base_path = sys._MEIPASS
    else:
        # Если скрипт запущен напрямую
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class StorageLoader:
    """Загрузка и сохранение настроек в файл"""
    file_name = 'options.json'
    data = dict()
    data['keyboard_controls'] = dict()
    data['input_types'] = dict()

    def save(self):
        self.data['port'] = Settings.port
        self.data['keyboard_controls']['left'] = KeyboardControls.KEY_LEFT
        self.data['keyboard_controls']['right'] = KeyboardControls.KEY_RIGHT
        self.data['keyboard_controls']['gas'] = KeyboardControls.KEY_GAS
        self.data['keyboard_controls']['brake'] = KeyboardControls.KEY_BRAKE
        self.data['keyboard_controls']['clutch'] = KeyboardControls.KEY_CLUTCH
        self.data['keyboard_controls']['handbrake'] = KeyboardControls.KEY_HANDBRAKE
        self.data['keyboard_controls']['shift_up'] = KeyboardControls.KEY_SHIFT_UP
        self.data['keyboard_controls']['shift_down'] = KeyboardControls.KEY_SHIFT_DOWN
        self.data['keyboard_controls']['honk'] = KeyboardControls.KEY_HONK
        self.data['keyboard_controls']['ignition'] = KeyboardControls.KEY_IGNITION
        self.data['keyboard_controls']['headlights'] = KeyboardControls.KEY_HEADLIGHTS
        self.data['keyboard_controls']['left_signal'] = KeyboardControls.KEY_LEFT_TURN_SIGNAL
        self.data['keyboard_controls']['right_signal'] = KeyboardControls.KEY_RIGHT_TURN_SIGNAL
        self.data['keyboard_controls']['emergency_signal'] = KeyboardControls.KEY_EMERGENCY_SIGNAL
        self.data['input_types']['wheel'] = Settings.wheel_input_type
        self.data['input_types']['gas'] = Settings.gas_input_type
        self.data['input_types']['brake'] = Settings.brake_input_type
        self.data['input_types']['clutch'] = Settings.clutch_input_type
        with open(self.file_name, 'w') as file:
            json.dump(self.data, file, indent=4)

    def load(self):
        try:
            with open(self.file_name, 'r') as file:
                self.data = json.load(file)
                Settings.port = self.data['port']
                KeyboardControls.KEY_LEFT = self.data['keyboard_controls']['left']
                KeyboardControls.KEY_RIGHT = self.data['keyboard_controls']['right']
                KeyboardControls.KEY_GAS = self.data['keyboard_controls']['gas']
                KeyboardControls.KEY_BRAKE = self.data['keyboard_controls']['brake']
                KeyboardControls.KEY_CLUTCH = self.data['keyboard_controls']['clutch']
                KeyboardControls.KEY_HANDBRAKE = self.data['keyboard_controls']['handbrake']
                KeyboardControls.KEY_SHIFT_UP = self.data['keyboard_controls']['shift_up']
                KeyboardControls.KEY_SHIFT_DOWN = self.data['keyboard_controls']['shift_down']
                KeyboardControls.KEY_HONK = self.data['keyboard_controls']['honk']
                KeyboardControls.KEY_IGNITION = self.data['keyboard_controls']['ignition']
                KeyboardControls.KEY_HEADLIGHTS = self.data['keyboard_controls']['headlights']
                KeyboardControls.KEY_LEFT_TURN_SIGNAL = self.data['keyboard_controls']['left_signal']
                KeyboardControls.KEY_RIGHT_TURN_SIGNAL = self.data['keyboard_controls']['right_signal']
                KeyboardControls.KEY_EMERGENCY_SIGNAL = self.data['keyboard_controls']['emergency_signal']
                Settings.wheel_input_type = self.data['input_types']['wheel']
                Settings.gas_input_type = self.data['input_types']['gas']
                Settings.brake_input_type = self.data['input_types']['brake']
                Settings.clutch_input_type = self.data['input_types']['clutch']
        except Exception as e:
            print(e)
