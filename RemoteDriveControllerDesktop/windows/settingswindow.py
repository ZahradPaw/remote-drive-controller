from PyQt6.QtGui import QIntValidator, QIcon
from PyQt6.QtWidgets import QWidget, QMessageBox
from windows.ui_settingswindow import Ui_SettingsWindow
from settings import KeyboardControls, Settings, InputType, KEYS
from utils import resource_path


class SettingsWindow(QWidget):
    """Окно настроек"""

    def __init__(self):
        super(SettingsWindow, self).__init__()

        self.icon = QIcon(resource_path('assets/icon.ico'))
        self.setWindowIcon(self.icon)

        self.ui = Ui_SettingsWindow()
        self.ui.setupUi(self)
        # pyuic6 -x windows/settingswindow.ui -o windows/ui_settingswindow.py

        self.setWindowTitle('Настройки')

        port_validator = QIntValidator(0, 65535)
        self.ui.port_edit.setValidator(port_validator)

        # Настройка чекбоксов управления
        self.control_checkboxes = (self.ui.gas_box, self.ui.brake_box, self.ui.clutch_box, self.ui.turn_left_box,
                                   self.ui.turn_rigth_box, self.ui.handbrake_box, self.ui.shift_up_box,
                                   self.ui.shift_down_box, self.ui.honk_box, self.ui.ignition_box,
                                   self.ui.headlights_box, self.ui.left_signal_box, self.ui.right_signal_box,
                                   self.ui.emergency_signal_box)

        for checkbox in self.control_checkboxes:
            checkbox.addItems(KEYS)

        self.ui.apply_button.clicked.connect(self.on_apply)
        self.ui.cancel_button.clicked.connect(self.on_cancel)

    def show(self):
        super().show()
        self.load_settings()

    def load_settings(self):
        """Загрузка текущих настроек"""
        self.ui.port_edit.setText(str(Settings.port))
        self.ui.analog_wheel_check.setChecked(True if Settings.wheel_input_type == InputType.ANALOG else False)
        self.ui.analog_gas_check.setChecked(True if Settings.gas_input_type == InputType.ANALOG else False)
        self.ui.analog_brake_check.setChecked(True if Settings.brake_input_type == InputType.ANALOG else False)
        self.ui.analog_clutch_check.setChecked(True if Settings.clutch_input_type == InputType.ANALOG else False)
        self.ui.gas_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_GAS))
        self.ui.brake_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_BRAKE))
        self.ui.clutch_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_CLUTCH))
        self.ui.turn_left_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_LEFT))
        self.ui.turn_rigth_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_RIGHT))
        self.ui.handbrake_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_HANDBRAKE))
        self.ui.shift_up_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_SHIFT_UP))
        self.ui.shift_down_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_SHIFT_DOWN))
        self.ui.honk_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_HONK))
        self.ui.ignition_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_IGNITION))
        self.ui.headlights_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_HEADLIGHTS))
        self.ui.left_signal_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_LEFT_TURN_SIGNAL))
        self.ui.right_signal_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_RIGHT_TURN_SIGNAL))
        self.ui.emergency_signal_box.setCurrentIndex(KEYS.index(KeyboardControls.KEY_EMERGENCY_SIGNAL))

    def on_apply(self):
        """Функция кнопки принятия изменений"""
        if not self.check_repetitions():
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setWindowTitle('Внимание!')
            msg.setText('Найдены повторяющиеся клавиши!')
            msg.exec()
            return
        Settings.port = int(self.ui.port_edit.text())
        Settings.wheel_input_type = InputType.ANALOG if self.ui.analog_wheel_check.isChecked() else InputType.DIGITAL
        Settings.gas_input_type = InputType.ANALOG if self.ui.analog_gas_check.isChecked() else InputType.DIGITAL
        Settings.brake_input_type = InputType.ANALOG if self.ui.analog_brake_check.isChecked() else InputType.DIGITAL
        Settings.clutch_input_type = InputType.ANALOG if self.ui.analog_clutch_check.isChecked() else InputType.DIGITAL
        KeyboardControls.KEY_LEFT = self.ui.turn_left_box.currentText()
        KeyboardControls.KEY_RIGHT = self.ui.turn_rigth_box.currentText()
        KeyboardControls.KEY_GAS = self.ui.gas_box.currentText()
        KeyboardControls.KEY_BRAKE = self.ui.brake_box.currentText()
        KeyboardControls.KEY_CLUTCH = self.ui.clutch_box.currentText()
        KeyboardControls.KEY_HANDBRAKE = self.ui.handbrake_box.currentText()
        KeyboardControls.KEY_SHIFT_UP = self.ui.shift_up_box.currentText()
        KeyboardControls.KEY_SHIFT_DOWN = self.ui.shift_down_box.currentText()
        KeyboardControls.KEY_HONK = self.ui.honk_box.currentText()
        KeyboardControls.KEY_IGNITION = self.ui.ignition_box.currentText()
        KeyboardControls.KEY_HEADLIGHTS = self.ui.headlights_box.currentText()
        KeyboardControls.KEY_LEFT_TURN_SIGNAL = self.ui.left_signal_box.currentText()
        KeyboardControls.KEY_RIGHT_TURN_SIGNAL = self.ui.right_signal_box.currentText()
        KeyboardControls.KEY_EMERGENCY_SIGNAL = self.ui.emergency_signal_box.currentText()
        self.close()

    def on_cancel(self):
        """Функция кнопки отмены"""
        self.close()

    def check_repetitions(self):
        keys = [checkbox.currentText() for checkbox in self.control_checkboxes]
        if len(keys) == len(set(keys)):
            return True
        return False
