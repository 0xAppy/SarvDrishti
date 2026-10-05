import random
import time
import datetime
import argparse
import socket
import json
import urllib.request

FIREWALL_LOGS = [
    "SRC=10.10.1.20 DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=DENY VENDOR_FLAG=RULE_101",
    "SRC=192.168.1.15 DST=8.8.8.8 SP=52110 DP=53 PROTO=UDP ACTION=ALLOW VENDOR_FLAG=RULE_02",
    "SRC=10.0.0.50 DST=10.0.0.1 SP=3389 DP=3389 PROTO=TCP ACTION=DENY VENDOR_FLAG=ALERT_RDP"
]

SYSLOG_LOGS = [
    "Aug 26 10:20:15 server01 sshd: Failed password for user admin from 10.10.1.20",
    "Aug 26 10:21:00 server01 sshd: Accepted password for root from 192.168.1.50 port 54321 ssh2",
    "Aug 26 10:22:12 webserver02 kernel: Out of memory: Kill process 1422 (mysqld)"
]

APPLICATION_LOGS = [
    '2026-08-26T10:20:16Z method=POST path=/login user=admin status=401 source_ip=10.10.1.20 duration_ms=45',
    '{"timestamp":"2026-08-26T10:20:17Z", "method":"GET", "path":"/dashboard", "user":"john", "status":200, "source_ip":"192.168.1.50"}',
    '2026-08-26T10:20:18Z method=DELETE path=/api/users user=hacker status=403 source_ip=10.10.1.20'
]

UNKNOWN_LOGS = [
    '[AUDIT] user=john op=DELETE file=secret.doc host=10.0.0.5 timestamp=1724667616 status=FAIL',
    'CUSTOM_SEC_EVENT device=fw_x99 src_ip=10.5.5.1 target=10.5.5.10 severity=CRITICAL detail="Buffer overflow attempt"'
]

def generate_sample_file(filename="sample_historical.log", count=100):
    all_logs = []
    for _ in range(count):
        category = random.choice(["fw", "syslog", "app", "unknown"])
        if category == "fw":
            all_logs.append(random.choice(FIREWALL_LOGS))
        elif category == "syslog":
            all_logs.append(random.choice(SYSLOG_LOGS))
        elif category == "app":
            all_logs.append(random.choice(APPLICATION_LOGS))
        else:
            all_logs.append(random.choice(UNKNOWN_LOGS))
    
    with open(filename, "w") as f:
        f.write("\n".join(all_logs) + "\n")
    print(f"Generated {count} synthetic logs in {filename}")

def send_syslog_udp(host="127.0.0.1", port=5140, count=20):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"Sending {count} Syslog events to UDP {host}:{port}...")
    for _ in range(count):
        log = random.choice(SYSLOG_LOGS)
        sock.sendto(log.encode("utf-8"), (host, port))
        time.sleep(0.05)
    print("Done streaming UDP Syslog logs.")

def send_api_ingest(url="http://localhost:8000/api/events/ingest", count=20):
    print(f"Streaming {count} events to API endpoint {url}...")
    for _ in range(count):
        log = random.choice(FIREWALL_LOGS + APPLICATION_LOGS)
        req = urllib.request.Request(
            url,
            data=json.dumps({"raw_payload": log, "source_id": "script-generator"}).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        try:
            urllib.request.urlopen(req)
        except Exception as e:
            print(f"API send failed: {e}")
        time.sleep(0.05)
    print("Done streaming REST API events.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SarvDrishti Synthetic Log Generator")
    parser.add_argument("--mode", choices=["file", "syslog", "api"], default="file")
    parser.add_argument("--file", default="sample_historical.log")
    parser.add_argument("--count", type=int, default=50)

    args = parser.parse_args()
    if args.mode == "file":
        generate_sample_file(args.file, args.count)
    elif args.mode == "syslog":
        send_syslog_udp(count=args.count)
    elif args.mode == "api":
        send_api_ingest(count=args.count)
