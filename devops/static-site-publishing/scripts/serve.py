#!/usr/bin/env python3
"""Unified HTTP server for static site publishing.
Serves static pages from ROOT on PORT with clean URL support.
Optionally proxies unmatched requests to API_BACKEND.
"""
import http.server
import os
import socketserver
import urllib.request
import urllib.error

# === CONFIGURATION ===
PORT = 8080
ROOT = os.environ.get("STATIC_ROOT", "/opt/data/www")
API_BACKEND = os.environ.get("API_BACKEND", "http://127.0.0.1:8642")
# Set API_BACKEND to empty string to disable proxy fallback


def is_static_path(path: str) -> str | None:
    """Check if path matches a static file. Returns the resolved path or None."""
    if os.path.splitext(path)[1]:
        full = os.path.join(ROOT, path.lstrip("/"))
        if os.path.isfile(full):
            return path
        return None

    html_path = path.rstrip("/") + ".html"
    full = os.path.join(ROOT, html_path.lstrip("/"))
    if os.path.isfile(full):
        return html_path

    index_path = path.rstrip("/") + "/index.html"
    full = os.path.join(ROOT, index_path.lstrip("/"))
    if os.path.isfile(full):
        return index_path

    return None


class UnifiedHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def do_GET(self):
        resolved = is_static_path(self.path)
        if resolved:
            self.path = resolved
            return super().do_GET()
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(404, "Not found")

    def do_POST(self):
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(405, "Method not allowed")

    def do_PUT(self):
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(405, "Method not allowed")

    def do_DELETE(self):
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(405, "Method not allowed")

    def do_PATCH(self):
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(405, "Method not allowed")

    def do_OPTIONS(self):
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_response(200)
            self.end_headers()

    def do_HEAD(self):
        resolved = is_static_path(self.path)
        if resolved:
            self.path = resolved
            return super().do_HEAD()
        if API_BACKEND:
            self._proxy_request()
        else:
            self.send_error(404, "Not found")

    def _proxy_request(self):
        """Forward to API backend and relay the response."""
        url = API_BACKEND + self.path
        body = None
        content_length = self.headers.get("Content-Length")
        if content_length:
            body = self.rfile.read(int(content_length))

        req = urllib.request.Request(
            url,
            data=body,
            headers={k: v for k, v in self.headers.items()
                     if k.lower() not in ("host",)},
            method=self.command,
        )
        req.add_header("X-Forwarded-For", self.client_address[0])
        req.add_header("X-Forwarded-Host", self.headers.get("Host", ""))

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self.send_response(resp.status)
                for key, val in resp.getheaders():
                    if key.lower() not in ("transfer-encoding", "connection"):
                        self.send_header(key, val)
                self.end_headers()
                self.wfile.write(resp.read())
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            for key, val in e.headers.items():
                if key.lower() not in ("transfer-encoding", "connection"):
                    self.send_header(key, val)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_error(502, f"Backend unreachable: {e}")

    def list_directory(self, path):
        """HTML directory listing with clickable links."""
        try:
            entries = sorted(os.listdir(path))
        except OSError:
            self.send_error(404, "No permission to list directory")
            return None

        html_files = [e for e in entries
                      if e.endswith(".html") and os.path.isfile(os.path.join(path, e))]
        dirs = [e + "/" for e in entries
                if os.path.isdir(os.path.join(path, e)) and not e.startswith(".")]

        body = '<!DOCTYPE html><html><head><meta charset="utf-8"><title>Pages</title>'
        body += '<style>body{font-family:-apple-system,sans-serif;background:#0a0a0f;'
        body += 'color:#e4e4ec;max-width:600px;margin:40px auto;padding:20px}'
        body += 'h1{font-size:20px;color:#a78bfa}'
        body += 'a{color:#6c5ce7;text-decoration:none;display:block;padding:8px 12px;'
        body += 'border-radius:8px;margin:4px 0}'
        body += 'a:hover{background:#1a1a2e}'
        body += '.slug{color:#9898b0;font-size:13px;margin-left:8px}'
        body += '</style></head><body>'
        body += '<h1>📄 Pages</h1>'

        if not html_files and not dirs:
            body += '<p style="color:#9898b0">No pages yet.</p>'

        for d in dirs:
            body += f'<a href="{d}">📁 {d[:-1]}</a>'

        for f in html_files:
            slug = f[:-5]
            body += f'<a href="/{slug}">{f}<span class="slug">/{slug}</span></a>'

        body += '</body></html>'
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body.encode())))
        self.end_headers()
        self.wfile.write(body.encode())
        return None


if __name__ == "__main__":
    os.makedirs(ROOT, exist_ok=True)
    print(f"Serving {ROOT}", end="")
    if API_BACKEND:
        print(f" + proxying to {API_BACKEND}", end="")
    print(f" on port {PORT}")
    with socketserver.TCPServer(("0.0.0.0", PORT), UnifiedHandler) as httpd:
        httpd.serve_forever()
