# Launch routes: evidence and gotchas

Checked against Claude Code 2.1.318, codex-cli 0.166.0 and T3 Code Nightly server 0.1.6 on macOS.
Deep-link and CLI behavior in these apps changes often; re-check when a route stops working.

## Claude Code -> Claude desktop

- Pre-minting `--session-id` means the id (and the desktop id `local_<uuid>`) is known before launch.
  Re-running with the same id fails with "Session ID ... is already in use", which guards against
  double launches.
- `claude://resume?session=<uuid>` imports the CLI session into the desktop Code tab; the sidebar
  title is `--name`. After import the stable link is `claude://claude.ai/epitaxy/local_<uuid>`.
- Opening mid-run makes the desktop warm its own process on the session while the CLI still
  writes. That's why the script opens only after the CLI exits.
- Launching from inside a Claude session passes that session's auth and wiring env vars
  (`CLAUDECODE`, `CLAUDE_CODE_*`, `ANTHROPIC_BASE_URL`) to the child; the script drops them so the
  nested CLI uses its own login.
- A folder Claude has never been trusted in can stop `-p` at a trust prompt; the script reports
  that as "never wrote its session file".
- `claude://code/new?q=&folder=` only prefills, and the folder shows a confirmation dialog. Don't use it.

## Codex -> Codex desktop (`com.openai.codex`)

- `codex exec --json` prints `{"type":"thread.started","thread_id":...}` first. Feed stdin from
  /dev/null or it waits on "Reading additional input from stdin".
- exec has no title flag. `thread/name/set` over `codex app-server --listen stdio://` sets it, and
  only works after the first turn has written its rollout, so the worker renames after exit.
- `codex://threads/<id>` loads the thread in the desktop app. Whether it shows a thread that is
  still running was not tested, so the link opens after exit.
- `codex://threads/new?prompt=&path=` only prefills.
- Pin `--model` if the default is rejected on a ChatGPT login (seen with older slugs).

## T3 Code

- `t3 thread start <project-or-path> <message|-> --json` returns the thread id with the prompt
  submitted. `--title`, `--provider` + `--model`, `--worktree` + `--branch`, `--wait` exist; there is
  no permission-mode flag (the project default applies).
- Use the bundled CLI at `~/.t3/bin/t3`; some older bundled versions lack the `thread` subcommand.
- `t3 project add <path>` registers a folder; the script runs it when `thread start` complains
  about the project, then retries once.
- The server address and pid are in `~/.t3/userdata/server-runtime.json`; the environment id for
  links is `~/.t3/userdata/environment-id`.
- T3 drives Claude through the Agent SDK and Codex through `codex app-server`, so its threads also
  land in `~/.claude/projects` and `~/.codex/sessions`.
- The T3 MCP server (`http://127.0.0.1:3773/mcp`: `t3_project_list`, `t3_thread_launch`,
  `t3_thread_read`, `t3_thread_send`) is the alternative when a session has it connected. It
  adds `runtimeMode` and `workspaceStrategy`.

## ChatGPT web chat

- `https://chatgpt.com/?q=` prefills the composer and creates no conversation. OpenAI added
  auto-submit protection (Tenable TRA-2025-22). Don't try DOM-injection auto-send.
- For ChatGPT-subscription work that should actually run, use `codex` instead.
