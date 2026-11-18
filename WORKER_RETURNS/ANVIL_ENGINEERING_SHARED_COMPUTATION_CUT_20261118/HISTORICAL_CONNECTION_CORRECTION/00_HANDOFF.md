# Historical → current shared computation connection

## Verdict

**Comparison complete. The prior three-file grouped patch remains a narrow optional proposal, not the historical sharing mechanism. No production change.**

- Current integrated HEAD: `7f0366de3ee83b90b9607e278193bd08c4478213`
- Integrated code/test: `68aa7cac7cce7057fefd458ef4a06bec2dede1b2`
- Product change in this correction: **none**
- Prototype reruns/benchmarks: **none**
- Machine account: `historical_connection.json`

## Old pipeline — actual shared preparation

Source checkpoint: archived `babb256ca43e887ab1519339108ae3a29c1928f4` (“Implement V550 shared respondent substrate bridge”), plus the frozen `Rawlsing_V550_Fused_GSS_Proof_babb256_20260803` artifact.

1. `build_determinicity_repository_v550.py`
   - `_prefetch_question_rows_by_country` (708–784) queries PostgreSQL
     `v_ddm_response_long_facet_ready` per source/wave/country and keeps one
     country frame in `question_row_cache`.
   - `_prepare_v550_question_row_cache` (787–825) harmonizes that country
     cache **once** in `country` mode.
2. `build_determinicity_wave_shard_v550.py`
   - selects the union of base + joint questions (1328–1353);
   - prefetches/harmonizes once (1380–1389);
   - writes the canonical shared substrate for each country (1391–1445).
3. `ddm_v550_shared_respondent_substrate.py`
   - schema has a wide respondent×variable prepared row set with 68 required
     columns (25–105);
   - canonicalization explicitly says it is “without reharmonizing rows”
     (332–346);
   - writes atomically with content hash, schema, manifest, validation and
     `COMPLETE` marker (565–637);
   - loads with exact parquet/manifest/validation checks (640–655).
4. `build_v550j_prepared_substrate.py` (316–374, 408–416)
   - has a per-source/wave/country prepared cache keyed by authority/schema
     signatures;
   - harmonizes once before writing, then loads without reharmonization.
5. `compile_v550j_joint_response_patterns.py`
   - `--forbid-database-access` requires `prepared_required` and the exact
     prepared path/manifest (1214–1236);
   - multiple family products load the same prepared country frame
     (1690–1725, 1750–1759).

Concrete archived artifact: `Rawlsing_V550_Fused_GSS_Proof_babb256_20260803/evidence/shard_manifest.json`

- shared substrate mode `write`, row count **25,067**, content hash
  `e58a7087…` (90–101);
- 22 V550 output artifacts listed (56–81), including distributions,
  position/indicator summaries, outlier cohorts, branch nodes, clouds and
  audits.

### What was shared

The expensive preparation was **population/respondent harmonization and
question-row preparation per country**, persisted as a reusable wide
respondent×variable substrate. Multiple V550 products and V550J family
products could consume the same prepared population/input without repeating
the harmonization/join path. PostgreSQL was the extraction dependency; the
prepared substrate itself was file-based and explicitly DB-free.

## Current implementation — what already exists

| Current surface | What it provides | Limitation |
|---|---|---|
| `DirectEstateI03Session` (`pre553_direct_estate_i03.py` 112–190) | Canonical 13-family Parquet estate; temporary SQLite posting index | No wide country respondent×variable substrate |
| `_respondent_family` (398–449) | Physical `gid/off` traversal, canonical refs, bounded respondent/family materialization, CURRENT before every yield | Still per-query routing/object materialization |
| `indices_for` (451–489) | Builds a lazy `_ReleaseIndex` over the estate | **Fresh index object per call**; grouped key includes `id(index)` |
| `PreparedI03Session` (51–150) | One estate/session, one posting-index build across its operations | No cross-session persistence; no query-independent routing selector |
| `I03GroupedExecutionScope` (`pre553_empirical_query.py` 490–627) | Measure-independent core cache keyed by exact index/release/universe, risk, predicate, target plan, authorities and registry | Only compatible cores; measure/weight excluded, but target/predicate changes miss |
| `_evaluate_index_group_core` (`_pre553_query_eval.py` 418–578) | Exact routing/risk/condition/target/denominator core | Rebuilt for each incompatible core; facts/replay always per operation |

The current canonical estate already preserves source, release, universe,
catalog, population, condition, target, weights, routing, negatives, full
members, refs, replay, authority closure, CURRENT and changed-root/body
invalidation. It is a real replacement for the old PostgreSQL extraction path,
but it is **not** a persistent wide country substrate.

## Five cost layers

