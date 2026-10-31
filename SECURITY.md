# Security Policy

## 1. Reporting Security Vulnerabilities

If you discover a security vulnerability or exploit in the ATLAS application ecosystem or catalogue tooling, please do **not** open a public issue.

Instead, please report it privately:
- **Email:** `reyanshniranjanodm@gmail.com`
- **GitHub Security Advisory:** Submit a private advisory via the [Security Advisories tab](https://github.com/Reyansh-Niranjan/APPS/security/advisories).

Please include:
1. Application ID or component name affected.
2. Step-by-step reproduction instructions or Proof of Concept (PoC).
3. Potential impact on hardware or host operating system integrity.

---

## 2. Application Ecosystem Security Architecture

ATLAS OS is an embedded operating system running on the ESP32-S3 microcontroller. Because standard microcontroller architectures share physical memory, application security relies on explicit design boundaries:

### A. Path Traversal Defenses
The ATLAS OS Application Manager and APPS validation tools enforce strict path traversal defenses:
- Application entry points must be relative paths within the package folder.
- Any reference to parent directories (`..`), root paths (`/`), Windows drive prefixes (`:`), or backslashes (`\`) is rejected.

### B. Prevention of Firmware Hijacking
- The APPS repository does not accept raw ESP-IDF firmware images (`.bin`).
- Firmware updates must be handled exclusively through the guarded ATLAS OS OTA engine (`atlas_ota`) with image checksum verification, magic byte checks, and hardware rollback.

### C. Execution Sandboxing Roadmap
- External community applications are designed to execute within an isolated WebAssembly (WASM) virtual machine sandbox running in 8MB Octal PSRAM.
- Virtual memory page sandboxing prevents malicious or crashing third-party code from corrupting the host OS kernel or freezing the device.
