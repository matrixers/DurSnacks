from kivy.config import Config

# Phone-shaped window (desktop only; ignored on a real phone)
Config.set("graphics", "width", "600")
Config.set("graphics", "height", "1000")
Config.set("graphics", "resizable", False)

import math
import json
import os

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Mesh
from kivy.lang import Builder
from kivy.properties import (BooleanProperty, ColorProperty, ListProperty,
                             NumericProperty, StringProperty)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex
from client import fetch_guidance

from doodle import DoodleBox


Window.clearcolor = get_color_from_hex("#12271D")  # dark forest green

TRUNK = get_color_from_hex("#6B4423")
TRUNK_DARK = get_color_from_hex("#3E2713")
GROUND = get_color_from_hex("#2F5A3F")
BARK = get_color_from_hex("#3A2A1C")   # guidance boxes
GOLD = get_color_from_hex("#D9B45B")

# Tree proportions, as fractions of the canopy radius R
TRUNK_LEN = 0.40    # visible trunk between the canopy and the ground
ROOT_DEPTH = 0.25   # how far the roots reach below the ground

# API Variables --- Emile
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # the paintings are in data/
backend_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             "backend_output.json")
#inspirationImage

# Core feeling -> (colour, [(secondary feeling, deeper feeling), ...])
# Order is clockwise, taken from the feelings wheel image.
FEELINGS = {
    "Mad": ("#DB4B52", [
        ("Hurt", "Distant"), ("Hostile", "Sarcastic"), ("Angry", "Frustrated"),
        ("Selfish", "Jealous"), ("Hateful", "Irritated"), ("Critical", "Skeptical")]),
    "Scared": ("#E99048", [
        ("Confused", "Bewildered"), ("Rejected", "Discouraged"),
        ("Helpless", "Insignificant"), ("Submissive", "Inadequate"),
        ("Insecure", "Embarrassed"), ("Anxious", "Overwhelmed")]),
    "Joyful": ("#D3CC52", [
        ("Excited", "Daring"), ("Sensuous", "Fascinating"),
        ("Energetic", "Stimulating"), ("Cheerful", "Amused"),
        ("Creative", "Playful"), ("Hopeful", "Optimistic")]),
    "Sad": ("#E26AC6", [
        ("Tired", "Sleepy"), ("Bored", "Apathetic"), ("Lonely", "Isolated"),
        ("Depressed", "Inferior"), ("Ashamed", "Stupid"),
        ("Guilty", "Remorseful")]),
    "Peaceful": ("#6984DD", [
        ("Nurturing", "Thankful"), ("Trusting", "Secure"), ("Loving", "Serene"),
        ("Intimate", "Responsive"), ("Thoughtful", "Pensive"),
        ("Content", "Relaxed")]),
    "Powerful": ("#9AE478", [
        ("Aware", "Surprised"), ("Proud", "Successful"),
        ("Respected", "Worthwhile"), ("Appreciated", "Valuable"),
        ("Important", "Discerning"), ("Faithful", "Confident")]),
}


def lighten(c, amount):
    return (c[0] + (1 - c[0]) * amount, c[1] + (1 - c[1]) * amount,
            c[2] + (1 - c[2]) * amount, c[3])


