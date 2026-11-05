# Gemini Live (Extended Thinking AI Communicator)

**Package ID:** `org.atlas.assistant`  
**Version:** `1.0.0`  
**Target:** ATLAS OS on ESP32-S3 Handheld  
**Runtime:** Native Executable (`app.bin`)  
**Permissions:** `display`, `input`, `audio_tx`, `audio_rx`, `network`  

---

## Overview

Gemini Live turns the Atlas Handheld into an ultra-low-latency cybernetic voice communicator powered by **Google Gemini 3.8 Flash** with **Extended Thinking** (`thinkingConfig: { includeThoughts: true }`).

### Key Features
1. **Push-to-Talk Voice Streaming:** Hold mechanical switch `[A]` to capture 16kHz audio directly from the onboard INMP441 MEMS microphone with real-time VU meter feedback.
2. **Dual-Pane Cybernetic HUD:**
   - **Thinking Inspector (Amber CRT Glow):** Real-time streaming visualization of Gemini's internal reasoning tokens as it plans and evaluates complex thoughts.
   - **Answer Terminal (Cyan Matrix Glow):** High-speed streaming output of the final response formatted for the 320x240 LCD.
3. **API Key Setup:**
   Create a file named `gemini_key.txt` on the root of your MicroSD card containing your Gemini API key:
   ```text
   AIzaSy...
   ```

### Hardware Controls
- **`[A] SW1` (Hold):** Push-to-Talk (Record voice query).
- **`[A] SW1` (Release):** Send query to Gemini cloud.
- **`Joystick Up / Down`:** Scroll through the Thinking Inspector history.
- **`[D] SW4`:** Cycle prompt presets or clear history.
- **`[B] SW2` / `[C] SW3`:** Return to ATLAS Home Launcher.
