from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle
from settings import InputType


class Pedal(Widget):
    """Виджет аналоговой педали"""
    source = StringProperty("assets/gas_pedal.png")
    glow_texture = StringProperty("assets/glow_pedal.png")
    press_value = NumericProperty(0.0)  # от 0 (не нажата) до 1 (максимально)
    _return_event = None
    _is_active = BooleanProperty(False)
    size_hint = None, None
    input_type = InputType.ANALOG

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        with self.canvas:
            self._pedal_rect = Rectangle(source=self.source, pos=self.pos, size=self.size)
            # Светящийся индикатор нажатия над педалью
            self._glow_rect = Rectangle(source=self.glow_texture, pos=self.pos, size=(self.width * 1.5, 0))

        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.bind(press_value=self._update_glow)

    def _update_graphics(self, *args):
        self._pedal_rect.pos = self.pos
        self._pedal_rect.size = self.size
        self._update_glow()

    def _update_glow(self, *args):
        """Обновление зоны нажатия"""
        h = self.height * self.press_value
        self._glow_rect.size = (self.width * 1.5, h)
        self._glow_rect.pos = (self.center_x - self.width * 1.5 / 2, self.y)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self)
            self._is_active = True
            if self._return_event:
                self._return_event.cancel()
                self._return_event = None
            self._update_press_from_touch(touch)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self._update_press_from_touch(touch)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            self._is_active = False
            if self._return_event:
                self._return_event.cancel()
            self._return_event = Clock.schedule_interval(self._return_to_zero, 1/60)
            return True
        return super().on_touch_up(touch)

    def _update_press_from_touch(self, touch):
        # Если аналоговый тип ввода, сила нажатия зависит от высоты нажатия
        if self.input_type == InputType.ANALOG:
            local_y = touch.y - self.y
            v = max(0.0, min(1.0, local_y / self.height))
        else:
            v = 1.0
        self.press_value = v

    def _return_to_zero(self, dt):
        """Плавное сбрасывание педали"""
        if self.press_value <= 0.001:
            self.press_value = 0
            if self._return_event:
                self._return_event.cancel()
                self._return_event = None
            return False
        # Скорость сбрасывания (чем меньше значение, тем быстрее)
        self.press_value *= 0.15
        return True

    @property
    def normalized_value(self):
        return self.press_value


class GasPedal(Pedal):
    """Виджет педали газа"""
    source = StringProperty("assets/gas_pedal.png")


class BrakePedal(Pedal):
    """Виджет педали тормоза"""
    source = StringProperty("assets/brake_pedal.png")


class ClutchPedal(Pedal):
    """Виджет педали сцепления"""
    source = StringProperty("assets/brake_pedal.png")
