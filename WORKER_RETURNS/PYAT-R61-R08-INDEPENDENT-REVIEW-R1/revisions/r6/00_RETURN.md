# R61-R08V R6 independent review — return

Verdict: **REVISE.** R6 closes the two exact R5 defects at the tested served-
value/provenance/export-object grain: the signed original provenance/mode are
served, the unsigned `cache_trust_grade` is gone, export refuses mutated
evidence/query/rule objects, and verifier-only re-export/import/read round-trips
at 60. Genuine native positives, changed case, cold replay and the main refusal
controls remain live.

One public cache/re-export path still carries unsigned producer-binding metadata
that is not authenticated against the signed owner identity material. A
manipulated cache can change `producer_binding.producer_query_ref` (and the
producer admission token), recompute the public entry seal, import into a
verifier-only resolver, re-export, and import/read again at 60 while the
exported binding record says the forged producer query. The signed envelope and
served measurement values remain canonical; the defect is the unauthenticated
cache/export binding record, not a wrong 54/6/60 value.

## Custody actually checked

- Exact root/worktree: `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/r61-r08v-r4`
  (folder suffix historical; no alternate worktree).
- Branch: `agent/opencode-pyat-r61-r08v-r6-independent-review-r1`; preflight
  `pwd`/toplevel/branch/status matched and the tree was clean.
- Candidate/startup: `d8a7b4005d23a1e39b35360ca96bf2aef5b9e591`.
- R6 code commit: `7450b4f389e4a95a85066065dec7acafe83da84d`.
- Module blob `ad165eba9d04644f4b5ab34cd9e52ea1cf9b0ebe`; test blob
  `576142c525e140fdfcd34af3949b5bf68ff2386f` (working tree matches).
- Precode amendment: `b9076985ec3be2ead1c47a2f754a52f774dfca59`;
  amendment blob `93589a1d9c04bf87dddba5a8767a5c195fe1464e`.
- Frozen R6 EXPECTATIONS:
  `57ce687fefca959fa736abeb822a87c3060521d9`, committed before reading R6
  candidate code or author conclusions.
- Prior R5 review `4a5d9a9f8d700cbc5e692401220623df1122e22b` and R4 review
  `d1baa92cb457c30bf6dffb91f23f8cee351de4f6` preserved on their old branches;
  their probes were replayed from exact copies
  (`r5_immutable_probe.py` blob `0f33dfd0...`, `r4_immutable_probe.py` blob
  `80b89a71...`) and no archived original was edited.
- Candidate delta from `6abd49f` is exactly the two allowlisted code/test paths
  plus the seven author R6 artifacts; the amendment commit adds only its
  amendment file. No native owner/evaluator/archived/HQ/workflow path changed.
- Author R6 manifest independently recomputed: all six listed artifacts match
  byte-for-byte; `manifest.json` is explicitly self-excluded.
- Native owner blobs independently re-hashed and unchanged:
  provider `23167aa2...`, composition `604c8d59...`, positioned evaluator
  `62e5eced...`, empirical objects `a61365b9...`, AT07/n10e fixture
  `0e384f72...`.
- Direct remote readback at start: `origin` R6 branch was at candidate
  `d8a7b4005d23a1e39b35360ca96bf2aef5b9e591`.

## What R6 actually fixes

- **Signed original execution:** envelope @2 signs
  `execution_provenance=CANONICAL_PRODUCER` and
  `execution_mode=LIVE_TRUSTED_EXECUTION`; `read`/`e04_step` return the signed
  original fields. No `cache_trust_grade` is derived from unsigned
  `EvidenceResult.provenance`. A canonical result mutated to
  `AUTHENTICATED_CACHE` still serves signed original canonical/live and an
  explicitly unsigned local `VERIFIED_REPLAY` label; a cache result mutated to
  `CANONICAL_PRODUCER` still serves signed original canonical/live.
- **Export objects:** export now applies `_objects_match_envelope`; mutated
  evidence geometry, query projection and substituted rule are refused by the
  reader/export; restoring each object restores a successful export and read at
  60.
- **Verifier-only re-export:** import/read/re-export/second import/read all
  return 60, preserve the original envelope signature and signed original
  provenance. The previous "cache entry lacks its admitted owner binding"
  refusal is gone.
- **Positives:** independent fixture-table counts 54/6/60 and changed 54/16/70;
  cold fresh process 60 and same consumer hash; observed-zero/status/currentness/
  Z UNRESOLVED controls retained.
