
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
        self._reply(*answer(ask))

    def log_message(self, *args):
        pass


def answer(ask):
    """The reply to one /guidance request: (status code, data)."""
    path = [ask.get(k, "") for k in ("core", "secondary", "deeper") if ask.get(k)]
    if not path:
        return 400, {"error": "core, secondary and deeper are needed"}
    who = (ask.get("who") or "").strip()
    answers = {"event": ask.get("what", ""), "cause": ask.get("why", ""),
               "extra": f"People involved: {who}" if who else ""}
    rewritten = Backend.rewrite(path, answers)
    result = Backend.find(path, answers, sentence=rewritten["sentence"])
    # one entry per quote box {"quote", "name", "years"}: 3, the first a well-known writer, then two lesser known
    quotes = [Backend.simple(r) for r in result["results"]]
    feeling = Backend.sentiment(path)
    # two short pieces of advice from the philosophy books {"quote", "name", "years"}
    guidance = Backend.find_guidance(path, answers, rewritten["sentence"])
    return 200, {"sentiment": feeling, "picture": Backend.picture(feeling),
                 "quotes": quotes, "guidance": guidance, "no_match": result["no_match"],
                 "message": Backend.as_text(result), "poem": rewritten["poem"],
                 "results": result["results"]}


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
