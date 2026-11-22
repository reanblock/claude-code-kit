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
| [cc-skill-security-review](./cc-skill-security-review/SKILL.md) | Security checklist for application code: secrets, input validation, SQL injection, auth, XSS, CSRF, rate limiting, data exposure and dependencies. Use when writing auth, API endpoints, uploads or payment code. From [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills). |
| [claude-bowser](./claude-bowser/SKILL.md) | Observable browser automation via Chrome MCP tools (`claude --chrome`) — browses, screenshots, and interacts with pages in your real Chrome profile. |
| [devops-engineer](./devops-engineer/SKILL.md) | Writes Dockerfiles, CI/CD pipelines (GitHub Actions, GitLab CI), Kubernetes manifests and Terraform/Pulumi templates, and covers deployment strategies, GitOps, release automation, incident-response runbooks and platform engineering. By [Jeffallan](https://github.com/Jeffallan). |
| [explain-code](./explain-code/SKILL.md) | Explains how code works using an everyday analogy, an ASCII diagram, a step-by-step walkthrough, and a common gotcha. |
| [firebase-expert](./firebase-expert/SKILL.md) | Builds, secures and reviews Firebase apps: Firestore modelling, indexes and cost control, Security Rules with emulator tests, Authentication, Cloud Functions (2nd gen), App Check, and Hosting/App Hosting deploys. Use for `firebase.json`, `firestore.rules` and similar files, or for permission-denied and missing-index errors. By [Jeffallan](https://github.com/Jeffallan). |
| [flova](./flova/SKILL.md) | Planner prompt for the Flova AI video pipeline — turns an uploaded shooting script into a full video spec, storyboard, key elements, and per-character voice anchors. |
| [gha-security-review](./gha-security-review/SKILL.md) | Reviews GitHub Actions workflows for exploitable vulnerabilities (pwn requests, expression injection, secrets and permissions, supply chain), with attack paths and harmless proof-of-concept sketches. Active testing needs explicit authorization. From [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills). |
| [incident-runbook-templates](./incident-runbook-templates/SKILL.md) | Creates structured incident-response runbooks: detection, triage, mitigation, resolution and communication steps, plus escalation paths and recovery actions (e.g. service outages, database connection, replication and disk alerts). From [wshobson/agents](https://github.com/wshobson/agents/tree/main/plugins/incident-response). |
| [just](./just/SKILL.md) | How to use the `just` command runner to save and run project-specific recipes as a simpler alternative to `make`. |
| [playwright-bowser](./playwright-bowser/SKILL.md) | Headless browser automation via `playwright-cli` — parallel named sessions, UI testing, screenshots, and scraping without loading MCP tool schemas into context. |
| [startup-research](./startup-research/SKILL.md) | Researches a startup or product idea and produces a detailed markdown report covering market, competition, go-to-market, and MVP planning. |
| [story-to-video](./story-to-video/SKILL.md) | Converts narrated prose into a tool-agnostic Markdown shooting script (Asset Bible plus per-scene setting, camera, blocking, dialogue, music, sound) for AI text-to-video generators such as Sora, Runway, Veo, Pika, or Kling. |

## Plugin: mattpocock-skills

[Matt Pocock's skills](https://github.com/mattpocock/skills) are installed as a Claude Code **plugin**, not copied into this repo. They are small, composable engineering skills, including grilling a plan, spec and ticket flows, TDD, diagnosing bugs, code review, domain modelling, PR writing and prototyping. In Claude Code they appear namespaced, e.g. `mattpocock-skills:tdd`.

Install:

```bash
claude plugins install mattpocock-skills
```

- Files are stored under `~/.claude/plugins/cache/claude-plugins-official/mattpocock-skills/<version>/`.
- The plugin is enabled in this repo's `settings.json` (`enabledPlugins`), and `install.sh` keeps the plugin and its settings when it runs.
- Don't also install these skills with `npx skills add mattpocock/skills`, or you'll have every skill twice.

### New project workflow

The general order to follow when starting a new application:

| # | Skill | When |
|---|---|---|
| 1 | `/setup-matt-pocock-skills` | Once per repo: sets the issue tracker, triage labels and where docs go. |
| 2 | `/grill-with-docs` | Before every feature or change. Interviews you and writes `GLOSSARY.md` and ADRs. |
| 3 | `/prototype` *(optional)* | When a question needs runnable code (logic, state, a UI to see). Use `/handoff` to move it to a fresh session and to bring the findings back. |
| 4 | `/to-spec` → `/to-tickets` | Multi-session builds only. Keep steps 2–4 in one context window (don't clear or compact). |
| 5 | `/implement` per ticket (`/clear` between tickets), **or** `/implement-spec` for the whole spec | For a small change, skip step 4 and run `/implement` directly. |
| 6 | `/retro` | After the build, in the same session. Suggests improvements to the setup, not the code. |

Also useful:

- `/tdd` and `/code-review`: `/implement` runs both, but you can use them on their own too.
- `/diagnosing-bugs`: for hard bugs. Follow it with `/retro`.
- `/handoff`: moves work to a new session, directory or colleague.
- `/wayfinder`: for huge, unclear efforts (e.g. greenfield) before `/to-spec`.
- `/pr`: Claude uses it automatically when writing a PR body.
- `/ask-matt`: run it any time to ask which skill fits. Claude won't call it on its own, so type it yourself.

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