- Author suite replay: 38/38. R5 probe replay: 6 pass, 2 fail; both failures are
  superseded old expectations (removed unsigned `cache_trust_grade`; old probe
  asserts import refusal after export already refused). R4 probe replay: 7 pass,
  2 fail with lawful `EvidenceAssociationError`; no TypeError/import/setup
  failure counted as safety.

## Remaining defect

### R6-D2/D5-01 — cache producer-binding metadata is not authenticated

Location: `EvidenceResolver.import_authenticated_cache` and
`EvidenceResolver.export_cache` (`pre553_universal_evidence_binding.py`).
Import checks `owner_identity_material` hash against the signed envelope, the
context labels/refs, and `validated_conditions`, but it does **not** compare the
duplicated top-level `producer_binding` fields (`producer_query_ref`,
`predicate_ref`/`predicate_hash`, `release_refs`, `consumer_query_ref`,
`model_rule_hash`, `source_universe_ref`, `risk_set_ref`, `target_ref`,
`context_ref`/`context`, `actual_conditions`,
`consumer_binding_fingerprint`) to `owner_identity_material`, and it does not
verify the producer admission token. `export_cache` rebuilds
`owner_identity_material` from retained material but copies the rest of the
raw binding payload, so altered metadata is re-exported.

Independent reproducer (`outcomes/r6_observations.json`, key
`producer_binding_metadata_mutation`):

1. Produce/export a legitimate cache; deep-copy one entry.
2. Replace `producer_binding.producer_query_ref` with a forged exact ref;
   recompute `binding_hash` and the public entry `seal`.
3. `EvidenceResolver(admission_verifier=<configured verifier>).import_authenticated_cache(...)`
   accepts; `resolve` returns 60.
4. `export_cache()` re-exports the forged `producer_query_ref`; a second
   verifier-only resolver imports and reads 60.
5. Replacing the producer admission token with `"0"*64` is likewise accepted on
   import.

Observed values:

```json
{
  "altered_producer_query_import_accepted": true,
  "reexported_producer_query_ref": {
    "kind": "FORGED_PRODUCER_QUERY",
    "object_id": "urn:forged:producer-query"
  },
  "second_import_denominator": 60,
  "altered_admission_token_import_accepted": true
}
```

The signed envelope's owner identity material and the served 54/6/60 values are
still canonical; the cache/export binding record is not. This violates the R6
requirement that every exposed cache/export value derive from authenticated
retained material (D2/D5) and that unsigned metadata not leak through export.

Minimal missing function: at import, require the duplicated producer-binding
fields to equal the signed `owner_identity_material` (or reconstruct them from
it), and verify the producer admission token against the configured verifier /
owner material or drop it; at export, rebuild the producer-binding payload from
the authenticated owner identity material and request/conditions, refusing if
the retained binding record is inconsistent. No new crypto/service.

## Limits and observations

- The `local_delivery_context_unsigned` label is derived from unsigned
  `EvidenceResult.provenance`; a cache result mutated to `CANONICAL_PRODUCER`
  reports local `LIVE_TRUSTED_EXECUTION`. It is explicitly unsigned, the signed
  original provenance/mode remain canonical/live, and no `cache_trust_grade` is
  served. It is recorded but not scored as a separate served-trust defect.
- Verifier-only re-export without the original ephemeral `cache_issuer` drops
  the optional `issuer_grade`/`issuer_seal` cache label; the original envelope
  signature, signed projection and 60 result are preserved. This is a local
  cache-label downgrade, not a grade upgrade or served-value change.
- The author R6 export-object test restores the mutated evidence cell to 60
  rather than its original 6, so its query-mutation refusal is not isolated.
  The independent probe mutates/restores evidence and query separately and
  confirms both are refused and the restored export succeeds. Author 38/38 is
  regression evidence, not independent qualification.
- Full live J42/P41/E04 integration remains NOT_REACHED. R01 High adjudication is
  separate and was not inspected or decided. No source/science/prod/CI/N11/N12/
  Sorok/J52/W52/R03/R09 authority or candidate edit/adoption/self-repair.

Artifacts: `EXPECTATIONS.md` (frozen), `defects.md`, `limits.md`, `RESUME.md`,
`FACILITY_HISTORY.md`, `proof_witness.json`, `SHA256manifest.json`,
`outcomes/r6_observations.json`, `outcomes/r4_probe_replay_observations.json`,
`outcomes/r5_probe_replay_observations.json`,
`probes/test_r08v_r6_independent_boundary.py`,
`probes/r4_immutable_probe.py`, `probes/r5_immutable_probe.py`,
`junit/*.xml`, `logs/stdout.jsonl`.
