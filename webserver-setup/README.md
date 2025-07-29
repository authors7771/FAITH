좋습니다. 아래는 **webserver-setup**에 대한 `README.md` 초안입니다. 위의 `Android AVD Rooting` 가이드와 유사한 형식으로 작성했으며, 구성 요소 및 동작 원리를 자세히 기술했습니다.

---

```markdown
# Web Server Setup for Certificate Validation Tests

This directory contains scripts and configurations to deploy an Apache2 web server for testing TLS certificate validation behaviors in mobile browsers and in-app WebView environments.

Test domains are dynamically generated and served using wildcard certificates under `.inapp.test`. Each test case resides in a separate directory under `tests/`.

---

## ✅ Directory Structure

```

webserver-setup/
├── apache-configs/         # Generated Apache virtual host configurations
├── scripts/
│   ├── auto\_conf.py        # Generates Apache conf files from test certs
│   ├── cert\_copy.py        # Copies certificate chains to Apache's SSL dir
│   ├── domain\_copy.py      # Copies index.html files for each test domain
│   └── setup\_apache.sh     # Full Apache2 install and configuration script
├── tests/
│   ├── test1/
│   ├── test2/
│   └── ...

````

---

## ✅ 1. Requirements

- Ubuntu 22.04+
- Root privileges (for Apache and cert file placement)
- Python 3
- Apache2

---

## ✅ 2. Usage

### Step 1: Install and Configure Apache

```bash
cd webserver-setup/scripts
sudo bash setup_apache.sh
````

This will:

* Install Apache2 with SSL support
* Enable necessary modules (`ssl`, `rewrite`, `headers`)
* Copy test certificates to `/etc/apache2/ssl/finaltest*/`
* Generate Apache virtual hosts (both HTTP and HTTPS)
* Create corresponding web roots at `/var/www/finaltest*.inapp.test/public_html/`

### Step 2: Customize Test Domains

To configure a specific range of test domains (e.g., test1, test3, test5):

* Edit `auto_conf.py` to set your desired `add_conf_list` range.
* Run it to generate updated `finaltest*.conf`.

Then move the generated `.conf` file into Apache:

```bash
sudo cp finaltest2.conf /etc/apache2/sites-available/
sudo a2ensite finaltest2.conf
sudo systemctl reload apache2
```

---

## ✅ 3. DNS Setup (for physical devices)

> **Note**: Android Emulator users can skip this section and rely on `/etc/hosts`.

To resolve test domains like `finaltest1.inapp.test` to your Apache server:

1. Install and configure `dnsmasq`:

```bash
sudo apt install dnsmasq
```

2. Use the `setup_dnsmasq.sh` script (see separate guide) to:

   * Disable `systemd-resolved`
   * Point `.inapp.test` domains to local IP
   * Restart the DNS service

Alternatively, add static entries in `/etc/hosts`:

```bash
192.168.0.XX finaltest1.inapp.test finaltest2.inapp.test ...
```

---

## ✅ 4. Customizing index.html

The script `domain_copy.py` automatically creates:

```
/var/www/finaltest1.inapp.test/public_html/index.html
```

The file contains:

```html
<html>
  <head><title>Test Page</title></head>
  <body>
    <h1>Success to access finaltest1.inapp.test</h1>
  </body>
</html>
```

Each test domain will have a unique index file based on its number.

---

## 🛠️ Notes

* Certificates must include:

  * `testLeafCert.pem`
  * `leafPrivateEcc384.key`
  * `testInterCa.pem`
  * `testRootCa.crt`

* Missing test directories (e.g., test17) will be skipped automatically.

* All configurations use wildcard domain `*.inapp.test` and port `443`.

---

You are now ready to run test cases for TLS certificate behaviors across Chrome, Android WebView, and other browsers.

