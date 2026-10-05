import subprocess
import socket
import time
import sys
import argparse

def stream_real_laptop_syslogs_continuous(target_host="127.0.0.1", port=5140):
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("==================================================================")
    print("    CONTINUOUS REAL-TIME MONITOR: YOUR LAPTOP'S ACTUAL SYSLOGS    ")
    print("==================================================================")
    print(f" Target SarvDrishti UDP Listener: {target_host}:{port}")
    print(" Following journalctl live stream... (Press CTRL+C to stop)")
    print("==================================================================\n")

    counter = 1
    try:
        # Run journalctl in follow mode (-f) to tail new real laptop system logs as they happen!
        proc = subprocess.Popen(
            ["journalctl", "-f", "-n", "5", "--no-pager"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        for line in iter(proc.stdout.readline, ""):
            line = line.strip()
            if line and not line.startswith("--"):
                udp_sock.sendto(line.encode("utf-8"), (target_host, port))
                print(f"[{counter}] [REAL LAPTOP LOG] -> {line}")
                counter += 1
                sys.stdout.flush()

    except KeyboardInterrupt:
        print("\n[Stopped] Real-time laptop syslog monitoring paused.")
    finally:
        udp_sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SarvDrishti Real Laptop Syslog Continuous Streamer")
    parser.add_argument("--host", default="127.0.0.1", help="Target SarvDrishti IP address")
    args = parser.parse_args()

    stream_real_laptop_syslogs_continuous(target_host=args.host)
