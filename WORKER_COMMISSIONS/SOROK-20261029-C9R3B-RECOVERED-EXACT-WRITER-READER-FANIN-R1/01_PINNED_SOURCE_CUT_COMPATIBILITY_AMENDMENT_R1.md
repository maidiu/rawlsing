# Binding scientific/engineering compatibility amendment to C9R3B-FANIN-R1

**STATUS:** UNLAUNCHED / user-selected worker+incumbent source-scope check pending. Original 00_COMMISSION remains binding; this amendment adds actual sourcebound execution evidence learned later and prevents redundant recovery.

## Already completed by independent PRE-MAIN-based recovery PR #514

Staging branch `integration/staging-sorok-c9r3b-sourcefree-recovery-20261028-r1` (inspect CURRENT HEAD at dispatch) now physically includes C9 R3B writer and matching verified reader. The original actor writer, schemas and reader source code remain byte-exact to their author commits. A historical migration test inert self-comparison was repaired with live source-swap and no-binding proof; original C9 writer test now permits selecting exact S36 and JOIN-E source roots with environment variables instead of hardcoded Mac paths.

**Actual passed GitHub Actions court** [#40798932389](https://github.com/maidiu/rawlsing/actions/runs/40798932389), head `3eb4aeeab5c9a91d644449026b509169160f9b81`:
- 15/15 author original C9 tests, zero skips, with S36 at `8da78d8031a06a4bd7e1297fd713e573299c0860` and **writer-era** JOIN-E `7bf2da302996491ddf34b9a039fea47ac982d135`.
- 12/12 C9 reader fork/cold source tests, with **reader-repaired** JOIN-E `68b058656254234f0af02df2a592aa6f8c6a8bd2`, plus all four SHA256 C12 import pins MATCH.
- Earlier 40 sourcefree actor/dry/migration tests with one historical V3 BackboneState Mac-only source test still unexecuted. Do not claim 100% original V3 coverage.

## Competing C12 cuts and specific reproduced RED — your major new issue

Using writer-era `7bf2da3...` in the later reader returns `C12_SOURCE_CHANGED_BEFORE_IMPORT` on all 12 fork cases (run #40798650310). Correct security denial, not a sourcefree engine bug. Using later repaired C12 `68b0586...` in the historical writer 15-case suite makes `test_c6_same_count_perception_substitution_is_held` RED: `len(perceptions(root))==len(perceptions(child))` is 2 vs 3 at run #40798810264 (14 PASS / 1 FAIL). **Do not delete that historical oracle or silently rewrite its expected equality**. A fork-perception prefix/suffix semantic change is likely, but the exact owner-authorized meaning and selected current writer fork guard must be adjudicated against actual code and original C12 owner contracts.

The worker's parent goal is a **single selected exact C12/world/actor cut** with one sourcefree real later-performed E2 reader/consumer and cold/fork consistency, rather than separately green author-era tests. First compare the old and repaired C12 `store.py` and `c12_integrity.py` by exact source diff; derive which semantics are intended and which C9 test expectation must be version-conditioned, with a new *positive and negative* test proving no leaking parent suffix. Only the rightful C12 actor/store owners may choose canonical fork semantics. The existing R3 reader already consumes repaired C12 and demonstrably passes its 12 sourcebound fork tests: reuse that path, not a third store.

**Separate original-source HOLD**: the legacy migration V3 `BackboneState` test expects local `v3/core/state.py` SHA256 `19e968d45e9d81eb7629f1c237dbc55119fec8fc7db0b29e2b39b2476d12ada2`, not in current sourcefree CI checkout. No skip-as-pass. Current author/programmatic code import/native/science claims remain held, notwithstanding 15+12 PASS.

**Governed CI qualification**: earlier global FIABC/LITS court had 144 PASS/3 FAIL in untouched `rawlsing_next` files at PR HEAD; the `.github/workflows/sorok-c9r3b-premain-fiabc-baseline-control.yml` comparison is being added to prove whether the exact same three failures occur on frozen PRE-MAIN. Never modify oracles or the global court spec merely to make C9 green. The narrow C9 courts are separate and do not supersede original scientific gates.

## Worker redirection of effort

DO NOT re-stage the 17 original source files, rerun obsolete four-skipped court as though still blocked, create a new C9 store, rebuild B3A repair, or claim the two valid C12 branch checks form a single native adoption. DO concentrate S2 on resolving one C12 source cut under owner decision, exact selected C9→C12 reader, performed E2 same-consumer new behavior with source-fault, and independent I2 review. Original Rule A/T/ADP/SCI05/Pyat N11/N12 source permissions remain held.

If worker cannot lawfully decide C12 fork semantics, stop with precise `C12_SOURCE_CUT_OWNER_SELECTION_HOLD` and a minimal separate request to the rightful owner, while finishing independent C9 parts not dependent on that decision. No unapproved code/command/host model switch. Preserve distinct tests and exact sha, return after actual execution, not a proposed architecture alone.
