from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs
from datetime import datetime
import logging

correct_username = "admin"
correct_password = "S3curePass!"

# configure simple logger to file
logger = logging.getLogger("failed_logins")
logger.setLevel(logging.INFO)
fh = logging.FileHandler("failed_logins.log")
formatter = logging.Formatter("%(asctime)s | %(message)s")
fh.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(fh)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                with open("index.html", "rb") as f:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(f.read())
            except Exception as e:
                self.send_error(500, "Server error")
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == "/login":
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode()
            data = parse_qs(body)
            user = data.get("username", [""])[0]
            pwd = data.get("password", [""])[0]
            client_ip = self.client_address[0] if self.client_address else "unknown"
            if user == correct_username and pwd == correct_password:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Login Successful")
            else:
                # log failed attempt
                logger.info(f"FAILED_LOGIN from {client_ip} username={user}")
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"Invalid credentials")
        else:
            self.send_error(404)

    def log_message(self, format, *args):
        # suppress default console logging to keep output clean
        return

if __name__ == "__main__":
    httpd = HTTPServer(("0.0.0.0", 5000), Handler)
    print("Server running on http://0.0.0.0:5000")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        httpd.server_close()
