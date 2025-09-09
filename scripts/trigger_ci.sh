#!/usr/bin/env bash
set -euo pipefail
REPO="adiracoon/forecast-advisor-open"
GH="$(command -v gh || true)"; [ -x "${GH:-}" ] || GH="/opt/homebrew/bin/gh"; [ -x "$GH" ] || GH="/usr/local/bin/gh"
[ -x "$GH" ] || { echo "gh not found"; exit 1; }
echo "using gh at: $GH"

trigger(){ "$GH" workflow run -R "$REPO" "$1"; }
last_id(){ "$GH" run list -R "$REPO" --workflow "$1" --branch main -L 1 --json databaseId -q '.[0].databaseId'; }
status(){ "$GH" run view -R "$REPO" "$1" --json status -q .status 2>/dev/null || echo unknown; }
concl(){ "$GH" run view -R "$REPO" "$1" --json conclusion -q .conclusion 2>/dev/null || echo unknown; }

wait_for(){
  WF="$1"; echo "waiting for $WF …"; sleep 3
  RID="$(last_id "$WF")"; while [ -z "${RID:-}" ]; do sleep 3; RID="$(last_id "$WF")"; done
  S="$(status "$RID")"
  while [ "$S" = "queued" ] || [ "$S" = "in_progress" ] || [ "$S" = "waiting" ]; do sleep 6; S="$(status "$RID")"; done
  "$GH" run view -R "$REPO" "$RID" --json status,conclusion,url -q '.status+" "+.conclusion+" "+.url'
  "$GH" run view -R "$REPO" "$RID" --log | tail -n 200 || true
  [ "$(concl "$RID")" = "success" ]
}

"$GH" workflow run -R "$REPO" .github/workflows/ci.yml
"$GH" workflow run -R "$REPO" .github/workflows/agent.yml
wait_for "CI"
wait_for "Agent"
