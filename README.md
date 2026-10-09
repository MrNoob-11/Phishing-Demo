# Phishing-Demo 🚀

A professional, module-compatible orchestration framework built in Python to automatically deploy, monitor, and tunnel a local Flask web application using Cloudflare Tunnels. 

This project fulfills the challenge of refactoring traditional standalone runner scripts into installable Python modules using native packaging standards (`pyproject.toml`).

---

## 🛠️ Features

- **Module-Driven Orchestration**: Leverages Python's `-m` architecture to run commands as formal package instances.
- **Automated Health Checks**: Uses native network pings (`urllib`) to track local port availability before launching external sub-processes.
- **Regex Stream Filtering**: Parses live Cloudflare logs dynamically using regular expressions to capture public tunnel URLs instantly.
- **Robust Cleanup Traps**: Uses global `try...finally` logic to cleanly terminate background web servers on `Ctrl+C`, keeping system ports spotless.
- **Persistent Local Logging**: Integrates a lightweight, persistent SQLite database layer to log transaction metrics securely on disk.

---

## 🚀 Installation

Anyone can install this project globally directly from this GitHub repository. Open your terminal and execute:

```bash
python3 -m pip install git+https://github.com --break-system-packages
```

### 🔍 Troubleshooting "Command Not Found"
If your system states that the shortcuts are not found after installation, your terminal's search path needs to be linked to your user-installed binaries folder. Run these commands to update your profile:

```bash
echo 'export PATH="$HOME/Library/Python/3.14/bin:$PATH"' >> ~/.zshrc
echo 'export PYTHONPATH="$HOME/Library/Python/3.14/lib/python/site-packages:$PYTHONPATH"' >> ~/.zshrc
source ~/.zshrc
```
*(Note: If you are running a different version of Python, replace `3.14` with your active version number).*

---

## ⚡ Global Terminal Shortcuts

Once installed, you can trigger individual components of this package from **any directory** on your Mac using these custom macro shortcuts:

### 1. Launch the Orchestrator
```bash
run-demo
```
This kicks off the core automation runner script. It moves into the application context, mounts the hidden environment, monitors server uptime, links the Cloudflare tunnel interface, extracts your public proxy link, and applies the background cleanup traps.

### 2. Launch the Web App Alone
```bash
launch-web
```
Bypasses the orchestration loop entirely and spins up only the local standalone Flask web dashboard using the Application Factory pattern.

### 3. Inspect Local Database Logs
```bash
view-logs
```
Queries your project's persistent SQLite binary database file and displays a beautifully formatted history chart grid directly in your terminal console.

---

## 🏗️ Architecture Design

| Command Shortcut | Entry Target File | Internal Trigger Function | Scope |
| :--- | :--- | :--- | :--- |
| `run-demo` | `smart_runner.py` | `main()` | Automated background orchestrator loop |
| `launch-web` | `app.py` | `start_server()` | Isolated local Flask application framework |
| `view-logs` | `view_database.py` | `display_logs()` | Local persistent database text grid viewer |

---

## 🛑 Clean Shutdown
To stop either command and free your system ports immediately, simply press **`Control + C`** in your active terminal window.

