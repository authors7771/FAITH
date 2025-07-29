#!/bin/bash

set -e

echo "[*] Installing Apache2 and Python3..."
sudo apt update
sudo apt install -y apache2 python3

echo "[*] Enabling Apache modules..."
sudo a2enmod ssl
sudo a2enmod rewrite

echo "[*] Preparing base directories..."
sudo mkdir -p /etc/apache2/ssl
sudo mkdir -p /var/www

echo "[*] Creating base index.html for domain_copy.py..."
sudo mkdir -p /var/www/finaltest0.inapp.test/public_html
sudo tee /var/www/finaltest0.inapp.test/public_html/index.html > /dev/null <<EOF
<!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Test Page</title>
  </head>
  <body>
    <h1>Success to access test0.inapp.test</h1>
  </body>
</html>
EOF

echo "[*] Running cert_copy.py to deploy certificates..."
cd scripts
sudo python3 cert_copy.py

echo "[*] Running auto_conf.py to generate Apache conf files..."
python3 auto_conf.py

echo "[*] Running domain_copy.py to deploy index.html for all domains..."
sudo python3 domain_copy.py

echo "[*] Copying and enabling Apache site configurations..."
cd ..
CONF_DIR="./scripts"
for conf in $(ls $CONF_DIR/finaltest*.conf); do
    CONF_NAME=$(basename "$conf")
    sudo cp "$conf" /etc/apache2/sites-available/"$CONF_NAME"
    sudo a2ensite "$CONF_NAME"
done

echo "[*] Allowing HTTP and HTTPS ports in firewall..."
sudo ufw allow 80
sudo ufw allow 443

echo "[*] Restarting Apache..."
sudo systemctl restart apache2

echo "[+] Apache web server setup complete!"
