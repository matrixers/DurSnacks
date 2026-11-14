from kivy.config import Config

# Phone-shaped window (desktop only; ignored on a real phone)
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")
Config.set("graphics", "resizable", False)

import math

from kivy.animation import Animation
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Mesh, Rectangle
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ListProperty, NumericProperty,
                             StringProperty)
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

Window.clearcolor = get_color_from_hex("#50836A")  # dark forest green

TRUNK = get_color_from_hex("#6B4423")
TRUNK_DARK = get_color_from_hex("#3E2713")

# Core feeling -> (colour, [(secondary feeling, deeper feeling), ...])
# Order is clockwise, taken from the feelings wheel image.
FEELINGS = {
    "Mad": ("#E8212A", [
        ("Hurt", "Distant"), ("Hostile", "Sarcastic"), ("Angry", "Frustrated"),
        ("Selfish", "Jealous"), ("Hateful", "Irritated"), ("Critical", "Skeptical")]),
    "Scared": ("#F07E22", [
        ("Confused", "Bewildered"), ("Rejected", "Discouraged"),
        ("Helpless", "Insignificant"), ("Submissive", "Inadequate"),
        ("Insecure", "Embarrassed"), ("Anxious", "Overwhelmed")]),
    "Joyful": ("#E6DC1E", [
        ("Excited", "Daring"), ("Sensuous", "Fascinating"),
        ("Energetic", "Stimulating"), ("Cheerful", "Amused"),
        ("Creative", "Playful"), ("Hopeful", "Optimistic")]),
    "Powerful": ("#6BBE45", [
        ("Aware", "Surprised"), ("Proud", "Successful"),
        ("Respected", "Worthwhile"), ("Appreciated", "Valuable"),
        ("Important", "Discerning"), ("Faithful", "Confident")]),
    "Peaceful": ("#3F5BB5", [
        ("Nurturing", "Thankful"), ("Trusting", "Secure"), ("Loving", "Serene"),
        ("Intimate", "Responsive"), ("Thoughtful", "Pensive"),
        ("Content", "Relaxed")]),
    "Sad": ("#B54C9C", [
        ("Tired", "Sleepy"), ("Bored", "Apathetic"), ("Lonely", "Isolated"),
        ("Depressed", "Inferior"), ("Ashamed", "Stupid"),
        ("Guilty", "Remorseful")]),
}


def lighten(c, amount):
    return (c[0] + (1 - c[0]) * amount, c[1] + (1 - c[1]) * amount,
            c[2] + (1 - c[2]) * amount, c[3])


def darken(c, factor):
    return (c[0] * factor, c[1] * factor, c[2] * factor, c[3])


def text_colour(c):
    """Dark text on light leaves, white text on dark leaves."""
    luminance = 0.299 * c[0] + 0.587 * c[1] + 0.114 * c[2]
    return (0.1, 0.1, 0.1, 1) if luminance > 0.55 else (1, 1, 1, 1)


