# Contributing to the ATLAS Application Ecosystem

Welcome to the **ATLAS APPS** community repository!

This document outlines how to create, test, and submit applications for the **ATLAS OS** ecosystem.

---

## 1. Architectural Principles & Safety Policies

ATLAS OS is an embedded operating system for the ESP32-S3. Applications in this repository must adhere to the following principles:

1. **Memory & Resource Discipline:**
   - The ESP32-S3 features 512 KB internal SRAM and 8 MB Octal PSRAM.
   - Applications must be efficient with heap allocations and avoid runaway loops.
2. **Standard Sandbox Targeting:**
   - Third-party applications target the upcoming **WebAssembly (WASM)** virtual machine sandbox.
   - All external packages must provide verifiable source code and/or reproducible WASM bytecode.
3. **No Firmware Image Replacements:**
   - **DO NOT** submit raw ESP-IDF firmware binaries (`.bin`) designed to be written into OTA partitions.
   - Replacing the running OS firmware partition is a firmware upgrade, not an application execution model.

---

## 2. Directory Structure

Every application submission must reside in its own folder under `apps/`:

```text
apps/
└── <app-id>/
    ├── manifest.json       # Required: Application metadata (schema-validated)
    ├── README.md           # Required: Documentation, usage, and build instructions
    ├── icon.png            # Recommended: 48x48 or 32x32 icon
    ├── src/                # Recommended: Source code (C, Rust, AssemblyScript, etc.)
    └── assets/             # Optional: Application assets (images, fonts, sounds)
```

---

## 3. Creating `manifest.json`

Your `manifest.json` must validate against [`schema/manifest.schema.json`](schema/manifest.schema.json).

```json
{
  "app_id": "com.example.calculator",
  "name": "QuickCalc",
  "version": "1.0.0",
  "runtime": "wasm",
  "entrypoint": "app/app.wasm",
  "tagline": "Simple pocket calculator",
  "description": "A basic scientific and arithmetic calculator designed for ATLAS Handheld.",
  "author": "YourName",
  "license": "MIT",
  "min_atlas_version": ">=1.0.0",
  "permissions": [
    "display",
    "input"
  ],
  "repository": "https://github.com/yourname/quickcalc"
}
```

### Constraint Checklist:
- `app_id`: Max 31 characters, alphanumeric, `.`, `-`, `_` only. Must be unique.
- `name`: Max 31 characters.
- `version`: Strict Semantic Versioning (e.g. `1.0.0`).
- `runtime`: `wasm` (preferred for third-party apps), `native`, `python`, or `lua`.
- `entrypoint`: Relative path inside app directory. Must exist on disk. **Path traversal (`..`) is strictly prohibited**.

---

## 4. Local Validation Workflow

Before submitting a Pull Request, run the validation tool:

```bash
# Validate all applications and update the catalogue:
python tools/validate_apps.py

# Run in check-only CI mode:
python tools/validate_apps.py --check-only
```

---

## 5. Submitting a Pull Request

1. **Fork** the repository: `https://github.com/Reyansh-Niranjan/APPS`.
2. **Create a branch**: `git checkout -b app/<app-id>`.
3. **Add your application** files inside `apps/<app-id>/`.
4. Run `python tools/validate_apps.py` to regenerate `CATALOG.md` and `catalog.json`.
5. **Commit and push**:
   ```bash
   git add apps/<app-id> CATALOG.md catalog.json
   git commit -m "feat(apps): add <app-id> v<version>"
   git push origin app/<app-id>
   ```
6. **Open a Pull Request** against `main`. Ensure all GitHub Actions CI checks pass.
