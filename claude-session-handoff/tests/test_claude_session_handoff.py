from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "claude_session_handoff.py"
PROJECT_PATH = "/tmp/claude-session-handoff-project"


def write_session(path: Path, turns: list[dict[str, object]], mtime_iso: str) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for turn in turns:
            handle.write(
                json.dumps(
                    {
                        "type": turn["role"],
                        "timestamp": turn["timestamp"],
                        "cwd": PROJECT_PATH,
                        "sessionId": path.stem,
                        "message": {"content": turn["content"]},
                    }
                )
                + "\n"
            )

    dt = datetime.fromisoformat(mtime_iso.replace("Z", "+00:00"))
    os.utime(path, (dt.timestamp(), dt.timestamp()))


class ClaudeSessionHandoffTests(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory(prefix="claude-session-handoff-test-")
        self.addCleanup(self.temp_dir.cleanup)

        self.claude_root = Path(self.temp_dir.name) / "claude-projects"
        project_dir = self.claude_root / "example-project"
        project_dir.mkdir(parents=True)

        self.old_session = project_dir / "old.jsonl"
        self.new_session = project_dir / "new.jsonl"

        write_session(
            self.old_session,
            [
                {
                    "role": "user",
                    "timestamp": "2026-03-16T10:00:00Z",
                    "content": "old ask",
                },
                {
                    "role": "assistant",
                    "timestamp": "2026-03-16T10:01:00Z",
                    "content": [{"type": "text", "text": "old reply"}],
                },
            ],
            "2026-03-16T15:00:00Z",
        )
        write_session(
            self.new_session,
            [
                {
                    "role": "user",
                    "timestamp": "2026-03-17T09:00:00Z",
                    "content": "start new work",
                },
                {
                    "role": "assistant",
                    "timestamp": "2026-03-17T09:01:00Z",
                    "content": [{"type": "text", "text": "initial response"}],
                },
                {
                    "role": "assistant",
                    "timestamp": "2026-03-17T09:02:00Z",
                    "content": [{"type": "tool_use", "name": "Write"}],
                },
                {
                    "role": "user",
                    "timestamp": "2026-03-17T09:03:00Z",
                    "content": "anchor phrase here please continue",
                },
                {
                    "role": "assistant",
                    "timestamp": "2026-03-17T09:04:00Z",
                    "content": [{"type": "text", "text": "anchored response"}],
                },
                {
                    "role": "user",
                    "timestamp": "2026-03-17T09:05:00Z",
                    "content": "<local-command-stdout> hidden",
                },
                {
                    "role": "user",
                    "timestamp": "2026-03-17T09:06:00Z",
                    "content": "final ask",
                },
                {
                    "role": "assistant",
                    "timestamp": "2026-03-17T09:07:00Z",
                    "content": [{"type": "text", "text": "final response"}],
                },
            ],
            "2026-03-17T15:00:00Z",
        )

    def run_script(self, *args: str) -> str:
        return subprocess.check_output(
            [
                "python3",
                str(SCRIPT_PATH),
                "--claude-root",
                str(self.claude_root),
                *args,
            ],
            text=True,
        )

    def test_prefers_latest_same_repo_session(self) -> None:
        output = self.run_script("--project-path", PROJECT_PATH, "--turns", "3")

        self.assertIn(str(self.new_session), output)
        self.assertIn("Recent turns (last 3 of 6)", output)
        self.assertIn("final ask", output)
        self.assertNotIn("old ask", output)

    def test_filters_by_exact_date(self) -> None:
        output = self.run_script(
            "--project-path",
            PROJECT_PATH,
            "--date",
            "2026-03-16",
            "--turns",
            "2",
        )

        self.assertIn(str(self.old_session), output)
        self.assertIn("old ask", output)
        self.assertNotIn(str(self.new_session), output)

    def test_reads_from_anchor_phrase_without_full_transcript(self) -> None:
        output = self.run_script(
            "--project-path",
            PROJECT_PATH,
            "--contains",
            "anchor phrase",
            "--from-match",
        )

        self.assertIn(str(self.new_session), output)
        self.assertIn("Matched turn:", output)
        self.assertIn("Turns from match (4):", output)
        self.assertIn("anchor phrase here please continue", output)
        self.assertIn("final response", output)

        turns_section = output.split("Turns from match (4):", 1)[1]
        self.assertNotIn("start new work", turns_section)


if __name__ == "__main__":
    unittest.main()
