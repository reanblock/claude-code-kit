---
name: qa-test
description: QA-test a deployed web app (UAT or PROD) in a headless browser, like a QA team would. Keeps a smoke and a full test plan in the project repo, turns them into Playwright scripts that can also run without AI, and writes a shareable HTML report with screenshots of failures. Use when the user asks to "QA test", "smoke test", "run QA", "test the UAT/prod deployment", "check the site after deploy", or invokes /qa-test. Not for unit tests or apps running on localhost.
argument-hint: <project> <uat|prod> [smoke|full]
---

# QA Test

Test a **deployed** site through a real (headless) browser. The tests are Playwright scripts kept in the project repo under `qa/`, so they can be re-run anywhere without AI: `cd qa && ./run.sh uat smoke`.

## Inputs

`/qa-test <project> <env> [suite]`

- **project**: the app's name. It should match `project` in `qa/qa.config.json`.
- **env**: `uat` or `prod`. Any other name works if it is defined in `qa.config.json`.
- **suite**: `smoke` or `full`. If it's not given, use `smoke` for PROD and ask for UAT (suggest `smoke`).

If anything is missing or unclear, ask. Don't guess.

## PROD safety rules

These apply every time, even if PROD was approved earlier in the session.

1. **Confirm PROD before doing anything else.** Use AskUserQuestion: "Run QA against PROD (`<url>`)? Tests may load live pages and could create test records." Use the options "Yes, test PROD" and "No, stop". Stop on anything but yes.
2. **PROD is read-only by default.** Tests tagged `@writes` are excluded unless the user explicitly approves writes in a second question. Only then set `QA_ALLOW_PROD_WRITES=yes`.
3. **A full suite on PROD needs its own confirmation,** because it's unusual. Recommend smoke instead.
4. **Exploring PROD is also read-only:** never submit forms, buy, delete, or change settings.
5. Only set `QA_CONFIRM_PROD=yes` after step 1 is approved. `run.sh` and `playwright.config.ts` refuse to run PROD without it.

## Files in the project repo

Templates are in this skill's `templates/` folder. The report script is `scripts/build_report.py`.

```
qa/
  qa.config.json        project name, URL per environment, auth settings
  test-plan-smoke.md    smoke plan (IDs SMK-xx)
  test-plan-full.md     full plan (IDs FULL-xx)
  playwright.config.ts  projects: setup (login), smoke, full
  qa-settings.ts        reads the config and env vars (shared helper)
  run.sh                runs a suite and builds the report
  package.json          its own dependencies, separate from the app
  scripts/build_report.py
  tests/auth.setup.ts   only if login is needed
  tests/smoke/*.spec.ts
  tests/full/*.spec.ts
  reports/              one folder per run (gitignored)
```

## Workflow

### 1. Find the project and the URL

- Look for `qa/qa.config.json` in the current repo. If the current directory isn't the project named in the arguments, ask for the repo path.
- If the config has a URL for this environment, confirm it: "Test `<url>`?" Otherwise, ask for the URL and save it to the config.
- Check the site is reachable: `curl -sS -o /dev/null -w '%{http_code}' <url>`. If it's down, stop and report that. This is already a smoke failure.
- For PROD, apply the safety rules now.

### 2. Set up `qa/` (first run only)

1. Copy the templates into `qa/`. Rename `gitignore` to `.gitignore`. Copy `scripts/build_report.py` to `qa/scripts/`. Fill in `qa.config.json`.
2. Ask whether the site needs a login. If it does, set `auth.required: true` and `auth.loginPath`, and tell the user to export `QA_<ENV>_USERNAME` and `QA_<ENV>_PASSWORD`. Never write credentials to any file. If login uses SSO or MFA, ask how a test account can sign in before going on. If no login is needed, delete `tests/auth.setup.ts`.
3. Install the dependencies with yarn:
   ```bash
   cd qa && touch yarn.lock && yarn add -D @playwright/test @types/node && yarn playwright install chromium
   ```
   The empty `yarn.lock` keeps `qa/` separate from the app's own yarn workspace. If yarn is missing, suggest `corepack enable`, or fall back to npm.

### 3. Create or update the test plan

Skip this step if the plan for the chosen suite exists and the user didn't ask for changes.

1. **Explore the site** headless with the `playwright-bowser` skill (`playwright-cli`). Use a named session, and close it when done. Record the navigation, the key pages, the forms, the user flows, and anything that needs a login.
   - Smoke: the home page, the main navigation, and one or two key features.
   - Full: crawl the navigation and inventory every feature. For large content sites (such as a blog with 1,000 pages), sample a few pages of each type instead of every page.
2. **Write the plan** from the template: `test-plan-smoke.md` (keep it to roughly 5–10 cases, under 3 minutes) or `test-plan-full.md` (as much as practical). Give every case an ID and mark the cases that write data.
3. **Show the plan summary** (cases, and anything that writes data) and get approval before writing specs.

### 4. Write the Playwright specs

- Put each test ID at the start of its title, e.g. `test('SMK-04 search returns results', ...)`, so the report maps back to the plan.
- Use stable locators: `getByRole`, `getByLabel`, `getByText` or `data-testid`. Avoid CSS chains and XPath.
- Never use fixed waits (`waitForTimeout`). Rely on web-first assertions (`await expect(...)`).
- Any test that creates, changes or deletes data must have `{ tag: '@writes' }`, and must name records with `testDataPrefix` from `qa-settings.ts`. Smoke tests must not write.
- Use relative URLs (`page.goto('/about')`), so one spec works on every environment.
- No secrets in specs. Credentials only come from env vars, through `credentials()`.
- Smoke specs go in `tests/smoke/`. Full-only specs go in `tests/full/`. The full suite runs both.
- Update the plan's Spec column and change log.

### 5. Run

```bash
cd qa && QA_CONFIRM_PROD=yes ./run.sh <env> <suite>   # the PROD flag only after the user confirmed
```

`run.sh` creates `reports/<env>-<suite>-<timestamp>/` containing `report.html` (one shareable file with failure screenshots embedded), `playwright-report/` (Playwright's own report, with traces) and `results.json`. Failures get one retry. A test that passes on retry is reported as flaky.

### 6. Triage failures

For each failure, read the error and the screenshot, then decide:

- **Site bug:** report it. Don't touch the test.
- **Broken test** (the locator changed, or the test made a wrong assumption): fix the spec, re-run once, and say in the summary that the test was fixed. Never weaken an assertion just to make a test pass.
- **Environment issue** (timeout, 5xx, login expired): report it. Re-run once if it looks transient.

### 7. Report back

Keep the reply short:

- **Verdict:** PASS or FAIL, with the counts (passed, failed, flaky, skipped).
- **Each failure:** one line with the ID, what broke, and whether it's a site bug or a test bug.
- **The full path to `report.html`.**
- **Anything the plan doesn't cover yet.**

Don't publish the report anywhere. It may contain internal URLs and screenshots. The user shares it.

## Running without AI

Anyone (or CI) can run it from the project repo:

```bash
cd qa && yarn install && yarn playwright install chromium
./run.sh uat smoke
QA_CONFIRM_PROD=yes ./run.sh prod smoke
```

The single-file report needs `uv`. Without it, use `playwright-report/index.html`.
