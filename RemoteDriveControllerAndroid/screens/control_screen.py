from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_file("screens/control_screen.kv")


class ControlScreen(Screen):
    """Окно с элементами управления"""
    status_label = ObjectProperty()
    controller_canvas = ObjectProperty()

    def on_enter(self, *args):
        self.update_widgets()

    def update_widgets(self):
        self.controller_canvas.update_widgets_settings()

    def open_settings(self):
        """Открытие настроек"""
        self.manager.current = 'settings'

    def turn_connecting_status(self):
        self.status_label.text = "Подключение..."
        self.status_label.color = 'white'

    def turn_connected_status(self, server_ip, server_port):
        self.status_label.text = f"Подключено к {server_ip}:{server_port}"
        self.status_label.color = 'lime'

    def turn_disconnected_status(self, error_msg=None):
        self.status_label.text = f"Ошибка: {error_msg}" if error_msg is not None else "Не подключено"
        self.status_label.color = 'red' if error_msg is not None else 'white'
