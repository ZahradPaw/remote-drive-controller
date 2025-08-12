KEYS = [
    # Буквы
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z',
    # Цифры
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    # Символы
    '`', '-', '=', '[', ']', '\\', ';', "'", ',', '.', '/',
    # Специальные клавиши
    'esc', 'enter', 'tab', 'backspace', 'insert', 'delete', 'right', 'left', 'down', 'up', 'space',
    'page up', 'page down', 'home', 'end', 'caps lock', 'scroll lock', 'num lock', 'print screen', 'pause',
    # Функциональные клавиши
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12',
    # Модификаторы
    'shift', 'ctrl', 'alt', 'win', 'cmd', 'menu',
    # Цифровая клавиатура
    'num 0', 'num 1', 'num 2', 'num 3', 'num 4', 'num 5', 'num 6', 'num 7', 'num 8', 'num 9',
]


class KeyboardControls:
    """Настройка управления с клавиатуры"""
    KEY_LEFT = 'a'
    KEY_RIGHT = 'd'
    KEY_GAS = 'w'
    KEY_BRAKE = 's'
    KEY_CLUTCH = 'shift'
    KEY_HANDBRAKE = 'space'
    KEY_SHIFT_UP = 'up'
    KEY_SHIFT_DOWN = 'down'
    KEY_HONK = 'h'
    KEY_IGNITION = 'v'
    KEY_HEADLIGHTS = 'n'
    KEY_LEFT_TURN_SIGNAL = 'left'
    KEY_RIGHT_TURN_SIGNAL = 'right'
    KEY_EMERGENCY_SIGNAL = '/'


class InputType:
    """Тип ввода (аналоговый или цифровой)"""
    ANALOG = 0
    DIGITAL = 1


class Settings:
    """Настройки"""
    port = 65432
    wheel_input_type = InputType.ANALOG
    gas_input_type = InputType.ANALOG
    brake_input_type = InputType.ANALOG
    clutch_input_type = InputType.DIGITAL
