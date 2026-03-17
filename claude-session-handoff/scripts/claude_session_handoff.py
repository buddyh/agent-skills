#!/usr/bin/env python3
from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IGNORE_USER_PREFIXES = (
    "<local-command-caveat>",
    "<command-name>",
    "<local-command-stdout>",
    "<local-command-stderr>",
)


@dataclass
class SessionHeader:
    path: Path
    cwd: str | None
    session_id: str | None
    started_at: str | None
    modified_at: float


@dataclass
class Turn:
    role: str
    timestamp: str | None
    text: str


@dataclass
class SessionDetail:
    header: SessionHeader
    last_timestamp: str | None
    turns: list[Turn]


@dataclass
class MatchResult:
    index: int
    turn: Turn


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Find and summarize Claude Code JSONL sessions for handoff work."
    )
    parser.add_argument(
        "--claude-root",
        default="~/.claude/projects",
        help="Root directory containing Claude Code project session logs.",
    )
    parser.add_argument(
        "--project-path",
        default=".",
        help="Project path to match against the session cwd. Defaults to the current directory.",
    )
    parser.add_argument(
        "--session",
        help="Specific session JSONL file to inspect instead of searching by project path.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List matching sessions instead of printing the newest one in full.",
    )
    parser.add_argument(
        "--recent",
        type=int,
        default=0,
        help="List the N most recent top-level Claude sessions across all projects.",
    )
    parser.add_argument(
        "--turns",
        type=int,
        default=12,
        help="Number of meaningful turns to show in the summary output.",
    )
    parser.add_argument(
        "--date",
        help="Only consider sessions whose file modification date matches YYYY-MM-DD in local time.",
    )
    parser.add_argument(
        "--contains",
        help="Only consider sessions whose meaningful turns contain this phrase.",
    )
    parser.add_argument(
        "--from-match",
        action="store_true",
        help="When used with --contains, show turns from the most recent matching turn onward.",
    )
    parser.add_argument(
        "--width",
        type=int,
        default=150,
        help="Line width for shortened turn excerpts.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of human-readable text.",
    )
    return parser.parse_args()


def normalize_path(path_value: str) -> str:
    expanded = os.path.expanduser(path_value)
    if os.path.exists(expanded):
        return os.path.realpath(expanded)
    return os.path.abspath(expanded)


def sanitize_project_path(path_value: str) -> str:
    normalized = normalize_path(path_value)
    trimmed = normalized.strip(os.sep)
    if not trimmed:
        return "-"
    return f"-{trimmed.replace(os.sep, '-')}"


def iter_top_level_sessions(claude_root: Path) -> Iterable[Path]:
    if not claude_root.exists():
        return []
    return sorted(
        (
            path
            for path in claude_root.glob("*/*.jsonl")
            if "subagents" not in path.parts
        ),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )


def read_header(path: Path) -> SessionHeader:
    cwd = None
    session_id = None
    started_at = None
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for index, line in enumerate(handle):
                if index >= 40:
                    break
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                cwd = cwd or obj.get("cwd")
                session_id = session_id or obj.get("sessionId")
                started_at = started_at or obj.get("timestamp")
                if cwd and session_id and started_at:
                    break
    except OSError:
        pass
    return SessionHeader(
        path=path,
        cwd=cwd,
        session_id=session_id,
        started_at=started_at,
        modified_at=path.stat().st_mtime,
    )


def content_to_text(content: object) -> str:
    if isinstance(content, str):
        return normalize_whitespace(content)
    if not isinstance(content, list):
        return ""

    parts: list[str] = []
    for item in content:
        if isinstance(item, str):
            parts.append(item)
            continue
        if not isinstance(item, dict):
            continue
        item_type = item.get("type")
        if item_type == "text":
            parts.append(item.get("text", ""))
        elif item_type == "image":
            parts.append("[image]")
        elif item_type == "thinking":
            parts.append("[thinking]")
        elif item_type == "tool_use":
            name = item.get("name", "tool")
            parts.append(f"[tool_use {name}]")
        elif item_type == "tool_result":
            parts.append("[tool_result]")
    return normalize_whitespace(" ".join(parts))


def normalize_whitespace(text: str) -> str:
    return " ".join(text.replace("\r", " ").split())


def is_meaningful_turn(turn: Turn) -> bool:
    if not turn.text:
        return False
    if turn.role == "user" and turn.text.startswith(IGNORE_USER_PREFIXES):
        return False
    if turn.role == "assistant" and turn.text in {"[thinking]", "[tool_result]"}:
        return False
    if turn.role == "assistant" and turn.text.startswith("[tool_use "):
        return False
    return True


