# ATLAS APPS — Community Application Repository

[![Validate Catalogue & Manifests](https://github.com/Reyansh-Niranjan/APPS/actions/workflows/validate.yml/badge.svg)](https://github.com/Reyansh-Niranjan/APPS/actions/workflows/validate.yml)
[![ATLAS OS Compatibility](https://img.shields.io/badge/ATLAS%20OS-v1.0.0-00d2ff.svg)](https://github.com/Reyansh-Niranjan/Atlas)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

**ATLAS APPS** is the official community application repository for **[ATLAS OS](https://github.com/Reyansh-Niranjan/Atlas)**, an embedded operating-system environment designed for the **ESP32-S3** microcontroller.

---

## 1. Architectural Relationship with ATLAS OS

The ATLAS ecosystem is divided into two decoupled repositories:

```text
┌────────────────────────────────────────┐       ┌────────────────────────────────────────┐
│               ATLAS OS                 │       │               ATLAS APPS               │
│  (Reyansh-Niranjan/Atlas)              │       │  (Reyansh-Niranjan/APPS)               │
├────────────────────────────────────────┤       ├────────────────────────────────────────┤
│ • Structured Boot Manager              │       │ • Community Application Catalogue      │
│ • Inter-Service Event Bus              │◄──────┤ • Application Source Code & Assets     │
│ • Hardware Abstraction Layer (HAL)     │       │ • Package Metadata & Manifests         │
│ • Dynamic Application Manager          │       │ • Validation Tools & CI Pipelines      │
│ • Inactive-Slot OTA Engine & Rollback  │       │ • Submodule Integration into ATLAS OS  │
└────────────────────────────────────────┘       └────────────────────────────────────────┘
```

- **[ATLAS OS](https://github.com/Reyansh-Niranjan/Atlas):** Host operating system, system services, drivers (ILI9341 LCD, SDSPI, I2S audio, ADC input), boot diagnostics, dynamic launcher shell, and the Application Manager.
- **[ATLAS APPS](https://github.com/Reyansh-Niranjan/APPS) (this repository):** Central hub for third-party and community applications, source code, metadata schemas, and package distribution.

---

## 2. Directory Hierarchy

```text
APPS/
├── README.md               # Main repository documentation & overview
├── CONTRIBUTING.md         # Developer guide for submitting applications
├── SECURITY.md             # Vulnerability disclosure & sandbox safety policy
├── CATALOG.md              # Human-readable catalogue of available applications
├── catalog.json            # Machine-readable application index for package managers
├── schema/
│   └── manifest.schema.json# Formal JSON schema for package manifests
├── apps/                   # Application packages directory
│   └── README.md           # Application packaging & directory conventions
├── assets/                 # Shared design templates and icon resources
│   └── README.md           # Icon specifications (PNG & RGB565 RAW)
├── tools/                  # Developer utilities & CI scripts
│   ├── README.md           # Tool documentation
│   └── validate_apps.py    # Manifest validator & catalogue generator
└── .github/
    ├── ISSUE_TEMPLATE/     # Application submission & bug report templates
    └── workflows/          # Automated GitHub Actions CI validation
```

---

## 3. Honest Runtime Support & Compatibility Status

> [!NOTE]
> **Current Operating System Status (ATLAS OS v1.0.0):**
> - **In-Firmware Applications:** Native compiled applications (such as *Settings*) execute directly within the ATLAS firmware.
> - **Manifest Discovery:** ATLAS OS includes a Dynamic Application Manager that scans `/sdcard/apps/installed/` for `manifest.json`, validates required fields, verifies entrypoint existence, and prevents path traversal.
> - **Third-Party Execution Engine:** A sandboxed WebAssembly (WASM) virtual machine executing out of the ESP32-S3's **8 MB Octal PSRAM** is currently under active development.
> - **No Raw Firmware Flashing:** Applications in this repository are **never** raw ESP-IDF `.bin` firmware replacements. Flashing arbitrary firmware into OTA partitions destroys the operating system context and is handled strictly via the guarded `atlas_ota` subsystem.

---

## 4. Application Manifest Specification (`manifest.json`)

Applications must include a `manifest.json` file conforming to [`schema/manifest.schema.json`](schema/manifest.schema.json):

```json
{
  "app_id": "com.example.notes",
  "name": "QuickNotes",
  "version": "1.0.0",
  "runtime": "wasm",
  "entrypoint": "app/app.wasm",
  "tagline": "Simple notepad utility",
  "description": "A lightweight text notepad designed for the ATLAS Handheld.",
  "author": "Reyansh",
  "license": "MIT",
  "min_atlas_version": ">=1.0.0",
  "permissions": [
    "display",
    "input",
    "storage_app"
  ],
  "repository": "https://github.com/example/quicknotes"
}
```

### Field Breakdown:
- **Core Engine Fields (Required by ATLAS OS):**
  - `app_id`: Unique identifier (alphanumeric, `.`, `-`, `_`, max 31 characters).
  - `name`: Display title rendered in the 2x2 launcher grid (max 31 characters).
  - `version`: Strict Semantic Versioning string (e.g. `1.0.0`).
  - `runtime`: Target runtime environment (`wasm`, `native`, `python`, `lua`).
  - `entrypoint`: Relative path to main executable or bytecode (no path traversal).
- **Catalogue & Store Fields:**
  - `tagline`, `description`, `author`, `license`, `min_atlas_version`, `permissions`, `icon`, `repository`.

---

## 5. Browsing the Catalogue

- **Human-readable catalogue:** Inspect [`CATALOG.md`](CATALOG.md) for a summary table of applications, versions, and runtimes.
- **Machine-readable catalogue:** Applications, store clients, and package managers can consume [`catalog.json`](catalog.json) directly without cloning the repository.

---

## 6. Contributing an Application

We welcome contributions from the embedded and retro-handheld community!

1. Fork this repository: `https://github.com/Reyansh-Niranjan/APPS`.
2. Create your application directory under `apps/<your-app-id>/`.
3. Add your `manifest.json`, source code, and assets.
4. Run the validator:
   ```bash
   python tools/validate_apps.py
   ```
5. Commit, push, and open a Pull Request.

Detailed instructions can be found in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 7. Submodule Integration in ATLAS OS

To clone ATLAS OS with the APPS repository included:

```bash
git clone --recurse-submodules https://github.com/Reyansh-Niranjan/Atlas.git
```

If you already have a clone of ATLAS OS:

```bash
git submodule update --init --recursive
```
