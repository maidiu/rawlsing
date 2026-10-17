# WG0O — independent issuer / release-authority residual seam verdict

**Verdict: `WG0O_ISSUER_SEAM_COURT__THREE_REAL_RED_SAME_IDENTITY_AUTHORITY_BODY__TYPED_HOLDS_PROVEN__OWNER_AND_HQ_DECISIONS_REQUIRED`**

Role: independent **WG0N reviewer continuation**. Not WG0P6 author, not HQ,
not a source/semantic issuer. This is a source-free scientific verdict.

- Branch: `agent/reviewer-pyat-r28-wg0o-source-issuer-authority-seam-court-r1`
- Sealed startup: `0533516fe939bb1d91be108b4bf05249639afbae`
- Parent reviewer: `WG0N@6cd28b429504ad47e1bbc0fbcc6c4ef91db59ccd`
- Candidate under review: `WG0P6@e7e429c3dfb649233e74e0e5106e51ff25024806`,
  module `wg0p4_workload.py`, `VERSION = WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`,
  sha256 `3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e`,
  git blob SHA-1 `ef4f2b33c07596ae6c3008320f13d9f5d027b9e4`.

## Independence discipline actually applied

Phase A froze `01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json` (14 controls),
`repro/authority_seam_adapter_v1.py` and `tests/test_authority_seam_court.py`,
and pushed them at `96e58625c` **before any candidate execution**; the staged
WG0P6 tree was verified byte-exact over all 195 expected files first and is
carried in the return (`3e331a96a`). The controls target the **actual**
`rel.authorities` / `rel.qauth` issuance fields and the **actual** owner
interfaces. The nonexistent `IngestedRelease.issuer_id` / `issuer_epoch`
fields are not targeted, and the parent's five unconstructible controls are not
rewritten to claim previously banked results.

## What the residual seam actually is — three REAL REDs

| Control (identity triple preserved) | Observed |
|---|---|
| `A2_stale_issuer_epoch_same_identity` — `effective_time_or_interval='2019-01-01'` + `supersession_refs` | **SERVED** 42 supported cells, 4 I03 calls |
| `A3_same_hash_foreign_signed_body` — foreign semantics fingerprint / replay root / parent refs | **SERVED** 42 supported cells, 4 I03 calls |
| `A4_foreign_governed_operations_same_hash` — foreign governed operations under the same hash | **SERVED** 42 supported cells, 4 I03 calls |

