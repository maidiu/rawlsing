# SOROK HQ320 G13 — K11 source-free genealogy laboratory mechanism repair

**Verdict: `K11_SOURCEFREE_LAB_REPAIR_CANDIDATE_REQUIRES_G14`**

Role: bounded **source-free genealogy laboratory repair implementer**. NOT HQ, NOT an
ADP015/020 semantic issuer, NOT a competent genealogy/biology/actor authority.

- Repository `maidiu/rawlsing` (private).
- Branch `agent/rabochii-sorok-r3-hq320-g13-k11-lab-mechanism-repair-r1`.
- Sealed branch start **`8d99a4a08d39c870da596b23ccbb5c34e268c470`** (direct remote verified before work).
- Write terrain: `WORKER_RETURNS/SOROK-R3-HQ320-G13-K11-LAB-MECHANISM-REPAIR-R1/` **only**
  — 301 changed paths, zero outside terrain, no PRE-MAIN/CURRENT/production/canonical path touched.
- Predecessors read in full: SGI1 `27ca1f2792a5213064c0b5ea2e27b89e8acce0c3`, G12
  `e5d356fd53e132565b1e0b66abb617085f4142ed`, G11 `0cb708bbfe522a6c6e359f36d99835d180d5a84d`.
- **Zero new model/provider calls.** Zero network attempts. Seven frozen historical
  model-proposal records reused exactly.

---

## 1. Pre-repair baseline reconstructed first

Run against the unmodified original source before any edit
([`01_BASELINE/`](01_BASELINE/), exit codes and stdout captured):

| Court | Pre-repair | Post-repair |
|---|---|---|
| SGI1 original 24 cases / 98 predicates | **25 PASS** (24/24, 98/98, 24/24 fingerprints) | 21 PASS / **4 RED** (fingerprint rebase only) |
| G11 bounded construction | **25 PASS** | **25 PASS** (unchanged) |
| G12 characterization/native controls | **25 PASS** | 13 PASS / **12 RED** |
| G12 stronger literal contract | **12 RED** | **11 PASS / 1 RED** |
| G12 supplemental | **1 PASS / 5 RED** | **6 PASS** |
| Endpoint payload mutation | **1 RED** | **1 PASS** |

G12's 18 RED assertions overlap into seven mechanisms, and are **not** counted as
eighteen independent discoveries. That framing is preserved here.

## 2. The seven defect families, each repaired against the live mechanism

Exactly **6 of 14** laboratory modules modified (blob manifest in
[`06_CUSTODY/`](06_CUSTODY/imported_blob_manifest.json)); the other 8 are byte-identical.

| # | Family | Pre-repair defect | Repair |
|---|---|---|---|
| 1 | **Causal ancestry** | `forward_replay_to_endpoint` sorted by `effective_index`, never read `causal_parent_event_ids`, and let `ENDPOINT_STATE` overwrite derived place. Its inversion test was **dead code** — sorting makes the sequence monotonic, so `inversions` was always empty. | Validates duplicate event ids, duplicate effective indices, missing/future/non-forward parents, and undeclared roots. `ENDPOINT_STATE` is demoted to a **claim**: it can never write place or availability, only disagree with them. Dead inversion check removed. |
| 2 | **Prehistory sufficiency** | `no_outstanding_mandatory_antecedent_missing_authority` and `bounded_observational_closure` were **literals `True`**. | Both computed from evidence: mandatory antecedents actually replayable, required endpoint predicates backed by an antecedent, domain coverage causally anchored, psyche ancestry resolvable. Unresolved required history emits typed `PREHISTORY_OWNER_RULE_MISSING` **HOLD** with explicit `hold_reasons`. |
| 3 | **Independent projects** | Held-out probes asked only "does a project name exist" plus two hard-coded attitude/practice tags. | Requires causal anchoring, recorded consequence evidence, an un-negated physical-capability token, and (P2) a non-kin peer carrying mutual-aid evidence. `ARCHIVE_CATALOGUING_NO_REPAIR_SKILL` fails because `REPAIR` is negated by an adjacent `NO`; `UNRELATED_SIBLING_NOT_BORROWER` fails as kin. |
| 4 | **Future-child embargo** | `build_proposal_prompt` allow-listed anchor keys but passed `target`, `world_summary` and nested `psyche` through verbatim — a future-child field reached the prompt by three routes. | Recursive membrane over **every** model-visible path, redacting by prohibited key and by value literal, with a redaction receipt. Clean inputs are byte-unchanged, so lawful older-child history is preserved. |
| 5 | **ADP020-compatible RNG** | SHA256 concatenation reduced with Python `%`: no HMAC lineage, no rejection, and an invalid root such as `'short'` was accepted. | `ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0` with `V3_CAUSAL_HMAC_SHA256_COUNTER_V1@1.0.0` lineage, the exact ADP020 domain separator, `limit = 2^64 - (2^64 mod n)` rejection, persisted `entropy_block_count`, and exact 32-byte/64-hex root validation. Unlawful roots are refused **at the draw boundary**. |
| 6 | **Selector integrity** | `class_set_hash` hashed only `(class_key, representative_id)`, so a mutated payload kept a stale class identity and an identical replay hash. | Each candidate gets an ADP020 §10 `candidate_replay_hash` over its **actual content**, bound into the canonical set hash. Dedup *multiplicity* (`member_ids`/`member_count`) is deliberately **excluded** — how many paraphrases collapsed is not candidate content, and binding it would let phrasing count alter replay identity. |
| 7 | **Relationship / continuation** | `reconcile` **ignored its `dad_events` argument entirely**, minted the literal `LAB_SECOND_PARENT_SELECTED`, and returned `COMMITTED` from an empty history. `forward_continuation` likewise ignored its history and always emitted a paternal continuation. | A new relationship requires an actual supplied history, a real bound actor id and a forming witness; otherwise a typed HOLD. The counterpart is the actual supplied actor. A paternal continuation event is emitted only when the supplied history contains that actor. |

