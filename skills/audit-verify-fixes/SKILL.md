---
name: audit-verify-fixes
description: Verify whether client code changes actually resolve issues identified in a smart contract security audit. Findings may come from an audit report file (PDF/markdown) or from a GitHub repository where each finding is an issue. Use when users request "verify fixes", "check remediations", "validate fixes", "check if issues are fixed", or pass a GitHub repo URL and ask to verify the fixes for its findings/issues.
---

# Audit Fix Verification

You are an expert smart contract security researcher. Your task is to take a set of security audit findings and verify whether the client's code changes (identified by commit SHAs or update references) actually resolve each issue described.

Findings arrive in one of two forms — an **audit report file**, or a **GitHub repository whose issues are the findings**. The workflow below branches only on how findings and fix commits are located; the verification, classification, and reporting logic is identical for both.

## ⛔ Read-Only Constraint — Non-Negotiable

**This skill is strictly read-only with respect to any remote repository. The repository under review is shared with the client.**

DO NOT MAKE ANY CHANGES OR POST ANY COMMENTS OR UPDATES TO THE GITHUB REPO SINCE THIS IS SHARED WITH THE CLIENT.

Concretely, you must **never** run any command that writes to the remote or its issues:

- ❌ `gh issue comment`, `gh issue close`, `gh issue reopen`, `gh issue edit`, `gh issue create`
- ❌ `gh pr create`, `gh pr comment`, `gh pr review`, `gh pr merge`
- ❌ `gh api` with `-X POST`, `-X PATCH`, `-X PUT`, or `-X DELETE`
- ❌ `git push`, `git commit`, `git tag`, or anything that mutates the shared branch
- ❌ Editing any file in the repository under review

The **only** permitted `gh` and `git` operations are read-only:

- ✅ `gh issue list`, `gh issue view` (including `--comments`)
- ✅ `gh api` GET requests (the default method)
- ✅ `git fetch`, `git log`, `git show`, `git diff`, `git branch`, `git checkout` (local inspection only)

Produce the verification report as terminal output (and a local file only if the user explicitly asks). Any finding that appears to require a comment or update on the client's repo is reported to the **user**, who decides what to communicate. If you believe a write operation is genuinely necessary, stop and ask the user first — never assume permission.

## Trigger Conditions

Use this skill when the user requests:
- "verify fixes"
- "check remediations"
- "validate fixes"
- "check if issues are fixed"
- "review client updates"
- "verify audit remediation"

AND a finding source is available — either a security audit report, or a GitHub repository whose issues are the findings.

## Processing Workflow

### 1. Determine the Finding Source

Before anything else, establish which mode applies:

| Signal | Mode |
|---|---|
| The argument is a GitHub repository URL (`https://github.com/<org>/<repo>`), or the user refers to findings as issues in a repo | **Mode B — GitHub Issues** |
| The argument is a file path, or a report file is named in conversation / found in the workspace | **Mode A — Audit Report** |

If both are present, ask the user which to use. If neither can be determined, ask — do not guess.

---

### 1A. Mode A — Locate the Audit Report

The audit report file must be resolved before any analysis begins. Use this priority order:

1. **Skill argument**: If the user invoked the skill with an argument (e.g., `/verify-fixes report.pdf`), use that path directly.
2. **Conversation context**: If the user mentioned a specific file name or path earlier in the conversation, use that.
3. **Workspace search**: If no file was specified, search the current workspace for candidate audit files:
   ```bash
   find . -maxdepth 3 -type f \( -name "*.pdf" -o -name "*.md" \) | head -20
   ```
   Look for files with names containing keywords like `audit`, `report`, `findings`, `security`, or `review`. If exactly one strong candidate is found, use it. If multiple candidates exist, present the list and ask the user to choose.
4. **Ask the user**: If no candidates are found, ask the user to provide the file path. Do not guess or proceed without a report.

---

### 1B. Mode B — Locate the GitHub Findings Repository

Used when the client tracks findings as GitHub issues. In this arrangement:

- Each **finding is an issue** in the repository.
- Each issue carries a **client comment** explaining how they fixed it, including a **commit SHA**.
- The **code lives in the same repository**, on the **`fixes-review` branch** — that is where the referenced SHAs are found.

**Step A — Resolve the repository.** Take the GitHub URL from the skill argument or the conversation. Confirm access before proceeding:

```bash
gh repo view <org>/<repo> --json name,defaultBranchRef
```

