class InputType:
    """Тип ввода (аналоговый или цифровой)"""
    ANALOG = 0
    DIGITAL = 1


class Settings:
    """Настройка элементов контроллера"""
    wheel_input_type = InputType.ANALOG
    steering_max_value = 1080
    gas_input_type = InputType.ANALOG
    brake_input_type = InputType.ANALOG
    clutch_input_type = InputType.ANALOG
    server_ip = "192.168.0.0"
    server_port = 65432
