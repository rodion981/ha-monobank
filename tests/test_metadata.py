"""Validate repository and Home Assistant metadata."""

from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
COMPONENT = ROOT / "custom_components" / "monobank"


def load_json(path: Path):
    """Load strict JSON from disk."""
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def leaf_paths(value, prefix=()):
    """Return paths to all scalar translation values."""
    if isinstance(value, dict):
        paths = set()
        for key, child in value.items():
            paths.update(leaf_paths(child, (*prefix, key)))
        return paths
    return {prefix}


class TestMetadata(unittest.TestCase):
    """Guard HACS, manifest, package, and translations."""

    def test_json_files_are_valid(self) -> None:
        paths = [
            ROOT / "hacs.json",
            ROOT / "package.json",
            COMPONENT / "manifest.json",
            COMPONENT / "strings.json",
            COMPONENT / "translations" / "en.json",
            COMPONENT / "translations" / "uk.json",
        ]
        for path in paths:
            with self.subTest(path=path):
                load_json(path)

    def test_repository_urls_and_versions_match(self) -> None:
        manifest = load_json(COMPONENT / "manifest.json")
        package = load_json(ROOT / "package.json")
        self.assertEqual(manifest["version"], package["version"])
        self.assertEqual(
            manifest["documentation"], "https://github.com/rodion981/ha-monobank"
        )
        self.assertEqual(
            manifest["issue_tracker"],
            "https://github.com/rodion981/ha-monobank/issues",
        )
        self.assertNotIn("YOUR_USERNAME", json.dumps(package))

    def test_translations_match_source_keys(self) -> None:
        source_paths = leaf_paths(load_json(COMPONENT / "strings.json"))
        for language in ("en", "uk"):
            translated_paths = leaf_paths(
                load_json(COMPONENT / "translations" / f"{language}.json")
            )
            self.assertEqual(source_paths, translated_paths, language)


if __name__ == "__main__":
    unittest.main()
