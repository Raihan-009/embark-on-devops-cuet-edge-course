# DNS Resolution Hands-on Lab

## Introduction
Domain Name System (DNS) is a critical component of the internet, translating human-readable domain names into IP addresses. This lab will guide you through various aspects of DNS resolution in Linux systems, helping you understand how DNS works at a practical level.

## Objectives
By the end of this lab, you will:
1. Understand the role of key configuration files in DNS resolution
2. Learn how to use command-line tools to query DNS servers
3. Set up a simple local DNS server
4. Observe DNS caching in action

## Prerequisites
- A Linux system (Ubuntu or similar distribution)
- Basic command-line knowledge
- Root or sudo access

## 1. Examining /etc/hosts

The `/etc/hosts` file is used for local DNS resolution.

```bash
# View the contents of /etc/hosts
cat /etc/hosts

# Add an entry to /etc/hosts
sudo echo "192.168.1.100 myserver.local" >> /etc/hosts

# Test the new entry
ping myserver.local
```

## 2. Checking /etc/resolv.conf

The `/etc/resolv.conf` file specifies DNS resolver information.

```bash
# View the contents of /etc/resolv.conf
cat /etc/resolv.conf

# You should see something like:
# nameserver 8.8.8.8
# nameserver 8.8.4.4
```

## 3. Understanding /etc/nsswitch.conf

The `/etc/nsswitch.conf` file determines the order of name resolution methods.

```bash
# View the hosts line in nsswitch.conf
grep hosts /etc/nsswitch.conf

# You might see:
# hosts: files dns
# This means the system checks /etc/hosts before querying DNS
```

## 4. Using dig to query DNS servers

The `dig` command is a powerful tool for DNS queries.

```bash
# Query for google.com
dig google.com

# Query a specific DNS server
dig @8.8.8.8 google.com

# Query for NS records to find authoritative nameservers
dig NS google.com

# Trace the DNS resolution process
dig +trace google.com
```

## 5. Simulating a local DNS server

We can use `dnsmasq` to set up a simple local DNS server.

```bash
# Install dnsmasq (if not already installed)
sudo apt-get install dnsmasq

# Configure dnsmasq
echo "address=/example.local/127.0.0.1" | sudo tee -a /etc/dnsmasq.conf

# Restart dnsmasq
sudo systemctl restart dnsmasq

# Test the local DNS server
dig @127.0.0.1 example.local
```

## 6. Observing DNS caching

```bash
# Clear the DNS cache (method varies by distribution)
sudo systemd-resolve --flush-caches

# Query a domain and note the query time
dig google.com | grep "Query time"

# Query again and compare the query time
dig google.com | grep "Query time"
# The second query should be faster due to caching
```

## Conclusion
This lab has provided hands-on experience with various aspects of DNS resolution in Linux systems. You've explored key configuration files, used DNS query tools, set up a local DNS server, and observed DNS caching in action. These skills will be valuable for network troubleshooting and understanding internet infrastructure.
