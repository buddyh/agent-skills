#!/usr/bin/env python3
"""Launch a new agent thread with its prompt already submitted, and hand back a link that opens it
in the matching desktop app.

    launch_thread.py claude  --cwd DIR [--title T] [--model M] [--mode acceptEdits] "PROMPT"
    launch_thread.py codex   --cwd DIR [--title T] [--model M] [--sandbox workspace-write] "PROMPT"
    launch_thread.py t3      --cwd DIR [--title T] [--provider P --model M] [--worktree BASE [--branch B]] "PROMPT"
    launch_thread.py chatgpt "PROMPT"            # prefill only: the user presses Enter

PROMPT may be "-" to read it from stdin.

Routes (see ../references/routes.md for evidence and gotchas):
  claude   claude -p --session-id <uuid> --name <title>, run detached; when it exits,
           open claude://resume?session=<uuid> (imports it into the Claude desktop Code tab)
  codex    codex exec --json -C <dir>, run detached; when it exits, set the title through
           `codex app-server` thread/name/set, then open codex://threads/<id> (ChatGPT.app)
  t3       t3 thread start <dir> <msg> --json (adds the T3 project first if needed), then
           open t3code://threads/<environment-id>/<thread-id> right away; T3 shows it live
  chatgpt  open https://chatgpt.com/?q=<prompt>; ChatGPT blocks auto-submit, so this only prefills

Every launch gets a run folder under ~/.local/state/cross-app-thread-launch/runs/ with launch.log,
receipt.jsonl (the agent's own output) and manifest.json. The last lines printed are:
    Thread: <id>
    Open: <url>
    Run: <run folder>
A non-zero exit means nothing was launched.

macOS only: links are opened with `open`.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import logging
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
import uuid
from pathlib import Path

STATE = Path(os.environ.get("THREAD_LAUNCH_HOME",
                           Path.home() / ".local/state/cross-app-thread-launch"))
T3_HOME = Path(os.environ.get("T3CODE_HOME", Path.home() / ".t3"))
T3_APP_NAMES = [os.environ["T3_APP_NAME"]] if os.environ.get("T3_APP_NAME") else [
    "T3 Code", "T3 Code (Nightly)"]
CODEX_THREAD_WAIT = 60  # seconds to wait for codex exec to report its thread id
log = logging.getLogger("cross-app-thread-launch")


# ---------------------------------------------------------------- run folder + logging

def make_run_dir(app: str, title: str) -> Path:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:40] or "thread"
    run = STATE / "runs" / f"{dt.datetime.now():%Y-%m-%d_%H%M%S}__{app}-{slug}"
    run.mkdir(parents=True, exist_ok=True)
    latest = STATE / "latest"
    if latest.is_symlink() or latest.exists():
        latest.unlink()
    latest.symlink_to(run)
    return run


def setup_logging(run: Path, to_stdout: bool = True) -> None:
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S")
    log.setLevel(logging.INFO)
    fh = logging.FileHandler(run / "launch.log")
    fh.setFormatter(fmt)
    log.addHandler(fh)
    if to_stdout:
        sh = logging.StreamHandler(sys.stderr)
        sh.setFormatter(fmt)
        log.addHandler(sh)


def save_manifest(run: Path, manifest: dict) -> None:
    (run / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")


def finish(thread: str, url: str, run: Path) -> None:
    print(f"Thread: {thread}")
    print(f"Open: {url}")
    print(f"Run: {run}")


def fail(msg: str) -> None:
    log.error(msg)
    print(f"Not launched: {msg}", file=sys.stderr)
    sys.exit(1)


def title_from(prompt: str) -> str:
    first = prompt.strip().splitlines()[0] if prompt.strip() else "thread"
    return first[:60]


def open_url(url: str) -> None:
    subprocess.run(["open", url], check=False)


def spawn_worker(run: Path) -> None:
    """Re-run this script detached as the worker that owns the agent process for this run."""
    subprocess.Popen([sys.executable, os.path.abspath(__file__), "_worker", str(run)],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True)


# ---------------------------------------------------------------- claude

def launch_claude(a, prompt: str, run: Path) -> None:
    if not shutil.which("claude"):
        fail("the claude CLI is not on PATH")
    sid = str(uuid.uuid4())
    cmd = ["claude", "-p", prompt, "--session-id", sid, "--name", a.title,
           "--output-format", "stream-json", "--verbose", "--permission-mode", a.mode]
    if a.model:
        cmd += ["--model", a.model]
    url = f"claude://resume?session={sid}"
    save_manifest(run, {"app": "claude", "cwd": a.cwd, "title": a.title, "thread": sid, "url": url,
                        "open": not a.no_open, "cmd": cmd,
                        "env_unset": ["claude"]})
    log.info("starting claude session %s in %s", sid, a.cwd)
    spawn_worker(run)
    # The session file appears once the CLI has started; wait briefly so a bad cwd or a trust
    # prompt is reported as a failure instead of a silent non-launch.
    deadline = time.time() + 30
    while time.time() < deadline:
        if list((Path.home() / ".claude/projects").glob(f"*/{sid}.jsonl")):
            log.info("session file written")
            # Auth and API errors end the run within a few seconds; catch them here.
            settle = time.time() + 8
            while time.time() < settle and not (run / "worker.exit").exists():
                time.sleep(0.5)
            err = early_claude_error(run)
            if err:
                fail(f"claude started but its first turn failed: {err}")
            return finish(sid, url, run)
        if (run / "worker.exit").exists():
            break
        time.sleep(1)
    fail(f"claude never wrote its session file; see {run}/receipt.jsonl and {run}/launch.log")


def early_claude_error(run: Path) -> str | None:
    """The error text if the run already ended with is_error, else None."""
    exit_file = run / "worker.exit"
    if not exit_file.exists() or exit_file.read_text().strip() == "0":
        return None
    for line in reversed((run / "receipt.jsonl").read_text(errors="replace").splitlines()):
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "result" and ev.get("is_error"):
            return str(ev.get("result") or ev.get("terminal_reason") or "unknown error")[:400]
    return f"claude exited rc={exit_file.read_text().strip()}"


# ---------------------------------------------------------------- codex

def launch_codex(a, prompt: str, run: Path) -> None:
    if not shutil.which("codex"):
        fail("the codex CLI is not on PATH")
    cmd = ["codex", "exec", "--json", "-C", a.cwd, "-s", a.sandbox, "--skip-git-repo-check"]
    if a.model:
        cmd += ["-m", a.model]
    cmd.append(prompt)
    save_manifest(run, {"app": "codex", "cwd": a.cwd, "title": a.title, "open": not a.no_open,
                        "cmd": cmd, "env_unset": []})
    log.info("starting codex exec in %s", a.cwd)
    spawn_worker(run)
    receipt = run / "receipt.jsonl"
    deadline = time.time() + CODEX_THREAD_WAIT
    while time.time() < deadline:
        if receipt.exists():
            for line in receipt.read_text(errors="replace").splitlines():
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") == "thread.started" and ev.get("thread_id"):
                    tid = ev["thread_id"]
                    log.info("codex thread %s started", tid)
                    return finish(tid, f"codex://threads/{tid}", run)
        if (run / "worker.exit").exists():
            break
        time.sleep(0.5)
    fail(f"codex exec reported no thread id; see {receipt}")


def codex_rename(tid: str, name: str) -> bool:
    """thread/name/set over a private `codex app-server` (exec has no title flag)."""
    p = subprocess.Popen(["codex", "app-server", "--listen", "stdio://"], stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, bufsize=1)

    def send(o):
        p.stdin.write(json.dumps(o) + "\n")
        p.stdin.flush()

    def wait(i):
        t = time.time()
        while time.time() - t < 20:
            line = p.stdout.readline()
            if not line:
                return None
            try:
                m = json.loads(line)
            except ValueError:
                continue
            if m.get("id") == i:
                return m
        return None

    try:
        send({"jsonrpc": "2.0", "id": 1, "method": "initialize",
              "params": {"clientInfo": {"name": "cross-app-thread-launch", "version": "1"}}})
        if not wait(1):
            return False
        send({"jsonrpc": "2.0", "method": "initialized"})
        send({"jsonrpc": "2.0", "id": 2, "method": "thread/name/set",
              "params": {"threadId": tid, "name": name}})
        r = wait(2)
        return bool(r) and "error" not in r
    finally:
        p.terminate()


# ---------------------------------------------------------------- t3

def t3_bin() -> str:
    b = T3_HOME / "bin/t3"
    if b.exists():
        return str(b)
    return shutil.which("t3") or fail("the T3 CLI was not found at ~/.t3/bin/t3 or on PATH")


def t3_server_up() -> bool:
    rt = T3_HOME / "userdata/server-runtime.json"
    try:
        os.kill(json.loads(rt.read_text())["pid"], 0)
        return True
    except (OSError, ValueError, KeyError):
        return False


T3_DEFAULT_PROVIDER = "claudeAgent"  # used when the T3 project has no default model


def t3_first_model(provider: str) -> str | None:
    """First model slug T3's own provider cache lists, so the pick matches this T3 build."""
    try:
        cache = json.loads((T3_HOME / "caches" / f"{provider}.json").read_text())
    except (OSError, ValueError):
        return None
    for m in cache.get("models") or []:
        slug = m.get("slug") if isinstance(m, dict) else None
        if slug:
            return slug
    return None


