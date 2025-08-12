import time
import threading
import socket
from controllers.keyboard_controller import KeyboardController
from controllers.joystick_controller import JoystickController
from settings import InputType, KeyboardControls, Settings


class ServerConnector:
    """Соединение сервера с приложением контроллера"""
    def __init__(self, window):
        self.host = "0.0.0.0"  # прослушивание всех локальных портов
        self.port = 65432
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.is_running = False
        self.is_connected = False

        # Контроллеры
        self.keyboard_controller = KeyboardController()
        self.joystick_controller = JoystickController()

        # Элементы управления
        self.steering = 0.5
        self.gas = 0
        self.brake = 0
        self.clutch = 0
        self.handbrake = 0
        self.transmission_up = 0
        self.transmission_down = 0
        self.honk = 0
        self.ignition = 0
        self.headlights = 0
        self.left_turn_signal = 0
        self.right_turn_signal = 0
        self.emergency_signal = 0

        # Соединение с интерфейсом
        self.window = window

    def toggle_connection(self):
        """Включение/выключение подключения для кнопки"""
        if self.is_connected:
            self.stop()
            self.window.update_status_label(f"Контроллер отключен по адресу: {self.client_address}", 'red')
            self.window.set_connect_button_disconnected()
        else:
            self.connect_to_controller()

    def connect_to_controller(self):
        """Подключение к контроллеру"""
        self.window.set_connect_button_connecting()
        try:
            self.port = int(Settings.port)
        except ValueError:
            self.port = 65432

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

        self.window.update_status_label(f"Сервер запущен на порту {self.port}. Ожидание подключения контроллера...")

        self.is_running = True
        # Запуск потока подключения
        threading.Thread(target=self.accept_connections, daemon=True).start()
        # Запуск потока обработки нажатий
        threading.Thread(target=self.input_control, daemon=True).start()

    def accept_connections(self):
        """Принимает входящие подключения"""
        while self.is_running:
            try:
                self.server_socket.settimeout(5.0)
                self.client_socket, self.client_address = self.server_socket.accept()
                self.window.update_status_label(f"Контроллер подключен по адресу: {self.client_address}", 'lime')
                self.window.set_connect_button_connected()
                self.is_connected = True

                while self.is_connected:
                    data = self.client_socket.recv(1024).decode()
                    if not data:
                        break
                    try:
                        (self.steering, self.gas, self.brake, self.clutch, self.handbrake,
                         self.transmission_up, self.transmission_down, self.honk, self.ignition,
                         self.headlights, self.left_turn_signal, self.right_turn_signal,
                         self.emergency_signal) = map(float, data.split(';'))
                    except (ValueError, UnicodeDecodeError):
                        continue

            except socket.timeout:
                self.window.update_status_label("Время ожидания подключения вышло", 'red')
                self.window.set_connect_button_disconnected()
                self.stop()
            except Exception as e:
                if self.is_running:
                    self.window.update_status_label(f"Ошибка подключения: {e}", 'red')
                    self.window.set_connect_button_disconnected()
                    self.stop()

    def input_control(self):
        """Обработка нажатий"""
        while self.is_running:
            if self.is_connected:

                # Газ
                if Settings.gas_input_type == InputType.DIGITAL:
                    if self.gas:
                        self.keyboard_controller.press_key(KeyboardControls.KEY_GAS)
                    else:
                        self.keyboard_controller.release_key(KeyboardControls.KEY_GAS)
                else:
                    self.joystick_controller.set_gas(self.gas)

                # Тормоз
                if Settings.brake_input_type == InputType.DIGITAL:
                    if self.brake:
                        self.keyboard_controller.press_key(KeyboardControls.KEY_BRAKE)
                    else:
                        self.keyboard_controller.release_key(KeyboardControls.KEY_BRAKE)
                else:
                    self.joystick_controller.set_brake(self.brake)

                # Руль
                if Settings.wheel_input_type == InputType.DIGITAL:
                    if self.steering < 0.4:
                        self.keyboard_controller.turn_left()
                    elif self.steering > 0.6:
                        self.keyboard_controller.turn_right()
                    else:
                        self.keyboard_controller.center_steering()
                else:
                    self.joystick_controller.set_steering(self.steering)

                # Сцепление
                if Settings.clutch_input_type == InputType.DIGITAL:
                    if self.clutch:
                        self.keyboard_controller.press_key(KeyboardControls.KEY_CLUTCH)
                    else:
                        self.keyboard_controller.release_key(KeyboardControls.KEY_CLUTCH)
                else:
                    self.joystick_controller.set_clutch(self.clutch)

                # Остальные функции
                if self.handbrake:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_HANDBRAKE)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_HANDBRAKE)

                if self.transmission_up:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_SHIFT_UP)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_SHIFT_UP)

                if self.transmission_down:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_SHIFT_DOWN)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_SHIFT_DOWN)

                if self.honk:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_HONK)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_HONK)

                if self.ignition:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_IGNITION)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_IGNITION)

                if self.headlights:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_HEADLIGHTS)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_HEADLIGHTS)

                if self.left_turn_signal:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_LEFT_TURN_SIGNAL)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_LEFT_TURN_SIGNAL)

                if self.right_turn_signal:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_RIGHT_TURN_SIGNAL)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_RIGHT_TURN_SIGNAL)

                if self.emergency_signal:
                    self.keyboard_controller.press_key(KeyboardControls.KEY_EMERGENCY_SIGNAL)
                else:
                    self.keyboard_controller.release_key(KeyboardControls.KEY_EMERGENCY_SIGNAL)

                # Небольшая задержка для снижения нагрузки
                time.sleep(0.02)

    def stop(self):
        """Выключение сервера"""
        self.is_running = False
        self.is_connected = False
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        self.keyboard_controller.cleanup()
        self.joystick_controller.cleanup()