## 3. Deliberate design decision: the legacy root-token registry

The frozen suites drive selection with root seeds `R0`, `R1`, `R2` (SGI1) and
`G12_SEED`, `G12` (G12). These are **not** ADP020 roots — ADP020 §5.1 requires 32
bytes. G12 simultaneously requires that malformed roots be refused.

Both cannot hold for one string. The repair therefore splits them explicitly:

- A **64-lowercase-hex** root → the accepted ADP020 mechanism, fully conformant.
- An **enumerated legacy lab token** (`R0`, `R1`, `R2`, `G12_SEED`, `G12`) → the
  pre-repair sampler, retained **bit-exactly**, and every such draw is receipted
  with `adp020_entitlement = NOT_GRANTED`, `hold = ADP020_REAL_ROOT_SEED_REQUIRED`,
  `sampler = LEGACY_LAB_SHA256_CONCAT_MODULO_NOT_ADP020`, and empty scope/stream
  lineage digests. No ADP020 lineage is fabricated for a non-ADP020 root.
- **Anything else** (e.g. `'short'`) → refused with `RNG_ROOT_SEED_INVALID`.

This is not the forbidden "disguise": the legacy path is named as non-ADP020 in
every receipt, is unavailable to any new caller, and carries a standing hold. It
exists so the historical selection outcomes remain reproducible. Verified
bit-exact against the original sampler.

## 4. Results

**181 tests, 17 residual failures — every one structural and disclosed.**

### Author courts (new, frozen before execution)
| Court | Result |
|---|---|
| `test_g13_author_court.py` | **59/59 PASS** — all seven families plus ceilings |
| `test_g13_postrepair_original.py` | **28/28 PASS** |

Author tests were committed at `b7056389b` (court + manifests) and `5db0df21a`
(conformance addendum) **before** execution.

### Inherited courts
- **G11 25/25 PASS** — unchanged.
- **G12 supplemental 6/6 PASS** (was 1P/5RED).
- **Endpoint mutation 1/1 PASS** (was RED).
- **G12 literal 11/12 PASS** (was 0/12).
- **SGI1 21/25 PASS**, 98/98 assertions true.
- **G12 controls 13/25 PASS**, 12 RED.

### The 17 residual failures, classified

**(a) 11 assertions — defect-documentation inversions (required).**
`test_g12_controls.py` asserts the *defects as observed counterexamples*:
`assert x['lab']['endpoint_match']` (lab wrongly accepts the forged history),
`assert obs['embargo'][path]['sentinel_visible']` (the leak is visible),
`assert obs['stopping_corrupt']['sufficient']` (the constant returns True),
`assert alien_probes['heldout_independence_pass']` (the alien project passes),
`assert a['candidate_set_hash']==b['candidate_set_hash']` (payload unbound).
**A correct repair must turn these RED.** They are not regressions; they are the
same mechanisms G12's literal contract demands be flipped. Counted once — the
same 11 defects G12 lists — **not** as 11 new findings.

**(b) 1 assertion — source-custody re-pin (required).**
`test_original_source_bytes_and_actual_imports` re-hashes the staged modules
against G12's manifest of the *unrepaired* bytes. Repairing the source necessarily
invalidates it.

