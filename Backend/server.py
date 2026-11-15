"""
A small web server so the app (its client.py) can ask the backend for passages.

    python -m Backend.server          starts on http://127.0.0.1:8000 (loads the library first, ~1 min)

    GET  /           {"status": "ok"}  (quick check that it is running)
    POST /guidance   {"core": "Sad", "secondary": "Lonely", "deeper": "Isolated",
                      "what": "...", "why": "...", "who": "..."}        (what / why / who are optional)
                  -> {"message": "the passages as text", "poem": "...", "results": [...]}

The API key stays here on the server; the app never sees it.
"""
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from Backend import Backend

PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _reply(self, status, data):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        self._reply(200, {"status": "ok"})

    def do_POST(self):
        if self.path != "/guidance":
            return self._reply(404, {"error": "unknown address"})
        try:
            ask = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"{}")
        except json.JSONDecodeError:
            return self._reply(400, {"error": "the request is not JSON"})
        path = [ask.get(k, "") for k in ("core", "secondary", "deeper") if ask.get(k)]
        if not path:
            return self._reply(400, {"error": "core, secondary and deeper are needed"})
        who = (ask.get("who") or "").strip()
        answers = {"event": ask.get("what", ""), "cause": ask.get("why", ""),
                   "extra": f"People involved: {who}" if who else ""}
        rewritten = Backend.rewrite(path, answers)
        result = Backend.find(path, answers, sentence=rewritten["sentence"])
        self._reply(200, {"message": Backend.as_text(result), "poem": rewritten["poem"],
                          "results": result["results"]})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    ThreadingHTTPServer.allow_reuse_address = False      # on Windows it would let two servers share the port
    try:
        server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    except OSError:
        sys.exit(f"Port {PORT} is already in use: the backend is probably already running in another window.")
    print("Loading the library (about a minute)...", flush=True)
    Backend.library()
    print(f"Ready on http://127.0.0.1:{PORT}  (Ctrl+C to stop)", flush=True)
    server.serve_forever()
