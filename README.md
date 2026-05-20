# Sandmux 🏝️

**Sandmux** is a lightweight, isolated Python execution sandbox tool designed specifically for **Termux** on Android. It leverages `proot-distro` to spin up a secure Ubuntu instance, paired with a custom local proxy engine to control network access using aggressive strict-deny policies, custom allowlists, and denylists.

> **Created By:** Aryan Giri

- GitHub: [https://github.com/giriaryan694-a11y](https://github.com/giriaryan694-a11y)
- Repository: [https://github.com/giriaryan694-a11y/Sandmux](https://github.com/giriaryan694-a11y/Sandmux)

---

# ✨ Features

## 🔒 File System Isolation

Sandmux forces `proot-distro` into `--isolated` mode, hiding:

* `/sdcard`
* Android internal storage
* Host Termux environment
* Sensitive user directories

This prevents untrusted code from directly interacting with your Android environment.

---

## 🛡️ Strict Network Locking

All outbound HTTP/HTTPS traffic is denied by default.

External connections are only permitted when explicitly allowed through:

* Allowlists
* Denylists
* Custom routing policies

This creates a strict-deny execution model for safer testing.

---

## 📝 Allowlisting & Denylisting

Sandmux supports external policy files:

* `--allowlist`
* `--denylist`

These files let you granularly control which domains or IPs the sandbox can access.

---

## 🧼 Lifecycle Management

Built-in sandbox management commands:

| Command    | Description                        |
| ---------- | ---------------------------------- |
| `--reset`  | Purge and reinstall sandbox image  |
| `--delete` | Destroy entire sandbox environment |

---

## 🎨 Polished Terminal UI

Sandmux includes:

* ASCII banners via `pyfiglet`
* Colored terminal output using `colorama`
* Route feedback indicators
* Clean operational UX

---

# 🚀 Installation & Setup

## 1. Clone Repository

```bash
git clone https://github.com/giriaryan694-a11y/Sandmux.git
cd Sandmux
```

---

## 2. Run Automated Environment Setup

Prepare the environment and install the required Ubuntu rootfs template.

```bash
chmod +x setup.sh
./setup.sh
```

---

## 3. Install Python Dependencies

Install the required packages:

```bash
pip install -r requirements.txt
```

Dependencies include:

* `pyfiglet`
* `colorama`

---

# 🔧 CLI Usage Guide

Display all available operational modes:

```bash
python sandmux.py -h
```

---

# 🧪 Common Commands

## Launch with strict-deny network isolation

```bash
python sandmux.py
```

---

## Launch with allowlisted domains

```bash
python sandmux.py --allowlist allow.txt
```

---

## Reset sandbox image

```bash
python sandmux.py --reset
```

---

## Delete sandbox completely

```bash
python sandmux.py --delete
```

---

# 📦 Allowing APT Package Access

By default, Sandmux blocks all outbound connections.

To allow Ubuntu package installation and updates inside the sandbox, create an allowlist file.

Example:

```txt
archive.ubuntu.com
security.ubuntu.com
ports.ubuntu.com
```

Save it as:

```bash
allow.txt
```

Then launch Sandmux:

```bash
python sandmux.py --allowlist allow.txt
```

This allows:

* `apt update`
* `apt install`
* Ubuntu package repository access

while still maintaining strict-deny behavior for everything else.

---

# 📸 Screenshots

## Initial Sandbox Launch

![Screenshot 1](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/1.png)

---

## Sandbox Routing & Isolation

![Screenshot 2](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/2.png)

---

## Network Control Demonstration

![Screenshot 3](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/3.png)

---

## Creating APT Allowlist

![Screenshot 4](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/4.png)

---

## Allowlist File Example

![Screenshot 5](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/5.png)

---

## Successful APT Update

![Screenshot 7](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/7.png)

---

## Additional Sandbox Preview

![Screenshot 8](https://raw.githubusercontent.com/giriaryan694-a11y/Sandmux/refs/heads/main/screenshots/8.png)

---

# ⚠️ Current Limitations

While Sandmux provides strong application-layer isolation, userland containers without root capabilities still have structural limitations.

## ICMP / Non-HTTP Traffic

Network filtering currently relies on:

* `http_proxy`
* `https_proxy`

Because of this:

* ICMP traffic (`ping`) cannot be filtered
* Raw TCP/UDP socket traffic may bypass proxy enforcement
* Non-HTTP protocols are not deeply inspected yet

---

## Storage Quotas / Rate Limiting

Filesystem storage currently grows dynamically.

There is no enforced quota system yet such as:

* Fixed disk allocation
* Maximum rootfs size limits
* Automatic cleanup thresholds

---

# 🔍 Future Research

Current areas of active research include:

* Stronger protocol-level filtering
* Userland network interception improvements
* Better containment for raw socket traffic
* Storage quota enforcement
* Safer execution workflows for untrusted code
* Improved Android-native isolation methodologies

---

# 🏗️ Technical Architecture

| Component                 | Purpose                           |
| ------------------------- | --------------------------------- |
| `proot-distro`            | Userland Ubuntu containerization  |
| Local proxy engine        | HTTP/HTTPS filtering              |
| Allowlist/Denylist system | Scope enforcement                 |
| `colorama`                | Colored terminal routing feedback |
| `pyfiglet`                | ASCII banner rendering            |

---

# 📜 License

This project currently does not specify a license.

Consider adding one if you plan to distribute or accept public contributions.

---

# ⭐ Support The Project

If you like Sandmux:

* Star the repository
* Share feedback
* Submit ideas/issues
* Contribute improvements

Repository:

[https://github.com/giriaryan694-a11y/Sandmux](https://github.com/giriaryan694-a11y/Sandmux)