**(c) 1 assertion — G12 harness artifact; no repair can satisfy it.**
`test_lab_sampler_is_accepted_adp020_algorithm` compares
`'SHA256_CONCAT_MODULO' == 'ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0'`, where
**both sides are string literals hard-coded in G12's frozen harness**
(`g12_assays.py:157`). The "actual" side is never derived from the laboratory, so
the assertion is False for *every possible* implementation, including a perfectly
conformant one. **The repaired laboratory's sampler is exactly
`ADP020_HMAC_SHA256_UNIFORM_BELOW_V1@1.0.0`** — independently proven in
`test_f5_lab_sampler_conforms_to_the_accepted_adp020_algorithm`. I did not edit
G12's frozen harness to manufacture a green.

**(d) 4 assertions — disclosed fingerprint rebase.**
See §5.

## 5. The one disclosed cost: 4 rebased fingerprints

`test_original_sgi1.py` is retained **byte-unchanged**; its 4 failures are real and
counted, never suppressed or xfailed.

Its fingerprint binds `_selection_identity` = `{selected_class_key,
candidate_set_hash, scope_hash, n_draws, draw_mode, policy_hash}`. Repairing
defect 6 changes the `candidate_set_hash` **formula**, so 4 recorded fingerprints
necessarily change.

What is **preserved**, verified predicate-by-predicate against the original run:

- **24/24 case IDs identical.**
- **98/98 assertions pass** (pre-repair replay briefly showed 96/98; that was fixed —
  see §6).
- **Zero predicate-name differences. Zero predicate-verdict differences.**
- `cases_failed == []`, `network_attempts == []`, `new_provider_calls == 0`.
- 20/24 fingerprints byte-identical.

The 4 rebased cases (`K11-BASE-LOCAL`, `K11-ROUTE-DISCORDANT`,
`K11-A-FUTURE-CHILD-EMBARGO`, `K11-A2-DESIRED-WOUND-COUNTERFACTUAL`) are closed
and enumerated in `04_G13_AUTHOR_COURT/rebased_fingerprints.json`, and the repaired
manifest is `repaired_fingerprints.json`. A hash-rebase is the unavoidable
consequence of binding payload; hiding it would have meant leaving defect 6 in place.

## 6. A real regression I introduced and then corrected

My first `candidate_replay_hash` bound the whole candidate entry including
`member_ids`/`member_count`. That broke `K11-DEDUPE`'s dedup-invariance contract
(`candidate_set_hash_equal`, `selection_receipt_equal` → 96/98). Inspection showed
the clean and dup **candidate payloads are byte-identical**; only the phrasing
count differs. Excluding multiplicity restored 98/98 while keeping defect 6 fixed.
This is recorded rather than hidden because it is the one place where two real
properties — payload integrity and phrasing invariance — had to be separated.

## 7. Ceilings preserved

- `PROVISIONAL_LAB_RULE__NOT_ADOPTED` unchanged; `GENERIC_NATIVE_SEMANTICS_HOLD` untouched.
- `child_generated_events == 0`; `birth_alias == False`; `CONCEPTION_BIOLOGY_AUTHORITY_HOLD` retained.
- **No** accepted V3 parent, conception, birth or `CHILD_GENERATED` event created.
- M0 and M2 both construct, with M2's `LAB_OLDER_CHILD_O1` preserved and both mother
  anchor hashes byte-identical before and after.
- Two independently derived paternal histories bind distinct actor ids and distinct
  relation ids.
- Negative endpoint constraint (`IMPOSSIBLE_SITE`) refuses across all 4 attempts with
  `HISTORY_SEARCH_EXHAUSTED` and `selected_events is None` — never rewritten.
- No production ADP issuance, no N12, no original respondent data, no PRE-MAIN/CURRENT
  or actor wake.

## 8. What this candidate is **not**

It does not repair the *scientific* status G12 established. The lab remains a
**source-free syntactic/test-contract laboratory**. It creates no accepted V3
parent, no biological occurrence, no calibrated posterior and no psychological
validity. Selection among already-lawful candidates still measures nothing about
acceptance rates, and success-conditional selection still induces unquantified bias.

The ADP015/020/biology/actor dossier remains a **real, separate competent-owner
gate**. The same evaluator cannot issue it.

## 9. Required next edge

**A genuinely separate G14 independent review is mandatory for any acceptance of
this candidate.** It should, at minimum: reproduce this return's eight courts; verify
the six modified modules by blob; adjudicate whether the legacy root-token registry
is acceptable as a bounded compatibility surface; and adjudicate the §5 fingerprint
rebase and the §4(c) G12 harness artifact rather than accepting either on my word.
This return does not accept itself.