def read_session_detail(path: Path) -> SessionDetail:
    header = read_header(path)
    turns: list[Turn] = []
    last_timestamp = header.started_at
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue

                timestamp = obj.get("timestamp")
                if timestamp:
                    last_timestamp = timestamp

                if obj.get("type") not in {"user", "assistant"}:
                    continue

                message = obj.get("message", {})
                text = content_to_text(message.get("content", []))
                turn = Turn(role=obj["type"], timestamp=timestamp, text=text)
                if is_meaningful_turn(turn):
                    turns.append(turn)
    except OSError:
        pass

    return SessionDetail(header=header, last_timestamp=last_timestamp, turns=turns)


def format_mtime(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp).isoformat(timespec="seconds")


def matches_date(header: SessionHeader, date_value: str | None) -> bool:
    if not date_value:
        return True
    return datetime.fromtimestamp(header.modified_at).date().isoformat() == date_value


def find_matching_sessions(
    claude_root: Path, project_path: str, date_value: str | None
) -> list[SessionHeader]:
    target = normalize_path(project_path)
    matches: list[SessionHeader] = []
    seen: set[Path] = set()

    for path in iter_top_level_sessions(claude_root):
        header = read_header(path)
        if (
            header.cwd
            and normalize_path(header.cwd) == target
            and matches_date(header, date_value)
        ):
            matches.append(header)
            seen.add(path)

    if matches:
        return matches

    fallback_dir = claude_root / sanitize_project_path(project_path)
    if fallback_dir.exists():
        for path in sorted(
            fallback_dir.glob("*.jsonl"),
            key=lambda item: item.stat().st_mtime,
            reverse=True,
        ):
            if path not in seen:
                header = read_header(path)
                if matches_date(header, date_value):
                    matches.append(header)

    return matches


def list_recent_sessions(
    claude_root: Path, limit: int, date_value: str | None
) -> list[SessionHeader]:
    recent: list[SessionHeader] = []
    for path in iter_top_level_sessions(claude_root):
        header = read_header(path)
        if not matches_date(header, date_value):
            continue
        recent.append(header)
        if len(recent) >= limit:
            break
    return recent


def shorten(text: str, width: int) -> str:
    return textwrap.shorten(text, width=width, placeholder=" ...") if text else ""


def find_latest_match(detail: SessionDetail, needle: str | None) -> MatchResult | None:
    if not needle:
        return None

    normalized_needle = normalize_whitespace(needle).lower()
    for index in range(len(detail.turns) - 1, -1, -1):
        turn = detail.turns[index]
        if normalized_needle in turn.text.lower():
            return MatchResult(index=index, turn=turn)
    return None


def build_json_payload(
    detail: SessionDetail, shown_turns: list[Turn], match: MatchResult | None
) -> dict[str, object]:
    first_user = next((turn for turn in detail.turns if turn.role == "user"), None)
    latest_user = next((turn for turn in reversed(detail.turns) if turn.role == "user"), None)
    latest_assistant = next(
        (turn for turn in reversed(detail.turns) if turn.role == "assistant"),
        None,
    )
    return {
        "session_path": str(detail.header.path),
        "project_cwd": detail.header.cwd,
        "session_id": detail.header.session_id,
        "started_at": detail.header.started_at,
        "last_timestamp": detail.last_timestamp,
        "turn_count": len(detail.turns),
        "first_user": first_user.text if first_user else None,
        "latest_user": latest_user.text if latest_user else None,
        "latest_assistant": latest_assistant.text if latest_assistant else None,
        "matched_turn": (
            {
                "index": match.index,
                "role": match.turn.role,
                "timestamp": match.turn.timestamp,
                "text": match.turn.text,
            }
            if match
            else None
        ),
        "shown_turns": [
            {
                "role": turn.role,
                "timestamp": turn.timestamp,
                "text": turn.text,
            }
            for turn in shown_turns
        ],
    }


def print_list(
    headers: list[SessionHeader],
    detail_by_path: dict[Path, MatchResult | None] | None = None,
) -> None:
    if not headers:
        print("No matching Claude sessions found.")
        return
    for header in headers:
        modified = format_mtime(header.modified_at)
        line = f"{modified}  {header.path}"
        if detail_by_path and header.path in detail_by_path and detail_by_path[header.path]:
            match = detail_by_path[header.path]
            assert match is not None
            line += f"  [match {match.turn.timestamp or '-'}]"
        print(line)


