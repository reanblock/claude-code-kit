---
name: audit-false-positive-review
description: Review an existing smart contract security audit report and check every finding for false positives. Takes a report (PDF/markdown) or a GitHub repo whose issues are the findings, plus the codebase it was written against, and independently re-verifies each finding against the source to classify it as VALID, FALSE POSITIVE, INCONCLUSIVE, or OUT-OF-DATE, with evidence and an FP category. Use when users request "false positive review", "check for false positives", "triage this audit report", "which findings are real", "validate the findings in this report", "review this report for FPs", or hand over a third-party/automated audit report to be sanity-checked. Supports Solidity, Vyper, Rust (Solana/CosmWasm), Move, Cairo, and other smart contract languages.
---

# Audit Report False Positive Review

This skill takes an **existing** audit report and independently re-verifies every finding in it against the actual source code, to separate real issues from false positives. It is the triage pass you run over a report you did not write — a third-party audit, an automated scanner dump, a contest/bug-bounty submission set, or an LLM-generated report — before anyone spends engineering time on remediation.

It complements the other audit skills: `audit-codebase` **discovers** findings, `audit-vuln-review` deep-dives a **single** suspected vulnerability, `audit-severity-review` re-rates the severities of findings **assumed valid**, and `audit-verify-fixes` confirms remediations **afterward**. This skill sits between report delivery and remediation: it asks, for each finding, "is this real at all?"

## ⛔ Read-Only Constraint — Non-Negotiable

**This skill never modifies the code under review.**

DO NOT MAKE CHANGES TO THE CODE, CREATE COMMITS, OR PUSH ANYTHING. If the findings live in a shared client GitHub repository, do not comment on, close, edit, or otherwise write to any issue — report conclusions to the **user**, who decides what to communicate to the client.

Permitted: reading files, `grep`/`rg`, `git log`/`show`/`diff`/`checkout` for local inspection, `gh issue list`/`gh issue view`, and `gh api` GET requests. Everything else requires asking the user first.

## Trigger Conditions

Use this skill when the user requests:
- "false positive review", "check for false positives", "FP review", "FP triage"
- "triage this audit report", "which of these findings are real?"
- "validate the findings in this report", "sanity check this audit"
- "review this scanner output" / "review this LLM-generated report"

AND both of the following are available (or can be located):
1. An **existing set of findings** — a report file, or a GitHub repo whose issues are the findings
2. The **codebase** the findings were written against

If the user supplies only a single vulnerability rather than a report, use `audit-vuln-review` instead. If the user accepts the findings as valid and only wants their severities re-rated, use `audit-severity-review` instead.

## Processing Workflow

### 1. Locate the Findings Source

Establish which mode applies before anything else:

| Signal | Mode |
|---|---|
| A file path, or a report file named in conversation / found in the workspace | **Mode A — Report File** |
| A GitHub repository URL, or the user refers to findings as issues in a repo | **Mode B — GitHub Issues** |

If both are present, ask which to use. If neither can be determined, ask — do not guess.

**Mode A — resolve the report file** in this priority order:
1. Skill argument (e.g. an explicit path passed on invocation)
2. A file named earlier in the conversation
3. Workspace search:
   ```bash
   find . -maxdepth 3 -type f \( -name "*.pdf" -o -name "*.md" \) | head -20
   ```
   Prefer names containing `audit`, `report`, `findings`, `security`, or `review`. One strong candidate → use it. Several → present the list and ask.
4. Ask the user. Do not proceed without a report.

For PDFs, extract text before parsing:
```bash
pip install pdfplumber --break-system-packages 2>/dev/null
```
```python
import pdfplumber
with pdfplumber.open(pdf_path) as pdf:
    text = "\n".join(p.extract_text() or "" for p in pdf.pages)
```

**Mode B — resolve the repository and read the issues** (read-only):
```bash
gh repo view <org>/<repo> --json name,defaultBranchRef
gh issue list --repo <org>/<repo> --state all --limit 200 --json number,title,labels,state,body
gh issue view <issue_number> --repo <org>/<repo> --comments --json number,title,labels,state,body,comments
```
Include closed issues — a closed issue is a claim, not evidence.

### 2. Pin the Code Version the Report Targeted

**This step is mandatory and is the most common source of wrong verdicts when skipped.** A finding that was real against the audited commit but has since been fixed is **OUT-OF-DATE**, not a false positive — conflating the two tells the client their auditor was wrong when they were right.

