# FIABC-W3-I04 — Runtime Packaging Rebind

Worker: `FIABC-W3-I04`

Repository: `maidiu/rawlsing`

Branch: `agent/rabochii-premain-fiabc-w3-i04-runtime-packaging-rebind-r1`

Base: `56697a27e94eb9603dfa412a15ab8f1feb819b0c`

Return: `WORKER_RETURNS/FIABC-W3-I04/`

## Holding

The four Wave-2 B04 packaging debts IMP06-IMP09 are implemented as bounded packaging/reference repairs. No semantic owner, candidate definition, authority root, replay root, negative-state law, or measured P2X state is changed.

The present executable call surface identified by B04 is the audited P2X backend at `617c9c9426db12a3c0f7fea6b68a582c10759553:rawlsing_next/ee_p2x_darwin_stage_backend.py`. That audited surface is not present on the Wave-2 HQ fan-in base, so this worker selectively fans in that exact backend and changes only its three R6S runtime locators.

A hostile normalization check proves that replacing the three new stable locators with their audited worker-return locator strings reconstructs the audited backend byte-for-byte. Audited backend blob: `b223d309b5f5fa45389badec719ce2882e672cca`. Rebound backend blob: `b0115ceffe7203c29646faffcbc5adfcfa373488`.

## Implemented repairs

### PKG-001 / IMP06 — LiTS R6S runtime materializer

The exact qualified materializer bytes are now bound at:

`rawlsing_next/runtime/ee_p2x/01_LITS_CURRENT_RUNTIME_MATERIALIZER.py`

Git blob remains exactly:

`9406bacfd928393f6a159a46216aa1f7ec129f34`

The stable path deliberately preserves the original path depth required by the materializer's `Path(__file__).resolve().parents[3]` repo-root calculation.

The backend now resolves `R6S_LITS_SUPPORT` to this stable current runtime path.

### PKG-002 / IMP07 — exact accepted Node4A carrier fan-in

The exact accepted R6O carrier was fanned in unchanged at the path already required and hash-checked by the preserved LiTS materializer:

`WORKER_RETURNS/EE-P2R6O/SUPPORT/01_NODE4A_PREDICATE_INPUTS.py`

Git blob:

`504944f9533b7385d201076e2e834b8a9446dee8`

No predicate reconstruction or current-tree substitution was performed.

### PKG-003 / IMP08 — WVS7 runtime package

The exact derivative R6S/P2F2 runtime package bytes are now bound at:

`rawlsing_next/runtime/ee_p2x/02_WVS7_P2F2_RUNTIME_PACKAGE.json`

Git blob remains exactly:

`e04e84b76f8b4eb53905276dd025938bf2e5f6fe`

The backend now resolves `R6S_RUNTIME_PACKAGE` to this stable current runtime path. Lock2, discovery authority, counts, refs, and package contents are unchanged.

### PKG-004 / IMP09 — WVS7 projection materializer

The exact qualified R6S WVS7 projection materializer bytes are now bound at:

`rawlsing_next/runtime/ee_p2x/05_WVS7_PROJECTION_MATERIALIZER.py`

Git blob remains exactly:

`11b28416aac5a4899706150721f2f8ac8bb6ee43`

The backend now resolves `R6S_MATERIALIZER` to this stable current runtime path. Projection identity and coordinate/source authority logic are unchanged.

## Identity / ownership guard

`rawlsing_next/runtime/ee_p2x/RUNTIME_PACKAGING_BINDING.json` records the exact source roots, Git blob identities, preserved runtime identities, and frozen candidate-owner identities.

Preserved identities include:

- LiTS runtime catalog `5983d7d5c579b916ad46c1acf9e41c1c89b516a4e561a99b1d2b477bf5ad2d02`
- LiTS active binding `a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308`
- LiTS runtime release `192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f`
- WVS Lock2 `8e5842eb01100e0b23c3fa0fe85736fee081d759ec5458fc0f95c307024c6188`
- WVS projection `838070ff6b85d60d4f26f9153b0507ba425936c11a3de94a18d57bfcd083f24d`
- P2R1 seam blob `e7cda773e6a2426bfa12b22790fd8e005fe75153`
- frozen A/B/C owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6` and exact owner blobs.

The current-tree Candidate-B facade is intentionally not treated as the frozen B owner.

## Tests added

`rawlsing_next/tests/test_fiabc_w3_i04_runtime_packaging_rebind.py`

It fails on:

- wrong Git blob for any rebound runtime asset;
- absent or wrong-hash Node4A carrier;
- wrong LiTS Node4A dependency path/hash;
- incorrect stable backend locator;
- any surviving direct R6S worker-return runtime locator in the backend;
- drift in R6O runtime catalog/binding/release, WVS Lock2, or WVS projection identities;
- silent replacement of frozen candidate-owner identity with the current-tree lookalike;
- packaging manifest claiming semantic-owner movement or measured-execution authorization.

## Browser/GitHub verification performed

Repository-object verification, without local execution, proved:

- LiTS materializer rebound bytes == audited R6S bytes;
- WVS runtime package rebound bytes == audited R6S bytes;
- WVS projection materializer rebound bytes == audited R6S bytes;
- Node4A fanned bytes == accepted R6O bytes;
- rebound backend, after reversing exactly three locator substitutions, == audited backend bytes.

No measured P2X work was performed.

## Tests not executed here

The Python test file and compile checks were not executed because this commission is GitHub/browser-only and prohibits local execution. The Wave-2 fan-in base also does not itself contain the full audited P2X/P2R1 runtime lineage, so live backend consumption is an integration/local qualification burden, not evidence that these packaging identities changed.

Exact later commands are recorded in `02_TESTS_AND_COMMANDS.md`.

## Exact blockers

None inside the bounded packaging repair.

A post-fan-in live-consumption receipt remains outside this worker's authority and must be established by the integrated qualification/local execution sequence.

## Terminal

`FIABC_W3_I04_RUNTIME_PACKAGING_REBOUND__IDENTITIES_PRESERVED__READY_FOR_FANIN`
