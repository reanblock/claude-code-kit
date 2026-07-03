# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`claude-code-kit` is **not an application** — it is a curated collection of Claude Code configuration components (commands, skills, hooks, agents, output styles, status lines, prompts, MCP notes) that are installed into the user's `~/.claude/` directory. Editing files here changes how Claude Code itself behaves once installed. There is no build step and no test suite; correctness is verified by installing and running Claude Code.

## Install / deploy

```bash
./install.sh
```

`install.sh` **deletes** the target subdirectories in `~/.claude/` and replaces them with copies from this repo. The synced directories are hardcoded in the `DIRS` array: `skills commands hooks status_lines output-styles agents prompts`. It also copies `settings.json` to `~/.claude/settings.json` (backing up the existing one to `settings.json.bak`). **If you add a new top-level component directory that should ship, add it to the `DIRS` array in `install.sh` — otherwise it will not be installed.**

Note: the repo's own `settings.json` (root) is the file that gets installed globally; `.claude/settings.local.json` is local-only project config and is not distributed.

## Justfile — manual smoke tests

`just` recipes drive end-to-end checks of the browser/QA tooling by launching real `claude` sessions (they use `--dangerously-skip-permissions`):

```bash
just                       # list recipes
just test-playwright-skill # headless Playwright browser skill sanity check
just test-chrome-skill     # Chrome MCP skill (requires --chrome)
just test-qa               # bowser-qa-agent structured user-story validation
just ui-review             # parallel UI review across YAML stories in ai_review/user_stories/
```

These are integration smoke tests, not unit tests — they actually spawn agents and a browser.

## Component model — how the pieces relate

The top-level directories each map to a Claude Code extension mechanism. Key distinctions that require reading multiple files to grasp:

- **commands/** — *explicit* slash commands (`/explore`, `/plan`, `/build`). Plain markdown; subfolders namespace them (`commands/posts/new.md` → `/posts:new`) and support argument parsing.
- **skills/** — `<skill-name>/SKILL.md` with YAML frontmatter (`name`, `description`). *Inferred* from conversation rather than explicitly invoked. The `description` is what Claude matches against to decide relevance — it must clearly state when to trigger. Conceptually skills and commands are converging; the difference is explicit (`/`) vs. inferred invocation.
- **agents/** — subagent definitions with frontmatter (`name`, `description`, `tools`, `model`, `color`). `agents/team/` (builder, tester, validator) are the roles used by the experimental Agent Teams workflow.
- **hooks/** — Python lifecycle scripts (see below).
- **output-styles/**, **status_lines/**, **prompts/** — formatting, status bar scripts, and system prompts respectively.

### The plan → build workflow

The commands and team agents form a pipeline documented in `agents/README.md`:
`/explore` (understand a codebase) → `/plan` or `/plan_with_team` (writes a spec to `specs/`) → `/build` or the `build-with-team` skill (executes the spec, optionally with parallel builder/tester/validator agents in tmux). Agent Teams require `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` (set in `settings.json` `env`) and `teammateMode: tmux`.

## Hooks architecture

Hooks are standalone Python scripts run via `uv run` (PEP 723 inline script metadata — dependencies declared in the `# /// script` header, no separate venv). Every hook is wired in `settings.json` under `hooks.<EventName>` and references `~/.claude/hooks/<file>.py` (the *installed* path, not the repo path).

Conventions all hooks follow:
- Read a JSON event payload from **stdin**.
- **Exit code 2 blocks** the tool call and surfaces stderr to Claude; exit 0 allows. `pre_tool_use.py` uses this to block `rm -rf` variants and `.env` access.
- Fail **open**: wrap logic so any unexpected error `sys.exit(0)` rather than breaking the session.
- Append event payloads to JSON files under `logs/` (gitignored).

`hooks/validators/` are PostToolUse/Stop hooks that gate on quality (`ruff_validator.py`, `ty_validator.py` run linters/type checks on written Python and block on failure; `validate_new_file.py` / `validate_file_contains.py` assert expected output). `hooks/utils/` holds shared helpers: `llm/` (anth/oai/ollama prompt wrappers + task summarizer) and `tts/` (pyttsx3/openai/elevenlabs voice backends with a queue). LLM/TTS features are optional and degrade gracefully when API keys are absent.

## Conventions when adding components

- New hook → add the script under `hooks/`, register it in `settings.json`, and (if it's a documented hook) add a row to the table in `hooks/README.md`.
- New skill → `skills/<name>/SKILL.md` with frontmatter; write the `description` to make trigger conditions explicit.
- New ship-able top-level directory → add it to `DIRS` in `install.sh`.
- Python scripts use the `#!/usr/bin/env -S uv run --script` shebang with inline PEP 723 dependency blocks rather than a project-wide requirements file.

## Not tracked in git

`logs/`, `.claude/data/`, `.playwright-cli/`, and `screenshots/` are gitignored (see `.gitignore`). The `logs/*.json` files are runtime hook output samples, not source.
