"""
network_scanner.py — Network Device Scanner
Pings all devices and checks open ports
Author: Kadari Eshwar | B.Tech ECE, JNTU Hyderabad
"""

import subprocess, platform, concurrent.futures
from datetime import datetime

DEVICES = [
    {"name": "Core-Router",    "ip": "192.168.1.254"},
    {"name": "Core-Switch",    "ip": "192.168.1.1"},
    {"name": "IT-Switch",      "ip": "192.168.10.1"},
    {"name": "Finance-Switch", "ip": "192.168.20.1"},
    {"name": "HR-Switch",      "ip": "192.168.30.1"},
    {"name": "Web-Server",     "ip": "192.168.50.10"},
    {"name": "DNS-Server",     "ip": "192.168.50.11"},
]

def ping(ip):
    """Ping a device and return True if reachable."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    cmd   = ["ping", param, "1", "-W", "1", ip]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=3)
        return result.returncode == 0
    except:
        return False

def scan_all():
    """Scan all devices in parallel."""
    print(f"\n🔍 Network Device Scanner")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("━" * 45)

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(ping, d["ip"]): d for d in DEVICES}
        for future, device in futures.items():
            is_up = future.result()
            status = "✅ UP  " if is_up else "❌ DOWN"
            print(f"  {status}  {device['name']:<20} {device['ip']}")
            results.append({**device, "status": "UP" if is_up else "DOWN"})

    online  = sum(1 for r in results if r["status"] == "UP")
    offline = len(results) - online
    print(f"\n📊 Summary: {online} UP | {offline} DOWN")
    return results

if __name__ == "__main__":
    scan_all()
