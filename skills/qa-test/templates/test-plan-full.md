# Full Test Plan: {{project}}

Covers as many features and scenarios as practical: every page in the navigation, every form and user flow, and the main error paths. Run it on UAT before a release. It includes the smoke suite.

## Scope

- **Environments:** UAT (PROD only with explicit approval; tests tagged `@writes` are excluded there by default)
- **Auth:** {{none | roles and the test account for each}}
- **Test data:** every record a test creates is named with the `QA-TEST-<timestamp>` prefix. Clean-up: {{how, or "manual"}}

## Feature inventory

| Area | Pages / entry points | Notes |
|---|---|---|
| {{area}} | {{/path, /path}} | {{notes}} |

## Test cases

Tag a case **W** if it creates, changes or deletes data. Its spec must carry `{ tag: '@writes' }`.

| ID | Area | Scenario | Steps | Expected | W | Spec |
|---|---|---|---|---|---|---|
| FULL-01 | {{area}} | {{scenario}} | {{steps}} | {{expected}} | | `tests/full/{{area}}.spec.ts` |

## Not covered

| Item | Why |
|---|---|
| {{e.g. payment with a real card}} | {{reason}} |

## Change log

| Date | Change |
|---|---|
| {{date}} | Plan created |
