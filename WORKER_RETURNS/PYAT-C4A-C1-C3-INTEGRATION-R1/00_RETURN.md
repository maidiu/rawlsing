# PYAT C4A — C1+C3 COMBINED TREE INTEGRATION + SOURCE-FREE QUALIFICATION — R1

**Disposition:** `PASS_C4A_COMBINED_TREE_QUALIFIED__FANIN_READY`
**Terminal:** `C4A_COMBINED_TREE_RETURNED__HQ_FANIN_REQUIRED`
**Branch:** `agent/opencode-pyat-hq170-c4a-c1-c3-integration-r1`
**Commissioned tip:** `603795eb6033a35516cea73add76a1b8a9ac6687`
**Merge commit:** `9a5752a8ce4a119efd24cbbeedd8cbcda8abbadb`
**Governing Omega-1:** `01762d7379be4e423dad3e21bcdcee47c536902d` (O1-C01, combined-tree portion)

No self-adoption. No raw survey access. No lane-B freeze work. No lane-C runtime
qualification. No C4 raw execution.

---

## 1. Result in one paragraph

The accepted C1-03 join and the accepted C3 source-free repair now exist in one tree,
merged with ancestry preserved and zero conflicts. All **11 pinned blobs are EXACT** —
five C1 owner blobs unchanged, six C3 blobs landed. The accepted C1 court reproduces
**exactly** on the combined tree at **454 passed / 0 failed**, and the C3 subset reproduces
the accepted C3 result **exactly** at 76 passed / 3 failed. Those 3 failures are **inherited,
not merge-induced** — I proved it by executing both accepted parents and reproducing them
identically. Two disclosures below are load-bearing and I am not burying either.

## 2. Lineage and merge

| | |
|---|---|
| C1 accepted tip | `149c3d263…` (`integration/pyat-hq168-c1-03-successor-join-accepted-r1`) |
| C3 accepted tip | `30686b185…` (`integration/pyat-hq130-c3-source-free-accepted-r1`) |
| Merge base | `b3b2fa130…` |
| Divergence | 425 C1-only / 6 C3-only |
| Strategy | `--no-ff`, two parents, no rebase, no squash |
| Conflicts | **0** |

**Why zero conflicts, stated precisely rather than as luck.** The C1 side had not modified
any of the six C3-owned files relative to the merge base — I verified that directly, not by
assuming it. Two of the six already existed on the C1 side at their merge-base blobs and
were advanced to the accepted C3 blobs; the other four were added. So the pinned C1 and C3
blob sets were never in competition, and **no conflict-resolution judgement was exercised**.
That is the honest reading: the merge was clean because the two accepted surfaces are
genuinely disjoint, not because I resolved anything under the accepted-blob law.

## 3. Blob matrix — 11/11 EXACT, 0 drift

Verified twice: once in the pre-commit merge index, once in the committed tree.

**C1 (must remain exact) — 5/5**

| blob | file |
|---|---|
| `3a5e3db8…` | `pre553_analytical_state_and_route.py` |
| `23167aa2…` | `pre553_empirical_possibility_provider.py` |
| `547e6bf2…` | `pre553_authority_maintenance.py` |
| `47e65aad…` | `pre553_analytical_replay_dependency.py` |
| `604c8d59…` | `pre553_analytical_composition.py` |

**C3 (must become exact) — 6/6**

| blob | file |
|---|---|
| `31a9afd7…` | `closed35_g01_sav_numeric_representation_authority.py` |
| `d3d828c1…` | `pre553_physical_decoder.py` |
| `6000a170…` | `pre553_r5_codec.py` |
| `fb7b0908…` | `test_closed35_g01_sav_numeric_representation_authority.py` |
| `8fc05965…` | `test_closed35_d01_declared_encoding_admission.py` |
| `3901f10a…` | `test_closed35_d02_opaque_datetime_carrier.py` |

No accepted contract was changed.

## 4. Court — and the two disclosures

**I am not claiming a zero-failure court.**

| Suite | Files | Collected | Passed | Failed |
|---|---|---|---|---|
| C1 accepted suite | 15 | 454 | **454** | 0 |
| C3 surface + compat | 10 | 79 | 76 | 3 |
| **Consolidated** | **25** | **533** | **530** | **3** |

