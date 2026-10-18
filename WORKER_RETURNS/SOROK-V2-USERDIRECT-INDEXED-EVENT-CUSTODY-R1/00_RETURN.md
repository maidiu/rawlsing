# User-directed indexed B2 custody repair candidate

**Implemented:** remove B2's per-entry full-ledger JSON scan while retaining fail-closed detection of conflicting direct B1 writes. **Grade: `TEST_ONLY_INDEXED_EVENT_CUSTODY_CANDIDATE_PENDING_INDEPENDENT_REVIEW`.** This author return follows the user's request to fix outstanding issues after E3. It is separate from the immutable E3 review and from reviewed repair `8f7966d6d0bbb1ea2e57359de9defbcf552268bd`.

The source derivative is `bridge.py` in this directory. `run_candidate.py` reconstructs the exact reviewed B2 closure and substitutes this file into an isolated runtime. No legacy source, frozen tests, owner law, CURRENT, PREMAIN or previous return is modified. Branch: `codex/b2-indexed-event-custody`, based on E3 return `a16ba353f3bc471776d60ce198f267be4e9e5773`. The same agent now authors this derivative; E3's independent verdict applies only to its original exact SHA. A different reviewer must qualify this new candidate.

## Change and actual verification

B2 creates the derived SQLite expression index `b2_occurrence_event_id` on `occurrence(json_extract(body, '$.event_id'))`. SQLite builds it once over existing rows and maintains it for all subsequent inserts/updates/deletes, including separate B1 and raw SQL writers. B2 looks up the requested ID with `LIMIT 2`; two rows suffice to reject ambiguity. The existing writer lock, exact binding checks, original objective rows and response transaction remain intact. This adds an index to the bounded database schema; it does not edit pinned B1 source or rewrite historical bodies. The runtime must support SQLite JSON functions, as verified here with SQLite 3.40.1.

| Executed suite | Result |
|---|---:|
| B1/P1/original D1/corrected D1/F1 reference | 249 PASS |
| B2 connected and applicability | 81 PASS |
| Frozen strict E2 legacy gate | 2 PASS |
| Frozen R1 | 45 PASS |
| Frozen repair controls | 5 PASS |
| Frozen E3 independent controls, replayed by this author | 26 PASS |
| New indexed-lookup controls | 7 PASS |
| Frozen full E2 | 42 PASS /2 historical observational failures |
| Frozen X2 | 16 PASS /1 historical defect-demonstration failure |
| Raw native F1 | 17 RED, exit 1, unchanged |

No historical oracle is changed, skipped or xfailed. The exact E2/X2 failing names are checked by the runner. E2/R1/E3 include cold replay, real concurrent processes, held-writer transactions, SIGKILL recovery, permission denial, stale state, pollution and full readset binding. These reruns are author validation of the new candidate, not a second independent review.

New tests cover migration of already populated legacy ledgers without changing occurrence bytes, raw SQL insert and update through independent connections, twenty conflicting rows, repeated reopen, integrity checks, and query work at 0/100/10,000 unrelated rows. `EXPLAIN QUERY PLAN` reports indexed `SEARCH ... USING INDEX b2_occurrence_event_id`. Across five measurements at each size the lookup took exactly **16 SQLite VM instructions**. Median lookup times were approximately **19.6 /20.2 /18.1 microseconds** respectively on this host. This measures the lookup only, not overall response throughput. Source/checkpoint hashes and SQL evidence are in `evidence/fixed/`.

First index creation still scans the existing table and holds a schema/write lock; that one-time startup cost is not removed. Index maintenance adds storage/write cost. Privileged SQL can still drop indexes or corrupt/replace coherent ledger state. This remains a bounded synthetic registrar over well-formed B1 JSON records, not production event authentication or immunity to privileged database access. JSON with duplicate property names and malformed/non-B1 bodies is outside the original well-formed B1 record assumption; no general arbitrary-JSON ingestion contract is claimed.

Development disclosure: the first seven-test index run had 5 PASS /2 fixture-setup errors because the migration helper supplied an initializer to a database with an existing checkpoint. The new helper now reopens existing state with `initial=None`; no candidate code or frozen expectations were altered for that correction. Initial failed log/JUnit is retained under `evidence/development/`.

## Remaining F1 capabilities

The 17 native F1 REDs are missing developmental behavior, not failures of repaired event identity. Their requirements are specified at a high level, but pinned B1 lacks the corresponding native causal rules and state representation:

- F01/F02/F11: caregiver response grounded in its own distinct history/project, independently of the child.
- F03/F04/F21: child reception conditioned by witnessed personal history and qualified capacity, without age-to-psyche inference.
- F05/F06: factual assent, affect, public conduct and retained practical habit can diverge; a durable practice effect needs its own enacted-history predicate.
- F07/F08: attributed peer claims, counterevidence, actor uptake and objective world facts remain distinct.
- F13: later explicit repudiation may coexist with retained procedural influence and separate interpretation lineage.
- F15/F16/F17: later interaction can support differentiation, hardening, or no change, with exact evidence/rules choosing among those possibilities and preserving original history.
- F18/F19: later counterpart has independent projects, history and possible refusal; the focal actor can retain its own project despite a user request.
- F10: an admissible event may yield no immediate or durable change.

The frozen F1 validator checks legal receipt structure/provenance. It does not define the mechanism deciding these responses. Its proposed action strings and proposed state values cannot simply be copied into B1 and called developmental implementation. The user asked for clarification of this missing behavior; no new psychological rule has been invented in this patch. The existing B3 commission at `63f07960eb04cc856d94ed85f4c3c597f2f6bc9e` addresses coupled developmental research and explicitly preserves the original F1 REDs; its branch was inspected read-only, not repurposed.

Native RED IDs: F01 F02 F03 F04 F05 F06 F07 F08 F10 F11 F13 F15 F16 F17 F18 F19 F21. No production signer, source/actor grant or canonical CAN011 permission is issued.

## Reproduction and custody

```sh
python3 run_candidate.py
python3 audit_candidate.py
```

Use the preexisting authorized Git object store and Python/pytest/Node/SQLite runtime. The runner pins the original reviewed repair, R1, E2, E3 and repair-control Git objects; all imported B1/P1/D1/F1 bytes remain pinned. `source_diff.patch` is the complete derivative source change. `source_manifest.json`, `frozen_manifest.json`, `loaded_modules.json`, `commands.json`, JUnit and `verification_receipt.json` provide source identities and actual results. Portable logs remove personal paths/hostnames only. Raw native F1 JSON/exit remains primary.

The evidence packaging includes preserved pytest traceback whitespace; `git diff --check` warnings confined to those log/XML copies are not source whitespace changes. Final remote publication is verified outside its own commit preimage.