| Layer | Evidence | Status |
|---|---|---|
| Redundant row-group reads | R3: 3,965 reads / 3,964 clears for one f4; locality G5: 50 reads | **Repaired** by accepted `gid/off` locality correction |
| Release index build | R2: 5 baseline builds vs 1 prepared; current prepared session one build | **Shared by prepared session** |
| Routing/object validation | R3: routing 18.222 s / 16 calls, 9,600 routing objects, object reconstruction/hash 6.774 s | **Still repeated per changed query** |
| Compatibility-specific statistical core | Existing grouped key; only same exact core; RAW/WEIGHTED share | **Narrow only** |
| Per-operation exact facts/member refs/output | EmpiricalFact, full refs, replay, aggregation and members rebuilt per operation | **Per-operation by design** |

The current grouped proposal:

- shares `selected` RAW vs GOVERNED_WEIGHTED as one core (`core_builds=1`,
  `core_hits=1` in the prior prototype);
- does **not** share `selected` vs `f2` (`core_builds=2`, `core_hits=0`);
- does **not** solve different predicates, targets, risk sets or authority
  closures;
- therefore does **not** reconstruct the old cross-product prepared-substrate
  reuse.

## The actual missing edge

Current `DirectEstateI03Session` is the population/body substrate, but it lacks
a **query-independent prepared routing/target lookup** over that substrate.
That is the materially different edge from the old wide prepared country frame:

- old: one harmonized wide country frame → many products;
- current: canonical 13-family estate → lazy family rows → per-query routing
  and object resolution; grouped core only reuses an exact compatible core.

The absent current implementation is `NOT_ESTABLISHED`:

- persistent current equivalent of `v550_shared_respondent_substrate.parquet`;
- query-independent routing selector across changing targets/predicates;
- reuse across distinct V550/V550J analytical products.

The absence is not a reason to invent a new backend; the current estate and
SQLite `members` index are the existing surfaces to connect.

## Smallest justified next cut

**Do not broaden the group-scope patch as the historical answer.**

The smallest evidenced candidate is an exact **session-local routing/target
selector** over the existing `DirectEstateI03Session` / SQLite `members` index,
keyed by exact release/universe, respondent, target and risk set. It would
avoid repeated full-family routing materialization for changing targets and
predicates while retaining:

- canonical source/release/universe/catalog/population scope;
- exact body/ref/replay/authority/CURRENT checks;
- per-operation facts, member refs and output;
- no result cache, no weighted cache, no new scientific method.

It does **not** recreate a persistent country substrate, nor make arbitrary
distinct queries share a statistical core.

If the required old behavior is the full persistent country/respondent
substrate, that is a larger architecture/representation decision; it is
**not** established as a current implementation.

### Authority terrain after choosing the selector cut

Only two exact owner surfaces would need grant:

1. S2C direct saved-reader owner — selector/index build and exact invalidation
   in the existing direct-estate session.
2. Native I03 evaluator owner — exact selector use without weakening routing,
   body/ref, member or CURRENT validation.

No source/science/issuer/actor/protected grant is implied.

### Hardest decision for BrowserHQ/user

Choose between:

- a narrow query-independent routing selector over the existing canonical
  estate; or
- a persistent prepared country/respondent substrate closer to V550's old
  representation.

The latter is materially broader and changes the current data/access boundary;
the former is mechanical but does not recreate all old cross-product sharing.
Neither is authorized by the existing two-edit grant.

## What is not established

- VOSKRES/ZAK/K3 source/native/scoped returns do not establish a different
  current shared-computation implementation.
- No current persistent prepared substrate, routing selector or V550/V550J
  product parity is established.
- No arbitrary hundreds-of-queries core sharing is claimed.
- No native/science/actor/100k/protected acceptance.

## Evidence sources

- Old archived commit/artifact: `babb256ca43e887ab1519339108ae3a29c1928f4`;
  `Rawlsing_V550_Fused_GSS_Proof_babb256_20260803`.
- Old file hashes and exact line locators: `historical_connection.json`.
- Current integrated source: `7f0366…` / code/test `68aa7cac…`.
- Existing R3 profile:
  `MEASUREMENT_PREP/WORKER_RETURNS/ANVIL_ENGINEERING_MEASUREMENT_PREP_20261117/R3_Q_PROFILE/`.
- Existing locality G5:
  `OWNER/WORKER_RETURNS/ANVIL_ENGINEERING_LOCALITY_G5_20261118/REVIEW_RECEIPT.json`.
- Narrow prior proposal and prototype remain preserved under
  `../proposal.patch` and `../evidence/qualification_test.py`; not broadened.

**STOP for BrowserHQ/user decision.** No production edit or patch application occurred.
