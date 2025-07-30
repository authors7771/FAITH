---

# 📱 Facebook Messenger Automated Link Tester (Appium-based)

This example automates the process of clicking test site links inside the apps using Appium. It is designed for Android but can be extended to iOS with minor adjustments.
This is just the automation evaluation example. Because different apps have different UI responses to certificate verification errors, you need to take this into account to use automation scripts.

---

## ✅ 1. Requirements

### Operating System
- Ubuntu 22.04 (64-bit)

### Software Dependencies
- Python 3.8+
- Android Emulator or real Android device
- Appium Server (v1.22.3 or newer)
- Android SDK + adb
- JDK 11+
- Node.js (for Appium)
- Apps (e.g., Facebook Messenger,Android app: `com.facebook.orca`)

> 🔹 For iOS: Replace `UiAutomator2` with `XCUITest` in your Appium configuration.

---

## ✅ 2. Installation

### 2.1 Install Python dependencies

```bash
sudo apt update
sudo apt install python3-pip -y
pip3 install appium-python-client selenium schedule
```

### 2.2 Install Android SDK and adb (If you have not done yet)

```bash
sudo apt install android-sdk adb -y
```

Verify device connection:

```bash
adb devices
```

### 2.3 Install Node.js and Appium

```bash
sudo apt install nodejs npm -y
sudo npm install -g appium
```

### 2.4 Run Appium server

```bash
appium --allow-insecure chromedriver_autodownload
```

---

## ✅ 3. Android Device Setup

1. **Enable Developer Mode**
   Go to Settings → About phone → Tap "Build number" 7 times

2. **Enable USB Debugging**
   Settings → Developer Options → Enable *USB debugging*

3. **Install Facebook Messenger**
   Make sure the Messenger app is logged in and a chat thread contains test site links

---

## ✅ 4. Prepare `testsitelist.txt`

Create a file named `testsitelist.txt` with one domain per line:

```
finaltest1.inapp.test
finaltest2.inapp.test
finaltest3.inapp.test
```

These are the domain links the automation will search for and click.

---

## ✅ 5. Run the Automation Script

```bash
python3 fm_automation_example.py
```

* Screenshots are saved under the `fm/` folder
* The script will:

  * Open a Messenger chat
  * Locate the corresponding link
  * Click it and wait for it to open
  * Take a screenshot and go back
  * Repeat for all test domains

---

## ✅ Directory Structure

```
project/
├── auto_fm_click.py
├── testsitelist.txt
└── fm/
    ├── 0_fm_20250729_16_40.png
    └── ...
```

---

## ✅ Appium Configuration Notes

* The script uses `UiAutomator2` as the automation engine for Android.
* For iOS testing, replace `UiAutomator2` with `XCUITest` in your Appium capabilities. You may need more modifications of automation scripts.
* Ensure the Appium server is running **before** launching the script.
* You can test on either a real device (USB) or an Android Emulator.

---

## 📌 Tips

* Use `adb devices` to confirm your device is connected.
* Check `testsitelist.txt` to ensure domain names match the content-desc attribute used in Messenger messages.
* The automation assumes Messenger is already logged in and the test message is accessible in the visible thread.

---


