# PYAT R2 LiTS — D2P portable packet Git import + independent acceptance — R1

**Disposition: `APPROVE_D2P_PORTABLE_EXPORT_AT_DECLARED_GRAIN__B001_B002_B003_CLOSED`**

Terminal: `D2P_STARRIYMAC_IMPORT_AND_INDEPENDENT_REVIEW_RETURNED__HQ_FANIN_REQUIRED`

Branch `agent/opencode-pyat-hq178-d2p-starriymac-import-review-r1`, commissioned tip `7e8123cb26e8ba03885bb1c8264302e02b83f2b3` (parent = commission base `7e84783b2`, verified). Remote is `maidiu/rawlsing`. No self-adoption.

## Result

| Blocker | Grain | Result |
|---|---|---|
| **B001** | 50/50 | `CLOSED_ACCEPTED` |
| **B002** | 24/24 snapshots, 208/208 per-object | `CLOSED_ACCEPTED` |
| **B003** | 50/50 rows, 18/18 P2 | `CLOSED_ACCEPTED` |
| Packet integrity | 10 files | 9/9 hashes exact, **0 stale** |
| Extraction script | 592 lines | **no ambiguous reconstruction** |
| Prohibitions | 9 counters | all corroborated by scan, not assertion |

Imported byte-for-byte to `NOVIYMAC_PACKET/` — **10 files, 3,836,107 bytes**, unmodified.

## The two reference namespaces that nearly cost this a PASS

This is the finding I most want HQ to see.

My first B002 resolution attempt matched each per-object `authority_snapshot_ref` against an `AuthoritySnapshot`'s `content_hash` and reported **14 unresolved refs**. That looked like a blocker. It was my error.

The two are a **disjoint namespace**:

- An **`AuthoritySnapshot`** *materialises* a governance authority. It carries `semantic_fields.authority_content_hash` / `authority_id` / `authority_version` — the same shape as the per-object refs — while its own `content_hash` / `object_id` are the snapshot's own identity. Its `authority_snapshot_refs` is **empty**.
- A **per-object** `authority_snapshot_ref` is `{authority_content_hash, authority_id, authority_version}` pointing at a governance authority document (e.g. `urn:rawlsing:governance:authority-30:...`), not at a snapshot object.

Re-run against the correct key: **2033 of 2033** per-object refs and **576 of 576** B001 refs resolve — with `authority_id` **and** `authority_version` agreeing on all 2033, so the match is a full triple, not a loose hash hit.

I am recording this rather than quietly fixing it, because a reviewer who stopped at the first result would have raised a **false blocker against an honest packet**.

## Independent recomputation, not prose acceptance

Commission line 96: *"Do not accept a worker prose assertion."* Nothing below was accepted on assertion.

- **B001** — 50/50 association grounded in each receipt's own retained `semantic_fields.candidate_identity.candidate_hash`; **50/50 receipt preimage digests recompute** from the included retained bodies. `winning_predicate_ref` non-null on all 50, so the "legitimate exact null" allowance wasn't needed.
- **B002** — 24 distinct snapshot `content_hash` **and** 24 distinct `object_id`; exactly one well-formed AuthorityRef triple each, at retained field `replay_protocol_ref`; 24/24 preimage digests recompute; 208 distinct object refs; **0 empty** `authority_snapshot_refs`.
- **B003** — 50/50 `binding_sha256` recompute from the included binding body; 50 distinct `logical_candidate_key` **on both join sides with identical key sets**; 18/18 P2 identified from retained `lane=="P2"` on *both* rows plus retained block membership, **zero disagreement**; 18 distinct `pre553_i05_candidate_hash`.

## The canonical-law check went further than required

The script's `canon_bytes` implements the commissioned law (UTF-8, `sort_keys`, `(",",":")`, `ensure_ascii=False`). I compared it **byte-for-byte against the repository's own `canonical_json` — identical** for non-float content.

One divergence: the script permits floats and would emit bare `NaN`, whereas the repo's `canonicalize()` raises `Pre553IntegrityError` on any float. So I scanned all four JSONL outputs: **0 floats, 0 NaN anywhere in the packet**. The divergence is provably inert here — not merely asserted harmless.

## Script findings — none blocking, and I did not edit the packet

