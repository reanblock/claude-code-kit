#!/usr/bin/env bash
# Run the QA suite against a deployed environment and build a shareable HTML report.
#
#   ./run.sh <env> [smoke|full]     e.g. ./run.sh uat smoke
#
# PROD needs QA_CONFIRM_PROD=yes (or typing PROD at the prompt).
# Tests tagged @writes are excluded in PROD unless QA_ALLOW_PROD_WRITES=yes.
set -euo pipefail
cd "$(dirname "$0")"

ENV="${1:?usage: ./run.sh <env> [smoke|full]}"
SUITE="${2:-smoke}"
case "$SUITE" in smoke|full) ;; *) echo "suite must be smoke or full" >&2; exit 64 ;; esac

if [[ "$ENV" == prod && "${QA_CONFIRM_PROD:-}" != yes ]]; then
  if [[ -t 0 ]]; then
    read -r -p "Run the $SUITE suite against PROD? Type PROD to confirm: " answer
    [[ "$answer" == PROD ]] || { echo "Aborted."; exit 1; }
    export QA_CONFIRM_PROD=yes
  else
    echo "Refusing to run against PROD: set QA_CONFIRM_PROD=yes" >&2
    exit 1
  fi
fi

URL="${QA_BASE_URL:-$(node -p "require('./qa.config.json').environments['$ENV']?.url ?? ''")}"
PROJECT="$(node -p "require('./qa.config.json').project")"
export QA_ENV="$ENV"
export QA_RUN_DIR="$PWD/reports/$ENV-$SUITE-$(date +%Y%m%d-%H%M%S)"
mkdir -p "$QA_RUN_DIR"

echo "QA: $PROJECT | $ENV | $SUITE | $URL"
set +e
./node_modules/.bin/playwright test --project="$SUITE"
CODE=$?
set -e

NOTE=""
if [[ "$ENV" == prod && "${QA_ALLOW_PROD_WRITES:-}" != yes ]]; then
  NOTE="PROD read-only run: tests tagged @writes were excluded."
fi

if [[ -f "$QA_RUN_DIR/results.json" ]] && command -v uv >/dev/null; then
  uv run --quiet scripts/build_report.py "$QA_RUN_DIR/results.json" \
    --out "$QA_RUN_DIR/report.html" --title "$PROJECT QA: $(echo "$ENV" | tr '[:lower:]' '[:upper:]') $SUITE" \
    --env "$ENV" --suite "$SUITE" --url "$URL" --note "$NOTE"
  echo "Report: $QA_RUN_DIR/report.html"
else
  echo "Report: $QA_RUN_DIR/playwright-report/index.html (install uv for the single-file report)"
fi
exit "$CODE"
