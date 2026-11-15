from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

INK_WIDTH = dp(1.5)  # thickness of the pen


class DoodleBox(Widget):
    """A white box you can draw in with black ink. Call clear() to wipe it."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._draw_background, size=self._draw_background)

    def _draw_background(self, *args):
        # Paper and border live in canvas.before so clear() doesn't erase them
        self.canvas.before.clear()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
            Color(0.6, 0.6, 0.6, 1)
            Line(rectangle=(self.x, self.y, self.width, self.height), width=1)

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        touch.grab(self)
        with self.canvas:
            Color(0, 0, 0, 1)
            # a dot, so a single tap leaves a mark too
            d = INK_WIDTH * 2
            Ellipse(pos=(touch.x - d / 2, touch.y - d / 2), size=(d, d))
            touch.ud["line"] = Line(points=[touch.x, touch.y], width=INK_WIDTH,
                                    cap="round", joint="round")
        return True

    def on_touch_move(self, touch):
        if touch.grab_current is self and "line" in touch.ud:
            # keep the ink inside the box if the finger drifts outside it
            x = min(max(touch.x, self.x), self.right)
            y = min(max(touch.y, self.y), self.top)
            touch.ud["line"].points += [x, y]
            return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super().on_touch_up(touch)

    def clear(self):
        self.canvas.clear()