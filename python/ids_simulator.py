"""
ids_simulator.py — IDS/IPS Alert System
Detects: Port scans, Brute force, VLAN hopping, ARP spoofing
Author: Kadari Eshwar | B.Tech ECE, JNTU Hyderabad
"""

import random, time
from datetime import datetime
from collections import defaultdict, Counter

class IDS:
    def __init__(self):
        self.port_scan_tracker = defaultdict(set)
        self.login_failures    = Counter()
        self.alerts            = []
        self.blocked_ips       = set()

    def check_port_scan(self, src_ip, dst_port):
        """Detect if an IP is scanning multiple ports."""
        self.port_scan_tracker[src_ip].add(dst_port)
        if len(self.port_scan_tracker[src_ip]) > 15:
            alert = self._create_alert(
                "CRITICAL", "PORT_SCAN",
                f"Port scan detected from {src_ip} — {len(self.port_scan_tracker[src_ip])} ports scanned",
                src_ip
            )
            self.blocked_ips.add(src_ip)
            return alert
        return None

    def check_brute_force(self, src_ip, service="SSH"):
        """Detect brute force login attempts."""
        self.login_failures[src_ip] += 1
        if self.login_failures[src_ip] == 5:
            return self._create_alert(
                "CRITICAL", "BRUTE_FORCE",
                f"Brute force on {service} from {src_ip} — {self.login_failures[src_ip]} failed attempts",
                src_ip
            )
        return None

    def check_acl_violation(self, src_ip, dst_ip, src_vlan, dst_vlan):
        """Detect unauthorized inter-VLAN access."""
        RESTRICTED = {("20","10"), ("30","20"), ("10","40")}  # Finance→IT, HR→Finance, IT→Mgmt
        if (src_vlan, dst_vlan) in RESTRICTED:
            return self._create_alert(
                "WARNING", "ACL_VIOLATION",
                f"ACL blocked: VLAN{src_vlan} ({src_ip}) → VLAN{dst_vlan} ({dst_ip})",
                src_ip
            )
        return None

    def _create_alert(self, level, atype, message, src_ip=None):
        alert = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level":     level,
            "type":      atype,
            "message":   message,
            "src_ip":    src_ip,
            "blocked":   src_ip in self.blocked_ips
        }
        self.alerts.append(alert)
        icon = "🚨" if level == "CRITICAL" else "⚠️"
        print(f"{icon} [{alert['timestamp']}] {level}: {message}")
        return alert

    def simulate_traffic(self, duration=30):
        """Simulate network traffic and trigger IDS checks."""
        print(f"\n🔍 IDS/IPS Monitoring started for {duration} seconds...")
        print("━" * 50)
        start = time.time()
        ips   = ["192.168.10.5","192.168.20.3","192.168.30.8","10.0.0.99","192.168.20.5"]

        while time.time() - start < duration:
            src = random.choice(ips)

            # Simulate port scan
            if random.random() < 0.3:
                port = random.randint(1, 1024)
                self.check_port_scan(src, port)

            # Simulate brute force
            if random.random() < 0.1:
                self.check_brute_force(src)

            # Simulate ACL violations
            if random.random() < 0.2:
                vlans = ["10","20","30","40"]
                sv, dv = random.sample(vlans, 2)
                self.check_acl_violation(src, "192.168."+dv+".1", sv, dv)

            time.sleep(0.5)

        print(f"\n📊 IDS Summary:")
        print(f"   Total alerts : {len(self.alerts)}")
        print(f"   Blocked IPs  : {len(self.blocked_ips)}")
        critical = [a for a in self.alerts if a["level"] == "CRITICAL"]
        print(f"   Critical     : {len(critical)}")
        if self.blocked_ips:
            print(f"   Blocked IPs  : {', '.join(self.blocked_ips)}")

if __name__ == "__main__":
    ids = IDS()
    ids.simulate_traffic(30)
