# P5 REJECT Semantic Parity Report

## Final disposition

`697_OF_697_REJECT_SEMANTIC_PARITY_PASS`

This is an evidence-only P5 court return. It does not retire a carrier, promote R3, install a live normalized REJECT carrier, choose a database, execute P8, consume P6/P7 findings, mutate I05/V553+, mutate main/live Trii, close G1A, or transfer semantic ownership.

## 1. Re-ground / drift

- Coordination branch: `agent/vozhd-to-vozhdy-inheritance-integration-r1`
- Coordination HEAD: `c0fef0b0d2074d4227ed6bd1bb281763d89a0a27`
- Canonical `main`: `0777a34e50221bde6801dbaca26c058a7350c9e8`
- Live Trii control: `agent/vozhd-trii-pre553-substrate-reconstruction-control @ 04a0109aa170c6041b199e5c6130a39a8e0f6029`
- Drift classification: `NO_LIVE_RAWLSING_GOVERNING_STATE_DRIFT`. Coordination advancement is the P5 continuation-handoff layer only.

## 2. PASS A — exact historical source-carrier recovery

Installed recovered-inheritance index:
- path: `data/ddm_build_copy/recovery_reservoir/semantic_relation_R1_through_Job3/R1_20260825/OBJECT_INDEX.tsv`
- Git blob: `2982f27c918c86e7315c436a652a94ce16c77c35`
- size: `2426127` bytes

The exact raw archaeology required by P5 was recovered from the certified Library bookend:
- Library path: `/Rawlsing/DDM_HANDOFFS/Rawlsing_DDM_S14_R1_THROUGH_JOB3_ER1_BOOKENDS_20260825/Rawlsing_DDM_Job3_R3_Complete_Recovery_ER1_20260825.zip`
- materialized SHA-256: `0e71234926438d89ba89c1b196eec372951c0781ffafd67dba86f0e2d57485ac`
- the Library `.sha256` sidecar states the same digest.

Exact frozen central carrier identities:
- Job3 frozen denominator: `2cb1d40f91c560cb480d881d8ec27b5db1f410ac0dcd52108c18343cb9c63b97`
- Job3 adjudication contract: `b192458901aa6ad259ff5a8337141b4042af107a8faf57f48db9dc5860b1ab9b`
- terminal ledger: `78b48d4a699053dc59b52401139a09c84aacc864db7d81d0f357a1555a1a5ec8`
- REJECT ledger: `6534de1a17055078e11e3d0c8dff46c5bb082743ce60056aeaa8b92b669001fc`
- BLOCKED ledger: `7fd3e4610c6558a5376f722853281d1b32a07c59b046cbef66abac93189d7485`
- successor obligations: `8a3083f213ac5daac123288d02a381e9e92e7e98663b3dc4dc61f155cfaaa205`
- current O10/S14 grammar: `63db4ecc7e73a2d3fbb9df5fbdbdc747c86a047e6d4e290274deaddcef7f67bc`
- central final state: `0260fe104d1387dcaff06d54f54227775dcf09f97db275628d7465fd8bc1263a`

Original worker-return ZIP pin validation:
- `W01`: `5d9ba3549cb4584a1f532c08f4b1070f5e341f1185378792c623814179694264` — `PASS` (candidate return count 390)
- `W02`: `55238ed63551a4f39f0ca3345e1ff04329292a8b3ab62e7a4fd808eda02a08b9` — `PASS` (candidate return count 272)
- `W03`: `c5e32cea3ad150d2afd3db4fc96e96095b62d62fc18074812aafc4acf053484d` — `PASS` (candidate return count 235)
- `W04`: `77c793fe546e30f98206cb0bcb8509762d074307d87bdbabb52b611215730262` — `PASS` (candidate return count 136)
- `W05`: `17f337d5ca0593d700fdee0128a5c2577ed9bb361f8292693f18c9824cb75a82` — `PASS` (candidate return count 102)
- `W06`: `eb152bb90324e9b32ba005698a8bc8338acbc19553547f05856b5be8939ae696` — `PASS` (candidate return count 129)

Failed retrieval routes before the successful bounded materialization:
1. GitHub code/content search over reservoir payload names returned no indexed carrier rows; this was treated as search-index incompleteness, not absence.
2. Guessing `objects/65/<REJECT-content-sha>.csv` from content SHA returned 404. The reservoir index is shard-relative; content SHA is not a universal path convention.
3. Exact GitHub fetch of the installed 5.8 MB terminal carrier resolved its path/Git blob but returned no body, including a bounded line-range request; connector body-size ceiling.
4. Exact raw-GitHub URL fetch was refused as too large/unsupported.
5. Direct Git transport from the container could not resolve/reach GitHub because external network/DNS egress is disabled.
6. Public web raw/blob fallback did not yield the repository bytes.
7. Lawful recovery then followed the R3 install statement to the certified Library raw-recovery bundle and succeeded.

