---


# 📡 iOS & External Device Support: Local DNS and Root Certificate Trust Setup

This guide explains how to configure `dnsmasq` to redirect local test domains (e.g., `finaltest1.inapp.test`) to your Apache webserver on Ubuntu. It also covers how to trust the custom root certificate on an iPhone for HTTPS testing.

This setup is essential if you're testing from **physical mobile devices**, such as iPhones, rather than an Android emulator (which does not require `dnsmasq`).

---

## ✅ When to Use This Setup

- You are testing HTTPS-based test domains like:
```

[https://finaltest1.inapp.test](https://finaltest1.inapp.test)
[https://finaltest2.inapp.test](https://finaltest2.inapp.test)

````
- You want these domains to resolve to your **local webserver** on an iPhone or external Android device.
- Your server is running `apache2` and uses self-signed certificates signed by a custom root CA.

---

## ✅ 1. Run the `setup-dnsmasq.sh` Script (Ubuntu)

This script does the following:

- Installs `dnsmasq`
- Enables it as a DNS service
- Scans your existing Apache test site configurations (`finaltest*.conf`) under `webserver-setup/apache-configs/`
- Extracts the domain names and maps them to your local IP (e.g., `192.168.0.10`) in `dnsmasq`
- Restarts the service

### 📜 Usage

```bash
sudo bash setup-dnsmasq.sh
````

> 📝 Make sure to edit `LOCAL_IP="192.168.0.10"` inside the script to reflect your Ubuntu server’s actual IP address.

---

## ✅ 2. Set Ubuntu Server as DNS on iPhone

You can configure DNS per-device or at the router level.

### Option A: Router-Wide DNS

* Login to your router settings.
* Locate DNS settings.
* Set **Primary DNS Server** to your Ubuntu machine’s local IP (e.g., `192.168.0.10`).
* Save and restart router if needed.

### Option B: iPhone DNS Only

1. Go to `Settings → Wi-Fi → (your network)`
2. Tap `Configure DNS → Manual`
3. Delete all existing DNS entries
4. Add your Ubuntu server’s IP (e.g., `192.168.0.10`)

---

## ✅ 3. Install and Trust Root Certificate on iPhone

### 3.1 Export Certificate for iOS

Assuming your root certificate is `testRootCa.crt`:

```bash
openssl x509 -in testRootCa.crt -outform der -out testRootCa.der
sudo cp testRootCa.der /var/www/html/
```

Access from Safari on iPhone:

```
http://192.168.0.10/testRootCa.der
```

### 3.2 Install and Trust

1. Open the URL in Safari
2. Tap "Allow" to download profile
3. Go to `Settings → General → VPN & Device Management`
4. Tap the profile and install
5. Then go to `Settings → General → About → Certificate Trust Settings`
6. Enable full trust for your installed root certificate

✅ Now your iPhone trusts the custom root CA.

---

## ✅ 4. Test Connection

On iPhone Safari or in-app browser:

```
https://finaltest1.inapp.test
```

You should see your Apache-hosted test page (like `index.html`) with **no certificate warning**.

---

## ✅ 5. Notes

* ❗ iOS uses system-level certificate validation. Trust must be manually enabled under “Certificate Trust Settings.”
* ⚠️ If the test page fails to load:

  * Check DNS resolution using a tool like `ping finaltest1.inapp.test` from another device.
  * Make sure Apache is serving the domain on port 443 with the correct SSL config.
  * Restart `dnsmasq` and check `/etc/dnsmasq.d/inapp-test.conf` for correctness.

---

## 🧪 Emulator Users (Android Only)

> If you are testing only inside Android **emulators**, you do **not** need to configure `dnsmasq` or your router. Use `/etc/hosts` or AVD-side overrides.

---

\
