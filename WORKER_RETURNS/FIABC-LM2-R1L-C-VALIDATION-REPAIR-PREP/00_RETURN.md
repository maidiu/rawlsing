# FIABC-LM2-R1L-C — Validation-Authority Repair Preparation

Status: `PASS__CONDITIONAL_REPAIR_READY__NOT_ACTIVATED`

Terminal:

`FIABC_LM2_R1L_C_CONDITIONAL_REPAIR_READY__AWAITING_PROVENANCE_AND_LOCK2_SUCCESSION_COURTS`

Repository: `maidiu/rawlsing`

Exact base:

`89bfde652eb8a983e51ff51f5258e5fdfbb2433b`

Branch:

`agent/rabochii-premain-fiabc-lm2-r1l-c-validation-repair-prep-r1`

## Holding

The complete source-free technical repair for the R16 validation-authority defect is prepared but deliberately **not activated**.

The repair constructor is:

`rawlsing_next/fiabc_lm2_r1l_validation_authority_successor.py`

blob:

`f29e80345afd7e953f8f03fc52350b83b220f350`

It consumes the exact frozen P2F2 runtime package and refuses to proceed unless fan-in supplies normalized PASS evidence from:

1. the R1L-A independent pre-outcome validation-authority provenance court; and
2. the R1L-B Lock2 succession/invalidation court.

No Worker A or Worker B result is assumed in this branch.

## Exact repair shape

The predecessor DiscoveryAuthority is fixed at:

`24591678ebf50ac153fabdbbcd90d6ce818c5a89a5307c395c48a04fe5a8b1ab`

The frozen candidate grammar remains exactly:

`a94bd2ed3b64b2c51f6d329560feef6b97f69da3527081d8ca6168ae63e5f7f6`

The successor may add to `validation_rules.kinds` only the canonical exact tuple:

1. `DISTRIBUTION_DIFFERS_FROM_BASELINE`
2. `JOINT_NOT_PRODUCT_OF_MARGINALS`
3. `TARGET_CELL_SUPPORTED`

No wildcard, `ALL`, future validation kind, adaptive expansion, candidate pruning, or outcome-derived authority is admitted.

Every other DiscoveryAuthority semantic field is required byte-semantically identical. The constructor also deterministically rebinds the authority replay/fingerprint root to the predecessor ref, exact grammar ref, exact three-kind envelope, accepted pre-outcome authority parent refs, and the independent provenance receipt ref. Any new authority parent must be an exact immutable AuthorityRef supplied by the R1L-A fan-in.

The generic I05 enforcement in `pre553_discovery_exact.py` is untouched.

## Lock2 seam

The predecessor Lock2 remains:

`8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`

The prepared seam does **not** preserve that hash at all costs. Once R1L-B supplies a PASS constitution, it deterministically recomputes:

- the exact replay binding with the successor DiscoveryAuthority ref;
- the replay hash;
- the Lock2 material;
- the successor Lock2 hash.

It refuses activation if R1L-B says the candidate grammar, predicates, queries, universe, risk set, or measure basis require semantic change. Candidate hashes may be reused only when the succession court classifies that as lawful; if R1L-B requires source-free replay with expected equality, exact replayed hashes must equal the frozen 46-candidate stream before Lock2 emission.

No candidate is added, removed, ranked, or pruned.

## Generic-I05 reentry proof

The hostile court directly exercised the unchanged generic I05 function.

- The old defective DiscoveryAuthority still fails with:
  `Pre553AuthorityError: candidate validation rule exceeds exact discovery validation authority`.
- The conditional exact-three-kind successor crosses that same generic validation-admission guard.
- The test then stops at a sentinel before any empirical candidate evaluation.

Thus the repair targets the authority envelope rather than weakening I05.

## Qualification

GitHub Actions:

- run: `35626098364`
- job: `106420722226`
- qualification head: `a0fcebeb14aecc628334d30cc84de634a5b8a721`
- protocol self-test: **20 passed**
- governed source-free court: **45 passed**
- artifact: `10652766242`
- artifact ZIP SHA-256:
  `3e27ace8d1dc22b5a7121b935d491ddbe95e80d24463ae95280f644524071dfd`

The governed court included the 17 R1L-C hostile/conservation/reentry tests plus the existing generic PRE553 discovery and authority suites.

## Preserved boundaries

No validation implementation was changed.

No candidate constructor was changed.

No predicate was changed.

No query template was changed.

No empirical outcome was inspected.

No real I05 was executed.

No WVS SAV/ZIP was opened.

No Candidate A/B/C process was started.

No measured P2X was run.

No Lock2 was activated or reissued on this branch.

R15 remains the exact already-admitted logical release law and is not patched by this worker.

The temporary qualification PR is CI-only and must not be treated as a fan-in adoption of the conditional repair.
