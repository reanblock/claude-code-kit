# Skills

Skills are markdown files that provide Claude a set of instructions to perform a specific task. You can get Claude to create a new skill by simply asking it to! Remember to ask the question "What else should I clarify?" after sharing all the details about your new skill.

**NOTE**: Claude Desktop ships with the `skill-creator` skill enabled (under Settings -> Capabilities -> Skills).

The skill must be placed in the following folder structure: `.claude/skills/<skill-name>/SKILL.md`.

## Install


Use [skills.sh](https://skills.sh/) and then follow instructions.

For example:

```bash
npx skills add anthropics/skills
npx skills add coreyhaines31/marketingskills
```

**NOTE**: When installing skills vua `npx skills` it will install in the `.agents/skills` folder and creates a symlink from the `.claude/skills` folder so that Claude can detect it.

## Create Skill

You can also create your own custom skills using `npx sills`. For details run `npx skills --help` and check this tutorial [here](https://www.youtube.com/watch?v=rcRS8-7OgBo&t=581s).

## Available Skills

| Skill | Description |
|---|---|
| [audit-codebase](./audit-codebase/SKILL.md) | Core smart contract security audit — systematically reviews in-scope files across the full vulnerability taxonomy (access control, reentrancy, arithmetic, oracle manipulation, accounting, upgradeability, DoS), traces exploit paths, and produces a report with severity-rated findings. |
| [audit-false-positive-review](./audit-false-positive-review/SKILL.md) | Triages an **existing** audit report (or GitHub-issue findings) by independently re-verifying every finding against the source: classifies each as VALID, PARTIALLY VALID, FALSE POSITIVE (with category), INCONCLUSIVE, or OUT-OF-DATE, with code evidence and an FP rate. |
| [audit-prototype](./audit-prototype/SKILL.md) | Builds a fully mocked interactive prototype UI from smart contracts so auditors can explore protocol mechanics, admin levers, and token flows. No blockchain, wallet, or RPC connection — SQLite persistence and simulated activity. |
| [audit-scope](./audit-scope/SKILL.md) | Client audit scoping assessment: analyzes in-scope files for LoC, test and documentation quality, complexity, and external integrations, then produces a scoping report with estimated audit hours and BD feedback. |
| [audit-severity-review](./audit-severity-review/SKILL.md) | Reviews an existing audit report and recommends severity reassessments, focused on financial impact and DeFi exploitability. |
| [audit-verify-fixes](./audit-verify-fixes/SKILL.md) | Verifies whether client code changes actually resolve audit findings. Findings can come from a report file (PDF/markdown) or from GitHub issues in a repo. Read-only. |
| [audit-vuln-review](./audit-vuln-review/SKILL.md) | Reviews a single suspected vulnerability against a set of files: assesses validity (is it a real finding or a false positive), severity, fix approach, and whether the same pattern appears elsewhere in the repo. |
| [build-with-team](./build-with-team/SKILL.md) | Builds a project from a plan document using Claude Code Agent Teams in tmux split panes, spawning and orchestrating multiple collaborating agents. |
| [claude-bowser](./claude-bowser/SKILL.md) | Observable browser automation via Chrome MCP tools (`claude --chrome`) — browses, screenshots, and interacts with pages in your real Chrome profile. |
| [explain-code](./explain-code/SKILL.md) | Explains how code works using an everyday analogy, an ASCII diagram, a step-by-step walkthrough, and a common gotcha. |
| [flova](./flova/SKILL.md) | Planner prompt for the Flova AI video pipeline — turns an uploaded shooting script into a full video spec, storyboard, key elements, and per-character voice anchors. |
| [just](./just/SKILL.md) | How to use the `just` command runner to save and run project-specific recipes as a simpler alternative to `make`. |
| [playwright-bowser](./playwright-bowser/SKILL.md) | Headless browser automation via `playwright-cli` — parallel named sessions, UI testing, screenshots, and scraping without loading MCP tool schemas into context. |
| [startup-research](./startup-research/SKILL.md) | Researches a startup or product idea and produces a detailed markdown report covering market, competition, go-to-market, and MVP planning. |
| [story-to-video](./story-to-video/SKILL.md) | Converts narrated prose into a tool-agnostic Markdown shooting script (Asset Bible plus per-scene setting, camera, blocking, dialogue, music, sound) for AI text-to-video generators such as Sora, Runway, Veo, Pika, or Kling. |

## External Examples

- [Systematic Debugging](https://www.skills.sh/obra/superpowers/systematic-debugging)
- Explain Code Skill above is taken from the docs [here](https://code.claude.com/docs/en/skills)


## Links

- Claude Skills Docs [here](https://code.claude.com/docs/en/skills#extend-claude-with-skills)
- Anthropics official skills repo [here](https://github.com/anthropics/skills)
- Marketing skills repo [here](https://github.com/coreyhaines31/marketingskills)
- Agent Skills Standard Open Format [here](https://agentskills.io/)
- skills.sh install utility [here](https://skills.sh/)
- Claude Code Skills & Create new using skills.sh [here](https://www.youtube.com/watch?v=rcRS8-7OgBo)
- Complete Skills Guide [here](https://resources.anthropic.com/hubfs/The-Complete-Guide-to-Building-Skill-for-Claude.pdf?hsLang=en)
- Claude Skills Explained - Step-by-Step Tutorial for Beginners [here](https://www.youtube.com/watch?v=wO8EboopboU)
