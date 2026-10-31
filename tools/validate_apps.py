#!/usr/bin/env python3
"""
ATLAS APPS Catalogue Validator & Generator
=========================================
Validates all applications in apps/ against schema/manifest.schema.json,
checks app_id uniqueness, verifies entrypoint existence, and updates
catalog.json and CATALOG.md.
"""
import os
import sys
import json
import re
import argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
APPS_DIR = os.path.join(REPO_ROOT, "apps")
SCHEMA_FILE = os.path.join(REPO_ROOT, "schema", "manifest.schema.json")
CATALOG_JSON = os.path.join(REPO_ROOT, "catalog.json")
CATALOG_MD = os.path.join(REPO_ROOT, "CATALOG.md")

APP_ID_REGEX = re.compile(r'^[a-zA-Z0-9._-]+$')
SEMVER_REGEX = re.compile(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$')

def load_schema():
    if not os.path.isfile(SCHEMA_FILE):
        return None
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def validate_manifest(app_folder, manifest, seen_ids):
    errors = []
    
    # 1. Required fields
    required = ["app_id", "name", "version", "runtime", "entrypoint"]
    for req in required:
        if req not in manifest or not str(manifest[req]).strip():
            errors.append(f"Missing required field '{req}'")

    if errors:
        return errors

    app_id = manifest["app_id"]
    name = manifest["name"]
    version = manifest["version"]
    runtime = manifest["runtime"]
    entrypoint = manifest["entrypoint"]

    # 2. Field constraints
    if len(app_id) > 31:
        errors.append(f"app_id '{app_id}' exceeds 31 characters limit ({len(app_id)})")
    if not APP_ID_REGEX.match(app_id):
        errors.append(f"app_id '{app_id}' contains invalid characters (alphanumeric, dot, dash, underscore only)")
    if app_id in seen_ids:
        errors.append(f"Duplicate app_id '{app_id}' (already registered by {seen_ids[app_id]})")
    seen_ids[app_id] = app_folder

    if len(name) > 31:
        errors.append(f"name '{name}' exceeds 31 characters limit ({len(name)})")

    if len(version) > 15 or not SEMVER_REGEX.match(version):
        errors.append(f"version '{version}' is not valid Semantic Versioning (e.g. 1.0.0)")

    allowed_runtimes = ["wasm", "native", "python", "lua"]
    if runtime not in allowed_runtimes:
        errors.append(f"runtime '{runtime}' is not valid (allowed: {allowed_runtimes})")

    # 3. Entrypoint security & existence
    if ".." in entrypoint or entrypoint.startswith("/") or entrypoint.startswith("\\") or ":" in entrypoint:
        errors.append(f"entrypoint '{entrypoint}' violates path traversal security constraints")
    else:
        full_ep = os.path.join(APPS_DIR, app_folder, entrypoint)
        if not os.path.isfile(full_ep):
            errors.append(f"entrypoint file not found on disk: {entrypoint}")

    # 4. Optional tagline check
    if "tagline" in manifest and len(manifest["tagline"]) > 47:
        errors.append(f"tagline exceeds 47 characters limit ({len(manifest['tagline'])})")

    return errors

def scan_applications():
    if not os.path.isdir(APPS_DIR):
        return [], []

    apps = []
    all_errors = []
    seen_ids = {}

    for entry in sorted(os.listdir(APPS_DIR)):
        app_path = os.path.join(APPS_DIR, entry)
        if not os.path.isdir(app_path) or entry.startswith("."):
            continue

        manifest_path = os.path.join(app_path, "manifest.json")
        if not os.path.isfile(manifest_path):
            all_errors.append((entry, ["Directory is missing manifest.json"]))
            continue

        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                manifest = json.load(f)
        except Exception as e:
            all_errors.append((entry, [f"Invalid JSON syntax in manifest.json: {e}"]))
            continue

        errs = validate_manifest(entry, manifest, seen_ids)
        if errs:
            all_errors.append((entry, errs))
        else:
            apps.append({
                "directory": entry,
                "manifest": manifest
            })

    return apps, all_errors

def generate_catalog(apps):
    catalog_data = {
        "version": 1,
        "total_applications": len(apps),
        "applications": []
    }

    md_lines = [
        "# ATLAS Application Catalogue",
        "",
        "This catalogue is automatically generated from verified manifests in [`apps/`](apps/).",
        "",
        "> [!NOTE]",
        "> Third-party runtime support (WebAssembly VM in 8MB PSRAM) is under active development in ATLAS OS.",
        "> Applications listed below are verified source/bytecode bundles preparing for the upcoming runtime engine.",
        "",
        "| Application | ID | Version | Runtime | Author | Status | Description |",
        "|---|---|---|---|---|---|---|"
    ]

    for item in apps:
        m = item["manifest"]
        app_id = m.get("app_id", "")
        name = m.get("name", "")
        version = m.get("version", "")
        runtime = m.get("runtime", "")
        author = m.get("author", "Community")
        tagline = m.get("tagline", m.get("description", "No description provided."))
        folder = item["directory"]

        catalog_data["applications"].append({
            "app_id": app_id,
            "name": name,
            "version": version,
            "runtime": runtime,
            "author": author,
            "tagline": tagline,
            "entrypoint": m.get("entrypoint", ""),
            "path": f"apps/{folder}",
            "manifest_url": f"apps/{folder}/manifest.json"
        })

        md_lines.append(
            f"| **[{name}](apps/{folder})** | `{app_id}` | `v{version}` | `{runtime}` | {author} | Verified | {tagline} |"
        )

    if not apps:
        md_lines.append("| *(No community apps currently submitted)* | - | - | - | - | - | - |")

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("To submit an application to this catalogue, see [CONTRIBUTING.md](CONTRIBUTING.md).")
    md_lines.append("")

    return catalog_data, "\n".join(md_lines)

def main():
    parser = argparse.ArgumentParser(description="ATLAS APPS Catalogue Validator & Generator")
    parser.add_argument("--check-only", action="store_true", help="Only validate without updating catalog files")
    args = parser.parse_args()

    print("=========================================================")
    print(" ATLAS APPS REPOSITORY VALIDATION SUITE")
    print("=========================================================")

    apps, errors = scan_applications()

    if errors:
        print(f"\n[FAIL] Validation errors found in {len(errors)} application(s):")
        for folder, err_list in errors:
            print(f"\n  • apps/{folder}:")
            for err in err_list:
                print(f"      - {err}")
        print("\nFix the errors above before committing or generating the catalogue.")
        sys.exit(1)

    print(f"\n[OK] Scanned {len(apps)} application package(s). All manifests valid.")

    if not args.check_only:
        cat_json, cat_md = generate_catalog(apps)
        with open(CATALOG_JSON, "w", encoding="utf-8") as f:
            json.dump(cat_json, f, indent=2)
        with open(CATALOG_MD, "w", encoding="utf-8") as f:
            f.write(cat_md)
        print(f"[OK] Updated {CATALOG_JSON}")
        print(f"[OK] Updated {CATALOG_MD}")

    print("\nValidation completed successfully.")
    sys.exit(0)

if __name__ == "__main__":
    main()
