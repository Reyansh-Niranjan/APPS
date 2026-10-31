# ATLAS APPS Assets

This directory contains shared assets, visual design guidelines, and branding resources for ATLAS application developers.

---

## 1. Icon Specifications

ATLAS OS displays application icons on the Home Launcher Shell (320x240 ILI9341 LCD).

### Recommended Dimensions & Formats:
- **Dimensions:** 48x48 pixels (preferred) or 32x32 pixels.
- **Formats:**
  - `icon.png`: Standard 24-bit/32-bit PNG with transparency.
  - `icon.raw`: Pre-converted RGB565 binary image for instant DMA blitting without PNG decoding overhead.

### Color Palette Recommendations:
- Dark background compatibility (background colors `#080c14` / `#0f172a`).
- High-contrast visual iconography.
