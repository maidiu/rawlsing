# Selective fan-in candidates and repair/retire contracts

**Status:** proposals and contracts only. No merge, no adoption, no self-review, no PRE-MAIN mutation. Each candidate requires an independent reviewer distinct from the author and this reconciler. Exact blob identity is not behavioral equivalence.

No speculative patch was made. The cases below do not meet the bar for a limited authorized sourcefree fix in this return.

## S-01 — F6: replace A with F6M, not a revival of S03FO

- **Candidate:** exact F6M blob `2df811d76db258d98d89ffb43c830cb221ff9a7d`, with the F6P sourcefree consumer chain at `7d7ed1cb0` / `016870e86`.
- **Reject:** S03FO A blob `fc5e37fa...`. A renormalizes support-gate-excluded source strata onto survivors and reports full coverage; it also lacks `PARTIAL_IDENTIFICATION_ONLY`. S03R found three genuine failures and R35 reproduced the support-gate defect twice.
- **Current receiver:** none. F6 is absent from PRE-MAIN. The RRIF-C test import is not an F6 consumer.
- **Required positive tests:** admitted two-source synthetic pair; complete target support; same marginals with opposite within-source joints; target standardization recovers the declared synthetic truth; F6P consumer reads the actual F6M output.
- **Required fault/severance tests:** support-gate exclusion must produce unknown mass and refusal, not renormalization; missing native joint cell must not become zero; outcome-as-predicate must be flagged or refused in predictive routing; incomplete target support must produce a subprobability and no point distribution; source-pair non-equivalence must refuse.
- **Independent reviewer:** F6 method/source reviewer distinct from the S03 and F6M authors and from this reconciler.
- **Gate:** real admitted source pair, real target, named consumer and source/design/transport authority. No real F6 claim without them. Do not merge A.

## S-02 — P07 native stage B: keep held; no cutover

- **Candidate:** none authorized. Native stage B blobs are `2d8ffc68`, `586f859a`, `fb5ed13a`, `253fbafe` across the repair chain, but none is current.
- **Open blockers:** `HQ246-OPEN-001` decide leak; `HQ248-OPEN-001` admission leak; two-candidate conflict/tie unexercised; module-init OOM not performed; TCB callables assumed; `F7-RR-04G` open.
- **Current receiver:** none. Native files are absent; the Python P07 owner is the only current implementation.
- **Required evidence before cutover:** zero-leak admission and decide measurements with spread; exact native blob identity; two-candidate `CONFLICTING_AUTHORITY` and precedence tie tests; OOM or an explicit written waiver; authenticated TCB/issuer boundary; independent native security review.
- **Gate:** native execution/TCB/refcount authority remains HELD. No merge.

## S-03 — F7 source relations: architecture decision, not a Python patch

- **Candidate:** none. HQ235 blob `8053d30d` closes single-primitive attacks but witness 7 still mints custody under coordinated multi-anchor substitution. Current blob `5b67e3f9` is the base owner and lacks the hardening.
- **Current receiver:** UNKNOWN. `fiabc_succession_producer.py:59` is a string path map only; tests are the only execution.
- **Options for HQ:**
  1. Move custody behind a native opaque capability handle with no Python-visible accessor.
  2. Isolate the owner behind a narrow IPC/process boundary.
  3. Explicitly accept the coordinated-substitution residual risk and restate the F7 claim as "adversarial-single-primitive", not "non-forgeable".
- **Required negatives:** exact HQ234/HQ235 coordinated substitution; caller-constructed state; visible `_by_ref`/`_by_key` replacement; recovered sealer transplant; productive positive paths preserved; victim refused before and after mutation.
- **Gate:** no non-forgeability claim until one option is adopted. Consume #571/#577 when returned; do not duplicate their reviews.

## S-04 — F7 temporal comparability: retain non-comparability; retire S04 unless re-qualified

- **Candidate:** none for current integration. The historical exact module is absent; S04 `ba0fc389` is absent and scientifically unqualified.
- **Reject as current authority:** S04 nearest-anchor backoff with `gap_years * 0.05` drift, polarity/3x-jump break heuristic and `MEASURED`/`INFERRED` labels. This is not a population/cohort/weight-comparable trend and has no real-source validation.
- **Current receiver:** UNKNOWN. `TEMPORAL_EVIDENCE` is an exact source-native time binding, not a comparability owner.
- **Required positives:** exact temporal anchors with issued `TEMPORAL_EVIDENCE`; missingness and non-comparability preserved; explicit refusal of trend/interpolation/cohort claims without owner authority.
- **Required fault/severance tests:** wrong use scope; missing `target_use_refs`; caller-authored identity; forged resolver; custody substitution; non-comparable populations; missing cohorts; weight/design mismatch; time-label-only alias.
- **Options:** revive exact comparability only with an authenticated owner/custody boundary and a real consumer; otherwise retire S04 and keep the current exact time binding.
- **Gate:** no integration of S04. Consume #571 when returned.

## S-05 — F8: retain exact current blob; no widening

- **Candidate:** none. Current binder blob `848d2d0e` is byte-identical to the independently reviewed HQ254/HQ258 candidate and the HQ259 adoption.
- **Current receiver:** EE14 ingress static import/call. EE14 has no production caller and remains under `KEEP_EE14_T1_HOLD`; actual service consumer UNKNOWN.
- **Keep:** exact blob, refusal-only guard at line 723, order-insensitive set semantics as reviewed, no permission/ranking/selection/pooling/model-use grant.
- **Open items:** R01 OBS_01 duplicate insensitivity; HQ253 T01 provenance/authority custody gap; EE14 T1 hold.
- **Required before any change:** new independent review at the exact new blob; positive and negative permission-identity cases; no widening of the accepted grain.
- **Gate:** no patch, no EE14 grant, no model-use inference.

## S-06 — Learned world product: independently review S06G before adoption

- **Candidate:** S06G lifecycle blob `dadf2362`, release blob `1cb76923`, test blob `23aaf95d`. It repairs the twelve S06FR `OBSERVED` defects.
- **Current receiver:** `pre553_learned_world_composition.py` imports the current owners, but composition has no production caller. Actual consumer UNKNOWN.
- **Keep current until review:** HQ118 lifecycle `a11c9eb7` and release `f76c3906` remain the canonical LOCAL_UNAUTHENTICATED runtime.
- **Required positives:** immutable public event snapshots; exact checkpoint round-trip; serialized selection and M2 writers; transactional rollback; lawful positive/negative cases.
- **Required fault/severance tests:** mutate nested payload and observe refusal/detachment; rehashed publication/receipt mismatch; concurrent stale selection; torn append; saved-helper bypass; M2 collision race; coherent replacement treated as LOCAL_UNAUTHENTICATED only.
- **Gate:** external issuer, protected current and external custody remain HOLD. No adoption without a distinct independent reviewer.

## Review and fan-in law

- HQ performs intake, distinct review and any protected fan-in.
- This worker cannot self-adopt, merge, issue source/model permission or create protected current.
- #580–#584 stay held.
- #571 and #577 were not returned at the time of this work; no review of them is claimed.
- No whole-estate recount and no PROGRAMMA PYAT work was performed.
