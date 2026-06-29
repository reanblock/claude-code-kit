# Plugins

Plugins are **bundles** of Claude Code components — commands, skills, agents, hooks, MCP servers and output styles — packaged together so they can be installed, versioned and shared as a single unit. Rather than copying individual files into `~/.claude/` (as the rest of this kit does), a plugin lets you install a whole feature set from a marketplace with one command and toggle it on or off.

## How plugins work

- A plugin is a directory containing a `.claude-plugin/plugin.json` manifest plus any of the standard component folders (`commands/`, `skills/`, `agents/`, `hooks/`, etc.).
- Plugins are distributed through **marketplaces** — a git repo (or local path) that exposes a catalogue of plugins. Anthropic ships an official marketplace in the [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/plugins) repo.
- Once a plugin is installed and enabled, its commands, skills and agents become available just as if they lived in your `~/.claude/` directory.

## Managing plugins

Use the `/plugin` command inside Claude Code to browse, install, enable, disable and remove plugins:

```text
/plugin
```

Add a marketplace, then install a plugin from it:

```bash
# Add the official Anthropic marketplace
/plugin marketplace add anthropics/claude-code

# Install a plugin from a marketplace
/plugin install feature-dev@anthropics/claude-code
```

## Recommended official plugins (from Anthropic)

These ship in the official [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/plugins) marketplace:

| Plugin | Description |
|--------|-------------|
| [feature-dev](https://github.com/anthropics/claude-code/tree/main/plugins/feature-dev) | Comprehensive feature development workflow with a structured 7-phase approach |
| [code-review](https://github.com/anthropics/claude-code/tree/main/plugins/code-review) | Automated PR code review using multiple specialized agents with confidence-based scoring |
| [pr-review-toolkit](https://github.com/anthropics/claude-code/tree/main/plugins/pr-review-toolkit) | PR review agents specializing in comments, tests, error handling and code quality |
| [commit-commands](https://github.com/anthropics/claude-code/tree/main/plugins/commit-commands) | Git workflow automation for committing, pushing and creating pull requests |
| [plugin-dev](https://github.com/anthropics/claude-code/tree/main/plugins/plugin-dev) | Toolkit for developing Claude Code plugins, with expert skills |
| [hookify](https://github.com/anthropics/claude-code/tree/main/plugins/hookify) | Create custom hooks to prevent unwanted behaviours by analysing conversation patterns |
| [security-guidance](https://github.com/anthropics/claude-code/tree/main/plugins/security-guidance) | Security reminder hook that warns about potential security issues when editing files |
| [frontend-design](https://github.com/anthropics/claude-code/tree/main/plugins/frontend-design) | Create distinctive, production-grade frontend interfaces that avoid generic AI aesthetics |
| [agent-sdk-dev](https://github.com/anthropics/claude-code/tree/main/plugins/agent-sdk-dev) | Development kit for working with the Claude Agent SDK |
| [plugin-context7](https://github.com/anthropics/claude-code/tree/main/plugins) | Context7 MCP integration for fetching up-to-date library documentation |

## Links

- Plugins documentation [here](https://code.claude.com/docs/en/plugins)
- Plugin marketplaces [here](https://code.claude.com/docs/en/plugin-marketplaces)
- Official Anthropic plugins [here](https://github.com/anthropics/claude-code/tree/main/plugins)
</content>
</invoke>