Independent frozen partition proof:
- `TOTAL_UNIQUE_CANDIDATES = 1264`
- `ACCEPT = 552`
- `REJECT = 697`
- `BLOCKED = 15`
- `ACCEPT ∩ REJECT = ∅`
- `ACCEPT ∩ BLOCKED = ∅`
- `REJECT ∩ BLOCKED = ∅`
- exact 697-row REJECT ledger candidate-ID set = exact terminal-ledger REJECT subset.
- exact ID enumeration: `P5_REJECT_IDS.txt`

REJECT census by worker: `{"W01": 349, "W02": 189, "W03": 87, "W04": 46, "W05": 8, "W06": 18}`
REJECT census by rule: `{"S14-T01": 142, "S14-T02": 7, "S14-T05": 59, "S14-T06": 4, "S14-T11": 476, "S14-T12": 6, "S14-T15": 3}`
REJECT census by source family: `{"Afrobarometer": 5, "Arab Barometer": 8, "Asian Barometer": 349, "EVS": 189, "GSS": 87, "Latinobarómetro": 2, "LiTS": 46, "WVS": 11}`

## 3. PASS B — 697/697 companion closure

All six original worker returns were cold-extracted. Their exact adjudication-return rows concatenate to 1,264 unique candidates and match the central terminal ledger on all 16 worker-owned adjudication fields.

The terminal ledger candidate-anatomy columns match the frozen denominator exactly for all 1,264 candidates. No candidate identity, membership, typed payload, provenance, or worker verdict was changed by central integration.

For every one of the 697 REJECT candidates:
- exact candidate identity/type/member anatomy is recoverable from the frozen denominator;
- exact typed role/topology anatomy is recoverable from the rule-specific `identity_payload`, with exact member order/multiplicity retained for replay;
- exact member-level source context exists in the SHA-pinned original worker-return carrier;
- exact decisive `semantic_rationale` is present;
- exact `evidence_refs_json` is present and valid JSON;
- no REJECT carries a BLOCKED `blocker_code`/`blocker_detail`;
- no REJECT carries an accepted relation type/label;
- candidate-scope defect flags = `125`;
- successor obligations = `125`, one per flagged candidate;
- the obligation candidate set equals the defect-flag candidate set exactly;
- the remaining 572 REJECTs have no append-only Job3 successor obligation recorded.

No `PARITY_BLOCKER(...)` remains.

### Historical empty-field closure

46 W04 REJECT rows contain historical empty-string cells for `semantic_confidence`, candidate-unique `evidence_ceiling`, and candidate-unique `prohibited_inference`. They are **not missing fields**: the schema fields are present with empty-string values. P5 preserves those values as `EMPTY_STRING` and does not manufacture row-specific language. Their governing exact-candidate scope remains in the Job3 contract, and rule-level prohibited-inference law remains in the frozen grammar. This satisfies the P5 requirement to preserve unique ceiling/inference material **where unique to the adjudication** without inventing content that never existed.

572 non-defect REJECT rows likewise retain an explicitly present empty defect-note cell rather than coercing it into null/missing/not-applicable.

## 4. PASS C — carrier-neutral logical REJECT contract

The proved logical contract is represented record-by-record in `P5_NORMALIZED_REJECT_PARITY.jsonl`. It preserves, directly or by exact governed reference:

1. `candidate_proposition_identity` — a P1-style relation-proposition structure, never a path/SHA/row ID;
2. `candidate_type_rule`;
3. `exact_members_topology_roles_material_order`;
4. non-truth-bearing `terminal_disposition = EXACT_CANDIDATE_REJECT`;
5. exact governing Job3 contract, central freeze, and SHA-pinned worker authority;
6. exact-candidate adjudication scope and subset/retyping prohibitions;
7. exact decisive reject rationale;
8. lossless reason class plus exact rationale;
9. candidate-unique evidence ceiling cell plus governing contract ceiling;
10. candidate-unique prohibited-inference cell plus rule/global firewall;
11. exact generator/scope-defect flag and note;
12. exact successor-obligation refs, if any;
13. future-candidate possibility scope without converting possibility to truth;
14. immutable historical/lifecycle/provenance refs;
15. explicit no-current-selection implication under accepted P2 law;
16. exact source/evidence/carrier refs and hashes;
17. replay-only fields needed not to erase routing/measurement/endpoint/anti-join/provenance distinctions.

`candidate_id` is retained only as a historical locator; it is not used as semantic proposition identity.

The contract preserves historical empty string, nested JSON null, empty list/object, literal unresolved/not-applicable tokens, and absent JSON keys without coercion.

## 5. Smallest governed REJECT reason taxonomy

All 697 are rooted in the Job3 contract's required REJECT meaning:

`FAILED_NAMED_O10_RELATION_PREREQUISITE`

The smallest non-lossy first split is:
- `NO_CANDIDATE_SCOPE_DEFECT_FLAG = 572`
- `CANDIDATE_SCOPE_OR_GENERATOR_DEFECT_FLAGGED = 125`

For the 572 non-defect rows, rule family + exact decisive rationale remains the lossless leaf meaning. Counts by rule: `{"S14-T01": 72, "S14-T05": 17, "S14-T06": 4, "S14-T11": 476, "S14-T15": 3}`.

