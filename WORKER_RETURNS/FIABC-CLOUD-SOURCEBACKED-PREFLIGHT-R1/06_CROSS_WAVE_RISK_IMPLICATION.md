# Cross-Wave Risk Implication

## LiTS-I-specific

The following are specific to the current LiTS-I successor:

- exact source SHA `7cac43e2...`;
- the DTA latin1 compatibility decode;
- `q301_2`/194 and `q301_7`/199;
- decoder float64 values 1.0–7.0;
- the bounded float64 → Decimal-string transport authority;
- the five current coordinate slots country/98, city/104, region/107, tablec/1117, tabled/1118;
- the exact accepted legacy C11 release/replay identities;
- the explicit current→legacy key rebound introduced at code head `ea0baa4d...`.

None of those facts may be projected onto another wave merely because it is also LiTS.

## LiTS-family-specific

The current generic decoder carries exact-SHA latin1 compatibility entries for all four LiTS DTA snapshots. That is a **physical reader configuration**, not intended-text or semantic authority.

Therefore the LiTS family shares exposure to DTA/pyreadstat representation details and compatibility decoding, but the LiTS-I q301 representation bridge is not family authority.

## Historical-replay-specific

The important architectural risk is dynamic loading of one historical file while its absolute imports resolve against the live `rawlsing_next` namespace.

Current backend pattern:

- `_deploy(... historical commit/path ...)`
- `_load(...)`
- `spec_from_file_location(...)`
- historical source executes `from rawlsing_next... import ...`

That does **not** constitute a historical dependency closure.

The legacy LiTS facade currently survives the key-law audit because its critical `pre553_empirical_objects.py` dependency is byte-identical between owner commit and current head, while the relevant missing-state enum text is unchanged. Other imported modules have changed and therefore still require runtime provenance/output closure.

The banked projection builder is a deliberate hybrid under the current successor: its historical file imports the current typed facade, which creates current R5 rule keys; the latest repair then performs an explicit bounded current-key → legacy-owner-key rebound.

## Generic risk for any old projection imported into current PRE553/R5

The LiTS failure class is generic whenever all three conditions hold:

1. a projection/rule set was produced under physical-key law A;
2. a current source cell or transport adapter is keyed under law B;
3. equality is attempted without an explicit, bounded A↔B successor authority.

The same risk exists when a historical file is dynamically loaded but one of its key-producing/hash-producing dependencies silently resolves to a changed current module.

An unchanged high-level projection/cache identity does not prove physical-key parity when that identity omits the individual physical rule keys. The old LiTS `cache_identity` is exactly such a warning: it hashes contract/projection/source/authority identity, not every response physical key.

## Impossible for waves using only current hermetic generic code

This **specific old-owner/current-R5 mismatch** is impossible when:

- source cells and rule keys are both produced by the same current `PRE553_PHYSICAL_VALUE_BINDING@2.0.0` + `PRE553_R5_TYPED_VALUE_CODEC@1.0.0`;
- no historical module is dynamically loaded;
- no persisted physical keys from an older law are replayed;
- dependency versions used for key construction are hermetically pinned together.

That does not make all representation defects impossible; it removes this cross-generation key-law class.

## Exact CLOSED35 search patterns

Search every wave/source path for:

- `_deploy(` or `git show <old-commit>:<path>` followed by dynamic import;
- `importlib.util.spec_from_file_location` applied to historical code;
- historical files containing absolute `from rawlsing_next...` imports;
- `sys.path` mutation inside deployed historical modules;
- physical keys persisted or compared across `PRE553_PHYSICAL_VALUE_BINDING` versions;
- `physical_value_binding_key` created in one module generation and consumed by another;
- old `semantic_hash(canonicalize(...))` physical keys beside current R5 typed keys;
- `Decimal(str(value))`, float→Decimal adapters, int/float/Decimal normalization, or any type-changing transport seam;
- projection/cache identities that do not include physical rule-key sets;
- historical replay files whose transitive dependency blobs are not pinned;
- tests that mock the historical owner instead of loading it with actual import provenance;
- exact output checks that occur only after a non-hermetic historical computation but lack import-origin receipts.

For every hit, CLOSED35 should either prove all participating historical dependency blobs are identical, pin/deploy the dependency closure hermetically, or mint an explicit source-bounded successor authority with fail-closed hostile tests.

No survey-value inference is needed for this search.
