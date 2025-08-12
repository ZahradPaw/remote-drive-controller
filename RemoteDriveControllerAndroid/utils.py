from kivy.storage.jsonstore import JsonStore
from settings import Settings


class StorageLoader:
    """Загрузка и сохранение настроек"""
    storage = JsonStore('options.json')

    def save(self):
        self.storage.put('gas', input_type=Settings.gas_input_type)
        self.storage.put('brake', input_type=Settings.brake_input_type)
        self.storage.put('clutch', input_type=Settings.clutch_input_type)
        self.storage.put('wheel', input_type=Settings.wheel_input_type,
                         steering_max_value=Settings.steering_max_value)
        self.storage.put('server', ip=Settings.server_ip, port=Settings.server_port)

    def load(self):
        if not (self.storage.exists('gas') or self.storage.exists('brake') or self.storage.exists('clutch') or
                self.storage.exists('wheel') or self.storage.exists('server')):
            return
        Settings.gas_input_type = self.storage.get('gas')['input_type']
        Settings.brake_input_type = self.storage.get('brake')['input_type']
        Settings.clutch_input_type = self.storage.get('clutch')['input_type']
        Settings.wheel_input_type = self.storage.get('wheel')['input_type']
        Settings.steering_max_value = self.storage.get('wheel')['steering_max_value']
        Settings.server_ip = self.storage.get('server')['ip']
        Settings.server_port = self.storage.get('server')['port']