def launch_t3(a, prompt: str, run: Path) -> None:
    t3 = t3_bin()
    if a.provider and not a.model:
        a.model = t3_first_model(a.provider) or fail(f"T3 lists no models for provider {a.provider}")
    if not t3_server_up():
        for name in T3_APP_NAMES:
            if subprocess.run(["open", "-a", name], capture_output=True).returncode == 0:
                log.info("T3 Code is not running; opened %s", name)
                break
        else:
            fail("T3 Code is not running and could not be opened (set T3_APP_NAME)")
        for _ in range(30):
            time.sleep(1)
            if t3_server_up():
                break
        else:
            fail("T3 Code did not start its server within 30 s")
    def build_cmd():
        cmd = [t3, "thread", "start", a.cwd, "-", "--json", "--title", a.title]
        if a.provider:
            cmd += ["--provider", a.provider, "--model", a.model]
        elif a.model:
            cmd += ["--model", a.model]
        if a.worktree:
            cmd += ["--worktree", a.worktree]
        if a.branch:
            cmd += ["--branch", a.branch]
        return cmd

    def start():
        c = build_cmd()
        log.info("running: %s", " ".join(c[:4] + ["<prompt>"] + c[5:]))
        return c, subprocess.run(c, input=prompt, capture_output=True, text=True, cwd=a.cwd)

    cmd, r = start()
    err = (r.stderr + r.stdout)
    if r.returncode != 0 and re.search(r"no (active )?project|project not found|unknown project", err, re.I):
        log.info("no T3 project for %s; adding it", a.cwd)
        add = subprocess.run([t3, "project", "add", a.cwd], capture_output=True, text=True)
        log.info("t3 project add: rc=%s %s", add.returncode, (add.stdout + add.stderr).strip()[:300])
        cmd, r = start()
        err = (r.stderr + r.stdout)
    if r.returncode != 0 and "no default model" in err and not a.provider:
        a.provider = T3_DEFAULT_PROVIDER
        a.model = t3_first_model(a.provider) or fail("the T3 project has no default model and "
                                                     f"T3 lists none for {a.provider}")
        log.info("project has no default model; using %s / %s", a.provider, a.model)
        cmd, r = start()
    (run / "receipt.jsonl").write_text(r.stdout)
    if r.returncode != 0:
        fail(f"t3 thread start failed (rc={r.returncode}): {(r.stderr or r.stdout).strip()[:500]}")
    try:
        out = json.loads(r.stdout)
    except ValueError:
        fail(f"t3 thread start printed no JSON: {r.stdout[:300]}")
    tid = out.get("threadId") or out.get("thread", {}).get("id")
    if not tid:
        fail(f"t3 thread start returned no threadId: {r.stdout[:300]}")
    env_file = T3_HOME / "userdata/environment-id"
    env = env_file.read_text().strip() if env_file.exists() else ""
    q = lambda s: urllib.parse.quote(s, safe="-._~")  # RFC 3986 unreserved only
    url = f"t3code://threads/{q(env)}/{q(tid)}" if env else "t3code://"
    save_manifest(run, {"app": "t3", "cwd": a.cwd, "title": a.title, "thread": tid, "url": url,
                        "cmd": cmd, "result": out})
    log.info("t3 thread %s started", tid)
    if not a.no_open:
        open_url(url)
    finish(tid, url, run)


