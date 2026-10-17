# WG0N Phase B — independent release-view source-binding court: verdict

**Verdict: `WG0N_INDEPENDENT_SOURCE_VIEW_COURT_PASS__ONE_INHERITED_CHARACTERISATION_SHAPED_RED__HQ_ACCEPTANCE_STILL_REQUIRED`**

Role: independent **WG0M reviewer continuation**. Not WG0P6 author, not HQ.
Sealed startup **`e97bf40029bf4c1b3493670c6c63882b97228a19`**.

- Parent reviewer: `WG0M@b91642ce98ec2c74b6d0c5d06ec8b83f67f02e86`.
- Candidate under review: `agent/rabochii-pyat-r27-wg0p6-release-view-artifact-source-binding-r1 @ e7e429c3dfb649233e74e0e5106e51ff25024806`.
- Productive code snapshot `292b74096e8af5f71006b97ebfab500656f063f9`, module
  `wg0p4_workload.py`, `VERSION = WG0P6_RELEASE_VIEW_SOURCE_SNAPSHOT_BINDING@1`,
  sha256 `3807e46eec947694a1bd76afe23fd96183dd989b511584ec2ad3991ae943925e`.

## Independence discipline actually applied

A WG0P6 branch existed on the remote before I began. **I did not open it.** My
17 controls were frozen and pushed at `a2b0092f107325fbc1006e03e46f8c3ddc624af4`
before any WG0P6 content was read. Only after that seal did I fetch and stage the
candidate. The hostiles therefore cannot have been tuned to whatever the repair
happens to block.

## The retained RED is genuinely falsified

WG0M's single RED was `source/release_source_artifact`. My commission allowed it
to change **only** if "physically falsified by real imported code and
independently verified outputs." That bar is met:

