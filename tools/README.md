# ATLAS APPS — Developer & CI Tools

This directory contains development and CI validation utilities for the ATLAS APPS repository.

---

## 1. `validate_apps.py`

Canonical validator and catalogue generator for ATLAS community applications.

### Functions:
- Validates each application manifest against `schema/manifest.schema.json`.
- Enforces strict constraints required by the ATLAS OS Application Manager:
  - `app_id` uniqueness and format (alphanumeric + `.` + `-` + `_`, max 31 characters).
  - Semantic versioning format (`MAJOR.MINOR.PATCH`).
  - Path traversal security checks on `entrypoint` (no `..`, leading `/` or `\`, or colons).
  - Verifies that the declared `entrypoint` file exists on disk.
- Generates and updates `catalog.json` and `CATALOG.md`.

### Usage:

```bash
# Validate and update catalogue files:
python tools/validate_apps.py

# Validation only (CI mode, fails with exit code 1 on errors):
python tools/validate_apps.py --check-only
```