# ---------------------------------------------------------------- chatgpt

def launch_chatgpt(a, prompt: str, run: Path) -> None:
    url = "https://chatgpt.com/?q=" + urllib.parse.quote(prompt)
    save_manifest(run, {"app": "chatgpt", "title": a.title, "url": url, "prefill_only": True})
    log.info("opening ChatGPT with the prompt prefilled (ChatGPT does not allow auto-submit)")
    if not a.no_open:
        open_url(url)
    finish("(none: prefilled, waiting for you to press Enter)", url, run)


# ---------------------------------------------------------------- detached worker

def clean_env(unset: list[str]) -> dict:
    """Environment for the agent. A Claude session hands its children its own host auth and session
    wiring (ANTHROPIC_BASE_URL, CLAUDE_CODE_*); a nested `claude` then authenticates as the host
    and fails once that login expires. Drop all of it so the CLI uses its own login."""
    env = {k: v for k, v in os.environ.items() if k not in unset}
    if "claude" in unset or os.environ.get("CLAUDECODE"):
        for k in list(env):
            if k.startswith(("CLAUDE_CODE_", "CLAUDE_AGENT_SDK_", "CLAUDE_ENV_")) or k in (
                    "CLAUDECODE", "CLAUDE_PID", "CLAUDE_EFFORT", "ANTHROPIC_BASE_URL"):
                env.pop(k)
    return env


