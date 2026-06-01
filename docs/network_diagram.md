# Network Topology Diagram

## Enterprise Network Architecture

```
                        INTERNET
                           |
                    [203.0.113.1]
                    [Core Router]  ← Cisco 2911
                    [203.0.113.1]
                    NAT | ACL | VPN
                           |
                    [192.168.1.254]
                    [Core Switch]  ← Cisco 3560 (L3)
                    [192.168.1.1]
          __________|___________|____________
         |           |          |            |
    [VLAN 10]   [VLAN 20]  [VLAN 30]   [VLAN 40]
    IT Dept     Finance     HR Dept    Management
  192.168.10.x 192.168.20.x 192.168.30.x 192.168.40.x
  [IT-Switch] [Fin-Switch] [HR-Switch]
  Cisco 2960  Cisco 2960   Cisco 2960
      |           |            |
   IT PCs    Finance PCs    HR PCs

                    [DMZ - VLAN 50]
                   192.168.50.0/24
              [Web Server] [DNS Server]
              192.168.50.10 192.168.50.11
```

## Security Zones

| Zone | VLAN | Network | Security Level |
|------|------|---------|---------------|
| IT Department | 10 | 192.168.10.0/24 | High |
| Finance | 20 | 192.168.20.0/24 | Highest |
| HR Department | 30 | 192.168.30.0/24 | Medium |
| Management | 40 | 192.168.40.0/24 | Admin |
| DMZ | 50 | 192.168.50.0/24 | Public |

## Traffic Flow Rules

```
IT ←→ IT          : ALLOW (same VLAN)
Finance ←→ Finance : ALLOW (same VLAN)
Finance → IT      : DENY  (ACL rule)
HR → Finance      : DENY  (ACL rule)
Management → ANY  : ALLOW (admin access)
ANY → DMZ HTTP    : ALLOW (public web)
ANY → DMZ SSH     : DENY  (security)
WAN → Internal    : DENY  (firewall)
```
