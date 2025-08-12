from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from settings import Settings, InputType

Builder.load_file("controller_widgets/controller_canvas.kv")


class ControllerCanvas(FloatLayout):
    """Поверхность контроллера со всеми элементами управления"""
    steering_wheel = ObjectProperty()
    turn_left_arrow = ObjectProperty()
    turn_right_arrow = ObjectProperty()
    shifter = ObjectProperty()
    gas_pedal = ObjectProperty()
    brake_pedal = ObjectProperty()
    clutch_pedal = ObjectProperty()
    handbrake = ObjectProperty()
    honk = ObjectProperty()
    ignition = ObjectProperty()
    headlights = ObjectProperty()
    left_turn_signal = ObjectProperty()
    right_turn_signal = ObjectProperty()
    emergency_signal = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Параметры контроллера
        self.turn_val = 0.5
        self.handbrake_val = 0
        self.honk_val = 0
        self.ignition_val = 0
        self.headlights_val = 0
        self.left_turn_signal_val = 0
        self.right_turn_signal_val = 0
        self.emergency_signal_val = 0

        Clock.schedule_interval(self.widgets_adjust, 1/60)

        # Clock.schedule_interval(lambda d: print(self.get_data()), .5)

    def update_widgets_settings(self):
        """Изменение типов управления элементов"""
        self.gas_pedal.input_type = Settings.gas_input_type
        self.brake_pedal.input_type = Settings.brake_input_type
        self.clutch_pedal.input_type = Settings.clutch_input_type
        if Settings.wheel_input_type == InputType.ANALOG:
            self.steering_wheel.max_rotation = Settings.steering_max_value
            self.steering_wheel.size = 500, 500
            self.turn_left_arrow.size = 0, 0
            self.turn_right_arrow.size = 0, 0
        else:
            self.steering_wheel.size = 0, 0
            self.turn_left_arrow.size = 250, 250
            self.turn_right_arrow.size = 250, 250

    def widgets_adjust(self, dt):
        """Цикличное выравнивание виджетов"""
        self.brake_pedal.right = self.gas_pedal.x - 50

    def on_touch_down(self, touch):
        self.steering_wheel.on_touch_down(touch)
        self.gas_pedal.on_touch_down(touch)
        self.brake_pedal.on_touch_down(touch)
        self.clutch_pedal.on_touch_down(touch)
        self.shifter.on_touch_down(touch)
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        self.steering_wheel.on_touch_move(touch)
        self.gas_pedal.on_touch_move(touch)
        self.brake_pedal.on_touch_move(touch)
        self.clutch_pedal.on_touch_move(touch)
        self.shifter.on_touch_move(touch)
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        self.steering_wheel.on_touch_up(touch)
        self.gas_pedal.on_touch_up(touch)
        self.brake_pedal.on_touch_up(touch)
        self.clutch_pedal.on_touch_up(touch)
        self.shifter.on_touch_up(touch)
        return super().on_touch_up(touch)

    def get_data(self):
        """Получение данных контроллера"""
        turn_value = self.steering_wheel.normalized_value if Settings.wheel_input_type == InputType.ANALOG \
            else self.turn_val
        data = (f"{turn_value:.3f};"
                f"{self.gas_pedal.normalized_value:.2f};"
                f"{self.brake_pedal.normalized_value:.2f};"
                f"{self.clutch_pedal.normalized_value:.2f};"
                f"{self.handbrake_val};"
                f"{1 if self.shifter.normalized_value == 1 else 0};"  # повышенная передача
                f"{1 if self.shifter.normalized_value == -1 else 0};"  # пониженная передача
                f"{self.honk_val};" 
                f"{self.ignition_val};"
                f"{self.headlights_val};"
                f"{self.left_turn_signal_val};"
                f"{self.right_turn_signal_val};"
                f"{self.emergency_signal_val}")
        return data
