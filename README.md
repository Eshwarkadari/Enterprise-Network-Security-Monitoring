# 🔐 Enterprise Network Security & Monitoring System

> A complete **Enterprise-grade Network Security and Monitoring System** designed in **Cisco Packet Tracer** with a **Python-based real-time monitoring dashboard** — implementing VLANs, Firewall ACLs, IDS/IPS, VPN tunnels, and live traffic analysis.

![Cisco](https://img.shields.io/badge/Cisco-Packet_Tracer-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![CCNA](https://img.shields.io/badge/CCNA-Networking-1BA0D7?style=for-the-badge&logo=cisco&logoColor=white)
![Security](https://img.shields.io/badge/Network-Security-red?style=for-the-badge&logo=shield&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white)

---

## 📌 Project Overview

This project simulates a **real-world enterprise network** for a multi-department organization with:
- 🏢 **4 Departments**: IT, Finance, HR, Management
- 🔒 **Security layers**: Firewall, ACLs, IDS/IPS, VPN
- 📊 **Live monitoring**: Python dashboard showing traffic, alerts, device status
- 🌐 **Inter-VLAN routing** with Layer 3 switches
- 🛡️ **DMZ zone** for public-facing servers

---

## 🏗️ Network Architecture

```
                    INTERNET
                       |
              [Edge Router/Firewall]
                       |
              [Core Layer-3 Switch]
            /      |        |      \
     [IT VLAN] [Finance] [HR VLAN] [Mgmt VLAN]
      VLAN 10  VLAN 20   VLAN 30   VLAN 40
                       |
                   [DMZ Zone]
               [Web Server] [DNS Server]
```

---

## ✨ Features

### 🔒 Security Features
- **VLAN Segmentation** — 4 isolated department VLANs
- **Extended ACLs** — block unauthorized inter-department traffic
- **Firewall Rules** — stateful packet inspection
- **IDS/IPS Simulation** — detect port scans and brute force
- **VPN Tunnel** — secure remote access
- **DMZ Zone** — isolated public server zone
- **Port Security** — MAC address limiting on switches
- **DHCP Snooping** — prevent rogue DHCP servers
- **Dynamic ARP Inspection** — prevent ARP spoofing

### 📊 Monitoring Features
- **Real-time dashboard** — live device status
- **Traffic analysis** — bandwidth per VLAN
- **Security alerts** — suspicious activity detection
- **Ping monitoring** — device up/down status
- **Port scanner detection** — alert on scan attempts
- **Log viewer** — all network events in one place

---

## 🗂️ Project Structure

```
Enterprise-Network-Security-Monitoring/
│
├── packet-tracer/
│   └── Enterprise_Network_Security_Monitoring.pkt  ← Open in Cisco PT
│
├── python/
│   ├── monitor.py              # Main monitoring dashboard
│   ├── network_scanner.py      # Ping & port scanner
│   ├── ids_simulator.py        # IDS/IPS alert system
│   ├── traffic_analyzer.py     # Traffic stats analyzer
│   └── alert_system.py         # Real-time alert engine
│
├── configs/
│   ├── router_config.txt       # Router IOS commands
│   ├── switch_config.txt       # Switch IOS commands
│   ├── firewall_acl.txt        # All ACL rules
│   └── vlan_config.txt         # VLAN configuration
│
├── docs/
│   ├── network_diagram.md      # Topology explanation
│   ├── security_policy.md      # Security policies applied
│   └── test_results.md         # Ping/ACL test results
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Open in Cisco Packet Tracer
```
1. Install Cisco Packet Tracer (free from netacad.com)
2. Open: packet-tracer/Enterprise_Network_Security_Monitoring.pkt
3. Explore the topology and test connectivity
```

### 2. Run Python Monitoring Dashboard
```bash
git clone https://github.com/Eshwarkadari/Enterprise-Network-Security-Monitoring
cd Enterprise-Network-Security-Monitoring
pip install -r requirements.txt
python python/monitor.py
```
Open **http://localhost:5000** to see the live dashboard!

---

## 🌐 Network Design Details

### VLAN Configuration

| VLAN | Department | Network | Gateway |
|------|-----------|---------|---------|
| VLAN 10 | IT Department | 192.168.10.0/24 | 192.168.10.1 |
| VLAN 20 | Finance | 192.168.20.0/24 | 192.168.20.1 |
| VLAN 30 | HR Department | 192.168.30.0/24 | 192.168.30.1 |
| VLAN 40 | Management | 192.168.40.0/24 | 192.168.40.1 |
| VLAN 50 | DMZ | 192.168.50.0/24 | 192.168.50.1 |

### Device Inventory

| Device | Model | Role | IP |
|--------|-------|------|----|
| Core-Router | Cisco 2911 | Edge routing, NAT, VPN | 203.0.113.1 |
| Core-Switch | Cisco 3560 | L3 switching, Inter-VLAN | 192.168.1.1 |
| IT-Switch | Cisco 2960 | VLAN 10 access | — |
| Finance-Switch | Cisco 2960 | VLAN 20 access | — |
| HR-Switch | Cisco 2960 | VLAN 30 access | — |
| Web-Server | Server | HTTP/HTTPS in DMZ | 192.168.50.10 |
| DNS-Server | Server | DNS resolution | 192.168.50.11 |

---

## 🔒 Security Policies Implemented

### ACL Rules (Firewall)
```
! Block Finance from accessing IT servers
deny ip 192.168.20.0 0.0.0.255 192.168.10.0 0.0.0.255

! Allow Management to access all VLANs
permit ip 192.168.40.0 0.0.0.255 any

! Block all to DMZ except HTTP/HTTPS
permit tcp any 192.168.50.0 0.0.0.255 eq 80
permit tcp any 192.168.50.0 0.0.0.255 eq 443
deny ip any 192.168.50.0 0.0.0.255

! Allow ICMP for monitoring
permit icmp any any
```

### Port Security
```
! Limit MAC addresses per port
switchport port-security maximum 2
switchport port-security violation restrict
switchport port-security
```

---

## 📊 Live Dashboard Screenshots

```
╔══════════════════════════════════════════════════════╗
║     Enterprise Network Security Dashboard            ║
╠══════════════════════════════════════════════════════╣
║  Devices Online: 12/14    Active Alerts: 2           ║
║  Total Traffic: 2.4 GB    Blocked Packets: 147       ║
╠══════════════════════════════════════════════════════╣
║  DEVICE STATUS          │  RECENT ALERTS             ║
║  ─────────────────────  │  ──────────────────────── ║
║  ✅ Core-Router   UP    │  ⚠️  Port scan: 192.168.20.5 ║
║  ✅ Core-Switch   UP    │  🚨 Brute force: SSH port  ║
║  ✅ IT-Switch     UP    │  ⚠️  VLAN hop attempt       ║
║  ✅ Finance-Switch UP   │                            ║
║  ❌ HR-Switch     DOWN  │  TRAFFIC BY VLAN           ║
║  ✅ Web-Server    UP    │  IT:      ████░░  42%      ║
║  ✅ DNS-Server    UP    │  Finance: ███░░░  31%      ║
║                         │  HR:      ██░░░░  18%      ║
║                         │  Mgmt:    █░░░░░   9%      ║
╚══════════════════════════════════════════════════════╝
```

---

## 🧪 Test Cases & Results

| Test | Expected | Result |
|------|---------|--------|
| IT → IT (same VLAN) | ✅ Allow | ✅ Pass |
| Finance → IT | ❌ Block | ✅ Pass |
| Management → any | ✅ Allow | ✅ Pass |
| Any → Web Server (HTTP) | ✅ Allow | ✅ Pass |
| Any → Web Server (SSH) | ❌ Block | ✅ Pass |
| Port scan detection | 🚨 Alert | ✅ Pass |
| Rogue DHCP detection | 🚨 Alert | ✅ Pass |

---

## 🛠️ Technologies Used

| Technology | Purpose |
|-----------|---------|
| Cisco Packet Tracer | Network simulation |
| Cisco IOS | Router/Switch configuration |
| Python + Flask | Monitoring dashboard |
| Scapy | Packet analysis |
| CCNA concepts | Network design principles |

---

## 📚 Concepts Applied

- ✅ OSI Model (Layers 2, 3, 4)
- ✅ VLAN & Trunking (802.1Q)
- ✅ Inter-VLAN Routing
- ✅ ACL (Standard & Extended)
- ✅ NAT/PAT
- ✅ OSPF Routing Protocol
- ✅ DHCP & DNS
- ✅ VPN (Site-to-Site)
- ✅ Network Security Best Practices
- ✅ IDS/IPS concepts

---

## 👨‍💻 Author

**Kadari Eshwar** — B.Tech ECE, JNTU Hyderabad
[GitHub](https://github.com/Eshwarkadari) | [LinkedIn](https://www.linkedin.com/in/eshwar-kadari-134aa4278)

> 💡 This project demonstrates enterprise-level networking skills applicable to roles at Cisco, TCS, Infosys, HCL, and network security companies.
