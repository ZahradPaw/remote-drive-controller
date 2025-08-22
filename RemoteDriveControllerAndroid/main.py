from kivy.app import App
from kivy.uix.screenmanager import ScreenManager
from screens import ControlScreen, SettingsScreen, ControlsSettingsScreen
from sever_connector import SeverConnector
from utils import StorageLoader


class MainApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.storage_loader = StorageLoader()
        self.server_connector = SeverConnector(self)

        # Окна
        self.screen_manager = ScreenManager()
        self.control_screen = ControlScreen(name='controls')
        self.settings_screen = SettingsScreen(name='settings')
        self.controls_settings_screen = ControlsSettingsScreen(name='controls_settings')

    def build(self):
        self.screen_manager.add_widget(self.control_screen)
        self.screen_manager.add_widget(self.settings_screen)
        self.screen_manager.add_widget(self.controls_settings_screen)

        return self.screen_manager

    def on_connection(self):
        """Функция подключения"""
        self.storage_loader.save()
        self.server_connector.toggle_connection()

    def on_start(self):
        self.storage_loader.load()
        self.control_screen.update_widgets()


if __name__ == '__main__':
    MainApp().run()
