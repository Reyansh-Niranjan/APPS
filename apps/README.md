# ATLAS Applications Directory

This directory contains community and official applications developed for **ATLAS OS**.

---

## 1. Directory Structure Convention

Each application must reside in its own dedicated directory named after its unique `app_id` (or clean slug):

```text
apps/
└── com.example.calculator/
    ├── manifest.json       # Required: Package manifest
    ├── README.md           # Required: Documentation & build instructions
    ├── icon.png            # Recommended: 32x32 or 48x48 PNG or RAW icon
    ├── src/                # Recommended: Application source code
    └── assets/             # Optional: Fonts, images, sounds, level data
```

---

## 2. Manifest Requirements (`manifest.json`)

The manifest must conform to [`schema/manifest.schema.json`](../schema/manifest.schema.json).

### Core Fields (Consumed by ATLAS OS Application Manager):

| Field | Type | Required | Constraints | Purpose |
|---|---|---|---|---|
| `app_id` | String | **Yes** | Max 31 chars, `^[a-zA-Z0-9._-]+$` | Unique reverse-DNS package identifier |
| `name` | String | **Yes** | Max 31 chars | Display title rendered in launcher |
| `version` | String | **Yes** | Max 15 chars, SemVer (`X.Y.Z`) | Semantic version string |
| `runtime` | String | **Yes** | `wasm`, `native`, `python`, `lua` | Target runtime environment |
| `entrypoint` | String | **Yes** | Relative path, no `..`, file must exist | Main executable or entry script |
| `tagline` | String | Optional | Max 47 chars | Short subtext on launcher cards |

### Ecological & Store Metadata (Catalogue Fields):

| Field | Type | Description |
|---|---|---|
| `description` | String | Long-form summary of application purpose |
| `author` | String | Developer handle or name |
| `license` | String | SPDX license identifier (e.g. `MIT`, `Apache-2.0`) |
| `min_atlas_version` | String | Minimum ATLAS OS version requirement (e.g. `>=1.0.0`) |
| `permissions` | Array | Requested capabilities (`display`, `input`, `audio_tx`, `storage_app`) |
| `repository` | URI | Source code repository URL |

---

## 3. Runtime Support Status & Policy

> [!IMPORTANT]
> **ATLAS OS Runtime Compatibility:**
> 1. ATLAS OS currently executes compiled in-firmware system applications.
> 2. External community applications are targeted for the upcoming **WebAssembly (WASM) virtual machine sandbox** running in 8MB Octal PSRAM.
> 3. Applications submitted here are indexed in the catalogue and validated for package integrity.
> 4. **No Raw Firmware Images (`.bin`):** Flashing an arbitrary `.bin` into an OTA partition replaces the operating system and is strictly prohibited in this repository.
