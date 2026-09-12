#!/usr/bin/env python3
"""Regression tests for policy migration, scope, and read-only checks."""

from __future__ import annotations

import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import apply_stage_transition_policy as policy


def skill_text(name: str, gate: str = "") -> str:
    return (
        f'---\nname: {name}\ndescription: Test fixture\nmetadata:\n  version: "1.2.3"\n---\n\n'
        "# Workflow\n\n**阶段完成一致性硬限制：核对真实证据。**\n\n"
        f"{gate}\n\n## Keep this content\n\nExisting task-specific instructions.\n"
    )


class StageTransitionPolicyTests(unittest.TestCase):
    def test_docs_migration_removes_stage_completion_requirement(self) -> None:
        original = skill_text("game-docs", policy.STAGE_TRANSITION_RULE)
        result = policy.patch_skill(original, Path("skills/game-docs/SKILL.md"))
        self.assertIn(policy.DOCS_TRANSITION_RULE, result)
        self.assertNotIn(policy.STAGE_TRANSITION_RULE, result)
        self.assertNotIn(policy.MAINTENANCE_ENTRY_RULE, result)
        self.assertIn('version: "1.2.4"', result)
        self.assertIn("Existing task-specific instructions.", result)
        self.assertEqual(result, policy.patch_skill(result, Path("skills/game-docs/SKILL.md")))

    def test_maintenance_entry_migration_bumps_once_and_preserves_stage_gate(self) -> None:
        original = skill_text("game-review", "**阶段切换门禁硬限制：旧门禁。**")
        original += "\n**维护升级入口硬限制：旧入口。**\n"
        result = policy.patch_skill(original, Path("skills/game-review/SKILL.md"))
        self.assertEqual(result.count(policy.STAGE_TRANSITION_RULE), 1)
        self.assertEqual(result.count(policy.MAINTENANCE_ENTRY_RULE), 1)
        self.assertIn('version: "1.2.4"', result)
        self.assertIn("Existing task-specific instructions.", result)
        self.assertEqual(result, policy.patch_skill(result, Path("skills/game-review/SKILL.md")))

    def test_missing_gate_is_inserted_without_duplicating_existing_content(self) -> None:
        original = skill_text("game-config")
        result = policy.patch_skill(original, Path("skills/game-config/SKILL.md"))
        self.assertEqual(result.count(policy.STAGE_TRANSITION_RULE), 1)
        self.assertEqual(result.count(policy.MAINTENANCE_ENTRY_RULE), 1)
        self.assertEqual(result.count("Existing task-specific instructions."), 1)
        self.assertIn('version: "1.2.4"', result)

    def test_lightweight_skills_receive_collaboration_without_formal_gates(self) -> None:
        for name in policy.LIGHTWEIGHT_SKILLS:
            with self.subTest(skill=name):
                original = skill_text(name)
                path = Path("skills") / name / "SKILL.md"
                result = policy.patch_skill(original, path)
                self.assertIn(policy.COLLABORATION_RULE, result)
                self.assertNotIn(policy.STAGE_TRANSITION_RULE, result)
                self.assertNotIn(policy.MAINTENANCE_ENTRY_RULE, result)
                self.assertEqual(result, policy.patch_skill(result, path))

    def test_missing_insertion_anchor_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing stage completion consistency"):
            policy.patch_skill('metadata:\n  version: "1.2.3"\n# Workflow\n', Path("skills/game-config/SKILL.md"))

    def test_check_is_read_only_and_apply_converges(self) -> None:
        with tempfile.TemporaryDirectory(prefix="skills-policy-test-") as directory:
            root = Path(directory)
            skills = root / "skills"
            skill = skills / "game-review" / "SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text(skill_text("game-review"), encoding="utf-8")
            readme = root / "README.md"
            readme.write_text("# Navigation only\n", encoding="utf-8")
            source = root / "collaboration.md"
            source.write_text("# Standalone guidance\n\nKeep this.\n\n## 维护方式\n\nRepository-only details.\n", encoding="utf-8")
            reference = skill.parent / "references" / "协作约定.md"
            before = skill.read_bytes(), readme.read_bytes()

            with patch.multiple(policy, ROOT=root, SKILLS_DIR=skills, README=readme, COLLABORATION_SOURCE=source):
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy", "--check"]):
                    self.assertEqual(policy.main(), 1)
                self.assertEqual((skill.read_bytes(), readme.read_bytes()), before)
                self.assertFalse(reference.parent.exists())
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy"]):
                    self.assertEqual(policy.main(), 0)
                after = skill.read_bytes(), readme.read_bytes()
                self.assertNotEqual(before[0], after[0])
                self.assertEqual(before[1], after[1])
                self.assertEqual(reference.read_text(encoding="utf-8"), "# Standalone guidance\n\nKeep this.\n")
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy", "--check"]):
                    self.assertEqual(policy.main(), 0)
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy"]):
                    self.assertEqual(policy.main(), 0)
                self.assertEqual((skill.read_bytes(), readme.read_bytes()), after)
                reference.write_text("Drifted guidance\n", encoding="utf-8")
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy", "--check"]):
                    self.assertEqual(policy.main(), 1)
                self.assertEqual(reference.read_text(encoding="utf-8"), "Drifted guidance\n")
                with contextlib.redirect_stdout(io.StringIO()), patch("sys.argv", ["policy"]):
                    self.assertEqual(policy.main(), 0)
                self.assertIn("Keep this.", reference.read_text(encoding="utf-8"))

    def test_current_repository_skills_are_a_fixed_point(self) -> None:
        for path in sorted(policy.SKILLS_DIR.glob("*/SKILL.md")):
            with self.subTest(skill=path.parent.name):
                original = path.read_text(encoding="utf-8")
                self.assertEqual(original, policy.patch_skill(original, path))


if __name__ == "__main__":
    unittest.main()
