import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


class HookScriptTests(unittest.TestCase):
    def run_cmd(self, cmd, home):
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        return subprocess.run(
            cmd,
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )

    def test_install_upgrades_old_two_file_install(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-upgrade-") as tmp:
            home = Path(tmp)
            hooks_dir = home / ".claude" / "hooks"
            hooks_dir.mkdir(parents=True)
            (home / ".claude" / "settings.json").write_text("{}\n")
            (hooks_dir / "laconic-activate.js").write_text("")
            (hooks_dir / "laconic-mode-tracker.js").write_text("")

            self.run_cmd(["bash", "hooks/install.sh"], home)

            statusline = hooks_dir / "laconic-statusline.sh"
            self.assertTrue(statusline.exists(), "upgrade should install statusline script")

            settings = json.loads((home / ".claude" / "settings.json").read_text())
            self.assertIn("statusLine", settings)
            self.assertIn(str(statusline), settings["statusLine"]["command"])

    def test_install_reconfigures_missing_statusline(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-statusline-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            hooks_dir = claude_dir / "hooks"
            hooks_dir.mkdir(parents=True)

            for name in ("laconic-activate.js", "laconic-mode-tracker.js", "laconic-statusline.sh"):
                (hooks_dir / name).write_text("")

            settings = {
                "hooks": {
                    "SessionStart": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": f'node "{hooks_dir / "laconic-activate.js"}"',
                                }
                            ]
                        }
                    ],
                    "UserPromptSubmit": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": f'node "{hooks_dir / "laconic-mode-tracker.js"}"',
                                }
                            ]
                        }
                    ],
                }
            }
            (claude_dir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")

            result = self.run_cmd(["bash", "hooks/install.sh"], home)

            self.assertNotIn("Nothing to do", result.stdout)

            updated = json.loads((claude_dir / "settings.json").read_text())
            self.assertIn("statusLine", updated)
            self.assertIn(str(hooks_dir / "laconic-statusline.sh"), updated["statusLine"]["command"])

    def test_uninstall_preserves_custom_statusline(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-uninstall-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            hooks_dir = claude_dir / "hooks"
            hooks_dir.mkdir(parents=True)

            for name in ("laconic-activate.js", "laconic-mode-tracker.js", "laconic-statusline.sh"):
                (hooks_dir / name).write_text("")

            settings = {
                "statusLine": {
                    "type": "command",
                    "command": "bash /tmp/custom-status-with-laconic.sh",
                },
                "hooks": {
                    "SessionStart": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": f'node "{hooks_dir / "laconic-activate.js"}"',
                                }
                            ]
                        }
                    ],
                    "UserPromptSubmit": [
                        {
                            "hooks": [
                                {
                                    "type": "command",
                                    "command": f'node "{hooks_dir / "laconic-mode-tracker.js"}"',
                                }
                            ]
                        }
                    ],
                },
            }
            (claude_dir / "settings.json").write_text(json.dumps(settings, indent=2) + "\n")

            self.run_cmd(["bash", "hooks/uninstall.sh"], home)

            updated = json.loads((claude_dir / "settings.json").read_text())
            self.assertEqual(
                updated["statusLine"]["command"],
                "bash /tmp/custom-status-with-laconic.sh",
            )
            self.assertNotIn("hooks", updated)

    def test_activate_does_not_nudge_when_custom_statusline_exists(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-activate-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)
            (claude_dir / "settings.json").write_text(
                json.dumps(
                    {
                        "statusLine": {
                            "type": "command",
                            "command": "bash /tmp/my-statusline.sh",
                        }
                    }
                )
                + "\n"
            )

            result = self.run_cmd(["node", "hooks/laconic-activate.js"], home)

            self.assertNotIn("STATUSLINE SETUP NEEDED", result.stdout)
            self.assertIn("LACONIC MODE ACTIVE", result.stdout)
            self.assertEqual((claude_dir / ".laconic-active").read_text(), "terse")

    def test_mode_tracker_records_balanced_mode(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-aliases-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)

            subprocess.run(
                ["node", "hooks/laconic-mode-tracker.js"],
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(home), "USERPROFILE": str(home)},
                text=True,
                input='{"prompt":"/laconic balanced"}',
                capture_output=True,
                check=True,
            )
            self.assertEqual((claude_dir / ".laconic-active").read_text(), "balanced")

    def test_mode_tracker_records_think_mode(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-think-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)

            subprocess.run(
                ["node", "hooks/laconic-mode-tracker.js"],
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(home), "USERPROFILE": str(home)},
                text=True,
                input='{"prompt":"/laconic-think balanced"}',
                capture_output=True,
                check=True,
            )
            self.assertEqual((claude_dir / ".laconic-active").read_text(), "think")

    def test_mode_tracker_normal_thinking_clears_think_mode(self):
        with tempfile.TemporaryDirectory(prefix="laconic-hooks-normal-thinking-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir(parents=True)
            (claude_dir / ".laconic-active").write_text("think")

            subprocess.run(
                ["node", "hooks/laconic-mode-tracker.js"],
                cwd=REPO_ROOT,
                env={**os.environ, "HOME": str(home), "USERPROFILE": str(home)},
                text=True,
                input='{"prompt":"normal thinking"}',
                capture_output=True,
                check=True,
            )
            self.assertFalse((claude_dir / ".laconic-active").exists())


class LaconicStatsTests(unittest.TestCase):
    """Tests for hooks/laconic-stats.js and its integration with laconic-mode-tracker.js."""

    def _run_node(self, script, home, prompt=None, extra_env=None):
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        env["CLAUDE_CONFIG_DIR"] = str(home / ".claude")
        if extra_env:
            env.update(extra_env)
        result = subprocess.run(
            ["node", script],
            cwd=REPO_ROOT,
            env=env,
            input=json.dumps({"prompt": prompt}) if prompt is not None else None,
            text=True,
            capture_output=True,
        )
        return result

    def _make_session_jsonl(self, claude_dir, turns):
        """Write a fake session JSONL under the slug for REPO_ROOT."""
        import re
        slug = re.sub(r"[/_]", "-", str(REPO_ROOT))
        project_dir = claude_dir / "projects" / slug
        project_dir.mkdir(parents=True, exist_ok=True)
        session_file = project_dir / "test-session.jsonl"
        lines = []
        for i, (output_tokens, model) in enumerate(turns):
            entry = {
                "type": "assistant",
                "message": {
                    "model": model,
                    "usage": {"output_tokens": output_tokens, "cache_read_input_tokens": 0, "input_tokens": 10},
                },
            }
            lines.append(json.dumps(entry))
        session_file.write_text("\n".join(lines) + "\n")
        return session_file

    # --- config exports ---

    def test_config_exports_compression_ratios(self):
        result = subprocess.run(
            ["node", "-e",
             "const c = require('./hooks/laconic-config');"
             "console.log(JSON.stringify(c.COMPRESSION_RATIOS));"],
            cwd=REPO_ROOT, text=True, capture_output=True, check=True,
        )
        ratios = json.loads(result.stdout)
        self.assertAlmostEqual(ratios["terse"], 0.65)
        self.assertAlmostEqual(ratios["balanced"], 0.45)

    def test_config_exports_model_pricing(self):
        result = subprocess.run(
            ["node", "-e",
             "const c = require('./hooks/laconic-config');"
             "console.log(JSON.stringify(c.MODEL_PRICING));"],
            cwd=REPO_ROOT, text=True, capture_output=True, check=True,
        )
        pricing = json.loads(result.stdout)
        self.assertIn("claude-sonnet-4", pricing)
        self.assertIn("claude-opus-4", pricing)
        self.assertIn("claude-haiku-4", pricing)
        self.assertGreater(pricing["claude-opus-4"], pricing["claude-sonnet-4"])
        self.assertGreater(pricing["claude-sonnet-4"], pricing["claude-haiku-4"])

    # --- no session file ---

    def test_stats_no_session_returns_block_with_message(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-nosession-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            self.assertEqual(result.returncode, 0)
            out = json.loads(result.stdout)
            self.assertEqual(out["decision"], "block")
            self.assertIn("no session data", out["reason"])

    # --- with session file ---

    def test_stats_with_session_returns_correct_turn_count(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-session-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            self._make_session_jsonl(claude_dir, [
                (200, "claude-sonnet-4-6"),
                (300, "claude-sonnet-4-6"),
            ])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            self.assertEqual(result.returncode, 0)
            out = json.loads(result.stdout)
            self.assertEqual(out["decision"], "block")
            self.assertIn("2", out["reason"])         # 2 turns
            self.assertIn("500", out["reason"])        # 200+300 output tokens
            self.assertIn("terse", out["reason"])      # default mode

    def test_stats_terse_mode_uses_65_percent_ratio(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-terse-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            (claude_dir / ".laconic-active").write_text("terse")
            self._make_session_jsonl(claude_dir, [(1000, "claude-sonnet-4-6")])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            out = json.loads(result.stdout)
            # 1000 * 0.65 = 650 saved, ~65%
            self.assertIn("650", out["reason"])
            self.assertIn("65%", out["reason"])

    def test_stats_balanced_mode_uses_45_percent_ratio(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-balanced-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            (claude_dir / ".laconic-active").write_text("balanced")
            self._make_session_jsonl(claude_dir, [(1000, "claude-sonnet-4-6")])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            out = json.loads(result.stdout)
            # 1000 * 0.45 = 450 saved, ~45%
            self.assertIn("450", out["reason"])
            self.assertIn("45%", out["reason"])

    def test_stats_includes_usd_estimate_for_known_model(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-usd-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            self._make_session_jsonl(claude_dir, [(1000, "claude-sonnet-4-6")])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            out = json.loads(result.stdout)
            self.assertIn("$", out["reason"])
            self.assertNotIn("n/a", out["reason"])

    def test_stats_usd_is_na_for_unknown_model(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-usd-unknown-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            self._make_session_jsonl(claude_dir, [(500, "unknown-model-xyz")])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats")
            out = json.loads(result.stdout)
            self.assertIn("n/a", out["reason"])

    # --- --share flag ---

    def test_stats_share_flag_returns_single_line(self):
        with tempfile.TemporaryDirectory(prefix="laconic-stats-share-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            self._make_session_jsonl(claude_dir, [(400, "claude-sonnet-4-6")])
            result = self._run_node("hooks/laconic-stats.js", home, prompt="/laconic-stats --share")
            out = json.loads(result.stdout)
            self.assertEqual(out["decision"], "block")
            self.assertNotIn("\n", out["reason"])       # single line
            self.assertIn("laconic saved", out["reason"])

    # --- mode-tracker intercept ---

    def test_mode_tracker_intercepts_laconic_stats(self):
        with tempfile.TemporaryDirectory(prefix="laconic-tracker-stats-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            result = self._run_node("hooks/laconic-mode-tracker.js", home, prompt="/laconic-stats")
            self.assertEqual(result.returncode, 0)
            out = json.loads(result.stdout)
            self.assertEqual(out["decision"], "block")

    def test_mode_tracker_intercepts_laconic_stats_share(self):
        with tempfile.TemporaryDirectory(prefix="laconic-tracker-stats-share-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            result = self._run_node("hooks/laconic-mode-tracker.js", home, prompt="/laconic-stats --share")
            self.assertEqual(result.returncode, 0)
            out = json.loads(result.stdout)
            self.assertEqual(out["decision"], "block")

    def test_mode_tracker_does_not_intercept_other_prompts(self):
        with tempfile.TemporaryDirectory(prefix="laconic-tracker-passthrough-") as tmp:
            home = Path(tmp)
            claude_dir = home / ".claude"
            claude_dir.mkdir()
            result = self._run_node("hooks/laconic-mode-tracker.js", home, prompt="/laconic balanced")
            self.assertEqual(result.returncode, 0)
            # Should NOT be decision:block — mode tracking writes flag and returns context
            try:
                out = json.loads(result.stdout) if result.stdout.strip() else {}
            except json.JSONDecodeError:
                out = {}
            self.assertNotEqual(out.get("decision"), "block")
            self.assertEqual((claude_dir / ".laconic-active").read_text(), "balanced")


class OpenClawInstallerTests(unittest.TestCase):
    """Tests for OpenClaw detection and installation in hooks/install.sh."""

    def _run_install(self, home):
        env = os.environ.copy()
        env["HOME"] = str(home)
        env["USERPROFILE"] = str(home)
        return subprocess.run(
            ["bash", "hooks/install.sh"],
            cwd=REPO_ROOT,
            env=env,
            text=True,
            capture_output=True,
        )

    def test_install_skips_openclaw_when_workspace_absent(self):
        with tempfile.TemporaryDirectory(prefix="laconic-openclaw-absent-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            result = self._run_install(home)
            self.assertEqual(result.returncode, 0)
            self.assertFalse((home / ".openclaw").exists())
            self.assertNotIn("OpenClaw", result.stdout)

    def test_install_detects_openclaw_workspace_and_copies_skill(self):
        with tempfile.TemporaryDirectory(prefix="laconic-openclaw-present-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            openclaw_ws = home / ".openclaw" / "workspace"
            openclaw_ws.mkdir(parents=True)

            result = self._run_install(home)

            self.assertEqual(result.returncode, 0)
            skill_dest = openclaw_ws / "skills" / "laconic" / "SKILL.md"
            self.assertTrue(skill_dest.exists(), "skill file should be copied to OpenClaw workspace")
            self.assertIn("laconic", skill_dest.read_text().lower())

    def test_install_injects_soul_md_block(self):
        with tempfile.TemporaryDirectory(prefix="laconic-openclaw-soul-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            openclaw_ws = home / ".openclaw" / "workspace"
            openclaw_ws.mkdir(parents=True)

            self._run_install(home)

            soul = openclaw_ws / "SOUL.md"
            self.assertTrue(soul.exists(), "SOUL.md should be created")
            content = soul.read_text()
            self.assertIn("<!-- laconic-begin -->", content)
            self.assertIn("<!-- laconic-end -->", content)
            self.assertIn("laconic mode", content.lower())

    def test_install_soul_md_idempotent(self):
        """Running install twice must not duplicate the marker block."""
        with tempfile.TemporaryDirectory(prefix="laconic-openclaw-idem-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            openclaw_ws = home / ".openclaw" / "workspace"
            openclaw_ws.mkdir(parents=True)

            self._run_install(home)
            self._run_install(home)

            soul_text = (openclaw_ws / "SOUL.md").read_text()
            self.assertEqual(soul_text.count("<!-- laconic-begin -->"), 1,
                             "marker block must appear exactly once after two installs")

    def test_install_soul_md_appended_to_existing_content(self):
        """Existing SOUL.md content is preserved; block is appended."""
        with tempfile.TemporaryDirectory(prefix="laconic-openclaw-existing-") as tmp:
            home = Path(tmp)
            (home / ".claude").mkdir()
            openclaw_ws = home / ".openclaw" / "workspace"
            openclaw_ws.mkdir(parents=True)
            soul = openclaw_ws / "SOUL.md"
            soul.write_text("# Existing content\n\nSome rules already here.\n")

            self._run_install(home)

            content = soul.read_text()
            self.assertIn("# Existing content", content)
            self.assertIn("<!-- laconic-begin -->", content)


if __name__ == "__main__":
    unittest.main()
