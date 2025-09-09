#!/usr/bin/env bash
set -euo pipefail

REPO="adiracoon/forecast-advisor-open"

trigger()       { gh workflow run -R "$REPO" "$1" >/dev/null; }
last_run_id()   { gh run list -R "$REPO" --workflow "$1" --branch main -L 1 --json databaseId -q '.[0].databaseId'; }
run_status()    { gh run view -R "$REPO" "$1" --json status     -q .status; }
run_conclusion(){ gh run view -R "$REPO" "$1" --json conclusion -q .conclusion; }

wait_for() {
  WF="$1"
  sleep 2
  RID="$(last_run_id "$WF")"
  while [ -z "${RID:-}" ]; do sleep 2; RID="$(last_run_id "$WF")"; done
  S="$(run_status "$RID")"
  while [ "$S" = "queued" ] || [ "$S" = "in_progress" ]; do sleep 5; S="$(run_status "$RID")"; done
  echo "=== $WF done ==="
  gh run view -R "$REPO" "$RID" --json status,conclusion,url
  gh run view -R "$REPO" "$RID" --log
  C="$(run_conclusion "$RID")"
  [ "$C" = "success" ]
}

trigger "CI"
wait_for "CI"

trigger "Agent"
wait_for "Agent"
