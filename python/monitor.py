"""
monitor.py — Enterprise Network Security Dashboard
Real-time monitoring of network devices, traffic and alerts
Author: Kadari Eshwar | B.Tech ECE, JNTU Hyderabad
Run: python monitor.py → http://localhost:5000
"""

from flask import Flask, render_template_string, jsonify
import threading, time, random, subprocess, platform
from datetime import datetime
from collections import deque

app = Flask(__name__)

# ── Network Devices ────────────────────────────────────────────────────────
DEVICES = [
    {"name": "Core-Router",    "ip": "192.168.1.254", "role": "Router",   "vlan": "ALL"},
    {"name": "Core-Switch",    "ip": "192.168.1.1",   "role": "L3 Switch","vlan": "ALL"},
    {"name": "IT-Switch",      "ip": "192.168.10.1",  "role": "Switch",   "vlan": "10"},
    {"name": "Finance-Switch", "ip": "192.168.20.1",  "role": "Switch",   "vlan": "20"},
    {"name": "HR-Switch",      "ip": "192.168.30.1",  "role": "Switch",   "vlan": "30"},
    {"name": "Web-Server",     "ip": "192.168.50.10", "role": "Server",   "vlan": "DMZ"},
    {"name": "DNS-Server",     "ip": "192.168.50.11", "role": "Server",   "vlan": "DMZ"},
    {"name": "IT-PC-01",       "ip": "192.168.10.10", "role": "PC",       "vlan": "10"},
    {"name": "Finance-PC-01",  "ip": "192.168.20.10", "role": "PC",       "vlan": "20"},
    {"name": "HR-PC-01",       "ip": "192.168.30.10", "role": "PC",       "vlan": "30"},
    {"name": "Mgmt-PC-01",     "ip": "192.168.40.10", "role": "PC",       "vlan": "40"},
]

# ── Simulated State ────────────────────────────────────────────────────────
device_status  = {d["name"]: random.choice(["UP","UP","UP","DOWN"]) for d in DEVICES}
traffic_data   = {"IT":0,"Finance":0,"HR":0,"Management":0,"DMZ":0}
alerts         = deque(maxlen=20)
blocked_pkts   = [0]
total_traffic  = [0]

ALERT_TYPES = [
    ("⚠️", "WARNING",  "Port scan detected from 192.168.20.5"),
    ("🚨", "CRITICAL", "Brute force attempt on SSH (port 22)"),
    ("⚠️", "WARNING",  "VLAN hopping attempt detected"),
    ("🚨", "CRITICAL", "Unauthorized access to Finance VLAN"),
    ("⚠️", "WARNING",  "ARP spoofing attempt blocked"),
    ("ℹ️", "INFO",     "ACL blocked: Finance→IT traffic"),
    ("⚠️", "WARNING",  "Unusual traffic spike on VLAN 20"),
    ("🚨", "CRITICAL", "Multiple failed login attempts on Core-Router"),
    ("ℹ️", "INFO",     "Port security violation on IT-Switch Fa0/5"),
    ("⚠️", "WARNING",  "DNS query flood detected"),
]

def simulate():
    """Background simulation of network activity."""
    while True:
        # Update traffic
        for vlan in traffic_data:
            traffic_data[vlan] += random.randint(10, 500)
        total_traffic[0] += random.randint(100, 2000)
        blocked_pkts[0]  += random.randint(0, 5)

        # Random device flaps
        for d in DEVICES:
            if random.random() < 0.02:  # 2% chance of status change
                device_status[d["name"]] = "DOWN" if device_status[d["name"]] == "UP" else "UP"

        # Random alerts
        if random.random() < 0.15:
            icon, level, msg = random.choice(ALERT_TYPES)
            alerts.appendleft({
                "time":  datetime.now().strftime("%H:%M:%S"),
                "icon":  icon,
                "level": level,
                "msg":   msg,
            })

        time.sleep(4)

@app.route("/")
def dashboard():
    return render_template_string(HTML)

