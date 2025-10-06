# Simple Hydra Demo (no WSL required)

This package contains a self-contained demo for demonstrating a brute-force attack and detection
without needing Hydra or WSL. You can optionally use Hydra if you have it on Windows, but a
pure-Python attacker is included so the demo runs on any Windows machine with Python 3.

## Files
- `index.html` - simple login page
- `login_server.py` - small HTTP server (Python) that serves the page and logs failed logins to `failed_logins.log`
- `passwords.txt` - sample password list (includes the correct password `S3curePass!`)
- `attacker.py` - Python script that posts passwords from `passwords.txt` to the login form
- `monitor.py` - tails `failed_logins.log` and simulates banning IPs after repeated failures
- `README.md` - this file

## Quick demo steps (Windows)
1. Open a command prompt / PowerShell and change to this folder.
2. Start the server:
   ```
   python login_server.py
   ```
3. Open a second terminal in the same folder and start the monitor:
   ```
   python monitor.py
   ```
4. In a third terminal, run the attacker (no Hydra required):
   ```
   python -m pip install requests
   python attacker.py
   ```
5. Watch the monitor terminal — after several failed attempts you should see:
   ```
   *** ALERT: Suspected brute-force from 127.0.0.1. Adding to banned list.
   ```
6. For a faster demo, put the correct password (`S3curePass!`) at the top of `passwords.txt`.

## Optional: Using Hydra (if you have a Windows build)
If `hydra` is available on your PATH, you can run:
```
hydra -l admin -P passwords.txt 127.0.0.1 http-post-form "/login:username=^USER^&password=^PASS^:Invalid credentials" -V
```

## Notes
- Only run in a local/lab environment. Do not attack external systems.
- The monitor simulates banning by writing `banned_ips.txt`. It does not change firewall rules.