| | Finding | Severity |
|---|---|---|
| F1 | `build_export_preimage` has a dead branch mutating a discarded shallow copy | cosmetic |
| F2 | `export = dict(item)` is shallow, so the deferred marker writes back into the retained item — harmless **only** because `full_sha` is computed first. Reorder those two lines and every `preimage_sha256` silently becomes the export digest, uncatchable | **fragility — worth a followup** |
| F3 | `validate()` omits receipt-ref distinctness, snapshot-ref distinctness and duplicate-key collapse. I closed all three **from the data** | gap closed independently |
| F4 | `contract` holds only the last row's value, interpolated as packet-wide (harmless — all 50 identical) | cosmetic |
| F5 | Both deferred member paths fail closed if absent | confirmed good |

Commission line 141 forbids rewriting imported files to fix them, and none needed fixing.

## Giant-body deviation — accepted, and the content is benign

All **60** EmpiricalFact rows carry complete `$deferred_retained_member` markers for both declared members: well-formed SHA-256, positive byte length, `retained_item_count` on all **120** markers, correct checkpoint SHA, marker present inside the exported preimage. Withheld total **3,276,820,474 bytes**, agreeing exactly with the closure file.

I checked what was withheld rather than taking the reason on trust: `dependency_refs` = **53,905 items / 13.18 MB** and `source_empirical_provenance_refs` = **53,902 items / 13.18 MB**. Both are enumerated **reference** lists, not respondent rows — consistent with the declared reason and with commission lines 73-78.

## What I could NOT verify, and did not pretend to

The 3.4 GB checkpoint is **not on this machine** — `LOCAL_CUSTODY` does not exist. Commission lines 48-50 direct that it must not be copied, so this is by design. Consequently I could **not** independently recompute `observed_bytes` / `observed_sha256` / `identity_gate`, could **not** re-run the script to confirm byte-reproducibility, and could **not** recompute the 120 withheld member digests.

What I did verify: the packet reports the bytes, SHA-256, estate and gate **consistently across five files**, and the checkpoint SHA is pinned identically in the script constant, the identity record, the manifest, and all 120 markers.

**`checkpoint_identity` and `canonical_closure_identity` remain recorded-but-unverified.** NoviyMac disclosed they were not verified; per commission line 162 I did **not** convert that into a pass. Commission line 164's sufficiency ruling holds — the blockers bind to the document SHA, and inventing a second field the checkpoint doesn't self-carry would demand fabrication.

## Prohibition audit — every counter corroborated

0 occurrences of `.dta`, `.sav`, `read_sav`, `read_dta`, `duckdb`, `rawlsing_next`. Only **3 absolute paths** in the whole packet: the Rawlsing root, the packet directory, and the governed checkpoint path.

Every residual hit is benign retained text, and I checked each: `pyreadstat` appears **once**, as a retained `reader_config` string inside an AuthoritySnapshot preimage; `rawlsing_next` appears 29 times as retained `object_id`s like `rawlsing_next/_pre553_query_predicate.py@<git-sha>#S…`; `Candidate A/B/C` and `P2X` appear **only inside the zero-counter rows themselves**.

## One bonus for fan-in

A retained AuthoritySnapshot preimage embeds `reader_config {pyreadstat 1.3.6, python 3.11.3, encoding latin1, apply_value_formats false, user_missing true, format DTA}` and `qualified_runtime "CPython 3.11.3 / pyreadstat 1.3.6"`. That is **packet-internal corroboration** that the retained LiTS reader config agrees with the Darwin/x86_64 anchor runtime frozen by C4C3. Recorded as a consistency observation — not a runtime qualification by this lane.

## Scope

This closes `C4B-LITS-ORACLE-PREIMAGE-CUSTODY-001` at the **retained preimage/custody grain**. It does **not** authorise raw-source C4 execution, fresh LiTS decode, a source warrant, C7, or PRE-V3→V3. Note for HQ: the 24 snapshots materialise **18** distinct authority documents — six are materialised once per governed operation scope. Read "24" as 24 snapshot objects over 18 authorities.

**0 raw survey reads · C4 not executed · 0 production mutations · 0 imported files modified · 0 prose claims accepted without recomputation · no self-adoption.**
