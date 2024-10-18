# DHCP Lab: Understanding Dynamic IP Address Assignment

## Introduction
This lab is designed to provide hands-on experience with Dynamic Host Configuration Protocol (DHCP) in a controlled environment. DHCP is a network management protocol used to dynamically assign an IP address to any device, or node, on a network so it can communicate using IP. This lab will demonstrate the process of setting up a DHCP server and observing how clients receive IP addresses dynamically.

## Objectives
1. Set up a DHCP server on an Ubuntu virtual machine
2. Configure a DHCP client and observe the IP assignment process
3. Understand and view DHCP leases, MAC address tables, and routing tables
4. Gain practical experience in DHCP troubleshooting

## Lab Setup

### VM1 (DHCP Server - 10.62.4.83)

1. Install DHCP server:
   ```
   sudo apt update
   sudo apt install isc-dhcp-server
   ```
   Explanation: This installs the ISC DHCP server, a widely used DHCP server implementation.

2. Configure DHCP server:
   ```
   sudo nano /etc/dhcp/dhcpd.conf
   ```
   Add this configuration:
   ```
   subnet 10.62.4.0 netmask 255.255.255.0 {
     range 10.62.4.100 10.62.4.200;
     option routers 10.62.4.1;
     option domain-name-servers 8.8.8.8, 8.8.4.4;
   }
   ```
   Explanation: This configuration defines the subnet, IP range for assignment, default gateway, and DNS servers for DHCP clients.

3. Start DHCP server:
   ```
   sudo systemctl restart isc-dhcp-server
   ```
   Explanation: This command starts the DHCP server with the new configuration.

4. View DHCP leases:
   ```
   cat /var/lib/dhcp/dhcpd.leases
   ```
   Explanation: This file contains information about all active DHCP leases.

5. View MAC address table:
   ```
   arp -e
   ```
   Explanation: This shows the ARP cache, mapping IP addresses to MAC addresses.

6. View routing table:
   ```
   ip route
   ```
   Explanation: This displays the routing table, showing how network traffic is directed.

### VM2 (DHCP Client - 10.62.4.84)

1. Release current IP and request new one:
   ```
   sudo dhclient -r eth0
   sudo dhclient -v eth0
   ```
   Explanation: This releases the current IP and requests a new one, demonstrating the DHCP process.

2. View current IP configuration:
   ```
   ip addr show eth0
   ```
   Explanation: This shows the current IP configuration for the eth0 interface.

3. View MAC address table:
   ```
   arp -e
   ```

4. View routing table:
   ```
   ip route
   ```

## Monitoring DHCP Process

On VM1 (DHCP server):
```
sudo journalctl -u isc-dhcp-server -f
```
Explanation: This command shows real-time logs of the DHCP server, useful for observing DHCP transactions.

On VM2 (DHCP client):
```
sudo dhclient -v eth0
```
Explanation: This shows the verbose output of the DHCP client process, including DISCOVER, OFFER, REQUEST, and ACK messages.

## Troubleshooting

If the client doesn't receive a new IP:

1. Verify DHCP server status:
   ```
   sudo systemctl status isc-dhcp-server
   ```
   Explanation: This checks if the DHCP server is running correctly.

2. Check DHCP server configuration:
   ```
   sudo cat /etc/dhcp/dhcpd.conf
   ```
   Explanation: This allows you to review the DHCP server configuration for errors.

3. Ensure no IP conflicts:
   ```
   sudo nmap -sn 10.62.4.0/24
   ```
   Explanation: This scans the network for active IP addresses, helping to identify any conflicts.

## Conclusion
This lab provides practical experience in setting up and managing a DHCP server, as well as observing the DHCP process from the client side. By completing this lab, you'll gain a deeper understanding of how IP addresses are dynamically assigned in networks, and how to troubleshoot common DHCP issues.
