# APKG Store (`org.atlas.store`)

Official on-device application manager and store for **ATLAS OS**.

## Overview
- Discover, browse, inspect, install, and uninstall applications directly from the ATLAS handheld terminal.
- Live storage free space monitoring and installed application badges.
- Native execution on Xtensa LX7 dual-core silicon with 0% performance degradation.

## Controls
- **Joystick UP / DOWN:** Navigate through catalogue applications.
- **Button A (SW1):** Install selected application or launch if already installed.
- **Button D (SW4):** Uninstall application and free storage.
- **Button B (SW2) / Button C (Menu):** Exit back to Home Launcher.

## Technical Details
- **App ID:** `org.atlas.store`
- **Version:** `1.0.0`
- **Runtime:** `native`
- **Entrypoint:** `app.bin`
- **Permissions:** `display`, `input`, `audio_tx`, `storage_app`, `storage_shared`

