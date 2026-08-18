---
name: audit-codebase
description: Perform a security audit of a smart contract codebase — the core, in-process review that discovers vulnerabilities. Takes a list of in-scope files, systematically reviews them across the full vulnerability taxonomy (access control, reentrancy, arithmetic, oracle manipulation, accounting, upgradeability, DoS, etc.), traces exploit paths, and produces an audit report with severity-rated findings. Use when users request "audit this codebase", "perform an audit", "do a security audit", "review these contracts for vulnerabilities", "find vulnerabilities", "security review", or provide a set of in-scope files to be audited. Supports Solidity, Vyper, Rust (Solana/CosmWasm), Move, Cairo, and other smart contract languages.
---

# Security Audit (Codebase Review)

This skill performs the core work of a security audit: a systematic, in-process review of an in-scope codebase to **discover** vulnerabilities and produce severity-rated findings with explanations, exploit paths, and recommended fixes.

It is the center of the audit lifecycle. Use the related skills for the surrounding phases: `audit-scope` to estimate effort before starting, `audit-prototype` to build a mock UI for understanding the protocol, `audit-vuln-review` to deep-dive a single suspected finding, `audit-severity-review` to reassess severities in an existing report, `audit-false-positive-review` to re-verify an existing report's findings for false positives, and `audit-verify-fixes` to confirm remediations afterward. This skill is what runs *between* scoping and fix verification — the audit itself.

## Trigger Conditions

Use this skill when the user requests:
- "audit this codebase" / "audit these contracts"
- "perform an audit" / "do a security audit" / "conduct an audit"
- "review these contracts for vulnerabilities"
- "find vulnerabilities" / "find bugs" / "security review"

AND provides (or points at) a set of in-scope files. If no scope is given, see *Determining Scope* below.

## Input Requirements

- **In-scope files**: A comma-separated list of file paths or glob patterns that are in scope for the audit.
  - Example: `src/Vault.sol, src/Router.sol, src/libraries/MathLib.sol`
  - Glob patterns are allowed: `src/contracts/*.sol`
- **Optional context** (use if provided): protocol description, architecture docs, known concerns, prior audit reports, a threat model, or a specific area of focus.

### Determining Scope

If the user does not provide a file list:
- Look for a `scope.txt`, an in-scope section in the README, or an existing `audit-scope-report.md` (produced by `audit-scope`).
- If none exists, infer scope from the primary source directory (e.g., `src/`, `contracts/`, `programs/`) but **list the files you intend to audit and confirm with the user before proceeding**. The scope is defined by the client — do not silently expand it.

## Processing Workflow

**IMPORTANT**: DO NOT MAKE CHANGES TO THE CODE OR MAKE ANY COMMITS USING GIT. This is a read-only review. The only file you write is the audit report.

### 1. Validate Scope

- Parse the file list / globs and resolve every path.
- Verify each file exists; report any missing files immediately.
- Group files by language/type (Solidity, Vyper, Rust, Move, Cairo, etc.).
- If no scope can be determined, stop and ask (see *Determining Scope*).

### 2. Build Context Before Reading Code

Understand the protocol before hunting for bugs — most real findings come from understanding *intent vs. implementation*, not pattern-matching.

- Read the README, `docs/`, whitepaper, NatSpec/rustdoc, and any provided architecture material.
- Identify **what the protocol does**, the **core invariants** that must always hold (e.g., "totalSupply == sum of balances", "collateral always ≥ debt", "shares never mint for free"), and the **trust/role model** (who is privileged, what they can do).
- Map the **contract/module topology**: entry points, external/public functions, inter-contract calls, and external integrations (DEXes, oracles, lending, bridges, tokens).
- Identify the **assets at risk** and **who holds them** (user funds, protocol fees, collateral).

### 3. Systematic Review Across the Vulnerability Taxonomy

Review **every in-scope file**. For each contract/module and each externally reachable function, work through the taxonomy below. Do not just scan for keywords — for each category, ask "can this invariant be broken here?" and trace the execution path an attacker would take.

**Vulnerability taxonomy (check each category against each relevant function):**

