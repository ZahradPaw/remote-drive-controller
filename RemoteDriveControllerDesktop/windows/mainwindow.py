from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtGui import QIcon
from windows.ui_mainwindow import Ui_MainWindow
from windows.settingswindow import SettingsWindow
from server_connector import ServerConnector
from utils import StorageLoader, resource_path


class MainWindow(QMainWindow):
    """Главное окно приложения"""

    def __init__(self):
        super(MainWindow, self).__init__()

        self.icon = QIcon(resource_path('assets/icon.ico'))
        self.setWindowIcon(self.icon)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # pyuic6 -x windows/mainwindow.ui -o windows/ui_mainwindow.py

        self.server_connector = ServerConnector(self)
        self.storage_loader = StorageLoader()

        self.ui.connect_button.clicked.connect(self.server_connector.toggle_connection)
        self.set_connect_button_disconnected()

        self.settings_window = SettingsWindow()
        self.ui.settings_button.clicked.connect(self.open_settings)

    def update_status_label(self, msg, color='white'):
        self.ui.connect_status_label.setText(msg)
        self.ui.connect_status_label.setStyleSheet(f'color: {color}')

    def set_connect_button_disconnected(self):
        self.ui.connect_button.setText('Подключиться')
        self.ui.connect_button.setStyleSheet("""QPushButton#connect_button { 
                background-color: green;
                }
                QPushButton#connect_button:hover { 
                background-color: rgb(66, 202, 66);
                }""")
        self.ui.connect_button.setDisabled(False)

    def set_connect_button_connecting(self):
        self.ui.connect_button.setText('Подключение...')
        self.ui.connect_button.setStyleSheet('background-color: gray')
        self.ui.connect_button.setDisabled(True)

    def set_connect_button_connected(self):
        self.ui.connect_button.setText('Отключиться')
        self.ui.connect_button.setStyleSheet("""QPushButton#connect_button { 
                background-color: red;
                }
                QPushButton#connect_button:hover { 
                background-color: rgb(255, 100, 100);
                }""")
        self.ui.connect_button.setDisabled(False)

    def open_settings(self):
        self.settings_window.show()

    def show(self):
        super().show()
        self.storage_loader.load()

    def closeEvent(self, event):
        super().closeEvent(event)
        self.storage_loader.save()
