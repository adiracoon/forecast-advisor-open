#!/usr/bin/env bash
set -euo pipefail
REPO="adiracoon/forecast-advisor-open"

trigger(){ gh workflow run -R "$REPO" "$1"; }
last_id(){ gh run list -R "$REPO" --workflow "$1" --branch main -L 1 --json databaseId -q '.[0].databaseId'; }
status(){ gh run view -R "$REPO" "$1" --json status -q .status 2>/dev/null || echo unknown; }
concl(){ gh run view -R "$REPO" "$1" --json conclusion -q .conclusion 2>/dev/null || echo unknown; }

wait_for(){
WF="$1"
sleep 2
RID="$(last_id "$WF")"
while [ -z "${RID:-}" ]; do sleep 2; RID="$(last_id "$WF")"; done
S="$(status "$RID")"
while [ "$S" = "queued" ] || [ "$S" = "in_progress" ] || [ "$S" = "waiting" ]; do sleep 5; S="$(status "$RID")"; done
gh run view -R "$REPO" "$RID" --json status,conclusion,url -q '.status+" "+.conclusion+" "+.url'
gh run view -R "$REPO" "$RID" --log || true
[ "$(concl "$RID")" = "success" ]
}

trigger CI; wait_for CI
trigger Agent; wait_for Agent
