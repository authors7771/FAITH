#!/bin/bash

# Usage:
#   chmod +x setup-dnsmasq.sh
#   sudo ./setup-dnsmasq.sh
#
# Description:
#   This script sets up local DNS resolution for inapp.test domains using dnsmasq.
#   It is intended for use on a physical local network, such as when testing with
#   real mobile devices.
#
#   ❗ On Android emulators, this script is NOT necessary.
#      Emulators typically use /etc/hosts via systemd-resolved, and bypass dnsmasq.
#
#   What this script does:
#     1. Installs dnsmasq
#     2. Disables systemd-resolved
#     3. Sets /etc/resolv.conf to use 127.0.0.1
#     4. Adds inapp.test domains to /etc/hosts mapped to a local Apache IP
#     5. Configures dnsmasq and restarts it

LOCAL_IP="192.168.0.123"  # <- Change this to your local Apache server IP

echo "[*] Installing dnsmasq..."
sudo apt update
sudo apt install -y dnsmasq

echo "[*] Disabling systemd-resolved..."
sudo systemctl disable systemd-resolved --now
sudo rm -f /etc/resolv.conf
echo "nameserver 127.0.0.1" | sudo tee /etc/resolv.conf

echo "[*] Creating dnsmasq configuration for inapp.test domains..."
sudo tee /etc/dnsmasq.d/inapp.conf > /dev/null <<EOF
# Configuration for inapp.test domains
domain-needed
bogus-priv
no-resolv
listen-address=127.0.0.1
EOF

echo "[*] Mapping inapp.test domains to $LOCAL_IP in /etc/hosts..."
for i in {1..129}; do
    DOMAIN="finaltest${i}.inapp.test"
    if ! grep -q "$DOMAIN" /etc/hosts; then
        echo "$LOCAL_IP $DOMAIN" | sudo tee -a /etc/hosts > /dev/null
    fi
done
echo "[+] Domain mappings added to /etc/hosts."

echo "[*] Restarting dnsmasq..."
sudo systemctl restart dnsmasq
sudo systemctl enable dnsmasq

echo "[✔] dnsmasq setup complete."
echo "Try: ping finaltest5.inapp.test"
