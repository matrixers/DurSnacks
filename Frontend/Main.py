from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen

KV = """
ScreenManager:
    HomeScreen:
    SettingsScreen:

<HomeScreen>:
    name: "home"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(16)

        Label:
            text: "Hello from Kivy!"
            font_size: "24sp"

        Label:
            text: f"Taps: {app.tap_count}"

        Button:
            text: "Tap me"
            size_hint_y: None
            height: dp(56)
            on_release: app.increment()

        Button:
            text: "Settings"
            size_hint_y: None
            height: dp(56)
            on_release: root.manager.current = "settings"

<SettingsScreen>:
    name: "settings"
    BoxLayout:
        orientation: "vertical"
        padding: dp(24)
        spacing: dp(16)

        Label:
            text: "Settings go here"

        Button:
            text: "Back"
            size_hint_y: None
            height: dp(56)
            on_release: root.manager.current = "home"
"""


class HomeScreen(Screen):
    pass


class SettingsScreen(Screen):
    pass


class MyApp(App):
    title = "My App"
    tap_count = NumericProperty(0)

    def build(self):
        return Builder.load_string(KV)

    def increment(self):
        self.tap_count += 1

    def on_pause(self):
        # Return True so Android keeps the app alive when backgrounded
        return True


if __name__ == "__main__":
    MyApp().run()