- **Access control**: missing/incorrect modifiers, unprotected privileged functions, missing `onlyOwner`/role checks, `tx.origin` misuse, uninitialized ownership, public functions that should be internal.
- **Reentrancy**: classic, cross-function, cross-contract, and read-only reentrancy; violations of checks-effects-interactions; state updated after external calls; ERC-777/ERC-721 callback hooks.
- **Arithmetic & precision**: overflow/underflow (and where `unchecked` is used), rounding/precision-loss, division-before-multiplication, truncation, decimal mismatches, share/asset conversion rounding direction.
- **Accounting & logic errors**: incorrect balance/share math, fee miscalculation, double-counting, off-by-one, wrong operator, mismatched units, state desync between tracked and actual balances.
- **Oracle & price manipulation**: spot-price reliance, manipulatable TWAPs, stale/negative price feeds, missing freshness/round checks, single-source oracles, sandwichable price reads.
- **Flash-loan / economic attacks**: invariants breakable within a single transaction, price/collateral manipulation via flash loans, profitable arbitrage against the protocol.
- **Front-running / MEV**: sandwichable operations, missing slippage/deadline params, predictable ordering dependence, approval race conditions, commit-reveal gaps.
- **External calls**: unchecked return values, gas-griefing via `.call`, return-bomb / unbounded return data, trust assumptions on external contracts, fee-on-transfer / rebasing / non-standard ERC-20 handling, `safeTransfer` vs `transfer`.
- **Denial of service**: unbounded loops over user-controlled arrays, griefing via reverts in callbacks, gas exhaustion, locking funds via failed external calls, push-vs-pull payment issues.
- **Upgradeability & initialization**: missing `initializer` guards, re-initialization, storage-layout collisions, uninitialized implementation contracts, unprotected `delegatecall`, `selfdestruct` exposure, proxy/admin clash.
- **Signatures & replay**: missing nonces, missing/incorrect domain separator (EIP-712), cross-chain replay (chainid), signature malleability, missing `ecrecover` zero-address check, unbounded deadline.
- **Randomness & timestamp**: predictable randomness (`blockhash`, `block.timestamp`), miner-influenceable values used for security decisions.
- **Token & standard compliance**: ERC-4626 inflation/first-depositor attack, ERC-20 approval issues, missing-return-value tokens, ERC-721/1155 safe-transfer reentrancy, non-compliant implementations.
- **Cross-chain / bridge**: message replay, source/destination validation, trust in relayers, ordering and finality assumptions.
- **Centralization & admin risk**: excessive privileges, no timelock, single-key control, rug vectors, unbounded admin parameter changes (e.g., fees to 100%), pausing that traps funds.
- **Input validation**: missing zero-address / zero-amount checks, unchecked array length mismatches, missing bounds on parameters.
- **Language/VM-specific**:
  - *Solidity/Vyper*: inline assembly correctness, `delegatecall` context, low-level memory, storage pointer aliasing.
  - *Rust (Solana/Anchor)*: missing account ownership/signer checks, account confusion, missing `has_one`/constraint checks, PDA seed/bump validation, integer math, CPI trust, `close` re-init.
  - *Rust (CosmWasm)*: missing `info.sender` auth, reply/submessage handling, fund validation.
  - *Move*: resource/ability misuse, capability leakage, missing access checks.

For each function, also confirm the **happy path** matches documented intent — divergence between spec and code is a rich source of high-severity findings.

### 4. Scale Coverage (Optional Parallel Review)

For larger scopes, you may fan out review using subagents to keep coverage thorough and parallel:
- **Partition by file/module or by vulnerability category**, giving each subagent a focused slice and the shared protocol context from Step 2.
- Each subagent returns candidate findings with file/line evidence and a draft severity.
- The main thread then **deduplicates, cross-checks, and validates** every candidate (Step 5) before anything enters the report — subagent output is raw input, not final findings.

Use parallel review when scope is large (e.g., >1000 LoC or many independent modules); for small scopes a single-threaded pass is clearer. State in the report whether parallel review was used.

### 5. Validate Every Candidate Finding

A finding only enters the report after it survives validation. For each candidate:

1. **Trace the full exploit path** through the actual code (across files if needed) — confirm the vulnerable code is reachable and not already mitigated upstream.
2. **Check for existing guards**: modifiers, reentrancy guards, input validation, safe-math, pause/timelock, compiler-version protections. If a guard prevents it, discard it (or downgrade to informational).
3. **Confirm exploitability**: are the preconditions realistic? Is it profitable / impactful? Who can trigger it?
4. **Eliminate false positives** the same way `audit-vuln-review` does — do not report theoretical issues that the broader context already prevents.
5. **Search the repo for the same pattern elsewhere** (grep/ripgrep): a real finding often recurs. Note every additional location.

### 6. Assign Severity

Use the same scale as the rest of the audit toolkit, weighing **impact × likelihood**:

| Severity | Criteria |
|----------|----------|
| **HIGH** | Direct loss of funds, unauthorized transfers, protocol insolvency, bypass of critical access control. Exploitable in a single transaction or with minimal setup; high likelihood and significant financial impact. |
| **MED** | Conditional fund loss (requires specific state or unlikely preconditions), partial protocol disruption, governance manipulation, economic exploits with limited profitability, or issues needing complex attack chains. |
| **LOW** | Minimal financial impact, best-practice violations with theoretical risk, edge cases with negligible impact, issues requiring impractical preconditions, or minor logic inconsistencies that don't affect core functionality. |
| **INFORMATIONAL** | No direct security impact. Code-quality, documentation, style, or minor gas optimizations that don't introduce risk. |

