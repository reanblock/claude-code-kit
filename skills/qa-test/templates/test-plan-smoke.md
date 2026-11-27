# Smoke Test Plan: {{project}}

A quick check (target: under 3 minutes) that a deployment is up and its main entry points work. Run it after every deploy, before sharing the link. This is the default suite for PROD.

## Scope

- **Environments:** UAT, PROD (see `qa.config.json`)
- **Auth:** {{none | test account via QA_<ENV>_USERNAME / QA_<ENV>_PASSWORD}}
- **Data:** read-only. Smoke tests must not create, change or delete data.

## Test cases

| ID | Area | Scenario | Expected | Spec |
|---|---|---|---|---|
| SMK-01 | Site | Home page loads | HTTP < 400, title set, page renders | `tests/smoke/smoke.spec.ts` |
| SMK-02 | Site | No JavaScript errors on home | No console or page errors | `tests/smoke/smoke.spec.ts` |
| SMK-03 | Navigation | A sample of internal links resolve | Each returns HTTP < 400 | `tests/smoke/smoke.spec.ts` |
| SMK-04 | {{area}} | {{one key feature, read-only}} | {{expected}} | `tests/smoke/{{area}}.spec.ts` |

## Out of scope

Anything that writes data, edge cases and full feature coverage: see `test-plan-full.md`.

## Change log

| Date | Change |
|---|---|
| {{date}} | Plan created |
