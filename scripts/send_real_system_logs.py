import socket
import platform
import getpass
import time
import datetime
import urllib.request
import json
import argparse
import random

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def send_real_laptop_syslog(target_host="127.0.0.1", port=5140):
    """Streams realistic security & system events from your machine to SarvDrishti UDP 5140"""
    hostname = socket.gethostname()
    username = getpass.getuser()
    local_ip = get_local_ip()
    os_info = platform.platform()

    now_str = datetime.datetime.now().strftime("%b %d %H:%M:%S")

    security_events = [
        # 1. Firewall Network Events
        f"{now_str} {hostname} kernel: [NETFILTER_DENY] SRC={local_ip} DST=172.16.2.10 SP=4521 DP=443 PROTO=TCP ACTION=DENY VENDOR_FLAG=FW_RULE_101",
        f"{now_str} {hostname} kernel: [NETFILTER_ALLOW] SRC={local_ip} DST=8.8.8.8 SP=54321 DP=53 PROTO=UDP ACTION=ALLOW VENDOR_FLAG=DNS_RULE_02",
        
        # 2. Linux Authentication & Security Events
        f"{now_str} {hostname} sshd[2410]: Failed password for user {username} from {local_ip}",
        f"{now_str} {hostname} sshd[2411]: Failed password for invalid user admin from 10.10.1.50 port 48212",
        f"{now_str} {hostname} sshd[2412]: Accepted password for {username} from {local_ip} port {port} ssh2",
        f"{now_str} {hostname} sudo[3042]: {username} : TTY=pts/0 ; PWD=/home/{username} ; USER=root ; COMMAND=/bin/systemctl restart sarvdrishti",

        # 3. System Health & Kernel Events
        f"{now_str} {hostname} systemd[1]: Started SarvDrishti Enterprise Security Ingestion Engine on OS ({os_info})",
        f"{now_str} {hostname} kernel: [SECURITY_ALERT] Out of memory protection triggered for process mysqld (PID 1422)"
    ]

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"[Syslog UDP] Streaming {len(security_events)} Security Events from ({hostname} - {local_ip}) to {target_host}:{port}...")

    for log in security_events:
        sock.sendto(log.encode("utf-8"), (target_host, port))
        print(f"  -> [UDP Sent]: {log}")
        time.sleep(0.2)
    
    sock.close()

def send_real_webapp_api_logs(target_host="127.0.0.1", api_port=8000):
    """Streams Web & Application Security events to SarvDrishti REST API"""
    hostname = socket.gethostname()
    username = getpass.getuser()
    local_ip = get_local_ip()
    api_url = f"http://{target_host}:{api_port}/api/events/ingest"

    now_iso = datetime.datetime.utcnow().isoformat() + "Z"

    webapp_events = [
        f"{now_iso} method=POST path=/login user={username} status=200 source_ip={local_ip} response_time_ms=18",
        f"{now_iso} method=GET path=/dashboard/stats user={username} status=200 source_ip={local_ip} response_time_ms=5",
        f"{now_iso} method=DELETE path=/api/admin/users user=unknown_attacker status=403 source_ip=10.10.1.99 response_time_ms=42 threat_flag=UNAUTHORIZED_ACCESS",
        f'{{"timestamp":"{now_iso}", "method":"POST", "path":"/api/config", "user":"{username}", "status":201, "source_ip":"{local_ip}", "config_updated":"firewall_rules"}}'
    ]

    print(f"[REST API] Ingesting {len(webapp_events)} Web Security Events to {api_url}...")

    for log in webapp_events:
        data = json.dumps({"raw_payload": log, "source_id": f"src-webapp-{hostname}"}).encode("utf-8")
        req = urllib.request.Request(api_url, data=data, headers={"Content-Type": "application/json"})
        try:
            res = urllib.request.urlopen(req)
            print(f"  -> [API Accepted]: {log[:70]}...")
        except Exception as e:
            print(f"  -> Error sending to API: {e}")
        time.sleep(0.2)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SarvDrishti Real System Security Log Integration Script")
    parser.add_argument("--host", default="127.0.0.1", help="Target IP address of SarvDrishti server (e.g. 192.168.43.174)")
    args = parser.parse_args()

    print("==========================================================")
    print("      SARVDRISHTI REAL SYSTEM & SECURITY EVENT INGESTION       ")
    print("==========================================================")
    send_real_laptop_syslog(target_host=args.host)
    print("----------------------------------------------------------")
    send_real_webapp_api_logs(target_host=args.host)
    print("==========================================================")
    print("Check your dashboard at http://localhost:3000 to view your live events!")
