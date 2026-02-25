# Packaging Flask+PyQt6 App for Windows

**Extracted:** 2026-01-25
**Context:** Packaging a hybrid Python desktop application (Flask backend + PyQt6 QWebEngine frontend) for Windows deployment using PyInstaller and Inno Setup.

## Problem
1. **Permission Errors:** Packaged apps installed in `Program Files` cannot write logs or data to their own directory, causing "500 Internal Server Error" or crashes.
2. **Distribution:** Converting a complex Python environment with web assets into a single installer file.

## Solution

### 1. Fix File Permissions (Code Level)
Do not write to `os.getcwd()` or `os.path.dirname(__file__)` for runtime data. Use `AppData/Local`.

```python
import os
import sys

def get_app_data_dir():
    """Get a writable directory for logs and data."""
    home = os.path.expanduser("~")
    if sys.platform == "win32":
        # Windows: %LOCALAPPDATA%/AppName
        base_dir = os.path.join(home, "AppData", "Local", "YourAppName")
    else:
        # Linux/Mac: ~/.appname
        base_dir = os.path.join(home, ".your_app_name")

    if not os.path.exists(base_dir):
        try:
            os.makedirs(base_dir)
        except:
            pass
    return base_dir

# Use this for all file writes (logs, databases, exports)
APP_DATA_DIR = get_app_data_dir()
log_path = os.path.join(APP_DATA_DIR, 'app.log')
```

### 2. Freeze with PyInstaller
Create a `spec` file that includes your Flask templates and static files.

```bash
pyinstaller app.spec --clean --noconfirm
```

### 3. Create Installer with Inno Setup
Use a `.iss` script to wrap the PyInstaller `dist` folder.

**Key `.iss` Configuration:**
```ini
#define MyAppName "Your App Name"
#define MyAppExeName "main_executable.exe"

[Setup]
DefaultDirName={autopf}\{#MyAppName}
OutputBaseFilename=YourApp_Setup

[Files]
; Include the main executable
Source: "dist\YourApp\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Include all dependencies recursively
Source: "dist\YourApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
```

### 4. Compile Installer
Run the Inno Setup Compiler CLI:
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "setup.iss"
```

## When to Use
- When deploying a Python desktop app to end-users on Windows.
- When encountering "Permission Denied" or "Internal Server Error" in installed apps that worked fine in development.
- When needing to bundle a local web server (Flask/FastAPI) with a browser UI (PyQt/CEF).