(For clients who use a Critical tier, treat HIGH-with-trivial-exploitation-and-catastrophic-impact as Critical and note it; otherwise keep to the four-tier scale above for consistency with `audit-vuln-review` and `audit-severity-review`.)

### 7. Recommend Fixes

For each finding, give a clear, minimal, actionable fix:
- Explain **what** to change and **why**.
- Provide a concise before → after code snippet in the project's language.
- Note any risk the fix itself introduces (e.g., a reentrancy guard breaking a legitimate callback).
- Keep it minimal — fix the vulnerability without unnecessary refactoring.

## Output Format

Save the complete audit report as a markdown file named `audit-report.md` in the current working directory. Also print the Findings Summary table directly in the conversation.

### Report Structure

```markdown
# Security Audit Report

**Project**: <project name>
**Date**: <current date>
**Files in Scope**: <count>  (<total LoC if known>)
**Auditor**: Claude Code (audit-codebase skill)
**Review method**: <single-pass | parallel (N agents)>

---

## Scope

| File | Language | LoC |
|------|----------|-----|
| ... | ... | ... |

<commit hash / branch audited, if available>

---

## Protocol Overview

<2-4 sentences: what the protocol does, core invariants, trust model, assets at risk.>

---

## Findings Summary

| ID | Title | Severity | Status |
|----|-------|----------|--------|
| H-01 | <title> | HIGH | Open |
| M-01 | <title> | MED | Open |
| L-01 | <title> | LOW | Open |
| I-01 | <title> | INFORMATIONAL | Open |

**Totals**: N High · N Medium · N Low · N Informational

---

## Detailed Findings

### [H-01] <Title>

**Severity**: HIGH
**Location**: `path/to/File.sol#L42-L58` (+ any other occurrences)

**Description**
<What the issue is, why it matters, and the invariant it breaks. 2-5 sentences.>

**Exploit Scenario**
<Step-by-step path an attacker takes to exploit it, with concrete actors and state.>

**Recommendation**
<Fix approach.>

```solidity
// Before
...
// After
...
```

**Other Occurrences**
<Same pattern elsewhere, or "None found.">

---

<repeat for every finding, ordered HIGH → MED → LOW → INFORMATIONAL>

---

## Coverage Notes

<What was reviewed, any areas given lighter attention and why, assumptions made, and anything out of scope that may warrant attention.>
```

## Edge Cases and Considerations

- **No scope provided**: infer a candidate scope, list it, and confirm with the user before auditing. Never silently audit more or less than intended.
- **Vulnerability spans multiple files/contracts**: trace the full cross-contract call chain (e.g., cross-contract reentrancy, proxy + implementation).
- **External dependencies**: read imported libraries/interfaces (`lib/`, `node_modules/`, crate deps) when a finding depends on their behavior.
- **Code doesn't compile / no tests**: note it, but still perform the review; do not attempt to fix the build.
- **Very large scope (>2000 LoC)**: use parallel review (Step 4) and explicitly note any areas given lighter coverage in Coverage Notes — never imply full coverage that wasn't done.
- **Findings overlap with a provided prior report**: cross-reference rather than re-reporting; flag anything new.
- **Zero findings**: that is a valid outcome — report it, and be specific in Coverage Notes about what was checked so the result is credible.

## Quality Checks

Before saving the report:
- Every in-scope file was actually read and reviewed (not assessed from the README alone).
- Each reported finding cites specific code evidence (file, function, line) and a concrete exploit path.
- Each finding survived validation (Step 5) — guards were checked, exploitability confirmed, false positives eliminated.
- The repo-wide same-pattern search was actually run (grep/ripgrep), and "Other Occurrences" reflects real results.
- Severities follow the defined scale and weigh both impact and likelihood.
- Fix recommendations are correct, minimal, and don't introduce new vulnerabilities.
- The Findings Summary table totals match the detailed findings.
- Coverage Notes honestly state what was and wasn't deeply reviewed.
- The report file has been saved to `audit-report.md`.

## User Interaction

After completing the audit:
1. Confirm the report was saved and provide the file path.
2. Print the Findings Summary table in the conversation.
3. Lead with the highest-severity findings and offer to walk through any finding in detail.
4. Offer follow-ups: deep-dive a finding with `audit-vuln-review`, reassess severities with `audit-severity-review`, or verify fixes later with `audit-verify-fixes`.
5. Be willing to revise a verdict if the user supplies additional context (e.g., an off-chain control or known constraint).
```
