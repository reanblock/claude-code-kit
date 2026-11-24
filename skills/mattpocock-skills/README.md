# Plugin: mattpocock-skills

[Matt Pocock's skills](https://github.com/mattpocock/skills) are installed as a Claude Code **plugin**, not copied into this repo. They are small, composable engineering skills, including grilling a plan, spec and ticket flows, TDD, diagnosing bugs, code review, domain modelling, PR writing and prototyping. In Claude Code they appear namespaced, e.g. `mattpocock-skills:tdd`.

Install:

```bash
claude plugins install mattpocock-skills
```

- Files are stored under `~/.claude/plugins/cache/claude-plugins-official/mattpocock-skills/<version>/`.
- The plugin is enabled in this repo's `settings.json` (`enabledPlugins`), and `install.sh` keeps the plugin and its settings when it runs.
- Don't also install these skills with `npx skills add mattpocock/skills`, or you'll have every skill twice.

## Which workflow?

The deciding factor is how big the work is, not whether it's a feature or an app:

- **Too big to design in one session** (a new application, 0 → MVP, a large epic): use the [greenfield workflow](#greenfield-workflow-new-application) with `/wayfinder`.
- **Can be designed in one session** (a feature, a change or a small app): use the [feature workflow](#feature-workflow-existing-application) with `/grill-with-docs`.

If you're not sure, start with `/wayfinder`. If the work fits in one session, it stops and asks how you'd like to go on.

## Greenfield workflow (new application)

To go from nothing to a fully specced, ticketed MVP and then build it:

| # | Skill | When |
|---|---|---|
| 1 | `/setup-matt-pocock-skills` | Once per repo: sets the issue tracker, triage labels and where docs go. Wayfinder needs the tracker. |
| 2 | `/wayfinder <idea>` | **Chart the map.** Grills you (grilling + domain-modeling, the same pair as `/grill-with-docs`) to name the destination, e.g. the MVP spec. Then creates a `wayfinder:map` issue with child decision tickets, and starts research tickets in the background. Don't run `/grill-with-docs` first, or you'll be interviewed twice. |
| 3 | `/wayfinder <map>` | **Work through the map**, one decision ticket per session (`/clear` between them). Each ticket is resolved by grilling, `/prototype`, research, or a manual task. Repeat until no open tickets are left and nothing remains under "Not yet specified". |
| 4 | `/to-spec` | In a fresh session, pass the map link so the spec builds on its decisions. It writes no code and doesn't interview you: it turns what's been decided into a spec with user stories, and publishes it to the tracker. |
| 5 | `/to-tickets` | In the same session. Breaks the spec into tracer-bullet vertical slices with blocking edges. |
| 6 | Pick an implementation strategy | **`/implement-spec`**: builds the whole spec on one integration branch, running parallel subagents across the ticket graph. Best for a fresh MVP. **Or `/implement <ticket>`** per ticket (`/clear` between them): slower, but you review each slice. |
| 7 | `/retro` | After the build, in the same session. Suggests improvements to the setup, not the code. |

Wayfinder only plans and makes decisions. It writes no code: once the way is clear, hand off to `/to-spec`.

## Feature workflow (existing application)

For a new feature or change in an existing codebase:

| # | Skill | When |
|---|---|---|
| 1 | `/setup-matt-pocock-skills` | Once per repo, if not already done. |
| 2 | `/grill-with-docs` | Before every feature or change. Interviews you and updates `GLOSSARY.md` and ADRs. Use `/grill-me` instead for a quick stress-test that writes no docs. |
| 3 | `/prototype` *(optional)* | When a question needs runnable code (logic, state, a UI to see). Use `/handoff` to move it to a fresh session and to bring the findings back. |
| 4 | `/to-spec` → `/to-tickets` | Multi-session builds only. Keep steps 2–4 in one context window (don't clear or compact). |
| 5 | `/implement` per ticket (`/clear` between tickets), **or** `/implement-spec` for the whole spec | For a small change, skip step 4 and run `/implement` directly. |
| 6 | `/retro` | After the build, in the same session. |

If grilling shows the feature is too big for one session, switch to `/wayfinder` and treat it as an epic.

## Also useful

- `/tdd` and `/code-review`: `/implement` runs both, but you can use them on their own too.
- `/diagnosing-bugs`: for hard bugs. Follow it with `/retro`.
- `/handoff`: moves work to a new session, directory or colleague.
- `/pr`: Claude uses it automatically when writing a PR body.
- `/ask-matt`: run it any time to ask which skill fits. Claude won't call it on its own, so type it yourself.
