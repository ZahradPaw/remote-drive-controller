from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, StringProperty
from kivy.clock import Clock
from kivy.graphics import Rectangle


class Shifter(Widget):
    """Виджет коробки передач"""
    background_source = StringProperty("assets/shifter_bg.png")
    lever_source = StringProperty("assets/shifter_lever.png")
    value = NumericProperty(0.0)  # от -1 (низ) до 1 (верх)
    size_hint = None, None

    _touch_offset_y = 0.0  # смещение внутри рычага при захвате
    _return_event = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Задаём размеры рычага пропорционально, можно менять
        with self.canvas:
            # Фон
            self._bg_rect = Rectangle(source=self.background_source, pos=self.pos, size=self.size)
            # Рычаг: мы будем рисовать его отдельно и смещать по y вручную
            self._lever_rect = Rectangle(source=self.lever_source, pos=self._lever_pos(), size=self._lever_size())
        self.bind(pos=self._update_graphics, size=self._update_graphics)
        self.bind(value=self._update_lever_position)
        Clock.schedule_interval(self._return_to_center, 1 / 60)

    def _lever_size(self):
        # Делаем рычаг чуть уже/меньше фона, можно настроить
        w = self.width * 1.6
        h = self.height * 0.5
        return w, h

    def _lever_pos(self):
        lw, lh = self._lever_size()
        cx = self.center_x - lw / 2
        # центрированное по вертикали с учётом current value
        half_range = (self.height - lh) / 2
        offset = self.value * half_range
        cy = self.center_y - lh / 2 + offset
        return cx, cy

    def _update_graphics(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size
        self._update_lever_position()

    def _update_lever_position(self, *args):
        # Обновляем позицию рычага в зависимости от self.value
        lw, lh = self._lever_size()
        cx = self.center_x - lw / 2
        half_range = (self.height - lh) / 2 + (lh / 2)
        offset = self.value * half_range
        cy = self.center_y - lh / 2 + offset
        self._lever_rect.pos = (cx, cy)
        self._lever_rect.size = (lw, lh)

    def on_touch_down(self, touch):
        # Захватываем, если клик попал на рычаг (по текущему положению) или близко к центру
        if self._point_on_lever(touch.pos) or self.collide_point(*touch.pos):
            touch.grab(self)
            if self._return_event:
                self._return_event.cancel()
                self._return_event = None
            # Запомним смещение внутри рычага, чтобы не "прыгал"
            lever_x, lever_y = self._lever_rect.pos
            self._touch_offset_y = touch.y - lever_y
            self._update_value_from_touch(touch)
            return True
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self._update_value_from_touch(touch)
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            # Плавный возврат к 0
            if self._return_event:
                self._return_event.cancel()
            self._return_event = Clock.schedule_interval(self._return_to_center, 1/60)
            return True
        return super().on_touch_up(touch)

    def _point_on_lever(self, pos):
        lx, ly = self._lever_rect.pos
        lw, lh = self._lever_rect.size
        x, y = pos
        return lx <= x <= lx + lw and ly <= y <= ly + lh

    def _update_value_from_touch(self, touch):
        # Пересчёт value по вертикальному положению рычага, ограничивая в [-1,1]
        # Берём y-координату центра рычага относительно фона
        lw, lh = self._lever_size()
        # Новая центрированная позиция lever_y так, чтобы учесть _touch_offset_y
        desired_lever_y = touch.y - self._touch_offset_y
        # Ограничиваем в пределах перемещения
        min_y = self.y - (lh / 2)
        max_y = self.top - lh + (lh / 2)
        constrained_y = max(min_y, min(max_y, desired_lever_y))
        # Нормализуем: середина фона -> 0, верх -> 1, низ -> -1
        center_lever_y = self.y + (self.height - lh) / 2
        half_range = (self.height - lh) / 2 + (lh / 2)
        delta = constrained_y - center_lever_y
        self.value = max(-1.0, min(1.0, delta / half_range))

    def _return_to_center(self, dt):
        # Плавное приближение к 0
        if abs(self.value) < 0.01:
            self.value = 0
            if self._return_event:
                self._return_event.cancel()
                self._return_event = None
            return False
        # Интерполяция: сглаживание
        self.value *= 0.8
        return True

    @property
    def normalized_value(self):
        if self.value > 0.9:
            return 1
        elif self.value < -0.9:
            return -1
        return 0
