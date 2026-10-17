# WG0P7 — real immutable authority-body repair (WG0P4→P5→P6 author continuation)

**IMPLEMENTER_REPAIR_RETURNED; WG0Q INDEPENDENT REVIEW AND PYAT HQ ACCEPTANCE
PENDING.** This continues the bounded WG0P4/WG0P5/WG0P6 author role. It supplies
no independent verdict, no HQ accession, no original source/issuer rights and no
method adoption.

- Branch: `agent/rabochii-pyat-r29-wg0p7-immutable-authority-body-binding-r1`
- Sealed startup: `a72e75a011468a1f0ea7b251f5b07969f59488e0`
- Parent implementation: WG0P6 `e7e429c3dfb649233e74e0e5106e51ff25024806`
- Independent court being answered: WG0O
  `agent/reviewer-pyat-r28-wg0o-source-issuer-authority-seam-court-r1@3ee5d6a4e246fca89740d4d36ab26206230c83bf`
- Repaired module: `wg0p4_workload.py`, sha256
  `89fed0a6078b5bb2ced8ce930ef6f56364acf2a4a9b24ab6210adfe90d89a643`,
  git blob SHA-1 `62895078908ff748771da9a9fbcec6b36d34a803`, previously
  WG0P6 sha256 `3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e`.

## The defect reproduced first, unmodified

The exact WG0O 14-case oracle and its unchanged adapter were executed against
the byte-exact WG0P6 module before the repair. The three REDs reproduce
verbatim: A2/A3/A4 each **served 42 supported cells with 4 native I03 calls**
while preserving the `(authority_id, authority_version, authority_content_hash)`
triple. The eight other negatives refused typed and the three positives served.
Root cause: `_release_material` folded only `authority_ref.as_dict()` (the
claimed triple), so the CONSTRUCTED `AuthoritySnapshot.content_hash` semantic
body was never bound; a substituted body with the same claimed hash was
invisible to the owner registration, compiled-plan material and every recheck.

## The actual productive repair (three coupled changes)

1. **Immutable constructed body binding.**
   `_release_material` now carries, for every `(*rel.authorities, rel.qauth)`,
   `_authority_body(a) = {claimed ref, constructed content_hash, full semantic
   projection}` under `authority_bodies`. The material digest — registered by
   the fixture owner at ingestion and rechecked at compile, every I03 boundary,
   consumer publication and cold restore — therefore changes when ANY body field
   changes, even under an identical claimed triple. A caller-crafted or
   self-rehashed body cannot authenticate itself against the owner-held digest.
2. **Owner-qualified operation binding.**
   `_authority_operation_check` derives the permitted operation from the
   owner-registered release tag (`WG0P3-OP-wg0p3-<release_tag>`) and refuses any
   qauth whose `governed_operations` is not exactly that singleton. A substituted
   body cannot make a foreign operation look permitted, and the native I03
   operation inference can no longer be steered by the mutable body.
3. **Typed HOLD for unqualified epoch/supersession.**
   `_authority_currentness_check` refuses a body whose
   `effective_time_or_interval` is not the fixture's qualified `ALL_TIME` or
   whose `supersession_refs` is non-empty, with a typed
   `AuthorityCurrentnessHold` (`AUTHORITY_EPOCH_UNQUALIFIED_HELD` /
   `AUTHORITY_SUPERSESSION_UNQUALIFIED_HELD`). No universal 2019-expiry rule is
   invented; a dated epoch or a supersession chain is simply not qualified by
   this sourcefree owner. The deeper issuer-side temporal interpretation remains
   an explicit owner-science decision (see `04_WG0Q_INDEPENDENT_REVIEW_WAKE.md`).

Both checks run at the top of `_check_plan`, so they fire before any native I03
execution on compile, pre/post-I03 recheck, run and cold restore. The accepted
native PRE553 owners, frozen oracles, the 25-operation frontier, the WG0P6
source-view binding and the owner journal schema are unchanged.

## What the repaired candidate actually does on the frozen 14

| Case | Before (WG0P6) | After (WG0P7) |
|---|---|---|
| A1 wrong issuer qauth | typed refuse | typed refuse |
| **A2 stale epoch + supersession** | **SERVED 42 / 4 I03** | **`AuthorityCurrentnessHold` HELD, 0 cells, 0 I03** |
| **A3 same-hash foreign body** | **SERVED 42 / 4 I03** | **`IdentityError` REFUSED, 0 cells, 0 I03** |
| **A4 foreign governed operations** | **SERVED 42 / 4 I03** | **`IdentityError` REFUSED, 0 cells, 0 I03** |
| A5 foreign `authorities[0]` | typed refuse | typed refuse |
| B1 self-rehashed checkpoint | typed refuse | typed refuse |
| B2 foreign signature | typed refuse | typed refuse |
| B3 captured callback | typed refuse | typed refuse |
| C1 source-artifact revocation | `UNKNOWN_RELEASE_NO_REVOCATION` | unchanged |
| C2 missing issuer | typed HOLD | unchanged |
| C3 cross-universe alias | typed refuse | unchanged |
| P1/P2/P3 positives | 42 cells each | 42 cells each, **consumer byte-identical** |

`01_FULL_AUTHORITY_SNAPSHOT_PREIMAGE_AND_THREE_NEGATIVES.json` carries the full
constructed body preimage now bound into the owner-registered material.

## Inherited sourcefree core, physically re-run on the repaired module

| Court | Tests | PASS | FAIL | ERROR | SKIP |
|---|---:|---:|---:|---:|---:|
| WG0M frozen descriptor 33 | 33 | 33 | 0 | 0 | 0 |
| Original frozen 65 (incl. original25, conditional yes1/no1 over 2, real cold) | 65 | 65 | 0 | 0 | 0 |
| Original J44 / retained K11 | 55 | 55 | 0 | 0 | 0 |
| Accepted native owners 80 | 80 | 80 | 0 | 0 | 0 |
| Original-three provenance negatives | 3 | 3 | 0 | 0 | 0 |
| WG0P6 author descriptor 26 | 26 | 26 | 0 | 0 | 0 |
| WG0P6 source-view boundary suite | 42 | 42 | 0 | 0 | 0 |
| **Mandatory 236 = 33 + 3 + 80 + 55 + 65** | **236** | **236** | **0** | **0** | **0** |

Exact cold/conditional nodes inside original65 are reproduced:
`conditional/original25_unchanged`,
`conditional/ordinary_full_chain_yes1_no1_over2`,
`cold/actual_abrupt_exit23_after_one`,
`cold/fresh_process_exactly_two_I03_calls`,
`cold/three_original_consumer_values`,
`cold/full_frontier25_retained`.

## Ceilings and non-grants

No original SAV/DTA/source35, no real external issuer, no independent
source-artifact revocation, no I05/Route B, no OC05/N11/N12/V3, no
production/canonical mutation, no accepted PRE553 native-owner rewrite, no
frozen-expectation edit, no semantic-issuer adoption. The WG0N five historically
unconstructible controls remain NOT GREEN. Two older characterisation scripts
that demand silently ignoring forgery remain unmodified failures where they
conflict with stronger pre-I03 refusal, not rewritten to green. Independent
WG0Q review and Pyat HQ acceptance decide the method.