def darken(c, factor):
    return (c[0] * factor, c[1] * factor, c[2] * factor, c[3])


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
    def metrics(self):
        """Return (cx, cy, R, ground_y): canopy centre, radius and ground level."""
        total = 2 + TRUNK_LEN + ROOT_DEPTH  # whole tree height, in units of R
        R = min(self.width / 2 * 0.95, self.height / total * 0.97)
        bottom = self.y + (self.height - total * R) / 2
        ground_y = bottom + ROOT_DEPTH * R
        cy = ground_y + (TRUNK_LEN + 1) * R
        return self.center_x, cy, R, ground_y

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

    def _cloud_centre(self, i, cx, cy, R, scale):
        """(x, y, size) of cloud i: cloud 0 in the middle, the other five around it."""
        if i == 5:
            return cx, cy, R * 0.4 * scale
        ang = math.radians((i + 1) * 72 + self.spin)  # 72 degrees apart, clockwise from the top
        dist = R * 0.5 * scale
        return cx + math.sin(ang) * dist, cy + math.cos(ang) * dist, R * 0.45 * scale

    def _back_button(self, cx, cy, R):
        """Position and size of the knot on the trunk that takes you back."""
        return cx, cy - R * 1.0, R * 0.12

    def _draw_leaf(self, i, cx, cy, R, rgba, scale):
        """Draws cloud number i as a cluster of overlapping circles."""
        if scale < 0.02:
            return
        x, y, size = self._cloud_centre(i, cx, cy, R, scale)
        # (sideways, up, radius), in units of the cloud's size
        puffs = [(0.0, 0.10, 0.55), (0.0, -0.15, 0.45),
                 (-0.45, -0.05, 0.42), (0.45, -0.05, 0.42),
                 (-0.25, 0.30, 0.38), (0.25, 0.30, 0.38)]
        circles = [(x + px * size, y + py * size, pr * size)
                   for px, py, pr in puffs]

        # Darker outline pass first, then the fills on top
        Color(*darken(rgba, 0.6))
        for qx, qy, r in circles:
            Ellipse(pos=(qx - r - 2, qy - r - 2), size=(2 * r + 4, 2 * r + 4))
        Color(*rgba)
        for qx, qy, r in circles:
            Ellipse(pos=(qx - r, qy - r), size=(2 * r, 2 * r))

    def _strip(self, points, half_widths, rgba):
        """Draw a tapered ribbon along a centre line."""
        verts = []
        n = len(points)
        for i, (x, y) in enumerate(points):
            x0, y0 = points[max(i - 1, 0)]
            x1, y1 = points[min(i + 1, n - 1)]
            tx, ty = x1 - x0, y1 - y0
            length = math.hypot(tx, ty) or 1
            nx, ny = -ty / length, tx / length
            h = half_widths[i]
            verts += [x + nx * h, y + ny * h, 0, 0,
                      x - nx * h, y - ny * h, 0, 0]
        Color(*rgba)
        Mesh(vertices=verts, indices=list(range(n * 2)), mode="triangle_strip")

    def _draw_trunk(self, cx, cy, R, ground_y):
        steps = 16
        pts, widths = [], []
        for k in range(steps + 1):
            t = k / steps
            pts.append((cx, cy + (ground_y - cy) * t))
            # slim at the top, flaring out where it meets the roots
            widths.append(R * (0.06 + 0.03 * t + 0.14 * t ** 4))
        self._strip(pts, widths, TRUNK)

        Color(*TRUNK_DARK)
        # outline on each side
        for side in (-1, 1):
            Line(points=[c for (x, y), w in zip(pts, widths)
                         for c in (x + side * w, y)], width=1.6)
        # a few wobbly bark lines
        for frac in (-0.5, 0.0, 0.5):
            line = []
            for k in range(4, steps):
                x, y = pts[k]
                wobble = math.sin(k * 0.9 + frac * 5) * R * 0.004
                line += [x + frac * widths[k] * 0.9 + wobble, y]
            Line(points=line, width=1.1)

    def _draw_roots(self, cx, R, ground_y):
        # (sideways reach, depth) for each root, as fractions of R
        roots = [(-0.55, 0.10), (-0.30, 0.20), (-0.05, 0.25),
                 (0.22, 0.19), (0.50, 0.11)]
        for reach, depth in roots:
            p0 = (cx + reach * R * 0.25, ground_y + R * 0.03)
            p1 = (cx + reach * R * 0.85, ground_y - depth * R * 0.1)
            p2 = (cx + reach * R, ground_y - depth * R)
            pts, widths = [], []
            for k in range(13):
                t = k / 12
                a, b, c = (1 - t) ** 2, 2 * (1 - t) * t, t * t
                pts.append((a * p0[0] + b * p1[0] + c * p2[0],
                            a * p0[1] + b * p1[1] + c * p2[1]))
                widths.append(R * (0.05 * (1 - t) + 0.008))  # taper to a point
            self._strip(pts, widths, TRUNK)

    def redraw(self, *args):
        cx, cy, R, ground_y = self.metrics()
        items = self.items()
        step = 360 / len(items)
        scale = max(self.progress, 0)

        self.canvas.before.clear()
        with self.canvas.before:
            self._draw_roots(cx, R, ground_y)
            self._draw_trunk(cx, cy, R, ground_y)
            # leaves
            for i, (_, colour) in enumerate(items):
                self._draw_leaf(i, cx, cy, R, colour, scale)
            # knot on the trunk (tap to go back)
            bx, by, knot = self._back_button(cx, cy, R)
            Color(*TRUNK)
            Ellipse(pos=(bx - knot, by - knot), size=(2 * knot, 2 * knot))
            Color(*TRUNK_DARK)
            Line(circle=(bx, by, knot), width=2)

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
            lbl.color = (1, 1, 1, 1)
            lbl.opacity = opacity
            lbl.center = self._cloud_centre(i, cx, cy, R, scale)[:2]


        back_text = "Back" if self.path else ""
        if self.centre_label.text != back_text:
            self.centre_label.text = back_text
        if abs(self.centre_label.font_size - R * 0.075) > 0.5:
            self.centre_label.font_size = R * 0.075
        self.centre_label.center = self._back_button(cx, cy, R)[:2]
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
            self.prompt = (f"Feeling {self.path[0].lower()}, what kind?")
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
        cx, cy, R, _ = self.metrics()
        bx, by, br = self._back_button(cx, cy, R)
        if self.path and math.hypot(touch.x - bx, touch.y - by) <= br * 1.5:
            self.go_back()
            return True
        for i in range(len(self.items())):
            x, y, size = self._cloud_centre(i, cx, cy, R, 1)
            if math.hypot(touch.x - x, touch.y - y) <= size:
                self.choose(i)
                return True
        return super().on_touch_down(touch)


