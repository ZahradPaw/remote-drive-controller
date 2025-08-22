from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from settings import Settings, InputType
from utils import StorageLoader

Builder.load_file("screens/controls_settings_screen.kv")


class ControlsSettingsScreen(Screen):
    """Окно настроек элементов управления"""

    analog_gas_check = ObjectProperty()
    analog_brake_check = ObjectProperty()
    analog_clutch_check = ObjectProperty()
    analog_wheel_check = ObjectProperty()
    wheel_slider = ObjectProperty()

    storage_loader = StorageLoader()

    def to_settings(self, instance=None):
        Settings.steering_max_value = self.wheel_slider.value
        self.manager.current = 'settings'

    def on_enter(self, *args):
        self.wheel_slider.value = Settings.steering_max_value
        self.wheel_slider.disabled = True if Settings.wheel_input_type == InputType.DIGITAL else False
        self.analog_wheel_check.active = True if Settings.wheel_input_type == InputType.ANALOG else False
        self.analog_gas_check.active = True if Settings.gas_input_type == InputType.ANALOG else False
        self.analog_brake_check.active = True if Settings.brake_input_type == InputType.ANALOG else False
        self.analog_clutch_check.active = True if Settings.clutch_input_type == InputType.ANALOG else False

    # Методы переключения режима педалей и руля
    def on_gas_active(self, checkbox, value):
        if value:
            Settings.gas_input_type = InputType.ANALOG
        else:
            Settings.gas_input_type = InputType.DIGITAL

    def on_brake_active(self, checkbox, value):
        if value:
            Settings.brake_input_type = InputType.ANALOG
        else:
            Settings.brake_input_type = InputType.DIGITAL

    def on_clutch_active(self, checkbox, value):
        if value:
            Settings.clutch_input_type = InputType.ANALOG
        else:
            Settings.clutch_input_type = InputType.DIGITAL

    def on_wheel_active(self, checkbox, value):
        if value:
            Settings.wheel_input_type = InputType.ANALOG
            self.wheel_slider.disabled = False
        else:
            Settings.wheel_input_type = InputType.DIGITAL
            self.wheel_slider.disabled = True

    def on_leave(self, *args):
        # Сохранение настроек
        self.storage_loader.save()
        return super().on_leave(*args)