def print_detail(
    detail: SessionDetail,
    turns_to_show: int,
    width: int,
    match: MatchResult | None,
    from_match: bool,
) -> None:
    print(f"Selected session: {detail.header.path}")
    if detail.header.cwd:
        print(f"Project cwd:     {detail.header.cwd}")
    if detail.header.session_id:
        print(f"Session ID:      {detail.header.session_id}")
    if detail.header.started_at:
        print(f"Started:         {detail.header.started_at}")
    if detail.last_timestamp:
        print(f"Last activity:   {detail.last_timestamp}")
    print(f"Meaningful turns:{len(detail.turns):>5}")
    if match:
        print(f"Matched turn:    {match.index}  {match.turn.role}  {match.turn.timestamp or '-'}")
        print(f"Matched text:    {shorten(match.turn.text, width)}")

    if not detail.turns:
        return

    first_user = next((turn for turn in detail.turns if turn.role == "user"), None)
    latest_user = next((turn for turn in reversed(detail.turns) if turn.role == "user"), None)
    latest_assistant = next(
        (turn for turn in reversed(detail.turns) if turn.role == "assistant"),
        None,
    )

    if first_user:
        print("\nInitial user ask:")
        print(f"  {first_user.text}")
    if latest_user and latest_user is not first_user:
        print("\nLatest user ask:")
        print(f"  {latest_user.text}")
    if latest_assistant:
        print("\nLatest assistant reply:")
        print(f"  {latest_assistant.text}")

    if match and from_match:
        shown_turns = detail.turns[match.index :]
    else:
        shown_turns = detail.turns[-turns_to_show:]

    if match and from_match:
        print(f"\nTurns from match ({len(shown_turns)}):")
    elif len(shown_turns) < len(detail.turns):
        print(f"\nRecent turns (last {len(shown_turns)} of {len(detail.turns)}):")
    else:
        print("\nTurns:")

    start_index = match.index if match and from_match else len(detail.turns) - len(shown_turns)
    for index, turn in enumerate(shown_turns, start=start_index):
        excerpt = shorten(turn.text, width)
        timestamp = turn.timestamp or "-"
        print(f"{index:>3}  {turn.role:<9} {timestamp}  {excerpt}")


def main() -> int:
    args = parse_args()
    claude_root = Path(os.path.expanduser(args.claude_root))

    if args.from_match and not args.contains:
        raise SystemExit("--from-match requires --contains.")
    if args.date:
        try:
            datetime.strptime(args.date, "%Y-%m-%d")
        except ValueError as exc:
            raise SystemExit("--date must be in YYYY-MM-DD format.") from exc

    if args.recent > 0:
        recent = list_recent_sessions(claude_root, args.recent, args.date)
        detail_by_path: dict[Path, MatchResult | None] | None = None
        if args.contains:
            detail_by_path = {}
            filtered: list[SessionHeader] = []
            for header in recent:
                detail = read_session_detail(header.path)
                match = find_latest_match(detail, args.contains)
                if match:
                    filtered.append(header)
                    detail_by_path[header.path] = match
            recent = filtered
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "session_path": str(header.path),
                            "project_cwd": header.cwd,
                            "session_id": header.session_id,
                            "started_at": header.started_at,
                            "modified_at": header.modified_at,
                        }
                        for header in recent
                    ],
                    indent=2,
                )
            )
        else:
            print_list(recent, detail_by_path)
        return 0

    if args.session:
        session_path = Path(os.path.expanduser(args.session))
        if not session_path.exists():
            raise SystemExit(f"Session file not found: {session_path}")
        matches = [read_header(session_path)]
    else:
        matches = find_matching_sessions(claude_root, args.project_path, args.date)

    detail_cache: dict[Path, SessionDetail] = {}
    detail_by_path: dict[Path, MatchResult | None] | None = None
    if args.contains:
        detail_by_path = {}
        filtered_matches: list[SessionHeader] = []
        for header in matches:
            detail = read_session_detail(header.path)
            detail_cache[header.path] = detail
            match = find_latest_match(detail, args.contains)
            if match:
                filtered_matches.append(header)
                detail_by_path[header.path] = match
        matches = filtered_matches

    if args.list:
        if args.json:
            print(
                json.dumps(
                    [
                        {
                            "session_path": str(header.path),
                            "project_cwd": header.cwd,
                            "session_id": header.session_id,
                            "started_at": header.started_at,
                            "modified_at": header.modified_at,
                        }
                        for header in matches
                    ],
                    indent=2,
                )
            )
        else:
            print_list(matches, detail_by_path)
        return 0

    if not matches:
        print("No matching Claude sessions found.")
        print("Try --recent 10 to inspect recent sessions across all projects.")
        return 1

    selected_path = matches[0].path
    detail = detail_cache.get(selected_path) or read_session_detail(selected_path)
    match = find_latest_match(detail, args.contains)
    if match and args.from_match:
        shown_turns = detail.turns[match.index :]
    else:
        shown_turns = detail.turns[-args.turns :]

    if args.json:
        print(json.dumps(build_json_payload(detail, shown_turns, match), indent=2))
    else:
        print_detail(detail, args.turns, args.width, match, args.from_match)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
