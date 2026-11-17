# D4B — hostile mutation return (initial, frozen)

**Pair question:** Can a malicious or merely incompetent author make the
repaired ANVIL claim no-loss/ready while discarding essential functions,
negative evidence, boundaries, or actual consumers?

**Answer at the tested cut:** **YES, against the supplied R7 instrument.**
The matrix has 14 rows: one clean baseline (H00), one clean restore (H13), and
**12 hostile mutations** (H01–H12). **11 of the 12 hostile mutations pass the
component they target**; of the 11 gate-targeted mutations (H02–H11), **10/10
pass**. Only the literal K3 `NOT_ADOPTED` boolean is defended (H12 RED).
Passing attacks include a synthetic 118-row ledger, a changed K3 row hash, an
attacker-authored source file, deleted negative content, a fabricated owner
grant, all seven boundary contracts removed, survey→actor causal knowledge, a
revoked release, and a non-existent builder test command. Exact accounting:
`ATTACK_ACCOUNTING.md`.

## 1. Exact source / currentness

| Item | Pin |
|---|---|
| worktree / branch | `D4B` / `agent/anvil-d4b-rabochii-20261117-r1` |
| product base | `cea2d4d3009e9087d2267e9d1f53bec28b730dc7` |
| live protected copy | `31291d08179890852246c8742700e055168e9933` |
| K3 snapshot | `7fc00289dd801d2d0a8ce159986c7595fc27a4d9` |
| K3 blobs | `a91214b9fd89ab97897ec1c3cd48cb5285b7029c`, `1f5a3ae8a40593dccf34753c9fa9577155ebf163`, `5a84ca8cb0a2b16d4a68b2200fa426fd9451b343` |
| K3 file SHA-256 | `0dfe6539f1a1f7f028c5968c0e85078cbf5f80a847d0c94ea1929f57d20c052d`, `6d0766ecc637ee03a705c1772e7bcda39c09c9534f0672cd36a27cfa85e0dfa2`, `8adf74cfbf2e916f41641f5836ab82305059b59e1665a2e1647dfb6bdeb0e9d3` |
| supplied ZIP | `ANVIL_R7_INTEGRATED_WORKFLOW_FIX_20261117.zip` SHA-256 `526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332`, 280 files |
| package digest (cold copy) | `4e951afefa29f29dc04d22cd9b0f2747590bcb1930f0d03ee8d028b3c96e53e0` before runner |
| report | `MUTATION_TESTS/REPORT.json` SHA-256 `b800cc4328f1387bc946549a56a3d5284dc8df95fc62332c6e0d9a332cdf4c53` |
| matrix | `HOSTILE_ATTACK_MATRIX.tsv` SHA-256 `78aaf2d830c2f5bfca95499897ffdd22060fa0c040711034466a538ab9bb3125` |
| strict overlay | `MUTATION_TESTS/strict_instrument.py` SHA-256 `b7eca19e07df4d61288ec4b7e055c150b4d21477900c3123eb5400047d900b48` |
| harness | `MUTATION_TESTS/hostile_attacks.py` SHA-256 `d9ae5dbea55f9d31f14002f389a360bcbc042cba51daf8430d6221f39722d5ad` |
| cold log | `COLD_RUN.log` SHA-256 `63ed1a7aa2ebda245939b7899a3d531b4a618661b49cae99252efe57591b78d8` |
| fleet bank | `8523007613d411390a76683fa464002c0f25df83`; `START_HERE` + `FORENSIC_RECOVERY` read |
| bank byte check | 299 entries, **297 hash-match, 2 mismatch**; 279 ZIP text members, **278 exact, 1 CRLF→LF** |

## 2. Confirmed observations / interpretation / owner holds

**FINDING (executed):** supplied gate results — 11 of 12 hostile mutations pass
their target (10/10 gate-targeted); H12 (K3 NOT_ADOPTED flip) RED. H00/H13 are
clean controls, not attacks. Strict overlay — H01–H12 RED, base H00 and restore
H13 PASS at FRAME/DECISION/C. Exact rows and error codes: `HOSTILE_ATTACK_MATRIX.tsv`.
Cold copy: author suite exit 0; quality runner `PASS_LOCAL_SYNTHETIC_AND_FORMAT_ONLY`
12/12; documented FRAME/DECISION CLI exit 2 because no packet exists. That last
observation is **not** proof of a defective finished builder: FRAME/DECISION/C
are author outputs (see `COLD_BUILDER_REHEARSAL.md`); the demonstrable builder
defect is H11, where a non-existent `test_command` is accepted.

