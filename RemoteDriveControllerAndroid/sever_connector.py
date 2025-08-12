from kivy.clock import Clock
import threading
import socket
from settings import Settings


class SeverConnector:
    """Подключение к серверу, куда направляются данные с контроллера"""

    def __init__(self, app):
        self.app = app

        # Сокет подключения
        self.socket = None
        self.is_connected = False

        # Запускаем поток отправки данных
        Clock.schedule_interval(self.send_data, 0.05)

    def toggle_connection(self):
        """Начало подключения"""
        if not self.is_connected:
            self.app.settings_screen.turn_connecting_status()
            self.app.control_screen.turn_connecting_status()
            threading.Thread(target=self.connect_to_server, daemon=True).start()
        else:
            self.disconnect_from_server()

    def connect_to_server(self):
        """Подключение к серверу"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5)
            self.socket.connect((Settings.server_ip, Settings.server_port))
            self.is_connected = True
            self.app.control_screen.turn_connected_status(Settings.server_ip, Settings.server_port)
            self.app.settings_screen.turn_connected_status()
        except Exception as error_msg:
            self.is_connected = False
            self.app.control_screen.turn_disconnected_status(str(error_msg))
            self.app.settings_screen.turn_disconnected_status()
            if self.socket:
                self.socket.close()
                self.socket = None

    def disconnect_from_server(self):
        """Отключение от сервера"""
        if self.socket:
            self.socket.close()
            self.socket = None
        self.is_connected = False
        self.app.control_screen.turn_disconnected_status()
        self.app.settings_screen.turn_disconnected_status()

    def send_data(self, dt):
        """Отправка данных серверу"""
        if self.is_connected:
            try:
                data = self.app.control_screen.controller_canvas.get_data()
                self.socket.sendall(data.encode())
            except Exception as e:
                self.app.control_screen.turn_disconnected_status(str(e))
                self.disconnect_from_server()
