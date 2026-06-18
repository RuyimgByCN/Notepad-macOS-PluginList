# Notepad-macOS Plugin List

Plugin catalog for the [Notepad++ macOS native port](https://github.com/RuyimgByCN/Notepad-macOS).

This repository serves the same role as the upstream [nppPluginList](https://github.com/notepad-plus-plus/nppPluginList) — it provides a machine-readable JSON catalog of available plugins that the Notepad-macOS Plugin Admin can fetch, compare, and install.

## Catalog Format

Each entry in `mac-arm64.json` follows this structure:

```json
{
  "identifier": "auto-detect-indent",
  "name": "Auto Detect Indention",
  "version": "2.3",
  "description": "Detects indention (tab or spaces) and auto adjust Tab key on-the-fly.",
  "author": "Mike Tzou (Chocobo1)",
  "homepage": "https://github.com/Chocobo1/nppAutoDetectIndent",
  "repository": "https://github.com/Chocobo1/nppAutoDetectIndent/releases/download/2.3/arm64.zip",
  "nppMacCompatibleVersions": "[8.9.6,]",
  "upstreamWindowsDLL": true,
  "upstreamFolderName": "nppAutoDetectIndent"
}
```

### Key Fields

| Field | Type | Description |
|-------|------|-------------|
| `identifier` | string | Unique plugin identifier (derived from folder name) |
| `name` | string | Display name shown in Plugin Admin |
| `version` | string | Plugin version |
| `description` | string | One-line description of what the plugin does |
| `author` | string | Plugin author name |
| `homepage` | string | URL to the plugin's project page |
| `repository` | string | Download URL for the plugin archive (.zip) |
| `nppMacCompatibleVersions` | string | Notepad-mac version compatibility range (semantic version interval notation) |
| `upstreamWindowsDLL` | boolean | `true` = this entry references an upstream Windows DLL that needs macOS-native reimplementatoin; `false` = a native macOS plugin exists |
| `upstreamFolderName` | string | Original upstream folder name for cross-referencing |

### Current Status

The initial catalog is **converted from the upstream Notepad++ nppPluginList** (`pl.arm64.json`). All 54 entries currently have `upstreamWindowsDLL: true`, meaning they reference Windows DLL plugins that cannot be directly loaded by the macOS host.

**To make a plugin actually installable on macOS**, it needs:
1. A macOS-native executable entry point (not a .dll)
2. A `notepad-mac-plugin.json` manifest inside the zip archive
3. The `upstreamWindowsDLL` field set to `false`

As macOS-native reimplementations of popular upstream plugins become available, their entries will be updated with native repository URLs and `upstreamWindowsDLL: false`.

## Files

| File | Description |
|------|-------------|
| `mac-arm64.json` | Full catalog for Apple Silicon (ARM64) — all 54 entries |
| `mac-arm64-portable.json` | Subset of plugins that could potentially be ported to macOS (50 entries, excluding obviously Windows-only ones) |

## For Plugin Authors

If you've created a macOS-native plugin for Notepad-macOS, please submit a PR to add your entry with:

```json
{
  "identifier": "your-plugin-id",
  "name": "Your Plugin Name",
  "version": "1.0.0",
  "description": "What your plugin does",
  "author": "Your Name",
  "homepage": "https://github.com/you/your-plugin",
  "repository": "https://github.com/you/your-plugin/releases/download/v1.0.0/your-plugin.zip",
  "nppMacCompatibleVersions": "[8.9.6,]",
  "upstreamWindowsDLL": false
}
```

The zip archive must contain a directory with `notepad-mac-plugin.json` and a native macOS executable.

## License

Same as upstream Notepad++ — GPL v3.
