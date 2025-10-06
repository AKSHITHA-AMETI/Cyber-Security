# monitor.py - tails failed_logins.log and simulates banning IPs by writing banned_ips.txt
import time
import re
from collections import defaultdict

LOGFILE = "failed_logins.log"
THRESHOLD = 5

banned = set()
fail_count = defaultdict(int)

ip_pattern = re.compile(r"FAILED_LOGIN from (\S+)")

def tail(f):
    f.seek(0, 2)
    while True:
        line = f.readline()
        if not line:
            time.sleep(0.5)
            continue
        yield line

def load_existing_bans():
    try:
        with open("banned_ips.txt", "r") as bf:
            for l in bf:
                banned.add(l.strip())
    except FileNotFoundError:
        pass

def save_ban(ip):
    with open("banned_ips.txt", "a") as bf:
        bf.write(ip + "\n")

def main():
    load_existing_bans()
    print("Starting monitor. Current bans:", banned)
    try:
        with open(LOGFILE, "r") as lf:
            for line in tail(lf):
                m = ip_pattern.search(line)
                if m:
                    ip = m.group(1)
                    if ip in banned:
                        print(f"[{time.ctime()}] Ignoring activity from already banned {ip}")
                        continue
                    fail_count[ip] += 1
                    print(f"[{time.ctime()}] Detected failed login from {ip} (count={fail_count[ip]})")
                    if fail_count[ip] >= THRESHOLD:
                        print(f"*** ALERT: Suspected brute-force from {ip}. Adding to banned list.")
                        banned.add(ip)
                        save_ban(ip)
    except FileNotFoundError:
        print(f'Log file {LOGFILE} not found yet; monitor will wait until it appears.')
        while True:
            time.sleep(1)

if __name__ == "__main__":
    main()