Arithmetic: 454 + 79 = 533 collected; 454 + 76 = 530 passed. Runtime 1226.41 s.

### Disclosure 1 — three inherited failures

| Case | Combined | C3 tip `30686b18` | C1 base `149c3d26` |
|---|---|---|---|
| `lits_i_representation_authority::test_actual_banked_projection_converts_to_exact_accepted_legacy_owner` | FAIL | FAIL | FAIL |
| `lm2_r1i_physical_native_hostile::test_native_to_canonical_mapping_authority_does_not_bridge_physical_representation` | FAIL | FAIL | FAIL |
| `lm2_r1i_physical_native_hostile::test_special_states_remain_noncanonical_and_mapping_authority_does_not_leak` | FAIL | FAIL | FAIL |

A merge-induced regression appears **only** on the combined tree. These appear on both
parents. On the same 10 C3 files the accepted C3 tip also gives **3 failed, 76 passed** —
the combined tree reproduces it exactly. So these are pre-existing failed evidence in the
repository, consistent with the accepted C1 record's own retained item *"Historical failed
evidence: 434 passed / 1 failed remains historical failed evidence and is not relabelled."*
I have not relabelled them either. **HQ must decide whether C4 fan-in carries them forward.**

### Disclosure 2 — five files excluded, surface is 25 of 30

Five declared C3 compatibility files fail at **collection** on `ModuleNotFoundError: pandas`,
absent from `/tmp/c1-01-r8-release-spine-venv`, `/tmp/c1-01-r7-execution-venv` and system
python3. Two of them additionally import the raw surface — `source_backed_c11_facade`
drives `pre553_c11_ingest`/`pre553_c11_repository`, and `sr06_decoder_carrier` imports
`pyreadstat`, the raw statistical-file reader.

**I deliberately did not install pandas.** Two of the five are raw-facing and therefore
outside lane A by the no-raw-access rule *regardless* of availability, so provisioning the
dependency would not have converted them into in-scope work. They are excluded on an
import-statement observation, not by inspecting any survey material.

## 5. How the two file lists were derived

**The C1 15-file list is a reconstruction, and I want that on the record.** The accepted
return records only the per-file profile `92/35/32/17/14/13/13/8/3/2/43/57/54/43/28 = 454`,
never the filenames. I reconstructed from the filesystem and then *constrained* by that
profile: identical multiset **and** identical 454 sum. That identifies the suite uniquely at
this grain — 15 files summing to exactly 454 with the accepted profile. It is not a verbatim
list carried in an accepted packet, and HQ should know that.

**The C3 set is mechanical, not judgemental:** the 3 pinned surface files, plus every test
file importing any of the three C3-owned modules. Those are exactly the unchanged
compatibility dependencies C3's court had to keep green. No C3 return packet at the accepted
tip enumerates its court, so this derivation is recorded for HQ to substitute if it holds an
authoritative list.

Every listed path was asserted to exist **before** execution (`missing=0`). C1/C3 overlap: 0.

## 6. Lane discipline

- **No raw survey access.** No file under `data/` was read, listed for content, hashed or
  probed. `data/` is untouched in git status. The `data/` directory was observed to contain
  only `ddm_build_copy` and `ddm_registries` at directory-listing granularity, and I did not
  descend into it.
- **No lane-B workload/oracle freeze.** Only the exact accepted input identities were
  identified, as the commission permits.
- **No lane-C runtime qualification.** Only the runtime is recorded (interpreter, Python
  3.12.14, pytest 9.1.1, wall-clock runtimes).
- **No C4 raw execution. No self-adoption.** Clean tree apart from this packet.

## 7. Requests for HQ

1. **Carry the 3 inherited failures forward as-is, or address them separately?** They are
   not mine to relabel and not merge-induced.
2. **Are the 5 pandas/raw-toolchain files in scope for any C4 runtime?** Two sit on the raw
   C11 ingest surface and are outside this lane's authority.
3. **Sanity-check the two derived file lists** against any authoritative C1/C3 court lists
   HQ holds, since neither was available verbatim at the accepted tips.

```
C4A_COMBINED_TREE_RETURNED__HQ_FANIN_REQUIRED
```