1. Look in the report for the audited commit SHA, tag, or branch (usually in the scope/metadata section).
2. If found, inspect that revision rather than `HEAD`:
   ```bash
   git log --oneline -1 <audited_sha>
   git diff --stat <audited_sha>..HEAD -- <in_scope_paths>
   ```
   Review each finding against `<audited_sha>`; if the diff to `HEAD` touches the finding's code, note that separately.
3. If no revision is stated, review against the current checkout and **say so explicitly** in the output — every verdict then carries that caveat.
4. If the report's file paths do not exist in the codebase at all, stop and ask the user for the right revision or repo before reviewing anything.

### 3. Extract the Findings Into a Worklist

Build a structured worklist so no finding is silently dropped. For each finding capture:

- **Finding ID** (report ID, or issue number `#42`)
- **Title**
- **Reported severity** (verbatim — do not normalise the client's scale)
- **Claimed vulnerability** — the mechanism as the report describes it
- **Claimed impact**
- **Affected locations** — files, contracts, functions, line numbers
- **Reported PoC / exploit path**, if any
- **Recommended fix**, if any

For reports with more than ~10 findings, persist the worklist to a scratch file (e.g. `findings.json` under the scratchpad or a user-specified path) and track a verdict per finding as you go. Report the extracted count back to the user before starting the review, so a parsing failure surfaces immediately rather than as a short final table.

### 4. Verify Each Finding Against the Source

Work through the findings one at a time. For each:

**Step A — Read the code, not the report's reasoning.** Open the cited files and form your own view of what the code does before adopting the report's narrative. A report's description of the code is a claim to be tested, not a source of truth; scanner and LLM reports frequently describe code that does not exist as described.

**Step B — Confirm the cited code actually matches the report.** Check the file, function, and line numbers. If they do not correspond (wrong function, code removed, line numbers off by a whole file), that is itself evidence — record it and locate the closest real counterpart before judging.

**Step C — Trace the exploit path end to end.** Follow the path an attacker would take: entry point → call chain → state changes → external interactions → profit or damage. Cross-contract and proxy-mediated paths must be traced across files, not assumed.

**Step D — Look for mitigations that already defeat the claim:**
- Access control (`onlyOwner`, `onlyRole`, `require(msg.sender == ...)`, Rust signer/owner checks, Move capabilities)
- Reentrancy guards (`nonReentrant`, mutex/lock patterns, checks-effects-interactions ordering)
- Input validation and boundary checks
- Language- or compiler-level protection (Solidity >=0.8 checked arithmetic, Rust checked math, safe casts)
- Pause mechanisms, timelocks, invariant assertions, slippage/deadline params
- Callers upstream that constrain the arguments the finding assumes are attacker-controlled

**Step E — Test the preconditions.** Can the attacker actually reach the required state? Is the "attacker-controlled" input really attacker-controlled? Is the privileged role the finding depends on already trusted by the protocol's documented trust model?

**Step F — Adversarially attack your own FP conclusion.** *This step is what makes the review worth running.* Before marking anything a false positive, deliberately try to defeat your own reasoning:
- Is the mitigation you found reachable on **every** path into the vulnerable code, or only the one you traced?
- Can the guard be bypassed — different entry point, delegatecall, initialiser, upgrade path, inherited override, or a public function that wraps the internal one?
- Does the mitigation hold at all values (zero amounts, first depositor, empty arrays, max ints, fee-on-transfer or rebasing tokens, decimals ≠ 18)?
- Does it hold across the full lifecycle (before initialisation, while paused, mid-upgrade, after migration)?
- Is the trust assumption you relied on actually documented, or did you invent it?

Only mark **FALSE POSITIVE** if this refutation attempt fails. If it succeeds, the finding is VALID (possibly by a different mechanism than the report described — say so).

**Step G — Check for duplicates.** Findings that restate the same root cause under different IDs are duplicates, not independent issues. Mark the later ones as FALSE POSITIVE with category *Duplicate*, cross-referencing the primary ID.

### 5. Assign a Verdict

| Verdict | Definition |
|---|---|
| **VALID** | The vulnerability is real and reachable in the audited code. The report's core claim holds, even if its wording, severity, or exploit path is imprecise. |
| **PARTIALLY VALID** | An underlying issue exists but the report materially overstates it — the impact is unreachable, a claimed attack vector is bogus while another is real, or only one of several cited locations is affected. |
| **FALSE POSITIVE** | The vulnerability does not exist in the audited code. Assign an FP category (below). |
| **INCONCLUSIVE** | Cannot be settled from the available material — the finding depends on off-chain behaviour, deployment configuration, unavailable dependency source, or economic assumptions that need client input. State exactly what is needed to resolve it. |
| **OUT-OF-DATE** | The finding was valid against the audited revision but the code has since changed such that it no longer applies. **Not** a false positive — the auditor was right at the time. |

Never mark a finding **FALSE POSITIVE** merely because its impact is small or its severity is inflated. An overrated real issue is VALID with a severity note — route severity disputes to `audit-severity-review`.

#### False Positive Categories

| Category | Meaning |
|---|---|
| **Mitigated** | A guard, modifier, check, or ordering already prevents the issue. Cite the exact guard. |
| **Unreachable** | The vulnerable path cannot be reached — dead code, unreachable branch, function never exposed. |
| **Misread semantics** | The report misunderstands the language, compiler, or library behaviour (e.g. claims overflow under Solidity >=0.8, misreads a `delegatecall` context, misreads storage layout). |
| **Impossible preconditions** | Exploitation requires state or inputs an attacker cannot produce. |
| **Trusted actor** | Requires a privileged role the protocol already trusts by documented design. Note it as a centralisation observation, not a vulnerability. |
| **Out of scope** | The code is not in scope — tests, mocks, scripts, examples, or third-party dependencies excluded by the engagement. |
| **By design** | The behaviour is intentional and documented, and the documented rationale holds. |
| **Duplicate** | Restates another finding's root cause. Cross-reference the primary ID. |
| **Non-existent code** | The cited code does not exist as described anywhere in the codebase (common in LLM-generated and stale reports). |

Assign a **confidence** to every verdict: **High** (direct code evidence, refutation attempted and failed), **Medium** (evidence is strong but some context is assumed), **Low** (leaning, needs a second look — treat as close to INCONCLUSIVE).

Never assign High confidence to a FALSE POSITIVE verdict without having completed Step F.

### 6. Output Format

Present a summary table first, then per-finding detail for everything that is not a plain VALID.

#### Summary Table

```
╔════════════╦══════════════╦═══════════════════╦════════════════════╦════════════╦══════════════════════════════════════════════════════╗
║ Finding ID ║ Reported Sev ║ Verdict           ║ FP Category        ║ Confidence ║ Evidence                                             ║
╠════════════╬══════════════╬═══════════════════╬════════════════════╬════════════╬══════════════════════════════════════════════════════╣
║ FIND-003   ║ Critical     ║ FALSE POSITIVE    ║ Mitigated          ║ High       ║ Vault.sol:112 withdraw() carries nonReentrant        ║
║ FIND-007   ║ High         ║ VALID             ║ --                 ║ High       ║ Router.sol:88 swap() lacks deadline; MEV path traced ║
║ FIND-011   ║ High         ║ PARTIALLY VALID   ║ --                 ║ Medium     ║ Rounding real, but drain path blocked by minOut check║
║ FIND-014   ║ Medium       ║ FALSE POSITIVE    ║ Misread semantics  ║ High       ║ Solidity 0.8.24 — arithmetic is checked, no overflow ║
║ FIND-019   ║ Medium       ║ OUT-OF-DATE       ║ --                 ║ High       ║ Fixed in a1b2c3d after audited commit 9f8e7d6        ║
║ FIND-022   ║ Low          ║ INCONCLUSIVE      ║ --                 ║ --         ║ Depends on oracle heartbeat config — need client ans ║
╚════════════╩══════════════╩═══════════════════╩════════════════════╩════════════╩══════════════════════════════════════════════════════╝

Reviewed against commit 9f8e7d6 (audited revision, per report §1.2)

Summary: 22 findings | 12 VALID | 2 PARTIALLY VALID | 6 FALSE POSITIVE | 1 INCONCLUSIVE | 1 OUT-OF-DATE
False positive rate: 27% (6/22) — Critical/High FPs: 2
```

**Output requirements:**
- Use ASCII box-drawing characters for terminal display
- Report severities verbatim from the source; do not translate between scales
- Sort by reported severity (highest first), then by verdict (FALSE POSITIVE → PARTIALLY VALID → INCONCLUSIVE → OUT-OF-DATE → VALID) so the disputed findings sit at the top
- Every row's Evidence cell must cite a concrete location (`file:line`, function, commit) — never a generic phrase like "code looks safe"
- Always state the revision reviewed, and flag it loudly when no audited revision was available
- Report the FP rate and call out false positives at Critical/High separately — those are the expensive ones

#### Per-Finding Detail

For every FALSE POSITIVE, PARTIALLY VALID, INCONCLUSIVE, and OUT-OF-DATE finding:

```
### [FINDING ID] — <title>

**Reported**: <severity> — <one-line summary of the claim>
**Verdict**: <verdict> (<FP category, if any>) — confidence <High|Medium|Low>

**What the report claims**: <1-2 sentences>

**What the code does**: <2-4 sentences citing specific files, functions, and line numbers>

**Why the verdict holds**: <the decisive evidence — the exact guard, unreachable path, compiler behaviour, or missing code>

**Refutation attempted**: <for FPs — which bypasses you tried (alternate entry points, edge values, lifecycle states) and why each failed>

**Residual risk**: <anything still worth the client's attention even though the finding is not valid as written — or "None">
```

VALID findings need only a line in the table unless the mechanism differs from the report's — in which case explain the real mechanism, since remediating the reported one would not fix it.

### 7. Close Out

After presenting results:
1. Highlight Critical/High findings judged FALSE POSITIVE — these carry the greatest cost if wrong, so offer a second-pass deep dive on each via `audit-vuln-review`
2. List every INCONCLUSIVE finding as an explicit question set for the client
3. Note any **new** issues you spotted while reviewing that the report missed — flag them, do not fold them into the FP triage; offer `audit-codebase` for a proper discovery pass
4. Offer to export the results (markdown or CSV) if the user wants to return them to the auditor or track remediation
5. If the user wants severities re-rated on the surviving VALID findings, hand off to `audit-severity-review`

## Edge Cases and Considerations

- **Report cites no commit**: Review against the current checkout, state the caveat prominently on every verdict, and ask the user for the audited revision before treating any OUT-OF-DATE verdict as final.
- **Findings without locations**: Some reports describe an issue with no file reference. Search the repo for the pattern; if it cannot be located, the verdict is INCONCLUSIVE (or FP / *Non-existent code* if the described construct plainly does not exist in the codebase).
- **Automated scanner output**: Slither/Mythril/Aderyn-style detectors produce high FP rates and cluster many rows under one detector. Group by detector, verify each occurrence individually anyway, and note the per-detector FP rate.
- **LLM-generated reports**: Expect plausible-sounding findings citing code that does not exist. Always confirm the cited code is real before analysing it (Step B).
- **Dependencies and inherited code**: Read imported libraries (`lib/`, `node_modules/`, crates) when the claim depends on them; a guard may live in a base contract rather than the cited file.
- **Upgradeable contracts**: Check both proxy and implementation, plus initialisers and storage layout — a finding that is FP on the implementation can be real via the proxy, and vice versa.
- **Trust-model disputes**: "Owner can rug" findings are usually *Trusted actor* FPs **only if** the trust assumption is documented. If it is undocumented, it is a valid centralisation finding.
- **Economic and MEV findings**: Profitability depends on market state. Where you cannot settle it from code alone, INCONCLUSIVE with stated assumptions beats a confident guess.
- **Test and mock files**: Confirm against the engagement's scope list before dismissing as out of scope — some engagements do include deployment scripts.
- **Disagreeing with a reputable auditor**: State the code evidence and let it stand on its own. Do not soften a well-evidenced FP verdict, and do not manufacture one to look thorough.

## Quality Checks

Before presenting results:
- Every finding in the source report appears in the output — count in equals count out
- The revision reviewed is stated, and matches the report's audited commit where one exists
- Each verdict cites concrete code evidence (file, function, line), not a generic assertion
- Every FALSE POSITIVE has an FP category and a completed refutation attempt (Step F)
- No finding was marked FALSE POSITIVE merely because its impact or severity was overstated
- Fixed-since-audit findings are OUT-OF-DATE, not FALSE POSITIVE
- Duplicates cross-reference their primary finding ID
- The cited code was actually read — no verdict rests on the report's description alone
- No code was modified, and no writes were made to any shared client repository
