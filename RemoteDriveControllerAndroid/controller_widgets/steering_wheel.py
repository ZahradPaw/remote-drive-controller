from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import PushMatrix, PopMatrix, Rotate, Rectangle
from math import atan2, degrees


class SteeringWheel(Widget):
    """Виджет аналогового руля"""
    source = StringProperty("assets/wheel.png")
    rotation_angle = NumericProperty(0)   # накопленный угол в градусах, ограничен ±max_rotation
    max_rotation = NumericProperty(1080)  # 3 оборота = 1080°
    _last_touch_angle = 0.0
    _return_event = None
    size_hint = None, None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas:
            PushMatrix()
            self.rot = Rotate(origin=self.center, angle=self.rotation_angle)
            self.rect = Rectangle(source=self.source, pos=self.pos, size=self.size)
            PopMatrix()

        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.bind(rotation_angle=self._update_rotation)

    def _update_graphics(self, *args):
        self.rot.origin = self.center
        self.rect.pos = self.pos
        self.rect.size = self.size

    def _update_rotation(self, *args):
        self.rot.angle = self.rotation_angle

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            # Отменяем возврат, если был
            if self._return_event:
                self._return_event.cancel()
                self._return_event = None

            # Захватываем касание, чтобы продолжать даже если оно ушло за границы
            touch.grab(self)
            self._last_touch_angle = self._get_angle(touch.pos)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        # Обрабатываем только захваченные
        if touch.grab_current is self:
            angle_now = self._get_angle(touch.pos)
            # Разница между текущим и предыдущим углом, учёт обёртывания
            delta = ((angle_now - self._last_touch_angle + 180) % 360) - 180
            # Накопить с ограничением по максимуму
            new_angle = self.rotation_angle + delta
            # Ограничиваем в пределах
            self.rotation_angle = max(-self.max_rotation, min(self.max_rotation, new_angle))
            # Обновим базовый для следующего шага
            self._last_touch_angle = angle_now
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            # Отпускаем захват
            touch.ungrab(self)
            # Запускаем плавный возврат
            if self._return_event:
                self._return_event.cancel()
            self._return_event = Clock.schedule_interval(self._return_to_center, 1/60)
            return True
        return super().on_touch_up(touch)

    def _get_angle(self, pos):
        dx = pos[0] - self.center_x
        dy = pos[1] - self.center_y
        return degrees(atan2(dy, dx))

    def _return_to_center(self, dt):
        # Плавно возвращаем к нулю (экспоненциальное затухание)
        if abs(self.rotation_angle) < 0.5:
            self.rotation_angle = 0
            self._return_event = None
            return False
        self.rotation_angle *= 0.9  # демпфинг
        return True

    @property
    def angle_degrees(self):
        return -self.rotation_angle

    @property
    def normalized_value(self):
        return (-(self.rotation_angle / self.max_rotation) + 1) / 2
