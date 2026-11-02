"""Regression tests for resource validation without changing real skill packages."""

import tempfile
import unittest
from pathlib import Path

from validate_skills import parse_frontmatter, validate_links, validate_skill


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / "sample-skill"
        self.package.mkdir()
        self.entry = self.package / "SKILL.md"

    def write(self, text):
        self.entry.write_text(text, encoding="utf-8")

    def test_frontmatter_requires_line_delimiters(self):
        self.write('---\nname: sample-skill\ndescription: "Uses --- within text"\n---\n# Body\n')
        self.assertEqual(parse_frontmatter(self.entry)["description"], "Uses --- within text")
        self.write('---\nname: sample-skill\ndescription: "Uses --- within text"\n')
        with self.assertRaises(ValueError):
            parse_frontmatter(self.entry)

    def test_missing_resource_is_rejected(self):
        self.write("[Template](references/missing.md)")
        self.assertEqual(validate_links(self.entry, self.package), ["missing reference: references/missing.md"])

    def test_existing_resource_and_external_links(self):
        refs = self.package / "references"
        refs.mkdir()
        (refs / "模板.md").write_text("# Template", encoding="utf-8")
        self.write("[Template](references/%E6%A8%A1%E6%9D%BF.md#template)\n[Web](https://example.com)\n[Here](#heading)")
        self.assertEqual(validate_links(self.entry, self.package), [])

    def test_package_cannot_depend_on_repo_only_file(self):
        (self.root / "shared.md").write_text("shared", encoding="utf-8")
        self.write("[Shared](../shared.md)")
        self.assertEqual(validate_links(self.entry, self.package), ["reference leaves package: ../shared.md"])

    def test_fenced_examples_are_not_package_dependencies(self):
        self.write("```markdown\n[Example](future-output.md)\n```\n[Missing](missing.md)")
        self.assertEqual(validate_links(self.entry, self.package), ["missing reference: missing.md"])

    def test_nested_reference_is_checked(self):
        self.write("---\nname: sample-skill\ndescription: Test skill\n---\n")
        refs = self.package / "references"
        refs.mkdir()
        (refs / "guide.md").write_text("[Gone](gone.md)", encoding="utf-8")
        self.assertTrue(any("missing reference: gone.md" in error for error in validate_skill(self.package)))

    def test_missing_entrypoint(self):
        self.assertEqual(validate_skill(self.package), ["missing SKILL.md"])


if __name__ == "__main__":
    unittest.main()
