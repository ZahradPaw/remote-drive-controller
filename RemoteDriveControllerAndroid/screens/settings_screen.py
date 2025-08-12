from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from settings import Settings

Builder.load_file("screens/settings_screen.kv")


class SettingsScreen(Screen):
    """Окно настроек"""
    ip_input = ObjectProperty()
    port_input = ObjectProperty()
    errors_label = ObjectProperty()
    connect_button = ObjectProperty()

    def on_enter(self, *args):
        self.ip_input.text = Settings.server_ip
        self.port_input.text = str(Settings.server_port)
        
    def connect(self):
        """Передача введенных IP и порта главному окну"""
        try:
            Settings.server_ip = self.ip_input.text
            server_port = int(self.port_input.text)
            if not 0 <= server_port <= 65535:
                raise ValueError
            Settings.server_port = server_port
            app = App.get_running_app()
            app.on_connection()
            self.errors_label.text = ''
            self.to_controls()
        except ValueError:
            self.errors_label.text = 'Ошибка: порт должен состоять только из цифр от 0 до 65535'

    def to_controls(self):
        self.manager.current = 'controls'

    def to_control_settings(self):
        self.manager.current = 'controls_settings'

    def turn_connecting_status(self):
        self.connect_button.disabled = True
        self.connect_button.text = "Подключение..."
        self.connect_button.background_color = 'gray'

    def turn_connected_status(self):
        self.connect_button.disabled = False
        self.connect_button.text = "Отключиться"
        self.connect_button.background_color = 1, 0, 0

    def turn_disconnected_status(self):
        self.connect_button.disabled = False
        self.connect_button.text = "Подключиться"
        self.connect_button.background_color = 'lime'
