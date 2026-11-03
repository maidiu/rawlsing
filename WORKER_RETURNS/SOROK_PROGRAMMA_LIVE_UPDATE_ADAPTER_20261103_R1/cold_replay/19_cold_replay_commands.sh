#!/bin/sh
# Reproduce the LIVE-02 cold replay and seven-view readback.
# Run from SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/LIVING_REFERENCE_CANDIDATE_R1.
# The state root must remain outside protected repository paths.
set -eu

D="${1:-/tmp/sorok-live02-cold-replay}"
PKG="$(pwd)"
export D PKG
export PYTHONDONTWRITEBYTECODE=1

rm -rf "$D"
mkdir -p "$D/evidence"

python3 -c 'import living_reference as lr; from pathlib import Path; r=lr.commit_event(lr._event("GENESIS", {"baseline_sha": lr.ENGINEERING_BASELINE}, created_at="2026-11-03T12:00:00+00:00"), journal_path=Path("'"$D"'/evidence/journal.jsonl"), state_path=Path("'"$D"'/state.json")); import json; print(json.dumps({"status": r["status"], "head": r["head"], "event_id": r["event"]["event_id"], "sequence": r["event"]["sequence"], "revision": r["revision"]}, indent=2))' > "$D/01_genesis.json"

python3 live_update_adapter.py --state "$D/state.json" freshness > "$D/02_freshness_pre.json"

H=$(python3 -c 'import json,sys; print(json.load(open(sys.argv[1]))["head"])' "$D/01_genesis.json")
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/join_e_scoped_review.json --expected-head "$H" > "$D/03_intake_join_e.json"
H=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["status"]=="EVENT_APPENDED", d; print(d["head"])' "$D/03_intake_join_e.json")
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/s35_authored_sourcefree.json --expected-head "$H" > "$D/04_intake_s35.json"
H=$(python3 -c 'import json,sys; d=json.load(open(sys.argv[1])); assert d["status"]=="EVENT_APPENDED", d; print(d["head"])' "$D/04_intake_s35.json")
python3 live_update_adapter.py --state "$D/state.json" intake fixtures/rrif_r2_negative.json --expected-head "$H" > "$D/05_intake_rrif.json"

python3 -c 'import evidence_store as es, json, sys; from pathlib import Path; p=Path(sys.argv[1]); events=es.read_journal(p); print(json.dumps({"count":len(events),"head":es.journal_head(p),"events":[{"sequence":e["sequence"],"kind":e["kind"],"event_id":e["event_id"],"prev_event_hash":e["prev_event_hash"],"transition_id":(e.get("payload") or {}).get("transition_id")} for e in events]}, indent=2))' "$D/evidence/journal.jsonl" > "$D/06_journal_chain.json"

python3 -c 'import living_reference as lr, json, sys; from pathlib import Path; s=lr._load_state(Path(sys.argv[1])); print(json.dumps({"warm_state_digest":s["state_digest"],"journal_head":s["journal_head"],"revision":s["revision"],"journal_applied":[x.get("status") for x in s.get("journal_applied",[])],"programma_deltas":len(s.get("programma_deltas",[]))},indent=2))' "$D/state.json" > "$D/07_warm_state.json"

cp "$D/state.json" "$D/state.warm.json"
rm -f "$D/state.json" "$D/SNAPSHOT.json"

python3 live_update_adapter.py --state "$D/state.json" freshness > "$D/08_freshness_cold.json"
python3 -c 'import living_reference as lr, json, sys; from pathlib import Path; s=lr._load_state(Path(sys.argv[1])); print(json.dumps({"cold_state_digest":s["state_digest"],"journal_head":s["journal_head"],"revision":s["revision"],"programma_deltas":len(s.get("programma_deltas",[]))},indent=2))' "$D/state.json" > "$D/09_cold_state.json"

python3 live_update_adapter.py --state "$D/state.json" whole > "$D/view_1_whole.json"
python3 live_update_adapter.py --state "$D/state.json" focus C12@INTEGRATE > "$D/view_2_focus_c12.json"
python3 live_update_adapter.py --state "$D/state.json" source-to-product E021@VERIFY > "$D/view_3_source_to_product_e021.json"
python3 live_update_adapter.py --state "$D/state.json" goal C9@INTEGRATE > "$D/view_4_goal_c9.json"
python3 live_update_adapter.py --state "$D/state.json" work-now > "$D/view_5_work_now.json"
python3 live_update_adapter.py --state "$D/state.json" changes-since a9ebf71e62d84e5dcc599662e976eca7fcd0e623 > "$D/view_6_changes_since.json"
python3 live_update_adapter.py --state "$D/state.json" freshness > "$D/view_7_freshness.json"
python3 live_update_adapter.py --state "$D/state.json" candidate-patch > "$D/view_8_candidate_patch.json"

python3 -c 'import living_reference as lr, json, sys; from pathlib import Path; s=lr._load_state(Path(sys.argv[1])); print(json.dumps({"post_views_state_digest":s["state_digest"],"journal_head":s["journal_head"],"revision":s["revision"]},indent=2))' "$D/state.json" > "$D/10_post_views_state.json"

echo "cold replay artifacts written to $D"