@app.route("/api/status")
def status():
    online  = sum(1 for v in device_status.values() if v == "UP")
    offline = len(device_status) - online
    alert_count = sum(1 for a in alerts if a["level"] == "CRITICAL")

    devices = []
    for d in DEVICES:
        devices.append({**d, "status": device_status[d["name"]]})

    total_mb = round(total_traffic[0] / 1024, 1)
    max_t    = max(traffic_data.values()) or 1

    return jsonify({
        "online":        online,
        "offline":       offline,
        "alert_count":   alert_count,
        "blocked":       blocked_pkts[0],
        "total_traffic": f"{total_mb} MB",
        "devices":       devices,
        "alerts":        list(alerts)[:8],
        "traffic": [
            {"vlan": k, "bytes": v, "pct": round(v/max_t*100)}
            for k, v in traffic_data.items()
        ],
    })

HTML = """<!DOCTYPE html>
<html><head>
<meta charset="UTF-8"><meta http-equiv="refresh" content="5">
<title>Enterprise Network Security Dashboard</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',sans-serif;background:#0a0e1a;color:#e2e8f0}
nav{background:#0d1117;padding:14px 28px;display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #1ba0d7}
.logo{font-size:16px;font-weight:700;color:#1ba0d7}
.badge{background:#1ba0d722;color:#1ba0d7;border:1px solid #1ba0d7;padding:3px 10px;border-radius:20px;font-size:11px}
.main{padding:20px 28px;max-width:1400px;margin:0 auto}
h2{margin-bottom:16px;font-size:18px;color:#f1f5f9}
.kpis{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin-bottom:20px}
.kpi{background:#0d1117;border-radius:10px;padding:16px;border:1px solid #1e2a3a;text-align:center}
.kpi .label{font-size:11px;color:#64748b;text-transform:uppercase;letter-spacing:.5px}
.kpi .val{font-size:26px;font-weight:700;margin:6px 0}
.online{color:#4ade80}.offline{color:#ef4444}.alert-c{color:#f59e0b}.blocked{color:#818cf8}.traffic{color:#38bdf8}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:14px}
.grid3{display:grid;grid-template-columns:2fr 1fr;gap:14px;margin-bottom:14px}
.card{background:#0d1117;border-radius:10px;padding:18px;border:1px solid #1e2a3a}
.card h3{font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:.5px;margin-bottom:12px;border-bottom:1px solid #1e2a3a;padding-bottom:8px}
.device{display:flex;align-items:center;justify-content:space-between;padding:7px 0;border-bottom:1px solid #0a0e1a;font-size:13px}
.dot{width:8px;height:8px;border-radius:50%;margin-right:8px;display:inline-block}
.dot-up{background:#4ade80}.dot-down{background:#ef4444}
.up{color:#4ade80}.down{color:#ef4444}
.vlan-tag{background:#1e2a3a;padding:2px 6px;border-radius:4px;font-size:10px;color:#94a3b8}
.alert-row{display:flex;gap:10px;padding:7px 0;border-bottom:1px solid #0a0e1a;font-size:12px;align-items:center}
.alert-time{color:#475569;width:55px;flex-shrink:0}
.alert-msg{color:#e2e8f0}
.CRITICAL .alert-msg{color:#fca5a5}
.WARNING  .alert-msg{color:#fde68a}
.INFO     .alert-msg{color:#94a3b8}
.bar-row{display:flex;align-items:center;gap:8px;margin-bottom:10px;font-size:13px}
.bar-label{width:90px;color:#94a3b8}
.bar-bg{flex:1;background:#0a0e1a;border-radius:4px;height:16px}
.bar-fill{height:16px;border-radius:4px;background:linear-gradient(90deg,#1ba0d7,#38bdf8)}
.bar-val{width:60px;color:#e2e8f0;font-size:12px;text-align:right}
footer{text-align:center;padding:12px;color:#475569;font-size:12px;margin-top:8px;border-top:1px solid #1e2a3a}
</style></head>
<body>
<nav>
  <div class="logo">🔐 Enterprise Network Security & Monitoring Dashboard</div>
  <div class="badge">● LIVE — auto refresh 5s</div>
</nav>
<div class="main">
  <h2>📊 Real-time Network Overview</h2>
  <div class="kpis">
    <div class="kpi"><div class="label">Devices Online</div><div class="val online" id="online">—</div></div>
    <div class="kpi"><div class="label">Devices Offline</div><div class="val offline" id="offline">—</div></div>
    <div class="kpi"><div class="label">Active Alerts</div><div class="val alert-c" id="alerts">—</div></div>
    <div class="kpi"><div class="label">Blocked Packets</div><div class="val blocked" id="blocked">—</div></div>
    <div class="kpi"><div class="label">Total Traffic</div><div class="val traffic" id="traffic">—</div></div>
  </div>
  <div class="grid3">
    <div class="card"><h3>🖥️ Device Status</h3><div id="devices"></div></div>
    <div class="card"><h3>🚨 Security Alerts</h3><div id="alert-list"></div></div>
  </div>
  <div class="card"><h3>📊 Traffic by VLAN (bytes transferred)</h3><div id="traffic-bars"></div></div>
  <p style="color:#475569;font-size:12px;margin-top:14px;text-align:center">
    Built by <b style="color:#94a3b8">Kadari Eshwar</b> — B.Tech ECE, JNTU Hyderabad
    &nbsp;|&nbsp; Cisco Packet Tracer + Python &nbsp;|&nbsp; CCNA Concepts Applied
  </p>
</div>
<footer>API: /api/status &nbsp;|&nbsp; Network: 192.168.0.0/16 &nbsp;|&nbsp; VLANs: 10,20,30,40,50</footer>
<script>
fetch('/api/status').then(r=>r.json()).then(d=>{
  document.getElementById('online').textContent  = d.online;
  document.getElementById('offline').textContent = d.offline;
  document.getElementById('alerts').textContent  = d.alert_count;
  document.getElementById('blocked').textContent = d.blocked.toLocaleString();
  document.getElementById('traffic').textContent = d.total_traffic;

  document.getElementById('devices').innerHTML = d.devices.map(dv=>
    '<div class="device">'
    +'<span><span class="dot dot-'+dv.status.toLowerCase()+'"></span>'+dv.name+'</span>'
    +'<span><span class="vlan-tag">VLAN '+dv.vlan+'</span> '
    +'<span class="'+dv.status.toLowerCase()+'">'+dv.status+'</span></span></div>'
  ).join('');

  document.getElementById('alert-list').innerHTML = d.alerts.map(a=>
    '<div class="alert-row '+a.level+'">'
    +'<span class="alert-time">'+a.time+'</span>'
    +'<span>'+a.icon+'</span>'
    +'<span class="alert-msg">'+a.msg+'</span></div>'
  ).join('') || '<div style="color:#475569;font-size:13px;padding:10px">No alerts — network is secure ✅</div>';

  const maxP = Math.max(...d.traffic.map(t=>t.bytes)) || 1;
  document.getElementById('traffic-bars').innerHTML = d.traffic.map(t=>
    '<div class="bar-row">'
    +'<div class="bar-label">VLAN '+t.vlan+'</div>'
    +'<div class="bar-bg"><div class="bar-fill" style="width:'+t.pct+'%"></div></div>'
    +'<div class="bar-val">'+t.bytes.toLocaleString()+'B</div></div>'
  ).join('');
});
</script></body></html>"""

if __name__ == "__main__":
    threading.Thread(target=simulate, daemon=True).start()
    print("\n🔐 Enterprise Network Security Dashboard")
    print("━" * 45)
    print("✅ Simulation started!")
    print("🌐 Dashboard: http://localhost:5000")
    print("   Auto-refreshes every 5 seconds")
    print("\nMonitoring:")
    for d in DEVICES:
        print(f"  {'✅' if device_status[d['name']] == 'UP' else '❌'} {d['name']} ({d['ip']})")
    print("\n   Press Ctrl+C to stop")
    app.run(host="0.0.0.0", port=5000, debug=False)
