# Workspace setup

One-command bootstrap for a fully equipped dev box — built for the
code-server VPS, but works on any Ubuntu/Debian machine.

## Quick start

From the code-server terminal:

```bash
git clone https://github.com/3p4e/3p4e
cd 3p4e
./setup/bootstrap.sh      # system packages, Node 22, Higgsfield CLI, Claude Code, skills
./setup/hf-auth-remote.sh # authenticate the Higgsfield CLI (headless-safe)
claude                    # authenticate Claude Code, then just start working
```

Re-running `bootstrap.sh` is safe — it skips anything already installed.

## What gets installed

| Layer | Contents |
|---|---|
| System | git, curl, jq, ripgrep, tmux, build-essential, python3 (+pip/venv), **ffmpeg**, **imagemagick** |
| Node | Node 22 via nvm (user-local, so `npm -g` needs no sudo) |
| CLIs | `@higgsfield/cli` (image/video/audio generation), `@anthropic-ai/claude-code` |
| Skills | the 8 Higgsfield companion skills, vendored in this repo under `.agents/skills/` |
| Editor | code-server extensions: Python, ESLint, Prettier (skipped when code-server is absent) |

Everything else is installed **on demand**: with Claude Code running in the
terminal, per-project dependencies (a Python venv, a Rust toolchain, a
database client…) get added when a task actually needs them, which keeps the
base image lean and never out of date.

## Higgsfield auth on a remote box

`higgsfield auth login` redirects the browser to `http://localhost:8765/callback`.
On a remote machine that redirect lands on *your* laptop instead of the server,
so the plain login hangs. Two working options:

1. **`./setup/hf-auth-remote.sh`** (recommended) — prints the sign-in URL,
   you approve in your browser, then paste the failed `localhost:8765/callback?...`
   URL back into the prompt. The script delivers it to the waiting CLI locally.
2. **SSH port forward** — connect with `ssh -L 8765:localhost:8765 user@server`,
   then run `higgsfield auth login` normally; the redirect tunnels through.

Credentials persist on the VPS (unlike ephemeral cloud sessions), so this is
a one-time step per machine.
