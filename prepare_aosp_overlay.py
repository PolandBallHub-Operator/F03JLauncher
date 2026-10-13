#!/usr/bin/env python3
"""Apply Android.mk resource overlay precedence to the standalone Gradle source tree.

AOSP's Android.mk uses WallpaperPicker/res first and Launcher3/res second with
--auto-add-overlay. Gradle's resource merger rejects those intentional duplicate
items, so this script removes lower-priority duplicates from WallpaperPicker/res
while retaining its non-overlaid resources.
"""
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
BASE = ROOT / "res"
OVERLAY = ROOT / "WallpaperPicker" / "res"
ET.register_namespace("xliff", "urn:oasis:names:tc:xliff:document:1.2")


def values_keys(path: Path):
    folder = path.parent.name
    if not folder.startswith("values"):
        return set()
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError:
        return set()
    keys = set()
    for item in root:
        name = item.attrib.get("name")
        if name:
            kind = item.attrib.get("type") if item.tag == "item" else item.tag
            keys.add((folder, kind, name))
    return keys


base_value_keys = set()
base_files = set()
for path in BASE.rglob("*"):
    if not path.is_file():
        continue
    relative = path.relative_to(BASE)
    if path.parent.name.startswith("values"):
        base_value_keys.update(values_keys(path))
    else:
        base_files.add(relative.as_posix())

removed_items = 0
removed_files = 0
for path in list(OVERLAY.rglob("*")):
    if not path.is_file():
        continue
    relative = path.relative_to(OVERLAY)
    if path.parent.name.startswith("values"):
        try:
            tree = ET.parse(path)
        except ET.ParseError:
            continue
        root = tree.getroot()
        local_removed = 0
        for item in list(root):
            name = item.attrib.get("name")
            kind = item.attrib.get("type") if item.tag == "item" else item.tag
            key = (path.parent.name, kind, name) if name else None
            if key and key in base_value_keys:
                root.remove(item)
                local_removed += 1
        if local_removed:
            removed_items += local_removed
            if not list(root):
                path.unlink()
                removed_files += 1
            else:
                tree.write(path, encoding="utf-8", xml_declaration=True)
    elif relative.as_posix() in base_files:
        path.unlink()
        removed_files += 1

print(f"Removed {removed_items} duplicate value entries and {removed_files} fully overlaid resource files; Launcher3/res remains the winning overlay.")