**Step B — Obtain the code locally.** If the current working directory is not already a clone of that repo, clone it (to a scratch location, not into the user's project):

```bash
git clone <repo_url> <scratch_dir>
```

**Step C — Fetch the review branch.** All fix commits are expected on `fixes-review`:

```bash
git fetch origin fixes-review
git log --oneline origin/fixes-review | head -20
```

If the `fixes-review` branch does not exist, stop and ask the user for the correct branch name rather than falling back to the default branch — verifying against the wrong branch produces confidently wrong results.

Re-read the read-only constraint above before running any `gh` command in this mode.

---

### 2. Extract Findings

#### 2A. Mode A — Extract Report Findings

Read and parse the located audit report. Extract each finding with:
- Finding ID/identifier
- Title
- Severity
- Description of the vulnerability
- Affected code locations (contracts, functions, line numbers)
- The specific fix recommendation (if provided)
- **Client commit SHA or update reference** (if present)
- **Client fix explanation** (if present) — the client's own description of how they addressed the finding

For PDF reports:
```bash
pip install pypdf --break-system-packages 2>/dev/null
```

#### 2B. Mode B — Extract Findings from GitHub Issues

**Step A — Enumerate the findings.** Include closed issues; a client may have closed an issue they consider fixed, and that claim is exactly what needs verifying:

```bash
gh issue list --repo <org>/<repo> --state all --limit 200 \
  --json number,title,labels,state,body
```

**Step B — Read each issue with its comments** to obtain the client's fix explanation and commit SHA:

```bash
gh issue view <issue_number> --repo <org>/<repo> --comments \
  --json number,title,labels,state,body,comments
```

**Step C — Extract per finding:**

- **Finding ID** — prefer an explicit identifier in the issue title (e.g. `FIND-01`); otherwise use the issue number (`#42`).
- **Title**, **description**, **affected code locations**, **fix recommendation** — from the issue body.
- **Severity** — search in this order, stopping at the first hit: issue **labels**, then a prefix/tag in the **title**, then the **body**. If severity cannot be determined for a finding, do not guess — ask the user.
- **Client fix explanation** — the client's comment describing how they addressed it.
- **Commit SHA** — extracted from that comment. A comment may reference multiple commits; capture all of them.

##### Severity Scale (Mode B)

This mode uses a four-level scale. **Use these terms verbatim in the output** — do not translate them into the Critical/High/Medium/Low/Informational scale used by Mode A. Mapping is lossy ("Major" spans High and Medium; "Minor" is closer to Low) and would misreport the client's own severities back to them.

| Severity | Definition |
|---|---|
| **Critical** | A serious and exploitable vulnerability that can lead to loss of funds, unrecoverable locked funds, or catastrophic denial of service. |
| **Major** | A vulnerability or bug that can affect the correct functioning of the system, lead to incorrect states or denial of service. |
| **Minor** | A violation of common best practices or incorrect usage of primitives, which may not currently have a major impact on security, but may do so in the future or introduce inefficiencies. |
| **Informational** | Comments and recommendations of design decisions or potential optimizations, that are not relevant to security. Their application may improve aspects such as user experience or readability, but is not strictly necessary. This category may also include opinionated recommendations that the project team might not share. |

**Note on Informational findings:** The definition above explicitly includes opinionated recommendations the project team may not share. A "Not Fixed" on an Informational finding is therefore often a legitimate, deliberate decline rather than a failure to act. Where the client's comment indicates a considered decision not to apply the recommendation, say so in the explanation rather than presenting it as an outstanding issue.

### 3. Analyze Git History for Each Finding

For each finding that has an associated commit SHA or update reference:

**Mode B — resolve every SHA against `fixes-review` first.** The commit must be reachable from that branch; a SHA that exists elsewhere (or not at all) has not landed in the code under review:

```bash
# Confirm the SHA exists and is reachable from the review branch
git merge-base --is-ancestor <commit_sha> origin/fixes-review && echo "on fixes-review"

# If the above fails, check whether the commit exists at all
git cat-file -t <commit_sha> 2>/dev/null
```

If a referenced SHA cannot be found, or exists but is not reachable from `fixes-review`, mark the finding **Unresolved** and state which of the two it was. Do not silently fall back to searching other branches.

**Step A — Retrieve the diff for the commit:**
```bash
git show <commit_sha> --stat
git show <commit_sha> -- <affected_files>
git diff <commit_sha>~1..<commit_sha> -- <affected_files>
```

**Step B — If no specific commit is provided**, search the git history for relevant changes:
```bash
# Search commit messages for references to the finding ID
git log --all --oneline --grep="<finding_id>"

# Search for changes to the affected files/functions
git log --all --oneline -- <affected_file_path>

# Look at recent commits for relevant changes
git log --all --oneline --since="<report_date>" -- <affected_file_path>
```

**Step C — Examine the actual code changes:**
```bash
# View the full diff
git diff <base_commit>..<fix_commit> -- <affected_files>

# Check the current state of the affected code
git show <fix_commit>:<file_path>
```

**Step D — Detect unrelated changes in the same commit:**

For every commit analyzed, compare the full commit scope against what the finding required:

```bash
# Get the full file list touched by the commit
git show <commit_sha> --stat --name-only

# Get the full diff to review ALL changes, not just the affected files
git show <commit_sha> -p
```

Classify each changed file/hunk in the commit as:
- **Related**: Directly addresses the finding (the fix itself, necessary refactors to support the fix, updated tests for the fix)
- **Unrelated**: Changes that have no connection to the finding (new features, unrelated refactors, formatting changes to other files, other bug fixes bundled in)

Flag a commit as containing unrelated changes when any of these are true:
- Files outside the affected scope were modified and the changes don't support the fix
- Hunks within an affected file make changes unrelated to the vulnerability (e.g., renaming an unrelated variable, adding a new unrelated function)
- The commit message references work beyond the finding (e.g., "fix FIND-001 and add new staking feature")

### 4. Verification Criteria

For each finding, determine the fix status by evaluating:

1. **Does the diff address the root cause?**
   - The code change must fix the underlying vulnerability, not just a symptom
   - Compare the fix against the vulnerability description and any recommendations in the report

2. **Is the fix complete?**
   - All affected code paths must be addressed
   - Edge cases mentioned in the finding must be covered
   - If multiple files/functions are affected, all must be updated

3. **Does the fix introduce new issues?**
   - Check for regressions or new attack vectors introduced by the change
   - Verify the fix doesn't break existing functionality
   - Look for common pitfalls (e.g., fixing reentrancy but introducing a DoS vector)

4. **Is the fix consistent with the recommendation?**
   - If the report suggests a specific fix, does the implementation match?
   - If a different approach was taken, is it equally effective?

5. **Does the client's explanation match the diff?**

   Both modes supply the client's own account of the fix — in Mode A from the report, in Mode B from the issue comment. Read it for context, but **verify against the diff, not the claim**. The stated fix is an assertion to be tested, not evidence.

   Compare what the client says they did against what the diff actually does, and resolve as follows:

   | Claim vs. diff | Root cause addressed? | Outcome |
   |---|---|---|
   | Match | Yes | **Fixed** — normal case |
   | Mismatch (wording is loose or inaccurate, but the code genuinely fixes it) | Yes | **Fixed** — note the discrepancy in the explanation; do not penalise imprecise wording |
   | Mismatch (the claim describes protection the diff does not contain) | No | **Not Fixed** or **Mitigated** as the diff warrants — state the discrepancy explicitly |
   | Claim describes work beyond the diff (e.g. "also added tests" with no tests present) | Yes | **Fixed** — note the unsubstantiated part of the claim |

   The status is always determined by the code, never by the claim. A discrepancy is reported because it is useful signal for the reviewer, and because a claim more thorough than the shipped diff often indicates the client believes they are more protected than they are — but it never by itself downgrades a fix that genuinely works.

### 5. Status Classification

Assign one of the following statuses to each finding:

| Status | Definition |
|---|---|
| **Fixed** | The code change fully resolves the described vulnerability. The root cause is addressed and the fix is complete. |
| **Mitigated** | The code change reduces the risk but does not fully eliminate the vulnerability. The fix may be partial, address only some attack vectors, or use an alternative approach that reduces but doesn't eliminate exposure. |
| **Not Fixed** | A commit/update was referenced but the code changes do not resolve the issue. The vulnerability remains exploitable as described. |
| **Unresolved** | No commit SHA or code change was provided for this finding, or the referenced commit could not be found in the repository. The issue has not been addressed. In Mode B this also covers: the issue has no client fix comment, the comment references no commit SHA, or the referenced SHA is not reachable from `fixes-review`. |

### 6. Output Format

Present results in two sections: the **Fix Verification Table** and (if applicable) the **Unrelated Changes Report**.

#### Fix Verification Table

```
╔════════════╦══════════╦══════════════╦════════════════╦═══════════════════════════════════════════════════════════════╗
║ Finding ID ║ Severity ║ Status       ║ Extra Changes? ║ Explanation                                                   ║
╠════════════╬══════════╬══════════════╬════════════════╬═══════════════════════════════════════════════════════════════╣
║ FIND-001   ║ Critical ║ Fixed        ║ Yes            ║ Reentrancy guard added via nonReentrant modifier on withdraw()║
║ FIND-002   ║ High     ║ Mitigated    ║ No             ║ Added slippage check but hardcoded at 5%; should be user-set  ║
║ FIND-003   ║ High     ║ Not Fixed    ║ Yes            ║ Commit updates comments only; unchecked return value remains  ║
║ FIND-004   ║ Medium   ║ Unresolved   ║ --             ║ No commit SHA provided; access control issue remains          ║
╚════════════╩══════════╩══════════════╩════════════════╩═══════════════════════════════════════════════════════════════╝

Summary: 4 findings reviewed | 1 Fixed | 1 Mitigated | 1 Not Fixed | 1 Unresolved
```

The **Extra Changes?** column values:
- **Yes** — the fix commit contains changes unrelated to this finding (details below)
- **No** — the commit is scoped cleanly to this finding only
- **--** — not applicable (no commit to analyze)

#### Unrelated Changes Report

If any commits were flagged with "Yes" in the Extra Changes column, output a second table detailing what else was changed:

```
╔════════════╦══════════════╦══════════════════════════════════════════════════════════════════════════════════╗
║ Finding ID ║ Commit       ║ Unrelated Changes                                                              ║
╠════════════╬══════════════╬══════════════════════════════════════════════════════════════════════════════════╣
║ FIND-001   ║ a1b2c3d      ║ Also adds new stake() function in Vault.sol; modifies unrelated Router.sol     ║
║ FIND-003   ║ e4f5g6h      ║ Reformats whitespace across 5 files; updates README                            ║
╚════════════╩══════════════╩══════════════════════════════════════════════════════════════════════════════════╝

⚠ 2 of 3 fix commits contain changes beyond the scope of their respective findings.
  These extra changes should be reviewed independently — they were not part of the original audit.
```

**Output Requirements:**
- Use ASCII box-drawing characters for terminal display
- Sort by severity, using the scale that matches the mode:
  - **Mode A** (audit report): Critical → High → Medium → Low → Informational
  - **Mode B** (GitHub issues): Critical → Major → Minor → Informational — print labels verbatim; do not translate them to the Mode A scale
- Within the same severity, sort by status (Not Fixed → Unresolved → Mitigated → Fixed)
- Keep explanations concise but specific — reference the actual code changes observed
- Include the summary line with counts for each status
- The unrelated changes report should list the specific files or functions that were changed outside the finding's scope
- End the unrelated changes report with a warning line summarizing how many fix commits had extra changes and a reminder that those changes were not covered by the audit

### 7. Detailed Findings (Optional)

After the summary table, offer to provide detailed analysis for any specific finding. When requested, include:

- The exact code diff reviewed
- Line-by-line analysis of the change
- Comparison against the original vulnerability description
- Any residual risk or recommendations

## Edge Cases and Considerations

- **Squashed commits**: If the client squashed multiple fixes into one commit, analyze the full diff against all relevant findings
- **Rebased history**: The commit SHA in the report may not exist if the branch was rebased; search by commit message or date range instead
- **Multiple commits per finding**: A fix may span multiple commits; trace the full change set
- **Indirect fixes**: Sometimes a finding is resolved by a broader refactor rather than a targeted fix; verify the vulnerability is no longer present regardless of approach
- **Removed code**: If the vulnerable code was entirely removed/replaced, verify the functionality is either no longer needed or implemented safely elsewhere
- **Configuration changes**: Some fixes may be parameter changes (e.g., updating a threshold) rather than code changes; validate these against the finding's requirements
- **Missing commit SHAs**: If the report references updates but no specific commits, use file-level git history and date ranges to identify candidate changes
- **Mode B — closed issues**: An issue being closed is a claim, not evidence. Verify the diff regardless of issue state, and flag any issue closed without a corresponding code change
- **Mode B — multiple SHAs in one comment**: Treat the full set as the fix; analyze each and assess the combined effect
- **No client explanation**: The claim/diff comparison is skipped, not failed. Verify the diff on its own merits and assign status normally

## Quality Checks

Before presenting results:
- **No write operation was performed against the client's repository** — no comments, no issue edits, no pushes
- All findings from the report have been accounted for
- Each status assignment has a clear, evidence-based justification
- Git diffs were actually reviewed (not just commit messages)
- The explanation references specific code changes, not generic statements
- No finding is marked "Fixed" without verifying the root cause is addressed
- Where the client provided an explanation, it was compared against the diff, and any discrepancy is noted in the finding's explanation
- No finding was downgraded solely because the client's wording was imprecise — status follows the code, not the claim
- Every fix commit was checked for unrelated changes (the full `--stat` was reviewed, not just the affected files)
- Unrelated changes are described with enough specificity (file names, function names) to be actionable

## User Interaction

After presenting the table:
1. Ask if the user wants detailed analysis on any specific finding
2. Highlight any "Not Fixed" or "Unresolved" findings that are Critical or High severity
3. Note any findings where the fix may have introduced new concerns
4. Offer to check if any additional commits since the referenced ones have further addressed open issues
