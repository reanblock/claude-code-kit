## Agent Teams

## UPDATE

Just use a prompt that includes:

- "Create an Agent Team to..."
- "Team members: frontend engineer to work on the frontend, a backend engineer to ... etc, etc"
- "Include an integration tester that builds and runs playwrite tests reporting issues to be fixed back to the team members...."
- "A Database engineer ...."
- "A DevOps engineer ...."
- "An LLM engineer ...."
- etc, etc add other things you want in the team + rules on how they should communicate and collaborate.

**Example**

*"Create an Agent Team to complete the project as defined. Team members: a Frontend Engineer to build the frontend, a Backend API engineer to work on the APIs and backend, a Database engineer for all database related code, an LLM engineer on the LLM calls. While all engineers should work on unit tests there should also be an integration tester that builds and runs playwrite tests reporting issues to be fixed back to the team members. Finally, a DevOps engineer for the Docker container and scripts."*

### (Optional - More comples) Steps 

Use the `/plan_w_team` and `/build-with-agent-team` skills especially for more complex projects that do not yet have a plan and you want claude to write the plan specifically for Agent Teams.

**Greenfield Project (brand new)**

1. Create new project directory `my-new-project` and cd into it then run `git init`.
2. Run `tmux` (install guide below).
3. Run `claude`.
4. Run `/plan_w_team` with your project spec prompt and team orchestration prompt (using the prompt example below).
5. Review `specs/<plan>.md` — tweak if needed.
6. Run `/build-with-agent-team` skill for example `/build-with-agent-team specs/<plan>.md`.

**Brownfield Project (adding new feature)**

1. Run `/explore` skill to get a summary of the project. 
2. Run `tmux` (install guide below).
3. Run `claude`.
4. Run `/plan` or `/plan_w_team` with your project spec prompt and team orchestration prompt.
5. Review `specs/<plan>.md` — tweak if needed.
6. Run `/build` or `/build-with-agent-team` skill for example `/build-with-agent-team specs/<plan>.md`.

**Example /plan_w_team user and orchestration promopt**

```bash
/plan_w_team "Build a simple calorie tracker web app. Users should be able to:
- Add food entries with a name and calorie count
- View a daily log of all entries
- See a running total for the day
- Delete entries
- Reset/clear the day

Use plain HTML, CSS, and vanilla JavaScript with a JSON file as the data store. No frameworks, no build tools. Keep it simple and self-contained." 

"Use two builder agents running in parallel: one focused on the data layer (storage, read/write operations, daily totals logic) and one focused on the UI (HTML structure, CSS styling, user interactions). The data builder should use Opus. The UI builder should use Sonnet. Both builders work simultaneously. Once both are complete, use the tester agent to write and run tests covering happy paths, edge cases, and failure scenarios. Keep at least one builder agent available to fix things should any tests fail. Finally, use the validator agent to wire everything together and verify the app meets all acceptance criteria end-to-end."
```

When you run this prompt, you should see something amazing like:

![Multi-Agent Teams](../images/multi-agent-teams.png)

NOTE: Currently an experimental feature - you need to add the following to your `settings.json`:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

### Tmux

Use iTerm (or tmux) to view agents working in split panes.

Install and start tmux session:

```bash
brew install tmux
tmux new
cd my-project
claude --dangerously-skip-permissions
```

![Tmux Cheat Sheet](../images/tmux-cheat-sheet.png)

### Orchestration using the Multi-Agent Observability Application

1. Clone the `claude-code-hooks-multi-agent-observability` repo [here](https://github.com/disler/claude-code-hooks-multi-agent-observability)
2. Follow the Integration steps [here](https://github.com/disler/claude-code-hooks-multi-agent-observability?tab=readme-ov-file#-integration)
3. Install `bun` [here](https://bun.sh/) and reload your environment using `source`.
4. Install `vite` [here](https://vite.dev/) by navigating to `apps/client` and running `bun install`.
5. Start the `./scripts/start-system.sh` script to start the Observability server.
6. Run a test using the provided `curl` example. The event should display in the Multi-Agent Observability app.
7. Run `claude` in the project where you copied the .claude files.

### Examples

- Spin up 4 agents to run a [parallel PR review](https://code.claude.com/docs/en/agent-teams#run-a-parallel-code-review) from different lenses: security, test coverage, performance imapaact and feature correctness.
- Spin up multiple agents to work on a [debuging problem](https://code.claude.com/docs/en/agent-teams#investigate-with-competing-hypotheses), each one can focus on different hypotheses and test out each case: one checks if it is a datbase issue, another checks if it is a server issue etc.
- Spin up multiple agents to build an MVP application: one on UI, one on DB, one on API, one on testing etc.

### Links

- Claude Code Multi-Agent Orchestration with Opus 4.6, Tmux and Agent Sandboxes [here](https://www.youtube.com/watch?v=RpUTF_U4kiw)
- Claude Code Agent Teams (Full Tutorial) [here](https://www.youtube.com/watch?v=zm-BBZIAJ0c)
- Claude Opus 4.6: Agent Teams Change Everything! [here](https://www.youtube.com/watch?v=RWDK5414yL4)