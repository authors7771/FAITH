# Android Studio & Rooted AVD Setup Guide (Ubuntu 22.04)

This guide provides step-by-step instructions for setting up Android Studio and rooted AVD (Android Virtual Device) environments on Ubuntu 22.04. It includes image installation, QEMU build information, and rooting instructions using the `rootAVD` project.

---

## ✅ 1. Install Android Studio

### Requirements

* **OS**: 64-bit Ubuntu 22.04
* **CPU**: Intel VT-x or AMD-V support
* **RAM**: 8GB minimum (16GB+ recommended)
* **Disk**: 8GB free space minimum
* **Dependencies**: `openjdk-11-jdk`, `snapd`

### Installation

```bash
sudo apt update
sudo apt install openjdk-11-jdk snapd
sudo snap install android-studio --classic
```

Launch Android Studio and complete SDK and AVD setup as needed.

---

## ✅ 2. Download and Configure AVD Images

### Supported Images

* **Android 11 (API 30)**: x86, x86\_64, arm64-v8a
* **Android 15 (API 34)**: x86\_64, arm64-v8a

### Setup Instructions

1. Open AVD Manager in Android Studio
2. Create AVD with desired image and architecture
3. Verify that the emulator boots and operates correctly

---

## ✅ 3. QEMU Update (If Needed)

Some architectures like `arm64` may require a custom QEMU build.

### Example QEMU Build

```bash
mkdir emu
cd emu
repo init -u https://android.googlesource.com/platform/manifest -b emu-master-dev --depth=1
repo sync -qcj 24
cd external/qemu
pip install absl-py urlfetch
python3 android/build/python/cmake.py --noqtwebengine --noshowprefixforinfo --target linux_aarch64
```

---

## ✅ 4. Root AVD using rootAVD

The [rootAVD](https://github.com/newbit1/rootAVD) tool allows rooting Android AVDs easily.

### Clone & Execute

```bash
git clone https://github.com/newbit1/rootAVD.git
cd rootAVD
```

### Root Your AVD

1. Launch your target AVD using Android Studio
2. Run the following to list available AVDs:

```bash
./rootAVD.sh ListAllAVDs
```

3. Choose your image and follow the commands on the shell.

---

## ✅ 5. Root Certificate Injection

To insert a custom root certificate:

### Android 11 (API 30)

Use the [Always Trust User Certs](https://github.com/NVISOsecurity/AlwaysTrustUserCerts) to inject your root certificate into the system trust store.

### Android 15 (API 34)

Use the following approach:

1. Push the certificate file (e.g., `12ac77fc.0`) and script (e.g., `system_cert_injection.sh`) to your AVD:

```bash
adb push 12ac77fc.0 /data/local/tmp/
adb push system_cert_injection.sh /data/local/tmp/
```

2. Make the script executable:

```bash
adb shell chmod +x /data/local/tmp/system_cert_injection.sh
```

3. Execute the script from AVD shell:

```bash
adb shell /data/local/tmp/system_cert_injection.sh
```

This will mount the modified CA store using tmpfs and bind it into both `/system/etc/security/cacerts/` and `/apex/com.android.conscrypt/cacerts/`, making the root certificate trusted system-wide.

---

## 📌 Notes

* **Avoid Emulator & VirtualBox Conflicts**: Simultaneous use may cause VT-x conflicts.
* **Certificate Injection**: Use rooted AVDs to test apps with custom root certificates.
* **Android Emulator (not physical device)**: When testing in this setup, `dnsmasq` is not needed as `/etc/hosts` resolution suffices.

---

You're now ready to develop and test Android apps with root-level access and advanced configurations!

---

## ✅ 6. Frida Setup and Hooking Guide

This section explains how to set up and use Frida to dynamically instrument and hook Android apps running on an AVD. Make sure your AVD is rooted as described earlier.

---

### 🔹 Install Frida CLI on Host (Ubuntu 22.04)

Ensure that both the host machine and the AVD use matching **Frida major versions**.

```bash
pip install --upgrade frida==17.0.1 frida-tools==10.2.0
```

---

### 🔹 Setup Frida Server on AVD

1. Download the matching Frida server binary from the [Frida Releases page](https://github.com/frida/frida/releases).
   Example for x86\_64 AVD:
   `frida-server-17.0.1-android-x86_64.xz`

2. Push and run on AVD:

```bash
adb push frida-server /data/local/tmp/
adb shell chmod +x /data/local/tmp/frida-server
adb shell setenforce 0  # If SELinux is enforcing
adb shell /data/local/tmp/frida-server &
```

---

## ✅ 7. Example Hook Script

Save the following as `hook2.js`. It demonstrates how to hook a Java method using Frida.

```javascript
Java.perform(function () {
    var MyClass = Java.use('com.example.MyClass');
    MyClass.myFunction.implementation = function () {
        console.log('[*] Hooked myFunction');
        var result = this.myFunction();
        console.log('[*] Result: ' + result);
        return result;
    };
});
```

Modify class and method names as needed for your target app.

---

## ✅ 8. Attaching the Hook Script

### Step 1: Identify target process

```bash
frida-ps -U | grep your.package.name
```

### Step 2: Attach the hook script

```bash
frida -U -n your.package.name -l hook2.js
```

> * `-U`: Connect to USB/ADB device (emulator is supported)
> * `-n`: Target process name (e.g., app package)
> * `-l`: Hook script path

---

## 📝 Notes

* If you get errors like `unexpectedly timed out`, make sure:

  * AVD is rooted and Frida server is running
  * The app is already launched before attaching
  * SELinux is set to `permissive` (`setenforce 0`)
  * Frida CLI and server versions match exactly (e.g., both 17.0.1)

---

