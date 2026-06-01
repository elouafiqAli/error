#!/usr/bin/env bash
# audit/run_external_audit.sh — Principal-Investigator final audit driver.
#
# Reproducibility-by-tier. Five tiers, each independently
# runnable, each emits a JSON manifest. Exit 0 iff every tier
# in the requested set passes.
#
# Usage:
#   ./audit/run_external_audit.sh           # all tiers
#   ./audit/run_external_audit.sh T0 T1 T2  # subset
#
# Tier inventory:
#   T0  build/import sanity (pdflatex, python -W error import)
#   T1  symbolic + property tests (verify_b_t1.py, 8 contracts)
#   T2  Monte-Carlo population (verify_b_t2_mc.py, 6 contracts)
#   T3  adversarial stress (audit/stress.py: seeds, mutations, boundary)
#   T4  real-data anchor (audit/anchor_real_data_full.py: 5 graphs x 4 depths)
#   T5  cross-paper parity (Paper A verify_t1_float + verify_t3 + verify_t4)
set -uo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/.." && pwd)"
REPO="$(cd "$ROOT/.." && pwd)"
OUT="$HERE/external_audit"
mkdir -p "$OUT"

SHA="$(cd "$REPO" && git rev-parse --short HEAD)"
DATE="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
PY=python3

requested=("$@")
[[ ${#requested[@]} -eq 0 ]] && requested=(T0 T1 T2 T3 T4 T5)

# macOS bash-3 has no associative arrays; use a tab-separated log instead.
STATUS_LOG="$OUT/.tier_status.tsv"; : > "$STATUS_LOG"

_get() { awk -F'\t' -v k="$1" -v c="$2" '$1==k {print $c}' "$STATUS_LOG" | tail -1; }
_rc()   { _get "$1" 2; }
_wall() { _get "$1" 3; }

run_tier() {
  local tier="$1"; shift
  local log="$OUT/${tier}.log"
  local t0=$(date +%s)
  echo "=== TIER $tier @ $SHA ==="
  ( cd "$ROOT" && "$@" ) > "$log" 2>&1
  local rc=$?
  local t1=$(date +%s)
  local w=$((t1 - t0))
  printf '%s\t%d\t%d\n' "$tier" "$rc" "$w" >> "$STATUS_LOG"
  if [[ $rc -eq 0 ]]; then
    echo "TIER $tier PASS (${w}s)"
  else
    echo "TIER $tier FAIL rc=$rc (${w}s) — see $log"
  fi
}

for t in "${requested[@]}"; do
  case "$t" in
    T0)
      run_tier T0 bash -c '
        set -e
        '"$PY"' -W error::SyntaxWarning -c "import verify_b_t1, verify_b_t2_mc" \
          && echo "imports clean"
        cd '"$REPO/partition-sandwich-preprint"' && make >/dev/null && echo "pdflatex clean"
      '
      ;;
    T1) run_tier T1 "$PY" verify_b_t1.py --seed 0 --samples 200 --manifest "$OUT/T1_verify_b_t1.json" ;;
    T2) run_tier T2 "$PY" verify_b_t2_mc.py --seed 0 --samples 50000 --trials 500 --manifest "$OUT/T2_verify_b_t2.json" ;;
    T3) run_tier T3 "$PY" audit/stress.py --seeds 15 --samples 50000 --trials 200 --manifest "$OUT/T3_stress.json" ;;
    T4) run_tier T4 "$PY" audit/anchor_real_data_full.py --depths 0 1 2 3 --manifest "$OUT/T4_anchor.json" ;;
    T5)
      run_tier T5 bash -c '
        set -e
        cd '"$REPO/partition-sandwich-preprint"' && \
        '"$PY"' verify_t1_float.py > '"$OUT/T5_paperA_t1.log"' 2>&1 && \
        '"$PY"' verify_t3_symbolic.py > '"$OUT/T5_paperA_t3.log"' 2>&1 && \
        '"$PY"' verify_t4_population.py > '"$OUT/T5_paperA_t4.log"' 2>&1
      '
      ;;
    *) echo "unknown tier: $t" >&2; exit 2 ;;
  esac
done

# emit summary manifest
{
  echo '{'
  echo '  "sha": "'"$SHA"'",'
  echo '  "date_utc": "'"$DATE"'",'
  echo '  "tiers": {'
  first=1
  for t in "${requested[@]}"; do
    [[ $first -eq 1 ]] && first=0 || echo "    ,"
    rc=$(_rc "$t"); [[ -z "$rc" ]] && rc=99
    w=$(_wall "$t"); [[ -z "$w" ]] && w=0
    echo "    \"$t\": {\"rc\": $rc, \"wall_s\": $w}"
  done
  echo '  },'
  any_fail=0
  for t in "${requested[@]}"; do rc=$(_rc "$t"); [[ "${rc:-1}" -ne 0 ]] && any_fail=1; done
  echo '  "all_pass": '$([[ $any_fail -eq 0 ]] && echo true || echo false)
  echo '}'
} > "$OUT/SUMMARY.json"

echo
echo "===== SUMMARY ====="
cat "$OUT/SUMMARY.json"

any_fail=0
for t in "${requested[@]}"; do rc=$(_rc "$t"); [[ "${rc:-1}" -ne 0 ]] && any_fail=1; done
exit $any_fail
