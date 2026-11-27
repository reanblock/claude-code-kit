#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = []
# ///
"""Build one self-contained, shareable HTML QA report from Playwright JSON results.

Failure screenshots are embedded as base64, so the single report.html file can be
sent to the team without the rest of the run folder.

Usage:
    uv run build_report.py results.json --out report.html \
        [--title T] [--env uat] [--suite smoke] [--url https://...] [--note "..."]
"""

from __future__ import annotations

import argparse
import base64
import html
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

ANSI_RE = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


@dataclass
class TestCase:
    title: str
    file: str
    project: str
    outcome: str  # passed | failed | flaky | skipped
    duration_ms: int
    error: str = ""
    screenshots: list[str] = field(default_factory=list)  # data: URIs
    missing_screenshots: int = 0


def strip_ansi(text: str) -> str:
    return ANSI_RE.sub("", text or "")


def _outcome(test: dict) -> str:
    status = test.get("status")
    if status == "expected":
        return "passed"
    if status == "flaky":
        return "flaky"
    if status == "skipped":
        return "skipped"
    return "failed"


def _screenshots(result: dict) -> tuple[list[str], int]:
    uris, missing = [], 0
    for att in result.get("attachments", []):
        ctype = att.get("contentType", "")
        if not ctype.startswith("image/"):
            continue
        if att.get("body"):
            uris.append(f"data:{ctype};base64,{att['body']}")
            continue
        path = Path(att.get("path") or "")
        if path.is_file():
            data = base64.b64encode(path.read_bytes()).decode()
            uris.append(f"data:{ctype};base64,{data}")
        else:
            missing += 1
    return uris, missing


def _error(result: dict) -> str:
    errors = result.get("errors") or ([result["error"]] if result.get("error") else [])
    parts = [strip_ansi(e.get("message") or e.get("value") or "") for e in errors]
    return "\n\n".join(p for p in parts if p).strip()


def collect(report: dict) -> list[TestCase]:
    cases: list[TestCase] = []

    def walk(suite: dict, prefix: list[str]) -> None:
        title = suite.get("title", "")
        # Top-level suites are titled by file name; keep describe() titles only.
        path = prefix + ([title] if title and title != suite.get("file") else [])
        for spec in suite.get("specs", []):
            for test in spec.get("tests", []):
                results = test.get("results", [])
                outcome = _outcome(test)
                failed = [r for r in results if r.get("status") not in ("passed", "skipped")]
                shown = failed[-1] if failed else (results[-1] if results else {})
                shots, missing = _screenshots(shown) if outcome in ("failed", "flaky") else ([], 0)
                cases.append(
                    TestCase(
                        title=" › ".join(path + [spec.get("title", "")]),
                        file=f"{spec.get('file', '')}:{spec.get('line', '')}".rstrip(":"),
                        project=test.get("projectName", ""),
                        outcome=outcome,
                        duration_ms=sum(int(r.get("duration", 0)) for r in results),
                        error=_error(shown) if outcome in ("failed", "flaky") else "",
                        screenshots=shots,
                        missing_screenshots=missing,
                    )
                )
        for child in suite.get("suites", []):
            walk(child, path)

    for suite in report.get("suites", []):
        walk(suite, [])
    return cases


def summarize(cases: list[TestCase]) -> dict[str, int]:
    counts = {k: 0 for k in ("passed", "failed", "flaky", "skipped")}
    for c in cases:
        counts[c.outcome] += 1
    counts["total"] = len(cases)
    return counts


CSS = """
body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;margin:0;background:#f6f7f9;color:#1f2328}
main{max-width:1100px;margin:0 auto;padding:24px}
h1{font-size:22px;margin:0 0 4px}h2{font-size:17px;margin:28px 0 10px}
.meta{color:#59636e;font-size:13px}.meta span{margin-right:16px}
.badge{display:inline-block;padding:4px 10px;border-radius:999px;font-weight:600;font-size:13px;color:#fff}
.PASS{background:#1a7f37}.FAIL{background:#cf222e}
.cards{display:flex;gap:12px;margin:16px 0}
.card{background:#fff;border:1px solid #d1d9e0;border-radius:8px;padding:12px 16px;min-width:90px}
.card b{display:block;font-size:22px}.card small{color:#59636e}
.note{background:#fff8c5;border:1px solid #d4a72c;border-radius:6px;padding:8px 12px;font-size:13px}
.fail{background:#fff;border:1px solid #d1d9e0;border-left:4px solid #cf222e;border-radius:6px;padding:12px 16px;margin-bottom:14px}
.fail.flaky{border-left-color:#bf8700}
.fail h3{font-size:15px;margin:0 0 4px}
pre{background:#f6f8fa;padding:10px;border-radius:6px;overflow:auto;font-size:12px;white-space:pre-wrap}
img{max-width:100%;border:1px solid #d1d9e0;border-radius:4px;margin-top:8px}
table{width:100%;border-collapse:collapse;background:#fff;font-size:13px}
th,td{text-align:left;padding:6px 10px;border-bottom:1px solid #e4e8ec}
.o-passed{color:#1a7f37}.o-failed{color:#cf222e;font-weight:600}.o-flaky{color:#9a6700}.o-skipped{color:#59636e}
"""


