# WSC001E — PRE-V3 → V3 COMPARATOR / PSEPF / METABOLISM CONTRACT R1

Status:

`PASS__WSC001E_PREV3_V3_METABOLISM_CONTRACT_CONSTITUTED__READY_FOR_CENTRAL_FANIN`

## Grounding

Working ancestry is exactly:

`d15f8973ddeff46dbaa15f352fe5d7e59e1fe1a3`

Instruction/evidence ref consumed without becoming working ancestry:

`e1b9ae0bbfeea000efee65a22622196cce40aa3e`

No sibling WSC001 worker branch was consumed. Library was not used.

Required WSC000 central fan-in inputs were consumed from the immutable evidence ref. Current PRE-MAIN executable/authority surfaces were preferred over historical reconstruction.

## Holding

The PRE-V3 → V3 seam is a semantic firewall, not a probability-to-person inference step.

The minimum lawful contract is:

1. V3 owns generated-subject identity and generated-subject facts. Upstream empirical services may use exact V3-owned facts as query/comparator criteria; they do not create, revise or reinterpret those actor facts.
2. PRE-V3 owns empirical/structural possibility products and their replay/provenance. A positioned-subject possibility field is still learned-world evidence, not actor belief, identity, personality, opportunity, action or realization.
3. A positive actor-facing transition requires an exact actor/generated-subject comparator with exact predicate ancestry. Lexical similarity, nearest-neighbor matching, fuzzy cohort substitution and ungoverned cross-source bridges are forbidden.
4. Exact PSEPF support alone cannot mutate V3. The seam may only delegate to a separately accepted V3 transition owner whose authority identity, acceptance binding, transition surface, operation class and allowed source lineage match exactly.
5. The seam itself is pure: even successful delegation has zero actor-state, causal-ledger, RNG and scheduler effect. The V3 owner, not this seam, owns any later causal mutation.
6. Exact proxy/walkback evidence is never sufficient for positive actor transition. `EXACT_UNRESOLVED_PROXY_AVAILABLE` remains unresolved at actor-transition grain.
7. `VALID_EMPTY`, `NONCOMPARABLE`, unresolved, blocked, integrity-failure and typed zero states remain typed and zero-effect; none may be laundered into default probability or actor state.
8. Optional structural context remains structural-peer/context eligibility only. It is not V3 mutation permission.

## Current authority ceiling

Current PRE-MAIN does **not** close the two primary parent gates:

- `OBL031` — exact predicate ancestry / actor comparator;
- `OBL032` — production PSEPF transition / metabolism.

`OBL032` depends on `OBL031` and on measurement portability (`OBL012`) where the concrete comparator/transition crosses a measurement boundary.

The current `v3_psepf_zero_positive_guard.py` production registry is empty. Therefore the currently executable positive-transition posture is intentionally:

`ZERO_POSITIVE_AUTHORITY__NO_ACTOR_STATE_EFFECT`

This is not a failure of the architecture. It is the lawful present state until a competent authority accepts a concrete V3 transition owner and binding.

## Minimal seam state family

The seam contract in `01_SEAM_CONTRACT.md` defines these semantic outcomes:

- `POSITIVE_DELEGATE_TO_ACCEPTED_V3_OWNER`
- `ZERO_EMPIRICAL_OR_COMPARATOR_EFFECT`
- `VALID_EMPTY_ZERO_EFFECT`
- `NONCOMPARABLE_ZERO_EFFECT`
- `UNRESOLVED_OR_PROXY_ZERO_EFFECT`
- `BLOCKED_COMPARATOR_ANCESTRY_ZERO_EFFECT`
- `BLOCKED_MEASUREMENT_OR_TRANSPORT_ZERO_EFFECT`
- `BLOCKED_POSITIVE_TRANSITION_AUTHORITY_ZERO_EFFECT`
- `INTEGRITY_FAILURE_ZERO_EFFECT`

Only the first state permits a call to a separately accepted V3 owner. It still causes no mutation inside this seam.

## Minimum GT0-compatible path

A current-lawful Golden Thread 0 can traverse this seam without inventing a positive actor transition:

1. receive one exact PRE-V3 positioned-subject possibility result bound to exact source universe, release, target, generated-subject query criteria, conditioner/comparator authorities and replay determinants;
2. require exact comparator/predicate-ancestry evidence for the generated subject;
3. if that evidence is absent, return `BLOCKED_COMPARATOR_ANCESTRY_ZERO_EFFECT`;
4. if comparator evidence exists but no separately accepted positive V3 transition authority exists, return `BLOCKED_POSITIVE_TRANSITION_AUTHORITY_ZERO_EFFECT`;
5. preserve the exact PRE-V3 evidence and blocker in replay/provenance while leaving V3 state byte-for-byte/identity-for-identity unchanged.

A later competent authority may enable the positive branch without changing the firewall: exact supported evidence + exact comparator + all required measurement/transport authority + exact accepted V3 transition-owner binding → `POSITIVE_DELEGATE_TO_ACCEPTED_V3_OWNER`.

## Reuse decision

Directly reuse/adapt rather than rewrite:

- `rawlsing_next/source_backed_positioned_subject_possibility.py`
- `rawlsing_next/v3_psepf_zero_positive_guard.py`
- `rawlsing_next/pre553_empirical_objects.py`
- `rawlsing_next/pre553_structural_admission.py`
- `rawlsing_next/m5_runtime_rsc_peer_prior.py`
- their exact tests, especially Z08/PSEPF zero-positive coverage.

The existing code already establishes the essential negative law. WSC001E adds the missing seam constitution and exact future delegation requirements; it does not manufacture the absent positive authority.

## Outputs

- `00_RETURN.md` — this disposition.
- `01_SEAM_CONTRACT.md` — minimum semantic/interface contract.
- `02_EXISTING_ASSET_REUSE.tsv` — exact current implementation/test reuse map.
- `03_OPEN_GATES.tsv` — unresolved authority/implementation gates and fail-closed behavior.

Terminal:

`PASS__WSC001E_PREV3_V3_METABOLISM_CONTRACT_CONSTITUTED__READY_FOR_CENTRAL_FANIN`