- WG0M's **own frozen 33** now runs **33/33 PASS** against the real imported
  candidate (I ran it; I did not accept WG0P6's tally).
- My independent control `A1_genuine_foreign_pointer` — which restates the same
  substitution — is refused with `IdentityError`, `served_positive = False`,
  `new_I03_calls = 0`.

So the RED moves, on real code and independently verified output.

## Independent results

| Court | Result |
|---|---|
| **WG0N preregistered hostiles (17)** | **12 PASS / 5 not-constructible / 0 RED** |
| WG0M frozen 33 (includes the retained RED) | **33/33 PASS** |
| Original frozen 65 (incl. cold + conditional) | **65/65 PASS** |
| WG0J 44 / K11 | **55/55 PASS** |
| Native owner 80 | **80/80 PASS** |
| Original 3 WG0L provenance negatives | **3/3 PASS** |
| WG0M adversarial 3 (outside the mandatory 235) | **1 PASS / 2 FAILED** |

### Mandatory set: 236 PASS / 0 RED

WG0M's mandatory total was 235 PASS / 1 RED = 65 + 44 + 11 + 80 + 3 + 32.
The 1 RED is now green, so the mandatory set is **236 / 0**.

### Frozen science unchanged and re-verified

- Original frontier **25 = 3 PRODUCED / 16 HELD / 6 INADMISSIBLE**
  (`conditional/original25_unchanged`).
- Ordinary conditional **yes 1 / no 1 over exactly R2 and R3, denominator 2**
  (`conditional/ordinary_full_chain_yes1_no1_over2`).
- Cold: `cold/actual_abrupt_exit23_after_one`,
  `cold/same_original_manifest`,
  `cold/original_UnitExecutionReceipt_preimage`,
  `cold/fresh_process_exactly_two_I03_calls`,
  `cold/three_original_consumer_values` — all PASS inside the original 65.
- Second frontier exact no-drop; household-person INADMISSIBLE; same-grain
  without-person HOLD.

### The 12 constructible hostiles, all refusing as required

`A1`/`A2`/`A3` release-view substitution — including the **coherent** whole-view
swap, which defeats naive per-field consistency — refused with `IdentityError`.
`B1`/`B2` pointer aliasing refused. `C1`/`C2` epoch-advance and release
revocation after binding refused with `RevocationError`. `D1`/`D2` altered and
self-rehashed snapshots refused with `IdentityError`. Every negative had
`served_positive = False` and `new_I03_calls = 0`.

**All three positives passed**, which is the guard against a blanket-refusal
implementation: `F1` pristine plan served with 4 I03 calls, `F3` own-pointer
rebind served with 4 I03 calls, `F2` replay produced **identical consumer values
and identical receipts**.

## What I am NOT claiming green — 5 of my own controls are untested

These are **my** preregistration limits, not candidate defects. I report them as
untested and do not count them as passes.

1. **`C3_source_artifact_revocation`** — the fixture owner's `revoke()` accepts
   only **release tags**; it raises `RevocationError('UNKNOWN_RELEASE_NO_REVOCATION')`
   for a source-artifact object id. Independent source-artifact revocation is
   therefore **not representable** on this owner surface. Whether it should be is
   an owner/design question I cannot adjudicate.

2. **`D3_truncated_or_empty_snapshot`** — `ExactRef` refuses an empty
   `content_hash` at **construction** (`Pre553IntegrityError: content_hash must be
   a non-empty string`). The property I wanted (no empty snapshot admitted) holds
   *earlier and more strictly* than my oracle's vocabulary anticipated. The
   oracle listed only the law's six typed error families; `Pre553IntegrityError`
   is a seventh. I did **not** widen `allowed_refusal_exceptions` to make this
   pass — that would be changing a frozen expectation.

3. **`E1`/`E2`/`E3` issuer mismatch** — `IngestedRelease` has **no**
   `issuer_id`/`issuer_epoch` fields. Issuance identity is carried in
   `rel.authorities` / `rel.qauth` and is folded into
   `_release_material`'s `authority_refs`. My three controls were specified
   against fields that do not exist, so they are **not constructible**. The
   underlying question — is a substituted or cross-epoch *authority* refused? —
   is **open** and should be preregistered as a fresh control against the real
   `authorities`/`qauth` surface. I deliberately did not silently re-target them,
   because that would be writing my oracle after seeing the code.

## The one real discrepancy: 2 inherited characterisation tests fail

`court/tests/phase_b/test_additional_descriptor_binding_red.py` — outside
WG0M's mandatory 235 — gives **1 PASS / 2 FAILED**:

- `test_bound_descriptor_cannot_change_served_provenance[source_edition]`
- `test_bound_descriptor_cannot_change_served_provenance[native_item_ids]`

Both fail with `IdentityError: COMPLETE_BOUND_SOURCE_DESCRIPTOR_CHANGED` raised
from `_check_plan`. Read their assertion shape: they call `execute(altered)` and
then assert `actual == expected`, i.e. **the served provenance equals the
original because the forgery was silently ignored**. Under WG0P5 the plan was
accepted and served unmutated values, so they passed. Under WG0P6 the plan is
**refused**, so `execute` raises before the assertion is reached.

Assessment, stated plainly:

- The **security property is stronger** now — a forged descriptor is refused
  outright rather than silently ignored. My own `A1`–`A3`, `D1`, `D2` confirm the
  refusal independently with zero new I03 calls.
- But those two tests **assert the weaker shape** and can therefore not
  distinguish "refused" from "forgery served": both make them fail. They are
  **uninformative against a refusing implementation**, and they are the only
  green path for them.

**I did not edit them and did not change any expectation.** The right fix is a
*test-shape* change — give these two the same explicit early-refusal transport
the third test in the file already has — and that is an owner decision, not
mine. Until it is made, the honest statement is: 2 non-mandatory
characterisation tests are not green against the repaired candidate, and the
property they loosely encode is satisfied more strictly than they require.

## Custody

All 9 WG0P6 pinned files verify byte-exact (sha256 **and** Git blob SHA-1).
The 8 copied court files are byte-identical to parent WG0M's — no reviewer-side
tampering. Six native owner modules were physically imported from
`pinned/rawlsing_next`, all under the pinned root, with blob identities recorded
in `observations/PHASE_B_IMPORTED_BLOBS.json`. Every project Python file is
verified against `SOURCE_INPUTS.json`/`CANDIDATE_CODE_PIN.json` before execution
by the candidate's own identity bootstrap, and the bootstrap refuses rather than
continuing on mismatch.

## Ceilings

No author code was edited. No frozen expectation was changed. No source grants,
no N11/N12, no V3, no original survey bytes, no model or actor authority. This
is an independent reviewer result; **it is not HQ acceptance** and does not grant
WG0N adoption to the candidate.

## Required next edge

1. Owner decision on the two characterisation tests (early-refusal transport).
2. A fresh, separately preregistered control against the **real**
   `rel.authorities`/`rel.qauth` surface for issuer/authority mismatch — the
   seam my E-group failed to reach.
3. Owner/design decision on whether source artifacts should be independently
   revocable (`C3`).
4. HQ acceptance remains a separate act.