def render(
    cases: list[TestCase],
    *,
    title: str,
    env: str = "",
    suite: str = "",
    url: str = "",
    note: str = "",
    started: str = "",
    duration_ms: int = 0,
    run_errors: list[str] | None = None,
) -> str:
    e = html.escape
    counts = summarize(cases)
    run_errors = run_errors or []
    verdict = "FAIL" if counts["failed"] or run_errors or not cases else "PASS"

    meta = [f"<span>Env: <b>{e(env.upper())}</b></span>" if env else "",
            f"<span>Suite: <b>{e(suite)}</b></span>" if suite else "",
            f'<span>URL: <a href="{e(url)}">{e(url)}</a></span>' if url else "",
            f"<span>Started: {e(started)}</span>" if started else "",
            f"<span>Duration: {duration_ms / 1000:.1f}s</span>" if duration_ms else ""]

    cards = "".join(
        f'<div class="card"><b>{counts[k]}</b><small>{k}</small></div>'
        for k in ("total", "passed", "failed", "flaky", "skipped")
    )

    blocks = []
    for msg in run_errors:
        blocks.append(f'<div class="fail"><h3>Run error</h3><pre>{e(msg)}</pre></div>')
    for c in (c for c in cases if c.outcome in ("failed", "flaky")):
        imgs = "".join(f'<img alt="screenshot" src="{s}">' for s in c.screenshots)
        if c.missing_screenshots:
            imgs += f'<p class="meta">{c.missing_screenshots} screenshot file(s) not found.</p>'
        label = "Flaky (failed, then passed on retry)" if c.outcome == "flaky" else "Failed"
        blocks.append(
            f'<div class="fail {c.outcome}"><h3>{e(c.title)}</h3>'
            f'<div class="meta"><span>{label}</span><span>{e(c.file)}</span></div>'
            f"<pre>{e(c.error or 'No error message recorded.')}</pre>{imgs}</div>"
        )

    rows = "".join(
        f'<tr><td>{e(c.title)}</td><td class="o-{c.outcome}">{c.outcome}</td>'
        f"<td>{e(c.project)}</td><td>{c.duration_ms / 1000:.1f}s</td><td>{e(c.file)}</td></tr>"
        for c in cases
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><style>{CSS}</style></head>
<body><main>
<h1>{e(title)} <span class="badge {verdict}">{verdict}</span></h1>
<div class="meta">{"".join(meta)}</div>
<div class="cards">{cards}</div>
{f'<p class="note">{e(note)}</p>' if note else ""}
{"<h2>Failures</h2>" + "".join(blocks) if blocks else ""}
<h2>All tests</h2>
<table><thead><tr><th>Test</th><th>Result</th><th>Project</th><th>Time</th><th>File</th></tr></thead>
<tbody>{rows or '<tr><td colspan="5">No tests ran.</td></tr>'}</tbody></table>
<p class="meta">Generated {datetime.now():%Y-%m-%d %H:%M}</p>
</main></body></html>
"""


def build(results_path: Path, out_path: Path, **opts: str) -> dict[str, int]:
    report = json.loads(results_path.read_text())
    cases = collect(report)
    stats = report.get("stats", {})
    run_errors = [strip_ansi(err.get("message", "")) for err in report.get("errors", [])]
    out_path.write_text(
        render(
            cases,
            started=stats.get("startTime", ""),
            duration_ms=int(stats.get("duration", 0)),
            run_errors=run_errors,
            **opts,
        )
    )
    return summarize(cases)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("results", type=Path, help="Playwright JSON reporter output")
    p.add_argument("--out", type=Path, required=True)
    p.add_argument("--title", default="QA report")
    p.add_argument("--env", default="")
    p.add_argument("--suite", default="")
    p.add_argument("--url", default="")
    p.add_argument("--note", default="")
    a = p.parse_args(argv)
    if not a.results.is_file():
        print(f"results file not found: {a.results}", file=sys.stderr)
        return 1
    counts = build(a.results, a.out, title=a.title, env=a.env, suite=a.suite, url=a.url, note=a.note)
    print(
        f"{counts['passed']} passed, {counts['failed']} failed, "
        f"{counts['flaky']} flaky, {counts['skipped']} skipped -> {a.out}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
