from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import json

PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = PROJECT_DIR / "lakehouse" / "data" / "transactions.jsonl"
DASHBOARD_DIR = Path(__file__).resolve().parent


class DashboardHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def do_GET(self):
        if self.path == "/api/transactions":
            transactions = []

            if DATA_FILE.exists():
                with DATA_FILE.open("r", encoding="utf-8") as file:
                    for line in file:
                        try:
                            transactions.append(json.loads(line))
                        except json.JSONDecodeError:
                            continue

            response = json.dumps(transactions).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
            return

        if self.path == "/":
            self.path = "/index.html"

        super().do_GET()


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8000), DashboardHandler)
    print("IceStream dashboard: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.")
    server.serve_forever()