For the 125 flagged rows, the exact central append-only successor obligation supplies the governed construction-defect subclass:
- `COMMON_PREDICATE_OR_SCOPE_OVERGENERALIZATION` = 42
- `CONDITION_AXIS_OR_RESPONSE_TOPOLOGY_DEFECT` = 7
- `IMPLEMENTATION_VARIANT_MISTAKEN_FOR_TARGET` = 13
- `RELATION_ROLE_TYPING_DEFECT` = 42
- `ROUTED_SCOPE_GENERATION_DEFECT` = 6
- `TARGET_CONDITION_AXIS_CONFUSION` = 15

This taxonomy does **not** replace the exact decisive rationale. It is only an index over it. Evidence insufficiency is not silently reclassified as REJECT: Job3's BLOCKED state owns insufficient/constitutionally constrained evidence, while all 697 P5 rows have empty blocker fields.

## 6. PASS D — exhaustive semantic round trip

For each exact historical REJECT:

`HISTORICAL_GOVERNED_REJECT_AUTHORITY → NORMALIZED_REJECT_RECORD → RECONSTRUCTED_SEMANTIC_ADJUDICATION`

First exhaustive run:
- `PASS = 697`
- `FAIL = 0`
- `BLOCKED = 0`

Each row was checked across candidate proposition identity, candidate type/rule, exact member/topology anatomy, terminal state/truth-bearing status, governing authority instance, exact adjudication scope, decisive reason, reason class, confidence state, evidence ceiling state, prohibited-inference state, generator defect, successor obligation, future-candidate possibility, lifecycle/provenance, current-selection nonclaim, evidence refs, and replay-only constitutive/boundary fields.

No count equality or hash equality was used as the semantic proof; they are only source-integrity prerequisites.

## 7. PASS E — independent hostile closure

A second parser (`csv.DictReader`) freshly reopened all frozen carriers and rebuilt the semantic projection independently of the first pandas-based normalization.

Independent rerun:
- `PASS = 697`
- `FAIL = 0`
- `BLOCKED = 0`

Every hostile invariant in `P5_HOSTILE_CLOSURE.md` is green, including:
- exact 697 unique REJECT IDs;
- zero duplicates/state leakage;
- complete frozen-denominator, worker-return, source-context, and successor joins;
- exact decisive reasons survive;
- exact candidate anatomy survives;
- all 125 material generator defects and obligations survive;
- obligation remains obligation, never successor truth;
- REJECT remains neither exact negative nor nonedge nor generic false;
- future differently typed/corrected candidates remain lawful where the historical/P5 law permits;
- no currentness from chronology;
- empty/null/missing/unresolved/not-applicable distinctions are not silently collapsed.

## 8. Exact-negative firewall

`REJECT → PROVEN_NEGATIVE` is impossible in the logical contract because:
- the juridical state is explicitly `EXACT_CANDIDATE_REJECT`;
- `truth_bearing = false`;
- the record explicitly forbids `PROVEN_NEGATIVE`, `NONEDGE`, `GENERIC_FALSE`, and universal relation absence implications;
- any separately governed exact negative remains outside this adjudication state and must be referenced under its own authority/claim identity.

Likewise:

`NO_CURRENT_POSITIVE → SEMANTIC_ABSENCE`

is not licensed.

## 9. Successor / lifecycle holding

Every historical REJECT remains immutable.

For all 125 flagged candidates:
- central disposition = `APPEND_ONLY_O12_SUCCESSOR_OBLIGATION__DO_NOT_MUTATE_R3`;
- current R3 effect = `SUPPLIED_CANDIDATE_REMAINS_TERMINAL_REJECT`;
- future scope explicitly permits inspecting generation and testing a missing correctly typed candidate **without reopening this Job3 verdict**;
- `blocks_job3_r3_freeze = false`.

For all 697, no `CURRENT_SELECT` is invented. Accepted P2 law requires currentness to be explicit and forbids timestamp/commit/filesystem/version fallbacks.

## 10. Central holding / downstream boundary

`697_OF_697_REJECT_SEMANTIC_PARITY_PASS`

P5 proves that the frozen REJECT semantic/adjudicative capital **can** be represented losslessly in a compact carrier-neutral adjudication-memory contract. That removes REJECT semantic parity as an eventual carrier-retirement blocker **in principle**, but authorizes no retirement here; broader gates still govern retirement/promotion.

The REJECT-side factual dependency needed by a later P8 policy/factoring court is now clear, but **P8 was not executed**.

No P6/P7 findings or drafts were read or produced.

## 11. Exact remaining P5 blocks

`NONE`

## 12. Evidence files

- `P5_REJECT_IDS.txt` — exact 697 candidate IDs.
- `P5_REJECT_SOURCE_INVENTORY.jsonl` — 697-row source/carrier/companion inventory.
- `P5_NORMALIZED_REJECT_PARITY.jsonl` — 697 logical normalized records + parity disposition.
- `P5_REJECT_PARITY_FAILURES.jsonl` — empty; zero failures.
- `P5_HOSTILE_CLOSURE.md` — independent hostile invariants and rerun.
- this report.

`P5_REJECT_PARITY_COURT_COMPLETE__RETURN_TO_HQ__NO_RETIREMENT_NO_LIVE_PROMOTION`
