import pyvjoy


class JoystickController:
    """Реализация управления через vJoy (джойстик)"""

    def __init__(self):
        self.joystick = pyvjoy.VJoyDevice(1)
        self.center_all()

    def center_all(self):
        """Центрирует все оси"""
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, 0x4000)  # Центр руля
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, 0)  # Сцепление отпущено
        self.joystick.set_axis(pyvjoy.HID_USAGE_Z, 0)  # Газ отпущен
        self.joystick.set_axis(pyvjoy.HID_USAGE_RZ, 0)  # Тормоз отпущен

    def set_gas(self, value):
        throttle_value = int(value * 0x7FFF)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Z, throttle_value)

    def set_brake(self, value):
        brake_value = int(value * 0x7FFF)
        self.joystick.set_axis(pyvjoy.HID_USAGE_RZ, brake_value)

    def set_clutch(self, value):
        clutch_value = int(value * 0x7FFF)
        self.joystick.set_axis(pyvjoy.HID_USAGE_Y, clutch_value)

    def set_steering(self, value):
        corrected_value = (value - 0.5) * 2
        steering_value = int((corrected_value + 1.0) * 0x4000)  # 0x0000-0x8000
        self.joystick.set_axis(pyvjoy.HID_USAGE_X, steering_value)

    def cleanup(self):
        self.center_all()
