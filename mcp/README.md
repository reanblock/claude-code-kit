# MCP

Model Context Protocol (MCP) are external integrations (local or remote) to provide Claude access to new tools, serviecsn, APIs etc.

To list the MCP servers installed run this in the terminal (or `/mcp` in Claude Code):

```bash
claude mcp list
```

## Install

To install a new MCP server, for example `context7` you follow the instructions [here](https://github.com/upstash/context7?tab=readme-ov-file#installation). For exmaple to install as a remote, http service run:

```bash
claude mcp add --header "CONTEXT7_API_KEY: YOUR_API_KEY" --transport http context7 https://mcp.context7.com/mcp
```

MCP servers for Claude Code are typically configured in one of these locations:

1. Project-level: `.mcp.json` in the project root
1. User-level: `~/.claude/settings.json` or `~/.claude/mcp.json`

## Links

- Glama [here](https://glama.ai/)
- MCP Sever Directory [here](https://mcpservers.org/)
- Chrome DevToops MCP [here](https://github.com/ChromeDevTools/chrome-devtools-mcp)
- Playwright MCP [here](https://github.com/microsoft/playwright-mcp)
- Vercel MCP [here](https://vercel.com/docs/ai-resources/vercel-mcp)
- Context7 MCP [here](https://github.com/upstash/context7)
- Repomix MCP [here](https://repomix.com/guide/)