def worker(run: Path) -> None:
    """Own the agent process, then rename/open once it exits (opening mid-run makes the Claude
    desktop run a second process on the same session, and Codex shows a finished thread only)."""
    setup_logging(run, to_stdout=False)
    m = json.loads((run / "manifest.json").read_text())
    env = clean_env(m.get("env_unset", []))
    rc = -1
    try:
        with open(run / "receipt.jsonl", "w") as out:
            rc = subprocess.run(m["cmd"], cwd=m["cwd"], env=env, stdin=subprocess.DEVNULL,
                                stdout=out, stderr=subprocess.STDOUT).returncode
        log.info("%s exited rc=%s", m["app"], rc)
        url = m.get("url")
        if m["app"] == "codex":
            tid = None
            for line in (run / "receipt.jsonl").read_text(errors="replace").splitlines():
                try:
                    ev = json.loads(line)
                except ValueError:
                    continue
                if ev.get("type") == "thread.started":
                    tid = ev.get("thread_id")
                    break
            if tid:
                url = f"codex://threads/{tid}"
                ok = codex_rename(tid, m["title"])
                log.info("codex rename to %r: %s", m["title"], "ok" if ok else "failed")
        if url and m.get("open"):
            open_url(url)
            log.info("opened %s", url)
    finally:
        (run / "worker.exit").write_text(str(rc))


# ---------------------------------------------------------------- main

def main() -> None:
    if len(sys.argv) == 3 and sys.argv[1] == "_worker":
        return worker(Path(sys.argv[2]))
    p = argparse.ArgumentParser(description="Launch an agent thread with its prompt submitted.")
    p.add_argument("app", choices=["claude", "codex", "t3", "chatgpt"])
    p.add_argument("prompt", help='the first message, or "-" for stdin')
    p.add_argument("--cwd", default=os.getcwd(), help="project folder (default: current)")
    p.add_argument("--title", help="thread title (default: first line of the prompt)")
    p.add_argument("--model")
    p.add_argument("--mode", default="acceptEdits",
                   help="claude --permission-mode (default acceptEdits)")
    p.add_argument("--sandbox", default="workspace-write",
                   help="codex exec --sandbox (default workspace-write)")
    p.add_argument("--provider", help="t3 provider instance, e.g. claudeAgent or codex")
    p.add_argument("--worktree", help="t3: run in a new git worktree from this base ref")
    p.add_argument("--branch", help="t3: branch name for --worktree")
    p.add_argument("--no-open", action="store_true", help="launch but do not open the app")
    a = p.parse_args()

    prompt = sys.stdin.read() if a.prompt == "-" else a.prompt
    if not prompt.strip():
        sys.exit("Not launched: empty prompt")
    a.cwd = str(Path(a.cwd).expanduser().resolve())
    if not Path(a.cwd).is_dir():
        sys.exit(f"Not launched: {a.cwd} is not a folder")
    a.title = a.title or title_from(prompt)

    run = make_run_dir(a.app, a.title)
    setup_logging(run)
    log.info("app=%s cwd=%s title=%r", a.app, a.cwd, a.title)
    {"claude": launch_claude, "codex": launch_codex, "t3": launch_t3,
     "chatgpt": launch_chatgpt}[a.app](a, prompt, run)


if __name__ == "__main__":
    main()
