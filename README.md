# Claude Code Kit

## Contents

| Feature | Description | Details |
|---------|-------------|---------|
| [Commands](./commands/README.md) | Custom slash commands invoked with `/` | Manual triggers for templates, audits, etc. |
| [Skills](./skills/README.md) | Markdown instruction files for specific tasks | Automatic behaviors inferred from conversation |
| [Plugins](./plugins/README.md) | Bundles of components installed from a marketplace | Commands, skills, agents & hooks packaged together |
| [MCP](./mcp/README.md) | Model Context Protocol integrations | External tools, services, and APIs |
| [Hooks](./hooks/README.md) | Shell commands triggered at lifecycle events | Pre/post tool use, session events, validators |
| [Agents](./agents/README.md) | CC Agent Teams Feature | Details of running Agent Teams in Tmux sessions |
| [Bowser](./bowser/README.md) | Browser Automation | AI driven browser automation for testing and everyday tasks |
| [Output Styles](./output-styles/README.md) | Custom output formatting | Bullet points, concise modes, etc. |
| [Status Line](./status_lines/README.md) | Custom status line displays | Real-time info in the Claude Code status bar |
| [Prompts](./prompts/README.md) | Custom system prompts that can be applied when claude is started up |
| [Dev Container](./devcontainer/README.md) | ToB Secure DevContainer | A secure and easy to use container for running CC dangerously! |
| [UI / UX Design](https://www.pencil.dev/) | Pencil | Dream on canvas. Land in code. |
| [Agent Sandbox](https://github.com/reanblock/agent-sandboxes/) | Run claude code agents in a secure [e2b](https://e2b.dev/) sandbox. |

## Install

Follow the recommended installation process [here](https://code.claude.com/docs/en/quickstart) to install Claude Code.

The following script will copy this repo `commands`, `hooks`, `output-styles`, `status_lines` and `skills` folders to your `~/.claude/skills`, `~/.claude/commands`, `~/.claude/hooks`, `~/.claude/status_lines` and `~/.claude/output-styles`.

```bash
./install.sh
```

## Basics

Below are some basics such as getting started, installation, CLI reference, different modes, and initiating a project.

- CLI reference [here](https://code.claude.com/docs/en/cli-reference)
- Plan Mode (shift+tab) [here](https://claudelog.com/mechanics/plan-mode/)
- Interactive Mode [here](https://code.claude.com/docs/en/interactive-mode#general-controls)
- Checkpointing [here](https://code.claude.com/docs/en/checkpointing)
- Use `plan` mode when starting new projects (toggle using tab+shift)
- Create a CLAUDE.md (and associated) files for context loading. Use `/init` command.

## Running Open Weights Models Locally

[Local LLM Setup](./local/README.md)

## Links

- [Agency Agents](https://github.com/msitarzewski/agency-agents)
- [BuildAtScale Claude Code Plugins](https://github.com/buildatscale-tv/claude-code-plugins)
- [Edmund's Claude Code Setup](https://github.com/edmund-io/edmunds-claude-code)
- [Vibe Coding Academy](https://www.vibecodingacademy.ai/)
- [Claude AI Developer Guide](https://claudeai.dev/)
- [Agentic Finance Review](https://github.com/disler/agentic-finance-review)

## Research

### Faceless / Wondercraft

- https://www.youtube.com/watch?v=ko7-69yddbo
- https://www.youtube.com/watch?v=H1Xq3aB5Yyk
- https://www.wondercraft.ai/?via=mrc

### OpenClaw

- https://docs.openclaw.ai/
- https://www.youtube.com/watch?v=3GrG-dOmrLU
- https://www.youtube.com/watch?v=BQRiw7VtabU

### AutoForge 

- https://autoforge.cc/
- https://www.youtube.com/watch?v=nKiPOxDpcJY