A foreign, stale-epoch or superseded authority body that keeps the
`(authority_id, authority_version, authority_content_hash)` triple serves
SUPPORTED original facts. The release-material binding and the owner
registration cannot see it (`_release_material` binds only
`authority_ref.as_dict()`; the claimed `authority_content_hash` is never checked
against the snapshot's semantic body hash), and the native positive-authority
check does not interpret `effective_time_or_interval` / `supersession_refs`
(A2/A3) or follows the substituted body's own `governed_operations` (A4).
This is exactly the scientifically material authority seam the commission
directed at real fields, and it is genuinely falsified on real imported code.

**Eight of eleven negatives ARE refused typed**, including the wrong-issuer and
cross-universe substitutions (`SOURCE_C11_READSET_CHANGED`), missing issuer
(`RELEASE_VIEW_SOURCE_BINDING_UNRESOLVABLE`), forged/self-rehashed checkpoint
signatures (`UNTRUSTED_OR_SELF_REHASHED_CHECKPOINT`), captured executor
callback (`INVALID_NATIVE_FACT_PAYLOAD`) and source-artifact revocation
(`UNKNOWN_RELEASE_NO_REVOCATION`). **All three positives serve** (42 supported
cells each; P2 identity rebind serves; P3 replay is byte-identical in consumer
values and receipts) — the guard against blanket refusal.

## Answers to the commission's determination question

1. **Executable at the adapter seam (no new issuer):** bind each
   `AuthoritySnapshot`'s immutable object `content_hash` into
   `_release_material`'s `authority_refs`, pin the plan-bound query operation,
   and enforce an epoch/currentness bound in `_check_plan`/`check_current`.
   The existing refusal machinery then closes all three REDs without touching
   the accepted PRE553 native owners.
2. **Source-owner design decision (deeper):** whether
   `require_positive_authority` should interpret
   `effective_time_or_interval`/`supersession_refs` (the FAIL_CLOSED_STATES
   vocabulary already contains `SUPERSEDED_NOT_REPLAYABLE`) and whether
   `authority_content_hash` is a semantic content binding or a label claim.
3. **Genuinely missing capability:** independent source-artifact revocation —
   `FixtureOwner.revoke()` accepts release tags only; `RevocationError('UNKNOWN_RELEASE_NO_REVOCATION')`
   is the honest typed ceiling. WG0N's C3 stays not-green.
4. **Missing independent issuer is typed HOLD** — proven by fresh control C2;
   the caller grant hint is explicitly `TEST_ONLY_HINT_CANNOT_ISSUE_PERMISSION`
   and any mutation of it is refused.

## Banks and regressions (not rebuilt, not re-claimed)

The parent's mandatory **236 PASS / 0 RED** stands banked. I reproduced the
physical courts as regression, not as a new whole-estate claim:

| Court | Result |
|---|---|
| WG0M frozen 33 | 33/33 PASS (retained RED `release_source_artifact` green on real code) |
| WG0L precommitted 65 | 65/65 PASS — includes `conditional/original25_unchanged`, `conditional/ordinary_full_chain_yes1_no1_over2`, `cold/actual_abrupt_exit23_after_one`, `cold/fresh_process_exactly_two_I03_calls`, `cold/full_frontier25_retained` |
| WG0N hostiles | 12 executed PASS / 5 unconstructible NOT GREEN / 0 RED |
| Historical characterisation (unmodified) | 1 PASS / 2 FAILED (`IdentityError: COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED`) |
| WG0L original3 provenance negatives | 3/3 PASS |
| **WG0O new authority-seam court** | **8 typed refusals / 3 REAL RED / 3 positives serve** |

The two historical characterisation failures are reproduced **without modifying
their expectations**; `03_HISTORICAL_COMPAT_AND_SOURCE_ARTIFACT_REVOCATION.md`
recommends an explicitly versioned safety-correct early-refusal transport to HQ
rather than acceptance by changing assertions. The five unconstructible
controls stay NOT green.

## Sourcefree acceptance ceiling

Accept the demonstrated sourcefree core only at the parent's banked ceiling,
**minus** the authority-body seam: release-view/source-snapshot binding
(A1/A5/C3 class), checkpoint signatures, owner journal, missing-issuer HOLD and
source-artifact-revocation honesty all hold on real imported code, but
**same-identity authority-body substitution (stale epoch, superseded, foreign
body, foreign governed operations) serves supported facts**. Until an
owner/HQ decision closes that seam (section "Answers" items 1–2), no broader
issuer/authority claim is supportable.

## Ceilings and non-grants

No author code was edited. No frozen expectation was edited. No original35
rights, no external authenticated issuer, no I05, no N11/N12, no Sorok V3, no
method adoption, no HQ acceptance, no source/semantic issuer. This is an
independent reviewer result; HQ acceptance remains a separate act.

## Return packet

- `00_INDEPENDENT_ISSUER_SEAM_VERDICT.md` (this file)
- `01_FROZEN_ACTUAL_AUTHORITY_API_CASES.json` — Phase A frozen oracle
- `02_PHYSICAL_ORIGINAL_NATIVE_COURTS.json` — per-case raw outcomes and court counts
- `03_HISTORICAL_COMPAT_AND_SOURCE_ARTIFACT_REVOCATION.md` — compatibility and capability classification
- `observations/` — raw per-case receipts, JUnit XML and import/custody records
- `staged_candidate/` — byte-verified WG0P6 candidate (195 expected files)
- `inherited_wg0n_court/` — byte-identical parent hostile court incl. its Phase A receipt