class EmotionWheel(Widget):
    progress = NumericProperty(1)      # 0 = leaves collapsed, 1 = fully grown
    spin = NumericProperty(0)          # extra rotation (degrees) while animating
    path = ListProperty([])            # e.g. ["Mad"] once a core feeling is picked
    result_path = ListProperty([])     # [core, secondary, deeper] when finished
    prompt = StringProperty("Tap the leaf that fits best")
    busy = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.labels = []
        for _ in range(6):
            lbl = Label(size_hint=(None, None), bold=True)
            lbl.bind(texture_size=lbl.setter("size"))
            lbl.bind(size=self.redraw)
            self.labels.append(lbl)
            self.add_widget(lbl)
        self.centre_label = Label(size_hint=(None, None), bold=True,
                                  color=(1, 1, 1, 1))
        self.centre_label.bind(texture_size=self.centre_label.setter("size"))
        self.centre_label.bind(size=self.redraw)
        self.add_widget(self.centre_label)

        self.bind(pos=self.redraw, size=self.redraw, progress=self.redraw,
                  spin=self.redraw, path=self.redraw)

    # ---------- data ----------
    @property
    def radius(self):
        return min(self.size) / 2 * 0.95

    def items(self):
        if not self.path:
            return [(name, get_color_from_hex(v[0]))
                    for name, v in FEELINGS.items()]
        colour, subs = FEELINGS[self.path[0]]
        base = get_color_from_hex(colour)
        return [(sub[0], lighten(base, 0.07 * (i % 3)))
                for i, sub in enumerate(subs)]

    # ---------- drawing ----------
    def _geometry(self, R, scale):
        r0 = R * 0.12
        r1 = R * (0.12 + 0.86 * scale)
        half_w = R * 0.29 * scale
        return r0, r1, half_w

    def _draw_leaf(self, cx, cy, R, ang, rgba, scale):
        if scale < 0.02:
            return
        r0, r1, half_w = self._geometry(R, scale)
        dx, dy = math.sin(ang), math.cos(ang)
        px, py = dy, -dx  # perpendicular to the leaf's axis

        left, right = [], []
        steps = 14
        for k in range(steps + 1):
            t = k / steps
            d = r0 + (r1 - r0) * t
            h = half_w * math.sin(math.pi * t ** 0.85)
            bx, by = cx + dx * d, cy + dy * d
            left.append((bx + px * h, by + py * h))
            right.append((bx - px * h, by - py * h))
        outline = left + right[::-1]

        mid = (cx + dx * (r0 + r1) / 2, cy + dy * (r0 + r1) / 2)
        verts = []
        for x, y in [mid] + outline + [outline[0]]:
            verts += [x, y, 0, 0]

        Color(*rgba)
        Mesh(vertices=verts, indices=list(range(len(verts) // 4)),
             mode="triangle_fan")
        Color(*darken(rgba, 0.6))
        Line(points=[c for p in outline for c in p], close=True, width=1.2)
        Color(*lighten(rgba, 0.35))
        Line(points=[cx + dx * r0, cy + dy * r0,
                     cx + dx * r1 * 0.95, cy + dy * r1 * 0.95], width=1.1)

    def redraw(self, *args):
        cx, cy = self.center
        R = self.radius
        items = self.items()
        step = 360 / len(items)
        scale = max(self.progress, 0)

        self.canvas.before.clear()
        with self.canvas.before:
            # trunk
            Color(*TRUNK)
            trunk_w = R * 0.1
            Rectangle(pos=(cx - trunk_w / 2, self.y),
                      size=(trunk_w, max(cy - self.y, 0)))
            # leaves
            for i, (_, colour) in enumerate(items):
                ang = math.radians((i + 0.5) * step + self.spin)
                self._draw_leaf(cx, cy, R, ang, colour, scale)
            # knot in the middle (tap to go back)
            knot = R * 0.19
            Color(*TRUNK)
            Ellipse(pos=(cx - knot, cy - knot), size=(2 * knot, 2 * knot))
            Color(*TRUNK_DARK)
            Line(circle=(cx, cy, knot), width=2)

        # labels sit in the middle of each leaf
        r0, r1, _ = self._geometry(R, scale)
        dmid = (r0 + r1) / 2
        font_size = max(R * 0.085, 9)
        opacity = min(1, max(0, (scale - 0.4) / 0.6))
        for i, lbl in enumerate(self.labels):
            name, colour = items[i]
            if lbl.text != name:
                lbl.text = name
            if abs(lbl.font_size - font_size) > 0.5:
                lbl.font_size = font_size
            lbl.color = text_colour(colour)
            lbl.opacity = opacity
            ang = math.radians((i + 0.5) * step + self.spin)
            lbl.center = (cx + math.sin(ang) * dmid, cy + math.cos(ang) * dmid)

        back_text = "Back" if self.path else ""
        if self.centre_label.text != back_text:
            self.centre_label.text = back_text
        if abs(self.centre_label.font_size - R * 0.075) > 0.5:
            self.centre_label.font_size = R * 0.075
        self.centre_label.center = (cx, cy)

    # ---------- animation / navigation ----------
    def _transition(self, change, expand=True):
        """Shrink and spin the leaves away, run `change`, then grow new ones."""
        self.busy = True
        out = Animation(progress=0, spin=40, duration=0.22, t="in_cubic")

        def after_out(*_):
            change()
            if not expand:
                return  # leaves stay collapsed while the screen switches
            self.spin = -40
            grow = Animation(progress=1, spin=0, duration=0.45, t="out_back")
            grow.bind(on_complete=lambda *_: setattr(self, "busy", False))
            grow.start(self)

        out.bind(on_complete=after_out)
        out.start(self)

    def _set_path(self, new_path):
        self.path = new_path
        self._sync_prompt()

    def _sync_prompt(self):
        if self.path:
            self.prompt = (f"Feeling {self.path[0].lower()}, which kind? "
                           "(tap the centre to go back)")
        else:
            self.prompt = "Tap the leaf that fits best"

    def choose(self, index):
        name = self.items()[index][0]
        if not self.path:
            self._transition(lambda: self._set_path([name]))
        else:
            core = self.path[0]
            secondary, deeper = FEELINGS[core][1][index]
            self._transition(
                lambda: setattr(self, "result_path", [core, secondary, deeper]),
                expand=False)

    def go_back(self):
        self._transition(lambda: self._set_path([]))

    def reset(self):
        Animation.cancel_all(self)
        self.path = []
        self.result_path = []
        self.progress = 1
        self.spin = 0
        self.busy = False
        self._sync_prompt()

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return super().on_touch_down(touch)
        if self.busy:
            return True
        dx = touch.x - self.center_x
        dy = touch.y - self.center_y
        dist = math.hypot(dx, dy)
        R = self.radius
        if dist <= R * 0.19:
            if self.path:
                self.go_back()
            return True
        if dist <= R:
            angle = math.degrees(math.atan2(dx, dy)) % 360  # clockwise from top
            self.choose(int(angle // (360 / len(self.items()))))
            return True
        return super().on_touch_down(touch)


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        wheel = self.ids.get("wheel")
        if wheel:
            wheel.reset()



class OutputScreen(Screen):
    pass


KV = """
ScreenManager:
    HomeScreen:
    OutputScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(8)

        Label:
            text: "Deep Rooted Guidance!"
            font_size: "32sp"
            bold: True
            size_hint_y: None
            height: dp(90)
            text_size: self.size
            halign: "center"
            valign: "middle"

        Label:
            text: "Let the past unearth your future, how are you feeling?"
            color: 0.81, 0.91, 0.84, 1
            font_size: "16sp"
            size_hint_y: None
            height: dp(56)
            text_size: self.size
            halign: "center"
            valign: "middle"

        EmotionWheel:
            id: wheel
            on_result_path: app.show_result(self.result_path)

        Label:
            text: wheel.prompt
            font_size: "14sp"
            size_hint_y: None
            height: dp(40)
            text_size: self.size
            halign: "center"
            valign: "middle"


<OutputScreen>:
    name: "output"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(16)

        Label:
            text: "You're feeling"
            font_size: "18sp"
        Label:
            text: app.secondary
            font_size: "44sp"
            bold: True
        Label:
            text: "A kind of feeling " + app.core.lower()
            font_size: "18sp"
        Label:
            text: "Deeper down, it might be " + app.deeper.lower()
            font_size: "18sp"
            text_size: self.size
            halign: "center"
            valign: "middle"

        Button:
            text: "Back to the tree"
            size_hint_y: None
            height: dp(56)
            background_normal: ""
            background_color: 0.42, 0.27, 0.14, 1
            on_release: root.manager.current = "home"
"""


class FeelingsApp(App):
    title = "Deep Rooted Guidance"
    core = StringProperty("")
    secondary = StringProperty("")
    deeper = StringProperty("")

    def build(self):
        return Builder.load_string(KV)

    def show_result(self, path):
        if not path:
            return
        self.core, self.secondary, self.deeper = path
        self.root.current = "output"


if __name__ == "__main__":
    FeelingsApp().run()