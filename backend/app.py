"""HA-3: minimal HealthTracker backend API (standard library only).

Endpoints
  GET  /health        -> {"status": "ok"}
  GET  /api/entries   -> list of stored health entries
  POST /api/entries   -> store a health entry (JSON body)
"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

ENTRIES = []
REQUIRED = {"date"}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, {"status": "ok"})
        elif self.path == "/api/entries":
            self._send(200, ENTRIES)
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        if self.path != "/api/entries":
            return self._send(404, {"error": "not found"})
        length = int(self.headers.get("Content-Length", 0))
        try:
            data = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._send(400, {"error": "invalid JSON"})
        if not REQUIRED.issubset(data):
            return self._send(400, {"error": "missing field: date"})
        ENTRIES.append(data)
        self._send(201, data)


if __name__ == "__main__":
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
