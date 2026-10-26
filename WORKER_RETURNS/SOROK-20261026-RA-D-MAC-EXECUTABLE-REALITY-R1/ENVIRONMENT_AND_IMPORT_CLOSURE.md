# RA-D environment and import closure

**Scope:** sourcefree local execution of the exact S39–S52 closure, G18, JOIN-E, language mediation and S50 recovered V3/PFF. No provider call, raw data, production edit or native grant.

## 1. Local environment

| Item | Observed |
|---|---|
| Host | macOS 13.7.8 (Darwin 22.6.0, x86_64 Intel Mac) |
| Python | `3.11.3` at `/usr/local/bin/python3` |
| pytest | `9.1.1` |
| numpy | `2.4.6` |
| PyYAML | absent (`ModuleNotFoundError`); S50 uses its own `yaml_compat` |
| Git | `2.39.1` |
| GitHub CLI | not installed; private Git access through the existing clone + osxkeychain |
| Isolated worktree | `<RA_D_WORKTREE>` (outside active worker worktrees) |
| Assigned branch | `agent/rabochii-sorok-20261026-ra-d-mac-executable-reality-r1` |
| HEAD at verification | `9c356a0189234f50cb07813eebbd68e4dc2d3740` |
| Remote branch at start and before push | `9c356a0189234f50cb07813eebbd68e4dc2d3740` (no movement) |
| Sealed commission blob | `e72b26e6f5d4a86b30ab6152bce5268cf1ec34a2a762010edcc57210bfb7fff9` |
| Provider calls | 0 |
| Accepted-source edits | 0 |

Isolation: the worktree was created from the sealed commit in a disposable scratch location. The S52/S50 source trees were extracted with `git archive` into `<RA_D_RETURN>/TEST_SOURCE_AND_LOGS/isolated_archive_s52c821` and executed there. No active author worktree, production branch, PRE-MAIN, Pyat or HQ branch was mutated. The archive and runtime state were deleted after execution; only scripts, sanitized logs and hashes are committed.

## 2. Exact source cuts

| Source | Commit | Role |
|---|---|---|
| S52 paid-activity repertoire | `c821b488b3a9a3f0fa01b1981989cc17af637dc1` | Actual S52 cut; 183 `.py` files extracted; archive matches commit exactly |
| S51 situated object relevance | `2a4cdd2d6dd26254b0c3a123c94024c0c0a06a65` | Accepted component; S52 cut modifies one file |
| S50 historical V3 actor recovery | `515b9a8ee45672c97051df4efef679117a679525` | Extracted separately; matches commit |
| S49 independent actor producer | `6604f2d9ebeca47ab58c5e1f5fee1e6a34b1bb43` | Accepted cut; S52 cut modifies two files |
| S48 one-call continuing turn | `9fe0d066e4bf61ab6819a1f56e42d6d07956c2f7` | One-event transport; no batch |
| S47 interval C9 conditioning | `765a441f87292aa4c17794745b65cb54e6aaa83f` | Objective conditioning |
| S46 interval participation | `f0ef39b92ce2e4add5c0a699389e12f1d7ae434e` | Objective interval producer |
| S45 generated root encounter | `f26a138e20d53c809d611cf8d834ec647b0804bf` | Generated root + user encounter |
| S44 sampled root consumer | `923278fbe6b030e2ffdd10fe42d7a18266344611` | Generated A/B root and ledgers |
| S39 generated response | `e41513fa65601a37e7b3b430d26c626ae0217d90` | Accepted cut; S52 cut modifies `model.py` |
| S37 integrated consumer | `e1f3c1daef6e37fb93ddc04f25f2b8fffa6943f9` | Accepted cut; S52 cut modifies `producer.py` |
| S36 actor access response | `8da78d8031a06a4bd7e1297fd713e573299c0860` | Imported S36 candidate |
| G18 `lab_sgi1` | R31J `64fec28c374d8f77fb0b412d0c934d798ede03e8` | Historical actor/world source |
| JOIN-E `joined` | `7bf2da302996491ddf34b9a039fea47ac982d135` | Same-person joined session |
| Language mediation | `8d2920da951f98cd8246d7c34cac777928e0c732` | Native/translation artifacts |
| M35 vendored producer | `4170fbf19a9d5a64bc728f5b22156bbffcec51e5` (declared cut) | Vendored under S37 `vendor/m35`; test-only CAN008/CAN011 ports |

## 3. Imported module origins

Full `__file__` and SHA-256 data is in `TEST_SOURCE_AND_LOGS/import_manifest.json`. The important origins:

