# R111 independent oracle — three R110 binding repairs

Status: frozen before successor code inspection. Baseline is the R109 oracle
and review; this is a scoped qualification of three completed repairs, not full
R107/R06/N10W acceptance.

## Exact identities

- R111 commission: `ac6a26809d8cb94cf806d15936f68a96cacd29c6`
  `WORKER_COMMISSIONS/PYAT-R111-R06-BINDING-REPAIR-REVIEW-R1/00_COMMISSION.md`.
- R110 candidate: `359ffcef4c2dbde0bea7233bdb8901e8ed28e9be`; code
  `b6acb241366b1a940c613a779037f97351bd0d85`.
- R110 baseline: `22280a3f43e751bab1bbebe0a9d8c601b3160120`; R110 contract
  `53981ac013755407ebf7de88f894add2f1dc2858`.
- Prior R109 review: `e38a6a8c07ea6535a0d4de38053c15e4278934d7`; frozen
  R109 ORACLE at that commit.
- R107 contract `bb4ad106af69eae197251d8c0d54f7162901fd5e`; P41 packet
  `f27d1101048638bba395143a48efb7ef00bfcda4`; prior R06 review
  `fbe7ffc00a021aeacce3b15a2ef74cd8657d9d56`.
- Reviewer branch:
  `agent/opencode-pyat-r111-r06-binding-repair-review-r1`; writes ONLY
  `WORKER_RETURNS/PYAT-R111-R06-BINDING-REPAIR-REVIEW-R1/`.

## Three repairs to qualify

1. **World/prefix identity agreement.** `configure_progressive_world_context`
   must derive actual source universe, release/consumer release, risk-set and
   repository identity from every producer prefix, require all prefixes to
   agree, and require the governed world's source universe/release/risk/
   repository to agree. A mixed-prefix or foreign-world mismatch must produce
   a typed refusal before serving. Verify actual values/refs used by the
   evaluator, not only matching labels or hashes.
2. **Empirical permission/revocation/currentness.** The actual selected
   snapshot empirical state must be read and carried into the N9 world/view
   availability. `revoked_scope="empirical"` must return typed unavailable, not
   a selected view; a clean context restores. Field revocation and current/as-of
   behavior must remain. Verify actual catalog state, not a wrapper label.
3. **Actual producer N10E→N10W positioned binding.** Each prefix must invoke
   the actual `evaluate_positioned_subject_possibility` on its actual computed
   evidence, require its result hash to match the producer/extension consumer
   hash, and emit actual P41
   `evaluate_positioned_subject_possibility` trace entries. The resulting
   `n10w.positioned_consumptions` must be `LIVE_TRACE` with actual N10E
   consumer result hashes, not cached null placeholders. Verify evaluator call
   and values, not labels/hashes alone.

## Fourth held gap

The T0/T1 world-value→N10W consumption gap is explicitly stopped at the pinned
P41 owner. Verify the author reports the exact owner/path/lines/API missing and
does not claim full N10W world consumption. Do not reject the three independent
repairs merely because this upstream gap remains; do not accept the whole
R107/R06 function as complete.

## Preserved baseline positives/controls

- Actual producer prefixes, condition VALUE mutation, semantically unlike target
  shape, minority/zero observed, uncertainty, actual N10E cells/denominators.
- Actual T0/T1 E04 route change; field revocation/restore; cold replay.
- Pinned owner/runtime and prior R06 boundary controls; no caller-selected
  runtime/original/admission authority; no actor state.
- Cross-unit/unsupported context behavior remains as previously scoped.
- No original 35/1890/global F6/F7/F8, source/science, F5/F6/F7, R09/CI/prod,
  N11/N12, Sorok/J52/W52, actor, production or full-estate acceptance.

## Verdict

Scoped recommendation: `ACCEPT_SCOPED` for the three demonstrated fixes only,
or `REVISE` with exact minimal defect(s). Full R107/R06 remains incomplete while
the P41 world-value/N10W gap is held. Reuse exact R109 probes plus minimal R110
successor controls; no broad sweep, new court, new worker/provider or candidate
repair.
