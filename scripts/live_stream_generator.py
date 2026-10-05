import socket
import time
import datetime
import random
import urllib.request
import json
import argparse
import platform
import getpass

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

USENAMES = ["admin", "root", "operator", "john_dev", "sec_auditor", "guest_user"]
PATHS = ["/login", "/dashboard", "/api/v1/users", "/api/v1/auth/token", "/admin/settings", "/checkout"]
ACTIONS = ["ALLOW", "DENY"]
PROTOCOLS = ["TCP", "UDP"]

def start_live_log_stream(target_host="127.0.0.1", delay_seconds=1.5):
    hostname = socket.gethostname()
    local_ip = get_local_ip()
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    api_url = f"http://{target_host}:8000/api/events/ingest"

    print("==================================================================")
    print("      SARVDRISHTI CONTINUOUS REAL-TIME LIVE LOG STREAM GENERATOR    ")
    print("==================================================================")
    print(f" Target Host: {target_host}")
    print(f" UDP Syslog Target: {target_host}:5140")
    print(f" REST API Target:   {api_url}")
    print(f" Event Stream Delay: {delay_seconds} seconds per event")
    print(" Press CTRL+C to stop streaming.")
    print("==================================================================\n")

    counter = 1
    try:
        while True:
            now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()
            now_syslog = datetime.datetime.now().strftime("%b %d %H:%M:%S")
            user = random.choice(USENAMES)
            path = random.choice(PATHS)
            action = random.choice(ACTIONS)
            proto = random.choice(PROTOCOLS)
            src_ip = f"10.10.{random.randint(1, 50)}.{random.randint(2, 250)}"
            dst_ip = f"172.16.{random.randint(1, 20)}.{random.randint(2, 100)}"
            src_port = random.randint(1024, 65000)
            dst_port = random.choice([80, 443, 22, 53, 3389, 8080])

            event_type = random.choice(["syslog", "firewall", "webapp"])

            if event_type == "syslog":
                # Real-time Syslog Auth Event
                msg = f"{now_syslog} {hostname} sshd[{random.randint(1000, 9999)}]: Failed password for user {user} from {src_ip}"
                udp_sock.sendto(msg.encode("utf-8"), (target_host, 5140))
                print(f"[{counter}] [LIVE UDP SYSLOG] -> Sent SSHD Auth Log: user={user} ip={src_ip}")

            elif event_type == "firewall":
                # Real-time Firewall KV Event
                msg = f"SRC={src_ip} DST={dst_ip} SP={src_port} DP={dst_port} PROTO={proto} ACTION={action} VENDOR_TAG=RULE_{random.randint(100, 999)}"
                data = json.dumps({"raw_payload": msg, "source_id": "src-firewall-live"}).encode("utf-8")
                req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
                try:
                    urllib.request.urlopen(req)
                    print(f"[{counter}] [LIVE FIREWALL KV] -> Sent Firewall Log: {src_ip}:{src_port} -> {dst_ip}:{dst_port} [{action}]")
                except Exception as e:
                    print(f"[{counter}] [LIVE FIREWALL KV] -> Ingestion error: {e}")

            else:
                # Real-time Web App Event
                status_code = random.choice([200, 201, 401, 403, 500])
                msg = f"{now_iso} method=POST path={path} user={user} status={status_code} source_ip={src_ip} response_time_ms={random.randint(5, 150)}"
                data = json.dumps({"raw_payload": msg, "source_id": f"src-webapp-live"}).encode("utf-8")
                req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
                try:
                    urllib.request.urlopen(req)
                    print(f"[{counter}] [LIVE WEB APP]     -> Sent HTTP Access Log: POST {path} [{status_code}] user={user}")
                except Exception as e:
                    print(f"[{counter}] [LIVE WEB APP]     -> Ingestion error: {e}")

            counter += 1
            time.sleep(delay_seconds)
    except KeyboardInterrupt:
        print("\n[Stopped] Live real-time log streaming paused.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SarvDrishti Continuous Real-Time Live Log Stream Generator")
    parser.add_argument("--host", default="127.0.0.1", help="Target SarvDrishti IP address (e.g. 127.0.0.1 or 192.168.43.174)")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay in seconds between live events")
    args = parser.parse_args()

    start_live_log_stream(target_host=args.host, delay_seconds=args.delay)
