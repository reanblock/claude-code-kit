"""Tests for build_report.py. Run: uv run --with pytest pytest skills/qa-test/scripts"""

import base64
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
spec = importlib.util.spec_from_file_location("build_report", HERE / "build_report.py")
br = importlib.util.module_from_spec(spec)
sys.modules["build_report"] = br
spec.loader.exec_module(br)

PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)


def result(status, attachments=(), error=None, duration=100):
    r = {"status": status, "duration": duration, "attachments": list(attachments)}
    if error:
        r["errors"] = [{"message": error}]
    return r


def make_report(tmp_path: Path) -> dict:
    shot = tmp_path / "fail.png"
    shot.write_bytes(PNG)
    png = {"name": "screenshot", "contentType": "image/png", "path": str(shot)}
    gone = {"name": "screenshot", "contentType": "image/png", "path": str(tmp_path / "gone.png")}
    trace = {"name": "trace", "contentType": "application/zip", "path": str(tmp_path / "t.zip")}
    return {
        "stats": {"startTime": "2026-11-27T10:00:00Z", "duration": 4200},
        "errors": [],
        "suites": [
            {
                "title": "smoke/home.spec.ts",
                "file": "smoke/home.spec.ts",
                "specs": [
                    {"title": "SMK-01 home loads", "file": "smoke/home.spec.ts", "line": 3,
                     "tests": [{"projectName": "smoke", "status": "expected",
                                "results": [result("passed")]}]},
                    {"title": "SMK-02 login <form>", "file": "smoke/home.spec.ts", "line": 9,
                     "tests": [{"projectName": "smoke", "status": "unexpected",
                                "results": [
                                    result("failed", [png, trace], "\x1b[31mExpected <b>200</b>\x1b[39m"),
                                    result("failed", [png], "\x1b[31mExpected <b>200</b>\x1b[39m"),
                                ]}]},
                ],
                "suites": [
                    {"title": "navigation", "file": "smoke/home.spec.ts",
                     "specs": [
                         {"title": "SMK-03 links", "file": "smoke/home.spec.ts", "line": 20,
                          "tests": [{"projectName": "smoke", "status": "flaky",
                                     "results": [result("timedOut", [gone], "Timeout"),
                                                 result("passed")]}]},
                         {"title": "SMK-04 writes", "file": "smoke/home.spec.ts", "line": 30,
                          "tests": [{"projectName": "smoke", "status": "skipped",
                                     "results": [result("skipped", duration=0)]}]},
                     ]},
                ],
            }
        ],
    }


def test_collect_flattens_nested_suites_and_maps_outcomes(tmp_path):
    cases = br.collect(make_report(tmp_path))
    assert [c.outcome for c in cases] == ["passed", "failed", "flaky", "skipped"]
    assert cases[2].title == "navigation › SMK-03 links"
    assert cases[0].title == "SMK-01 home loads"  # file-name suite title is dropped
    assert cases[1].file == "smoke/home.spec.ts:9"
    assert cases[1].duration_ms == 200


def test_failed_test_embeds_only_image_attachments_from_last_failure(tmp_path):
    failed = br.collect(make_report(tmp_path))[1]
    assert len(failed.screenshots) == 1
    assert failed.screenshots[0].startswith("data:image/png;base64,")
    assert failed.error == "Expected <b>200</b>"  # ANSI stripped


def test_missing_screenshot_file_is_counted_not_fatal(tmp_path):
    flaky = br.collect(make_report(tmp_path))[2]
    assert flaky.screenshots == [] and flaky.missing_screenshots == 1


def test_passed_tests_carry_no_screenshots_or_errors(tmp_path):
    passed = br.collect(make_report(tmp_path))[0]
    assert passed.screenshots == [] and passed.error == ""


def test_summarize_counts():
    cases = [br.TestCase("a", "", "", o, 0) for o in ("passed", "passed", "failed", "flaky", "skipped")]
    assert br.summarize(cases) == {"passed": 2, "failed": 1, "flaky": 1, "skipped": 1, "total": 5}


def test_render_escapes_html_and_marks_fail(tmp_path):
    out = br.render(br.collect(make_report(tmp_path)), title="Acme <QA>", env="uat",
                    suite="smoke", url="https://uat.example.com", note="read-only")
    assert 'badge FAIL' in out
    assert "Acme &lt;QA&gt;" in out
    assert "Expected &lt;b&gt;200&lt;/b&gt;" in out and "<b>200</b>" not in out
    assert "SMK-02 login &lt;form&gt;" in out
    assert "data:image/png;base64," in out
    assert "read-only" in out and "UAT" in out
    assert "1 screenshot file(s) not found." in out


def test_render_pass_when_no_failures():
    out = br.render([br.TestCase("ok", "", "smoke", "passed", 10)], title="t")
    assert "badge PASS" in out and "<h2>Failures</h2>" not in out


def test_render_fails_on_empty_run_or_run_errors():
    assert "badge FAIL" in br.render([], title="t")
    out = br.render([br.TestCase("ok", "", "", "passed", 1)], title="t", run_errors=["config <boom>"])
    assert "badge FAIL" in out and "config &lt;boom&gt;" in out


def test_cli_writes_report(tmp_path, capsys):
    results = tmp_path / "results.json"
    results.write_text(json.dumps(make_report(tmp_path)))
    out = tmp_path / "report.html"
    assert br.main([str(results), "--out", str(out), "--env", "prod", "--suite", "smoke"]) == 0
    assert out.read_text().startswith("<!doctype html>")
    assert "1 passed, 1 failed, 1 flaky, 1 skipped" in capsys.readouterr().out


def test_cli_missing_results_file(tmp_path):
    assert br.main([str(tmp_path / "nope.json"), "--out", str(tmp_path / "r.html")]) == 1
