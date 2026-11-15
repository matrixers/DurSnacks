"""Talks to the backend. The Kivy app only needs to call fetch_guidance()."""
import json

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest

API_URL = "http://127.0.0.1:8090/guidance"  # the Node server (server.js), which asks the Python backend
USE_MOCK = False   # True = no server needed, returns placeholder text
TIMEOUT = 120     # seconds (a search takes about 30)


def fetch_guidance(core, secondary, deeper, on_success, on_error, what="", why="", who=""):
    """Send the three feelings and the What / Why / Who boxes to the backend.

    on_success(reply) is called with the backend's whole reply (a dict), mainly
        reply["quotes"]: [{"quote", "name", "years"}, ...]  (3, one per quote box)
        reply["picture"]: {"imageURL", "title", "artist", "year", "link"} or None
        (example: Backend/example_output.json)
    on_error(text) is called with a short, user-friendly error message.
    Both callbacks run on Kivy's main thread, so they can update the UI.
    """
    payload = {"core": core, "secondary": secondary, "deeper": deeper,
               "what": what, "why": why, "who": who}

    if USE_MOCK:
        reply = {"quotes": [{"quote": f"(placeholder)\n{secondary} sits under\nfeeling {core.lower()}.",
                             "name": "Nobody yet", "years": "2026"}], "picture": None}
        Clock.schedule_once(lambda dt: on_success(reply), 0.5)
        return

    def success(req, result):
        if isinstance(result, dict) and isinstance(result.get("quotes"), list):
            on_success(result)
        else:
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