"""CLI checks for the theme's published files and control colors."""

import json
import re
import unittest
from pathlib import Path
from xml.etree.ElementTree import fromstring

import cssselect2
import tinycss2


ROOT = Path(__file__).resolve().parents[1]
CSS = (ROOT / "theme.css").read_text(encoding="utf-8")
SURFACES = {"dark": "#000000", "light": "#ffffff"}


class ThemeTests(unittest.TestCase):
    def setUp(self):
        self.matcher = cssselect2.Matcher()
        rules = tinycss2.parse_stylesheet(CSS, skip_whitespace=True, skip_comments=True)
        for rule in rules:
            self.assertEqual(rule.type, "qualified-rule")
            declarations = tinycss2.parse_declaration_list(
                rule.content, skip_whitespace=True, skip_comments=True
            )
            for declaration in declarations:
                self.assertEqual(declaration.type, "declaration")
            values = {
                item.name: tinycss2.serialize(item.value).strip()
                for item in declarations
            }
            selector = tinycss2.serialize(rule.prelude)
            # The static matcher needs a fixture attribute for keyboard focus.
            selector = selector.replace(":focus-visible", "[data-focus-visible]")
            for compiled in cssselect2.compile_selector_list(selector):
                self.matcher.add_selector(compiled, values)

    def styles(self, mode, html):
        body = cssselect2.ElementWrapper.from_html_root(
            fromstring(f'<body class="theme-{mode}">{html}</body>')
        )
        child = next(body.iter_children())
        inherited = self.declarations(body)
        return inherited, inherited | self.declarations(child)

    def declarations(self, element):
        values = {}
        for _, _, pseudo, declarations in self.matcher.match(element):
            if pseudo is None:
                values.update(declarations)
        return values

    def color(self, name, declarations):
        visited = set()
        while name not in visited:
            visited.add(name)
            value = declarations[name]
            ref = re.fullmatch(r"var\((--[\w-]+)\)", value)
            if not ref:
                self.assertRegex(value, r"^#[0-9a-fA-F]{6}$")
                return value
            name = ref[1]
        self.fail(f"Circular color reference: {name}")

    def test_accents_are_visible_on_pure_surfaces(self):
        for mode, surface in SURFACES.items():
            with self.subTest(mode=mode):
                body, _ = self.styles(mode, "<div />")
                for name in (
                    "--background-primary",
                    "--background-secondary",
                    "--modal-background",
                    "--canvas-background",
                ):
                    self.assertEqual(self.color(name, body), surface)
                for name in ("--interactive-accent", "--interactive-accent-hover"):
                    self.assertNotEqual(self.color(name, body), surface)
                self.assertEqual(self.color("--text-on-accent", body), surface)

    def test_primary_button_keeps_surface_and_native_focus(self):
        for mode, surface in SURFACES.items():
            with self.subTest(mode=mode):
                body, button = self.styles(mode, '<button class="mod-cta" />')
                _, focused = self.styles(
                    mode, '<button class="mod-cta" data-focus-visible="" />'
                )
                for styles in (button, focused):
                    self.assertEqual(self.color("background-color", styles), surface)
                    self.assertNotEqual(self.color("--text-on-accent", styles), surface)
                    self.assertEqual(
                        self.color("--interactive-accent", styles),
                        self.color("--interactive-accent", body),
                    )
                self.assertIn("box-shadow", button)
                self.assertNotIn("box-shadow", focused)

    def test_enabled_settings_toggle_has_visible_thumb_on_pure_surface(self):
        for mode, surface in SURFACES.items():
            with self.subTest(mode=mode):
                _, toggle = self.styles(mode, '<div class="checkbox-container is-enabled" />')
                self.assertEqual(self.color("background-color", toggle), surface)
                self.assertNotEqual(self.color("--toggle-thumb-color", toggle), surface)

    def test_readme_matches_manifest_and_preview_files(self):
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(f"Version {manifest['version']}", readme)
        self.assertIn(f"Obsidian {manifest['minAppVersion']} or later", readme)
        self.assertIn(f"{manifest['name']} {manifest['version']}", CSS)
        for image in re.findall(r"!\[[^\]]+\]\(([^)]+)\)", readme):
            self.assertTrue((ROOT / image).is_file(), image)


if __name__ == "__main__":
    unittest.main()
