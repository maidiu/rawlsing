# Codex continuation instructions

This packet is designed to be copied into the worker branch:

`agent/vozhd-trii-hist01-original-ddm-authority-trace`

at exact start:

`299ef47a17fc96ea31589ea9e3c846e715e96d5d`

under:

`data/ddm_build_copy/vozhd_trii/20260820_pre553_empirical_compiler_activation/SUBSTRATE_RECONSTRUCTION/CONTROL_ROOM_AUTHORITY_PRESERVATION_AND_DEDUP/AUTHORITY_CENSUS_CAMPAIGN/returns/BROWSER/AUTHORITY_SUFFICIENCY_AND_QUALITY_REVALIDATION_CAMPAIGN/returns/HIST-01/`

Do **not** simply commit this packet as a completed HIST01 court. Finish the mechanical full-history
denominator first, then revise these files in place and seal only if §8 is satisfied.

## 1. Reproduce branch/root proof

```bash
git switch agent/vozhd-trii-hist01-original-ddm-authority-trace
test "$(git rev-parse HEAD)" = "299ef47a17fc96ea31589ea9e3c846e715e96d5d"

git rev-list --parents -n 1 a819fb35337ea28c4a83352d0040030b3da83a7a
git ls-tree -r --long a819fb35337ea28c4a83352d0040030b3da83a7a -- data/ddm_build_copy
```

Confirm `a819fb35337ea28c4a83352d0040030b3da83a7a` has no parent and replace/extend `ROOT_SNAPSHOT_MANIFEST.csv` with the **complete**
`git ls-tree` result. Classify every root object, not just the high-value subset in this handoff.

## 2. Exhaust producer ancestry

For every non-documentation root object:

- `git grep` actual reads/writes at the root.
- `git log --all --follow -- <path>`
- `git log --all -S'<literal path or authority id>' --source --decorate --date-order`
- trace inputs outside `data/ddm_build_copy`.
- explicitly distinguish:
  - versioned manual authority,
  - generated authority,
  - external/unversioned source,
  - source survey binary reference,
  - code constant,
  - environment/toolchain semantics,
  - unknown/unrecovered.

Priority unresolved objects already proved by this handoff:

1. `data/final_codebooks/questions_master_drivers.csv`
2. `data/final_codebooks/structural_registries/gss2010_structural_overlay.csv`
3. generated `data/ddm_build_copy/reports/*` overlays selected by family/wave filename precedence
4. root-era `DATABASE_URL` and exact live Postgres snapshot
5. exact joint-registry instances supplied to V550J/shared respondent substrate
6. execution-time `DDM_AUTHORITY_ROOT` / `RAWLSING_QUESTION_RELATION_AUTHORITY_PATH`
7. historical meaning/adoption of `COUNTRY_ALIASES = {"BF":"LS","LY":"YE"}`

## 3. Exhaust forward material mutations

Do not rely on the commit-message-only rows as proof. For each row in
`FORWARD_AUTHORITY_EVOLUTION_LEDGER.csv`, inspect the actual diff and predecessor/successor object.

Then mechanically discover additional material events:

```bash
git log --all --date-order --name-status -- data/ddm_build_copy section85
git log --all -S'DDM_AUTHORITY_ROOT' -- data/ddm_build_copy
git log --all -S'RAWLSING_QUESTION_RELATION_AUTHORITY_PATH' -- data/ddm_build_copy
git log --all -S'P3-AUTHORITY-2026-08-02-R184' -- data/ddm_build_copy section85
git log --all -S'question_structural_mapping' -- data/ddm_build_copy section85
git log --all -S'v550_shared_respondent_substrate' -- data/ddm_build_copy section85
git log --all -S'questions_master_drivers.csv' -- .
```

Trace adoption into Odin/Dva/Trii/Chetiri by **consumer evidence**, not names alone.

## 4. Exhaust the consumer denominator

Build the set of every reachable executable/script/build/replay/analysis/runtime consumer.
For each revision where dependency semantics change, record:

- exact path/function;
- exact commit/range;
- imported/read/query object;
- exact fields/keys where recoverable;
- direct/transitive/default/environment-mediated mode;
- supersession;
- terminal meaning.

Specifically search for hidden authority through:

- sorted/globbed file order;
- first/last row wins;
- default fallback names;
- nullable coercion;
- numeric-code ordering;
- dataframe/decoder behavior;
- environment/package versions;
- generated ID derivation;
- compatibility aliases;
- copied/generated products later treated as inputs.

## 5. Re-adjudicate the 68-TIR crosswalk last

The current handoff found **no proved new terminal information class** but several unrecovered exact
historical objects. Do not convert that provisional result into closure until the historical DAG is
complete.

A new TIR is warranted only for a historically consumed terminal distinction that cannot be
faithfully represented by any existing TIR. If found, emit it individually as:

`HISTORICAL_AUTHORITY_FOUND__TERMINAL_INFORMATION_NOT_YET_ACCOUNTED`

Do not shoehorn it.

## 6. Required final condition

Only mark HIST01 closed when:

- complete root manifest exists;
- every non-doc root object classified;
- every generated root object has producer/input or unresolved disposition;
- every material forward mutation is recorded;
- every reachable historical consumer dependency is enumerated;
- every dependency maps to an authority object or explicit missing object;
- every authority maps to current TIR/succession/dead legacy/orphan/unresolved;
- no unaccounted reachable consumer edge remains.

If any one fails, final status must remain non-closure.