| Module | Imported from | SHA-256 |
|---|---|---|
| `s39.model` | S52 cut, `S39…/s39/model.py` | `6afba4b77b71c40654986fed4eda40915c7a0cc454e07d8293e353f135f1c603` |
| `s39.sources` | S52 cut, `S39…/s39/sources.py` | `cddd0ecfa2cc35affc10d3d3bee51bfc280bf2949a5850e0a8963ba5ac93a7d5` |
| `s49.actor` | S52 cut, `S49…/s49/actor.py` | `c2a889c825807c174cdc91ce4ec08cde07c2e6e0575fadf9ee97185324c5eb95` |
| `s49.session` | S52 cut, `S49…/s49/session.py` | `9932029c529a399ffedb24545ea5d0f6884a5fe8719ffc39c8af9fe1db0f3625` |
| `s51.session` | S52 cut, `S51…/s51/session.py` | `6ef8e92eb3ea2d83cfdb5aba1121ed42f1706a0df9bc3f36aff2b91a47596a82` |
| `s52.session` | S52 cut, `S52…/s52/session.py` | `3ed6dadf2c809a0f6e2d4094c41e34be3e51b4a984a219898e20f6a7b299e32e` |
| `s52.performer` | S52 cut, `S52…/s52/performer.py` | `ff12b71743f421b7f14ff51ae34e4f01cc0cae296bfbebda2fba91942aae8a14` |
| `lab_sgi1.history` | G18, `…/lab_sgi1/history.py` | `2d861d7a820168d443e23efb2403b7ed9c3e899a8a79aaa72fd859c46f47c1c1` |
| `joined.session` | JOIN-E, `joined/session.py` | `ea820ec3e30a2825c3d0d8c5dc66e812afdda40b08f9cc0a8c868c8b3e0dd0da` |
| `language_mediation.session` | language root, `language_mediation/session.py` | `d6a1628cbfdc1c601f68fb3d3b9adbe91f9464875996b543caf69e548ece25aa` |
| `candidate` | S52 cut, `S36…/candidate/__init__.py` | `f176282b70d4c1c21831ab3d664a82919c5ea9583c425d527ee584c45be0cd3f` |
| `bp4.world` | JOIN-E `vendor/j/.../bp4/world.py` | `848bb6d3e3e0375a11077a3cf6984509366863e81e9deb212fd30d7878782ddd` |
| `bp1.composer` | G18 R31J vendored `bp1/composer.py` | `358a3c6e2f187e21618ed56af17025e80d5153d29af003dcd9e8df9393b63c88` |

The probe imported `s52.bootstrap` first, so the S52 cut's ancestor copies are the loaded modules. It did not substitute the accepted ancestor returns.

## 4. Exact external source checks

| Source | Git identity | Working-tree hash | Result |
|---|---|---|---|
| G18 `history.py` | R31J `64fec28c…`: blob `d6674481…` | `2d861d7a…` | exact |
| G18 `joint.py` | R31J `64fec28c…` | `755820d7…` | exact |
| JOIN-E `joined/session.py` | `7bf2da302…`: blob `dc089428…` | `ea820ec3…` | exact |
| Language `language_mediation/session.py` | `8d2920da…`: blob `4f2cdc62…` | `d6a1628c…` | exact |
| S50 V3 selected source files | 31 identities | `source_all_exact:true` | exact |
| S52-commit subtree | S52 commit | 183 `.py` files | exact (S50 separately extracted and exact) |

The G18 and JOIN-E working trees contain untracked `__pycache__` and `.DS_Store` files from prior use; the tracked source files match their declared Git blobs. No source was modified.

## 5. Missing or blocked sources

**None for the executed S52/S39/S44/S45/S46–S52 closure.** The hard-coded Mac roots required by `s37/bootstrap.py` and `s51/bootstrap.py` are present and matched:

- G18: `<G18_SOURCE_ROOT>`
- JOIN-E: `<JOIN_E_SOURCE_ROOT>`
- Language mediation: `<LANGUAGE_SOURCE_ROOT>`
- S50 V3 source: `<V3_SOURCE_ROOT>` and its 31-file identity document.

**S50 is deliberately not wired to the S52 actor.** Its actual-root probe returns `SOURCE_OWNER_HOLD` and lists the missing current-person fields. This is not an import failure; it is an explicit missing-owner/wiring boundary.

**M35** is a vendored read-only test surface under S37; its declared cut is `4170fbf…`. No separate production M35 owner or native grant was accessed. Its CAN008/CAN011 resources are `TEST_ONLY` and are not native rules.

## 6. Source-cut integrity warning

The S52 cut modifies five ancestor files relative to their accepted cuts (see `00_RETURN.md` §3 and `TEST_SOURCE_AND_LOGS/source_blob_comparison.json`). The modified files are imported and executed; therefore:

- an accepted S39 `model.py` claim is **not** the S52 behavior;
- an accepted S49/S51 claim is **not** the S52 behavior without the repertoire/source-override deltas;
- the S52 paid option exists only because of those edits;
- no claim in this return is based on the accepted ancestor blobs.

## 7. Sanitization and retention

Committed logs replace user-home, worktree, scratch, G18/JOIN-E and language roots with placeholders. Raw scratch copies are not committed. The source archive is removed after execution. The committed JSON/scripts preserve source SHAs, module origins, commands, exit codes and observed values needed for independent replay.