**INTERPRETATION:** the passive checks (IDs, prose floors, schema, JSON pins)
are real but are not source authentication or semantic conservation. The
instrument's own documentation says the opposite ("source-byte anchored
handoff", "full 118-record meaning"). That is a false readiness surface, not
merely a missing benchmark.

**ACTION:** authored a private strict overlay that binds K3 rows to exact Git
bytes, requires per-118 design dispositions, restores the seven frozen
boundaries, rejects textual grants and survey→actor causality, pins
release/revocation, and resolves builder commands. Sabotage now fails; clean
restoration passes.

**OWNER:** any uptake of the overlay belongs to the R7 integrator and final C;
K3 semantic truth belongs to K3 source owners; release/actor rights belong to
their existing owners. I claim none.

## 3. Strongest alternative / counterexample

The strongest defence of the supplied package is that `tools/anvil.py` *does*
contain a strict K3 row check (`row_sha256`, blob equality, ID census). If that
check were wired into the active R7 path, D1–D3 might be documentation defects
rather than gate defects. Counterexample: the check is unreachable in two
independent ways — the active path never calls `anvil.validate(strict_repo=...)`,
and the check itself fails on every correct repo because `anvil.py:95` appends
`/` to a `k3_source_root` that already ends in `/`
(`03_FROZEN_SOURCE_CUTS.json:5`), producing a non-existent `//` path. Verified
by direct `git rev-parse`. So the defence does not hold at this cut.

## 4. Work and tests actually executed

```
python3 MUTATION_TESTS/hostile_attacks.py
python3 PACKAGE/tools/test_r7_integrated.py        # exit 0
python3 PACKAGE/tools/run_r7_quality.py            # 12/12 exit 0, synthetic only
cold cp -R PACKAGE; documented FRAME/DECISION      # exit 2, no packet files
```

All XML/JSON/TSV results are under `MUTATION_TESTS/`; cold log at `COLD_RUN.log`.

## 5. Final-integrated-candidate status

No integrated repair candidate was supplied to this return. Attacks on its
exact bytes are **NOT_RUN**. My strict overlay is bounded authored evidence on
the old package, not an acceptance of any candidate.

**Fleet bank (same commission, source-access update):** pinned at
`8523007613d411390a76683fa464002c0f25df83`; `START_HERE.md` and
`FORENSIC_RECOVERY/ANVIL_118_FORENSIC_AUDIT.md` read. The forensic audit is an
allegation tested against my own runs; it independently corroborates synthetic-
spine acceptance, the 118→decision gap, boundary demotion and the false R5 SPINE
prerequisite. Bank limits are exact: 299 manifest entries, 297 hash-match, 2
mismatch; 278/279 extracted ZIP text members exact, one CRLF→LF synthetic TSV.
The original ZIP SHA-256 remains byte authority and my `PACKAGE/` was not
overwritten.

**Probe-5 correction:** the earlier 000/111 illustration was false. The
replacement XOR witness (identical univariate and pairwise marginals, different
true 3-way joint, forward and reverse denominators) is computed in
`MUTATION_TESTS/probe5_witness.py` and logged in `PROBE5_WITNESS.log`.

**Probe-2 correction:** the earlier attribution to 4913 is withdrawn. Its exact
`FRAME.json` has 53 requirements, no disposition field, `architecture_selected=false`,
and its gate is RED only at `FRAME:HISTORY:NO_POINTER`; `00_RETURN.md` says no
decision exists. The surviving criticism is its false dependency on an
accepted R5/R6 SPINE.

## 6. Authority ceiling

No final C, no HQ accreditation, no protected H1, no source/scientific/actor
permission, no architecture selection. Earlier `4913b562...` is treated only as
an unaccepted challenge fixture. This is one complete initial return; no
peer-based acceptance and no sibling worktree inspection was performed.

**STOP.** Return to the one integrator for frozen A/B comparison.