class HomeScreen(Screen):
    def on_pre_enter(self, *args):
        # On startup this fires before the wheel exists, so check first
        wheel = self.ids.get("wheel")
        if wheel:
            wheel.reset()


class OutputScreen(Screen):
    pass

class WriteOut(Screen):
    pass

class InspoPage(Screen):
    pass


class LoadingSpinner(Widget):
    """A green arc that turns round a ring while the backend is searching (its look is in the KV below)."""
    angle = NumericProperty(0)
    active = BooleanProperty(False)
    _tick = None

    def on_active(self, *_):
        if self.active and self._tick is None:
            self._tick = Clock.schedule_interval(self._turn, 1 / 60)
        elif not self.active and self._tick is not None:
            self._tick.cancel()
            self._tick = None

    def _turn(self, dt):
        self.angle = (self.angle + 300 * dt) % 360


class QuoteBox(BoxLayout):
    """One quote from the backend (its look is in the KV below)."""
    quote = StringProperty("")
    author = StringProperty("")
    accent = ColorProperty((1, 1, 1, 1))          # stripe and name: the colour of the picked feeling
    fill = ColorProperty((0.11, 0.24, 0.17, 1))   # box: a lighter green than the background


KV = """
ScreenManager:
    HomeScreen:
    OutputScreen:
    WriteOut:
    InspoPage:


<Owl@Widget>:
    size_hint: None, None
    size: dp(64), dp(64)
    canvas:
        # body
        Color:
            rgba: 0.55, 0.37, 0.24, 1
        Ellipse:
            pos: self.x + self.width * 0.12, self.y + self.height * 0.02
            size: self.width * 0.76, self.height * 0.84
        # ear tufts
        Triangle:
            points: [self.x + self.width * 0.15, self.y + self.height * 0.70, self.x + self.width * 0.20, self.y + self.height * 0.98, self.x + self.width * 0.42, self.y + self.height * 0.80]
        Triangle:
            points: [self.x + self.width * 0.85, self.y + self.height * 0.70, self.x + self.width * 0.80, self.y + self.height * 0.98, self.x + self.width * 0.58, self.y + self.height * 0.80]
        # belly
        Color:
            rgba: 0.85, 0.72, 0.55, 1
        Ellipse:
            pos: self.x + self.width * 0.27, self.y + self.height * 0.06
            size: self.width * 0.46, self.height * 0.46
        # eyes
        Color:
            rgba: 1, 1, 1, 1
        Ellipse:
            pos: self.x + self.width * 0.18, self.y + self.height * 0.50
            size: self.width * 0.30, self.height * 0.30
        Ellipse:
            pos: self.x + self.width * 0.52, self.y + self.height * 0.50
            size: self.width * 0.30, self.height * 0.30
        # pupils
        Color:
            rgba: 0.1, 0.1, 0.1, 1
        Ellipse:
            pos: self.x + self.width * 0.27, self.y + self.height * 0.58
            size: self.width * 0.13, self.height * 0.13
        Ellipse:
            pos: self.x + self.width * 0.60, self.y + self.height * 0.58
            size: self.width * 0.13, self.height * 0.13
        # beak
        Color:
            rgba: 0.95, 0.65, 0.15, 1
        Triangle:
            points: [self.x + self.width * 0.44, self.y + self.height * 0.50, self.x + self.width * 0.56, self.y + self.height * 0.50, self.x + self.width * 0.50, self.y + self.height * 0.36]

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(8)

        Label:
            text: "Deep Rooted Guidance"
            font_size: "55sp"
            font_name: "Assets/ChanceryLaneBold.ttf"
            bold: True
            size_hint_y: None
            height: dp(80)
            text_size: self.size
            halign: "center"
            valign: "middle"

        Label:
            text: "A new world isn't always tomorrow. Explore your thoughts with yesterday's wisdom"
            color: 0.81, 0.91, 0.84, 1
            font_size: "20sp"
            font_name: "Assets/Butler-Free-Med.otf"
            size_hint_y: None
            height: dp(60)
            padding: dp(12), dp(8)
            text_size: self.size
            halign: "center"
            valign: "middle"
            canvas.before:
                Color:
                    rgba: 0.18, 0.35, 0.25, 0.9
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(14)]
                Color:
                    rgba: 0.55, 0.75, 0.6, 1
                Line:
                    rounded_rectangle: (self.x, self.y, self.width, self.height, dp(14))
                    width: 1.2

        EmotionWheel:
            id: wheel
            on_result_path: app.show_result(self.result_path)

        Owl:
            pos_hint: {"right": 0.98, "y": 0.03}

        Label:
            text: wheel.prompt
            font_size: "14sp"
            size_hint_y: None
            height: dp(30)
            text_size: self.size
            halign: "center"
            valign: "middle" 

<OutputScreen>:
    name: "output"
    AnchorLayout:
        anchor_y: "top"
        BoxLayout:
            orientation: "vertical"
            padding: dp(24)
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "You're feeling"
                font_size: "18sp"
                size_hint_y: None
                height: self.texture_size[1] + dp(8)
            Label:
                text: app.secondary
                font_size: "44sp"
                bold: True
                size_hint_y: None
                height: self.texture_size[1] + dp(8)
            Label:
                text: "Branching from the emotion: " + (app.core).lower()
                font_size: "18sp"
                size_hint_y: None
                height: self.texture_size[1] + dp(8)
            Label:
                text: "Deeper down, you might be " + (app.deeper).lower()
                font_size: "18sp"
                size_hint_y: None
                height: self.texture_size[1] + dp(8)  

            # --- Inputs sent to API --- Emile            
            TextInput:
                id: Who
                hint_text: "Who was involved?"
                multiline: True
                size_hint_y: None
                height: dp(100)
                background_color: 1, 1, 1, 0.95
                foreground_color: 0.1, 0.1, 0.1, 1
                padding: dp(30)
            TextInput:
                id: What
                hint_text: "What happened?"
                multiline: True
                size_hint_y: None
                height: dp(100)
                background_color: 1, 1, 1, 0.95
                foreground_color: 0.1, 0.1, 0.1, 1
                padding: dp(30)
            TextInput:
                id: Why
                hint_text: "Why do you feel this way?"
                multiline: True
                size_hint_y: None
                height: dp(100)
                background_color: 1, 1, 1, 0.95
                foreground_color: 0.1, 0.1, 0.1, 1
                padding: dp(30)

            Button:
                text: "Let's dig deeper..."
                size_hint_y: None
                height: dp(56)
                background_normal: ""
                background_color: 0.42, 0.27, 0.14, 1
                on_release: app.dig_deeper(Who.text, What.text, Why.text)

# One quote from the backend: a rounded box with a stripe in the feeling's colour,
# the words as poem lines, and the writer underneath, set further in and to the right.
<QuoteBox>:
    orientation: "vertical"
    size_hint_y: None
    height: self.minimum_height
    padding: dp(20), dp(12), dp(14), dp(10)
    spacing: dp(6)
    canvas.before:
        Color:
            rgba: self.fill
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        Color:
            rgba: self.accent
        RoundedRectangle:
            pos: self.x, self.y + dp(8)
            size: dp(4), self.height - dp(16)
            radius: [dp(2)]
    Label:
        text: "“" + root.quote + "”"
        italic: True
        font_size: "15sp"
        line_height: 1.1
        color: 0.95, 0.96, 0.92, 1
        text_size: self.width, None
        halign: "left"
        size_hint_y: None
        height: self.texture_size[1]
    Label:
        text: root.author
        font_size: "12sp"
        bold: True
        color: root.accent
        padding: dp(40), 0, 0, 0
        text_size: self.width, None
        halign: "right"
        size_hint_y: None
        height: self.texture_size[1]

<LoadingSpinner>:
    canvas:
        Color:
            rgba: 0.18, 0.35, 0.25, 1
        Line:
            circle: (self.center_x, self.center_y, min(self.width, self.height) * 0.35)
            width: dp(3)
        Color:
            rgba: 0.60, 0.85, 0.55, 1
        Line:
            circle: (self.center_x, self.center_y, min(self.width, self.height) * 0.35, self.angle, self.angle + 100)
            width: dp(3)
            cap: "round"

<InspoPage>:
    name: "inspo"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20), dp(20), dp(20), dp(16)
        spacing: dp(12)
        ScrollView:
            do_scroll_x: False
            bar_width: dp(4)
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(14)
                Label:
                    text: "Others have felt this too"
                    font_size: "24sp"
                    bold: True
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4)
                Label:
                    text: "Use their words to help lead your tree of thought"
                    font_size: "15sp"
                    color: 0.81, 0.91, 0.84, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(6)
                # --- loading animation while the backend searches --- Emile
                LoadingSpinner:
                    active: app.loading
                    size_hint: None, None
                    size: dp(72), (dp(72) if app.loading else 0)
                    pos_hint: {"center_x": 0.5}
                    opacity: 1 if app.loading else 0
                # --- API output: "Searching..." or an error --- Emile
                Label:
                    text: app.inspirationText
                    font_size: "16sp"
                    color: 0.81, 0.91, 0.84, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8) if self.text else 0
                    opacity: 1 if self.text else 0
                # --- API output: the 3 quote boxes go here (filled in show_guidance) --- Emile
                BoxLayout:
                    id: quote_list
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)
                # --- the painting for the feeling (from the backend) ---
                Image:
                    source: app.picture_path
                    fit_mode: "contain"
                    size_hint_y: None
                    height: dp(360) if app.picture_path else 0
                    opacity: 1 if app.picture_path else 0
                # the painting's title (from the backend's picture JSON), then who painted it and when
                Label:
                    text: app.picture_title
                    font_size: "17sp"
                    italic: True
                    bold: True
                    color: 0.95, 0.96, 0.92, 1
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(2) if self.text else 0
                Label:
                    text: app.picture_caption
                    font_size: "13sp"
                    color: 0.81, 0.91, 0.84, 0.85
                    text_size: self.width, None
                    halign: "center"
                    size_hint_y: None
                    height: self.texture_size[1] + dp(8) if self.text else 0
                # --- API output: 2 pieces of advice from the philosophy books --- Emile
                Label:
                    text: "Words to guide you" if app.has_guidance else ""
                    font_size: "20sp"
                    bold: True
                    size_hint_y: None
                    height: self.texture_size[1] + dp(4) if self.text else 0
                BoxLayout:
                    id: guidance_list
                    orientation: "vertical"
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)

                # only shown once the quotes have loaded (or the search has failed)
                Button:
                    text: "Let's write about it..."
                    size_hint_y: None
                    height: dp(56) if not app.loading else 0
                    opacity: 1 if not app.loading else 0
                    disabled: app.loading
                    background_normal: ""
                    background_color: 0.42, 0.27, 0.14, 1
                    on_release: root.manager.current = "write"

       


<WriteOut>:
    name: "write"
    AnchorLayout:
        anchor_y: "top"
        BoxLayout:
            orientation: "vertical"
            padding: dp(24)
            spacing: dp(16)

            TextInput:
                id: notes
                hint_text: "Let's write it out..."
                multiline: True
                size_hint_y: None
                height: dp(300)
                background_color: 1, 1, 1, 0.95
                foreground_color: 0.1, 0.1, 0.1, 1
                padding: dp(50)   
            Label:
                text: "Or draw out your feelings..."
                font_size: "20sp"

            DoodleBox:
                id: doodle
                size_hint_y: None
                height: dp(300)
            Button:
                text: "Plant the thoughts"
                size_hint_y: None
                height: dp(56)
                background_normal: ""
                background_color: 0.42, 0.27, 0.14, 1
                on_release: root.manager.current = "home"               
            Button:
                text: "Back"
                size_hint_y: None
                height: dp(56)
                background_normal: ""
                background_color: 0.42, 0.27, 0.14, 1
                on_release: root.manager.current = "inspo"
                

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

    inspirationText = StringProperty("")
    picture_path = StringProperty("")
    picture_title = StringProperty("")
    picture_caption = StringProperty("")
    has_guidance = BooleanProperty(False)
    loading = BooleanProperty(False)     # True while the backend searches: spinner on, button hidden

    def dig_deeper(self, who, what, why):
        """'Let's dig deeper...': send the feelings and the three boxes to the backend."""
        self.show_guidance({"quotes": []})
        self.loading = True
        self.inspirationText = "Exploring archives, please wait"
        self.root.current = "inspo"
        fetch_guidance(self.core, self.secondary, self.deeper,
                       on_success=self.show_guidance, on_error=self.set_backend_text,
                       what=what, why=why, who=who)

    def show_guidance(self, reply):
        """Entry point for the backend's reply: one QuoteBox per quote, then the painting."""
        self.loading = False
        page = self.root.get_screen("inspo")
        page.ids.quote_list.clear_widgets()
        page.ids.guidance_list.clear_widgets()
        accent = get_color_from_hex(FEELINGS.get(self.core, ("#CFE8D6",))[0])
        for q in reply.get("quotes", []):
            page.ids.quote_list.add_widget(QuoteBox(quote=q["quote"], accent=accent,
                                                    author=f"— {q['name']}  ({q['years']})"))
        # advice from the philosophy books: warm brown boxes with a gold stripe, set apart from the letters
        for q in reply.get("guidance", []):
            page.ids.guidance_list.add_widget(QuoteBox(quote=q["quote"], accent=GOLD, fill=BARK,
                                                       author=f"— {q['name']}  ({q['years']})"))
        self.has_guidance = bool(reply.get("guidance"))
        self.inspirationText = "" if reply.get("quotes") else (reply.get("message") or "")
        picture = reply.get("picture")
        path = os.path.join(PROJECT_DIR, picture["imageURL"]) if picture else ""
        self.picture_path = path if os.path.exists(path) else ""
        self.picture_title = picture["title"] if self.picture_path else ""
        self.picture_caption = f"{picture['artist']}, {picture['year']}" if self.picture_path else ""

    def set_backend_text(self, text):
        """Entry point for the backend: sets the text shown on the inspiration screen."""
        # Clock makes this safe to call from another thread
        def show(dt):
            self.loading = False          # an error ends the search too: stop the spinner, show the button
            self.inspirationText = str(text)
        Clock.schedule_once(show, 0)

    def load_backend_json(self, path=backend_JSON):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            self.set_backend_text(data.get("message", ""))
        except (FileNotFoundError, json.JSONDecodeError):
            self.set_backend_text("Waiting for the backend...")


if __name__ == "__main__":
    FeelingsApp().run()