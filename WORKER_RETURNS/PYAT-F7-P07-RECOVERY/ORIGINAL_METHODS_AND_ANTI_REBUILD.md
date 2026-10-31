# Original F7 methods, actual shortcomings, and anti-rebuild boundary

**Lane:** `PYAT-F7-P07-RECOVERY`
**Branch:** `agent/pyat-recover-f7-temporal-p07-hostile-successor-20261030-r1`
**Current PRE-MAIN pinned at runtime:** `8e44ca9c751049d65e6def47600b5c073ee04b29`
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-recover-f7-temporal-p07-hostile-successor-20261030-r1`
**Status:** sourcefree archaeology and a TEST-ONLY candidate. No production owner, no PRE-MAIN mutation, no merge, no native revival.

## 1. Exact material read

| Material | Exact cut | Result |
|---|---|---|
| Historical F7 method | blob `6f6b462b1cdef54d7989f15452473383c1661594`, present at `c86ae335eaf70e82b5764c46754b16ca7e1587ce` | 79,679 bytes; 28 function defs; 6 classes; no native import |
| Historical F7 tests | blob `8a82bd5905d266c1d500b1bf2bdcb01ea948efd6`, same cut | 127,419 bytes; 129 test functions; 163 collected/passed |
| Historical outer/nested source relations at that cut | blob `8053d30d306a3654ebf563043088311ff390bb2b` | 75,322 bytes; nested `_make_sealed_source_relation_owner` present; authenticated entrypoint present |
| Current source relations | blob `5b67e3f98a5faf95a6c82700af2346fef6e306a5` | outer resolver only; no nested owner; no authenticated entrypoint; no production importer |
| Current authority kinds | blob `ca65a7fd4d52f0c44447434559b1d09412e7aa39` | 18 kinds; `TEMPORAL_EVIDENCE` present; `TEMPORAL_COMPARABILITY` absent |
| Current F7 path | `rawlsing_next/pre553_temporal_comparability.py` | ABSENT |

The exact historical probe and current surface probe are in
`test_receipts/historical_probe.json` and
`test_receipts/current_surface_probe.json`.

## 2. What the historical F7 method actually is

The historical module is a **bounded two-anchor temporal relation producer**, not an
EE12 scientific-comparability calculator.

Its own contract, accepted at documentary grain at
`c57a96897788108db7b194e4e51691d1ca8ab729`, defines:

- exactly two authorized anchors and two bound observations;
- three authorized order bases plus one typed no-basis refusal:
  `CALENDAR_TOTAL_ORDER`, `FAMILY_LOCAL_ORDINAL`,
  `PARTIAL_ORDER_NO_DIRECTION`, `ORDER_UNKNOWN_NONCOMPARABLE`;
- twelve relation states with a total precedence and one scalar reason;
- exact-zero `NO_AUTHORIZED_CHANGE` with no deadband;
- one exact authorized comparison operation,
  `TEMPORAL_BOUND_QUANTITY_DIFFERENCE`;
- cross-universe comparison requiring both a positive `SOURCE_EQUIVALENCE`
  through the source-relation owner and a positive `TEMPORAL_COMPARABILITY`;
- no public-object registration for the receipt;
- no F8, pooling, backfill, interpolation, trajectory, rupture, causal,
  scalar-pressure or actor power.

The implementation at blob `6f6b462` realizes the bounded producer at
`compare_temporal_anchors` and `_validate_receipt_cross_field_law`. The parts that
are genuinely present and useful are:

- exact int/Decimal/Fraction numeric law and exact signed delta;
- deterministic 12-state precedence and retained lower-priority failures;
- exact-zero direction law;
- two-anchor cardinality and one-observation-per-anchor binding;
- live read of `FORBIDDEN_BACKFILL_TARGET_STATES`;
- cross-universe material derivation and two-path consumption;
- no native import and no F8 import.

The parts that are not present:

- timestamp/point/interval **geometry**; the request carries a caller
  `intervals_overlap` boolean and a caller disposition, not authorized time math;
- **as-of/version** comparison, future-publication exclusion, revocation
  exclusion, or ambiguous-as-of refusal;
- per-surface **scientific requirement authority**. The module reads a
  caller-supplied, hash-bound `comparability_requirements_material` whose
  `requirement_results` are declared mappings. It detects a listed
  `reason` string, but it does not independently authorize construct, item,
  route, population, weight or time comparability;
- any current owner for the authenticated/nested resolver path;
- any current `TEMPORAL_COMPARABILITY` authority kind;
- any current N9/N10W receiver.

This is why the historical method cannot be called accepted current
comparable-world semantics. It is a valid bounded temporal-method skeleton with
a missing scientific-comparability owner and a missing secure owner path.

## 3. Historical review and repair chain

| Cut / return | What happened | Consequence for this lane |
|---|---|---|
| HQ204 F7 forensics `ac444c5a` | EE12 is operation-scoped comparability; positive temporal relation and temporal directionality authority were never constituted; V553 scalar pressure excluded | Science framing must not revive V553 scalar pressure or infer comparability from wave proximity |
| HQ208 hostile contract review | Seven contract defects: order-basis incoherence, cross-field invariants, zero/deadband, state derivation, implementation ceiling, documentary errors, backfill direction | Contract repaired at HQ210; still documentary only |
| HQ210 contract repair `c57a9689` | 12 states, four dispositions, exact-zero, one proposed new kind `TEMPORAL_COMPARABILITY` | Accepted documentary contract of record, never adopted as a production authority instance |
| HQ211 implementation `caf6644a` | First code; 49-test sourcefree suite | 49/49 passed at exact historical cut |
| HQ213 hostile review | Fail-open fabricated refs, decorative authorities, missing exact owner path, caller-minted delta | Implementation repaired, not scientifically enriched |
| HQ214 `a9335251` | Machinery repair; no 13th state; NOT_COMPARABLE for negatives; precedence dominates isolated no-basis | Preserved |
| HQ217 `13622350` | Exact-ref binding, owner-path resolution, precedence | Preserved |
| HQ219 `6da37721` | Authority-chain findings: use scope, identity owner, owner adjudication | Preserved |
| HQ222 `a190988b` | No A/B split for equivalence snapshot; identity scope must cover the compared pair | Preserved |
| HQ225 `06b10cc0` | Subclass/outer-method forgery boundary | Preserved |
| HQ227 `f90b29ce1` | Authenticated P07 owner entrypoint; target method blob `6f6b462` introduced | Exact HQ227 suite collected 141, passed 134, failed 7; the method blob is not self-sufficient at that cut |
| HQ231/HQ235 `c86ae335e` | Lexical custody changes and final source-relations blob `8053d30d`; final test blob `8a82bd` | Exact paired final suite 163/163 passed |
| HQ234/HQ236/HQ238 | Ledger-cell-only forgery and coordinated anchor transplant; `F7-RR-04G` OPEN | Historical owner boundary is not accepted; do not port |
| HQ240 | Conditional native P07 owner + trusted Python F7 design, not adopted | Design only |
| HQ245/HQ246/HQ247/HQ248 | Native Stage A/B: constructor OOB/SIGSEGV, leaks, decide leak, positive parity failures, caller-selected trusted callback | Native path is adverse NO-GO, not a repair task in this lane |

The exact historical evidence used here is:

- `test_receipts/historical_hq211_49.log`: 49 passed at `caf6644a`.
- `test_receipts/historical_hq235_163.log`: 163 passed at `c86ae335e`.
- `test_receipts/historical_hq227_141.log`: 134 passed, 7 failed at `f90b29ce1`.
  The failures are all cross-universe positive expectations; the later HQ235
  source-relations/test pair supersedes them. This is a historical coupling
  warning: the method blob alone does not make its owner path positive.
- `test_receipts/historical_probe.json`: exact blob hashes, sizes, counts, and
  absence of timestamp/as-of selectors and native imports.

The 49/159 phrasing in some later summaries is not exact at this repository cut.
The exact counts are 49 at HQ211 and 163 at HQ235. The 7/141 intermediate HQ227
state is retained rather than hidden.

## 4. Scientific status of the historical method

### Present and scientifically meaningful

- Two authorized temporal anchors may be compared without inventing a
  trajectory.
- Exact calendar order, family-local ordinal, and partial order are kept
  distinct.
- Overlap is not replaced by a midpoint, representative date, or interpolation.
- Exact zero is not a deadband; a tiny non-zero exact delta is still a change.
- Direction is claimable only under a direction-permitting authorized basis and
  a bound exact quantity surface.
- Noncomparability is a typed limit, not absence of the underlying facts and not
  empirical zero.
- `TEMPORAL_NONCOMPARABLE` remains a forbidden source-backfill target.
- Cross-universe comparison requires a separate source-equivalence decision; it
  is not inferred from a shared label or family.
- No causal, trend, rupture, continuity, currentness or actor claim is derivable.

### Missing or not owned

- **Construct and item comparability** are not computed. They are declared.
- **Route/instrument comparability** is not computed. It is declared.
- **Population/risk-set comparability** is not computed. It is declared.
- **Weight/design comparability** is not computed. It is declared.
- **Time-grain adequacy** is not validated. The contract names
  `TIME_REFS_CURRENTLY_EXACT_AND_GRAIN_UNVALIDATED` as a residual.
- **Observation meaning** and **persistent temporal identity** are not produced.
- **As-of/version selection** is absent; the current B5 lifecycle is event-based
  currentness, not scientific temporal comparability.
- **Secure owner attestation** is absent and historically failed at both pure
  Python and native boundaries.

The historical method therefore satisfies a bounded **temporal-relation
method-law** obligation. It does not satisfy the prospective **EE12 scientific
comparability** obligation for constructs, items, routes, population frames,
weights or time. Those must remain HOLD until an original EE12/F7 issuer and an
exact data-product pair exist.

## 5. Current alternatives, status and classification

| Current artifact / branch | Status | Why it is not F7 acceptance |
|---|---|---|
| `rawlsing_next/pre553_temporal_comparability.py` | ABSENT | Historical path only; no current module |
| `rawlsing_next/pre553_source_relations.py` blob `5b67e3f` | TEST_ONLY; 24 tests pass; no production importer | Outer P07 resolver only; no nested owner, no authenticated entrypoint, no current F7 consumer |
| `rawlsing_next/pre553_empirical_authority.py` blob `ca65a7f` | IMPLEMENTED current provider | 18 kinds; `TEMPORAL_EVIDENCE` exists; `TEMPORAL_COMPARABILITY` does not |
| `rawlsing_next/m1_temporal_v554_admission_dedup.py` | IMPLEMENTED production temporal-signature gate | Checks V553/V554 fingerprints and missing temporal/comparability authority; does not compare timestamps or produce an F7 relation |
| `rawlsing_next/pre553_learned_product_lifecycle.py` | IMPLEMENTED lifecycle, current/as-of owner | Event/checkpoint currentness; not scientific wave comparability; no F7 receiver |
| `rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py` | TEST-ONLY lifecycle court | Proves selected current/as-of lifecycle, not empirical temporal comparison |
| `rawlsing_next/pre553_n9_n10w_progressive_candidate.py` | TEST-ONLY synthetic N9/N10W candidate | Progressive F8 conditioning; opaque pairing authority; no temporal/as-of first consumer |
| `rawlsing_next/field_forge_conditional_support.py` | IMPLEMENTED Field Forge conditional support | Not a temporal comparator; no F7 receiver |
| `rawlsing_next/source_backed_positioned_subject_possibility.py`, `pre553_analytical_composition.py`, `pre553_empirical_possibility_provider.py` | IMPLEMENTED opaque `comparability_authority_ref` seam | Type/equality-checked only; no temporal meaning; sole current caller is the TEST-ONLY N9 candidate |
| R3-S04 `rawlsing_next/s04_temporal_policy.py` on `agent/rabochii-pyat-r3-s04-f7-temporal-sociology-r1 @ 9ae87f22` | ABSENT from current baseline; adverse alternative | Linear interpolation / nearest-anchor backoff / fixed `0.05` drift / binary float; contradicts the accepted contract's no-interpolation, no-nearest, no-deadband law. Do not revive |
| HQ250 S03, HQ254 E01, HQ257 E02 EVS A048 documentary lanes | DOCUMENTARY ONLY / NOT ADOPTED | One construct crosswalk at best; no exact two measured products, no pair authority, no N9 consumer; retained SRC/version and country design gaps |
| R40/R41/R52/F43 commissions | COMMISSION ONLY / no current return or code in this baseline | Dependent on original source/EE12 authority; must not be inferred as implemented |
| Historical native P07 Stage A/B | UNSAFE / ADVERSE NO-GO | Alias TCB, untrusted receipt, writable ledger, constructor OOB, `PyObject_Call`/`PyErr_Fetch` crash, decide leak; no revival |
| Issue #565 | OTHER LANE | Narrow map correction by a different worker; not edited or duplicated here |

External S7-FIX evidence is also reconciled but not rerun: S7-FIX `80bc5d9bf6624c2ea04027322947a41c347330aa`
and independent I3 `1b89fd49c330e4a2c976e6af8d6c1a5e6dbfb088` establish five historical
outer/nested boundary splits plus one emit join, 1,885 corrected families,
3,135 exact-once function IDs and 2,595 preserved negative records. The I3
review records `CURRENT_OWNER_MAP RED`, zero of five current outer AST matches,
and historical emit different from current PR526. This lane uses that only as
identity/custody evidence; it does not edit the S7-FIX map or duplicate issue
#565.

## 6. Exact recoverable pure scope chosen by this lane

The candidate recovers only the genuinely missing pure method surface:

1. **Exact temporal geometry** for authorized `POINT` and `CLOSED_INTERVAL`
   extents, with exact rational arithmetic and no midpoint/interpolation.
2. **As-of/version eligibility** using authorized publication, validity and
   revocation points; future publication and revoked versions are excluded;
   multiple eligible versions are refused rather than resolved by latest/default.
3. **Explicit comparability-attestation gating** for construct, response,
   route, population, estimand, measure, weight and time surfaces, using present
   current authority kinds. Numeric equality, same labels, same wave index and
   as-of timestamps do not satisfy a surface.
4. **Noncomparability refusal** with retained failures, no delta, no direction,
   and no cross-population inference.
5. **Cross-universe source equivalence consumption** through the present current
   outer `SourceRelationResolver`, not a historical nested owner or native P07.

The candidate deliberately refuses `TEMPORAL_COMPARABILITY` because that kind is
not current. It does not mint a replacement authority. It is TEST-ONLY and has
no current production receiver.

## 7. Anti-rebuild prohibitions

Do not:

- port or reconstruct the historical nested
  `_make_sealed_source_relation_owner.SourceRelationResolver`;
- implement or revive the quarantined native P07 C extension;
- add `TEMPORAL_COMPARABILITY` to current authority kinds without an original
  EE12/F7 issuer and a separate adoption;
- turn caller-declared requirement results into accepted scientific
  comparability;
- infer comparability from equal numeric values, shared labels, wave index,
  as-of timestamp, latest/default selection, or cross-wave plug compatibility;
- pool or compare populations without an exact population/equivalence authority;
- claim a measured F7 result for EVS A048 or any other pair without exact
  source-authorized products, pair authority and a named receiver;
- treat the historical 163/163 court as security acceptance;
- merge this candidate into PRE-MAIN in this lane.

## 8. Correct future owners

| Missing edge | Correct owner |
|---|---|
| Scientific construct/item/route/population/weight/time comparability | Original EE12/F7 comparability issuer (not this worker) |
| `TEMPORAL_COMPARABILITY` authority kind and ceiling | Separate authority-registry adoption after original issuance |
| Current nested/authenticated source-relation owner | Separate owner decision; only if a future production cross-universe consumer actually requires it |
| Historical/as-of N9 first consumer | N9/N10W service owner with exact purpose admission; none exists now |
| P07 native owner | Separate qualified native issuer/implementer plus independent hostile review; only if a protected future consumer requires it |
| Measured EVS or other wave pair | Source custodian + source-use warrant + product producers + EE12 pair authority + independent methods review |

**Anti-rebuild terminal:** `HISTORICAL_METHOD_IDENTITY_PRESERVED__CURRENT_OWNER_ABSENT__NO_NESTED_OWNER_PORT__NO_NATIVE_REVIVAL__SCIENCE_AUTHORITY_HOLD`.
