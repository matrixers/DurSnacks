"""Talks to the backend. The Kivy app only needs to call fetch_guidance()."""
import json

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

API_URL = "http://127.0.0.1:8000/guidance"  # change to your teammate's address
USE_MOCK = False   # True = no server needed, returns placeholder text
TIMEOUT = 10      # seconds


def fetch_guidance(core, secondary, deeper, on_success, on_error):
    """Send the three feelings to the backend.

    on_success(text) is called with the backend's message string.
    on_error(text) is called with a short, user-friendly error message.
    Both callbacks run on Kivy's main thread, so they can update the UI.
    """
    payload = {"core": core, "secondary": secondary, "deeper": deeper}

    if USE_MOCK:
        text = f"(placeholder) {secondary} sits under feeling {core.lower()}."
        Clock.schedule_once(lambda dt: on_success(text), 0.5)
        return

    def success(req, result):
        try:
            on_success(str(result["message"]))
        except (KeyError, TypeError):
            on_error("Unexpected reply from the server")

    def failure(req, result):  # server answered with an HTTP error code
        on_error(f"Server error ({req.resp_status})")

    def error(req, err):  # no connection, timeout, etc.
        on_error("Couldn't reach the server")

    UrlRequest(
        API_URL,
        req_body=json.dumps(payload),  # giving a body makes this a POST
        req_headers={"Content-Type": "application/json"},
        on_success=success,
        on_failure=failure,
        on_error=error,
        timeout=TIMEOUT,
    )