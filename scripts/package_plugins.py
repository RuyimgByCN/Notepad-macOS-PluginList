#!/usr/bin/env python3
"""Package each macOS-native plugin into <identifier>-<version>.zip under dist/.

The zip layout is a single wrapping directory (ditto --keepParent), so after
extraction PluginCatalog.locateManifestDirectory finds notepad-mac-plugin.json
one level below the archive root — the same structure exercised by
PluginArchiveInstallationTests.

The zip filename follows the catalog version, which is what the repository URL
in mac-arm64.json points at:
    https://github.com/RuyimgByCN/Notepad-macOS-PluginList/releases/download/plugins/<identifier>-<version>.zip

Any mismatch between the catalog version and the manifest version is reported so
the catalog can be reconciled before publishing.
"""
import json
import os
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLUGINS_DIR = os.path.join(ROOT, "plugins")
DIST_DIR = os.path.join(ROOT, "dist")
CATALOG_PATH = os.path.join(ROOT, "mac-arm64.json")


def load_manifest(plugin_id):
    path = os.path.join(PLUGINS_DIR, plugin_id, "notepad-mac-plugin.json")
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def main():
    if os.path.exists(DIST_DIR):
        shutil.rmtree(DIST_DIR)
    os.makedirs(DIST_DIR)

    with open(CATALOG_PATH, encoding="utf-8") as handle:
        catalog = json.load(handle)
    catalog_version = {p["identifier"]: p.get("version") for p in catalog["plugins"]}

    packaged = []
    mismatches = []
    for plugin_id in sorted(os.listdir(PLUGINS_DIR)):
        plugin_dir = os.path.join(PLUGINS_DIR, plugin_id)
        if not os.path.isdir(plugin_dir) or plugin_id.startswith("."):
            continue
        manifest = load_manifest(plugin_id)
        if manifest is None:
            continue
        identifier = manifest["identifier"]
        manifest_version = manifest.get("version")
        catalog_ver = catalog_version.get(identifier)
        if catalog_ver != manifest_version:
            mismatches.append((identifier, catalog_ver, manifest_version))
        version = catalog_ver or manifest_version
        zip_name = f"{identifier}-{version}.zip"
        zip_path = os.path.join(DIST_DIR, zip_name)
        subprocess.run(
            ["/usr/bin/ditto", "-c", "-k", "--keepParent", plugin_dir, zip_path],
            check=True,
        )
        packaged.append((identifier, version, zip_name))
        print(f"packaged {identifier} {version} -> {zip_name}")

    print(f"\n{len(packaged)} plugins packaged into dist/")
    if mismatches:
        print("\nVersion mismatches (catalog vs manifest):")
        for identifier, catalog_ver, manifest_ver in mismatches:
            print(f"  {identifier}: catalog={catalog_ver!r} manifest={manifest_ver!r}")
        print("Resolve these before publishing — zip name follows the catalog version.")
    else:
        print("All manifest versions match the catalog.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
