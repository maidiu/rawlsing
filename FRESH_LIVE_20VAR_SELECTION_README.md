# Fresh live 35-wave × 20-variable selector — corrected contract

## Governing boundary

`variables_by_wave_from_db_20260814.csv` is the **mandatory and sole variable candidate universe**. Its required SHA-256 is:

`bc011a93e42d2de9997cea6754c5885cacc1813e341398453f4a165b52746b35`

PostgreSQL is used **only** to attach exact source/wave/country liveness evidence to `var_code`s already present in that CSV:

- aggregate live response-row count;
- aggregate distinct-respondent count.

PostgreSQL cannot discover, add, or substitute variables outside the locked inventory. No respondent rows or respondent IDs are written.

The historical `question_relation_registry_35wave_active_v1.csv` is optional **crosswalk evidence only**. Its expected SHA-256 is:

`a91239a5e630c554d2c397f739a60f1313ea8ab7377780ee3c64f4969e49267b`

It may not seed candidates, assign bucket membership, or constrain the new selection.

## Current 35-scope freeze

The script freezes the current 35 scopes, including **Afrobarometer R1/LS**, **Arab Barometer I/YE**, and **no Asian Barometer W6**.

The inventory contains source/wave variables but no country column. Therefore:

- source + wave select candidate rows from the locked inventory;
- country is applied only at the PostgreSQL liveness check.

## Corrected selection law

A variable is eligible only when:

1. it is present in the locked 18,518-variable inventory for the source/wave; and
2. the exact source/wave/country PostgreSQL response surface reports both:
   - `live_response_row_count > 0`; and
   - `live_respondent_count > 0`.

The diversity buckets are **MAXIMA, NOT MINIMUM QUOTAS**:

- up to 4 demographic/context;
- up to 4 directional/attitudinal;
- up to 4 relation-evidence;
- up to 4 structurally mapped;
- up to 2 edge/ambiguous;
- up to 2 known-fragile position/structural-context;
- then fill every remaining slot from the remaining live inventory pool;
- deterministic seed = zero-based current scope order;
- final 20 shuffled deterministically.

Therefore **zero variables in any bucket is lawful**. A scope with zero directional/attitudinal bucket metadata but at least 20 live inventory variables must still produce 20 selections by deterministic fill.

### No heuristic bucket inference

The selector no longer infers bucket membership from:

- question text;
- `relation_axis_id` + `target_entity_id` combinations;
- `mapping_status` keywords;
- structural field keywords;
- review-note text;
- any other heuristic reconstruction.

Bucket membership is used only when supplied by **explicit canonical governed metadata**:

1. an explicit `selection_bucket` column in the locked inventory, if such a future inventory contains one; or
2. an optional `--bucket-authority` CSV joined by exact `source,wave,var_code` and containing a canonical `selection_bucket`.

Allowed canonical bucket labels are:

- `demographic_context`
- `directional_attitudinal`
- `relation_evidence`
- `structural_mapped`
- `edge_ambiguous`
- `known_fragile`

If no exact governed bucket metadata exists for a live variable, it is marked `UNBUCKETED` and remains fully eligible for deterministic fill. **Missing bucket metadata is not a blocker.**

An optional bucket-authority file can enrich only variables already present in the locked inventory. It cannot add candidates.

## Optional governed joint-family seed

`--joint-registry` remains optional and disabled by default. When supplied, a governed joint-family registry may seed only variables that:

- already exist in the locked inventory; and
- are live in the exact PostgreSQL scope.

It cannot create candidates.

## Run

From the Rawlsing environment with PostgreSQL access:

```bash
python3 build_fresh_live_20var_selection.py \
  --inventory ./variables_by_wave_from_db_20260814.csv \
  --old-fixture ./question_relation_registry_35wave_active_v1.csv \
  --env-file ./.env \
  --output-dir /private/tmp/rawlsing-fresh-live-selection-20260814
```

No bucket authority is required. With none supplied, the selector simply uses any exact governed buckets available in the inventory and otherwise fills from `UNBUCKETED` live variables.

If an exact governed bucket-authority CSV exists:

```bash
  --bucket-authority /path/to/exact_governed_bucket_authority.csv
```

If current governed joint-family YAMLs should seed the fixture:

```bash
  --joint-registry /path/to/governed_registry.yaml
```

## Actual blocking conditions

The selector fails closed only for real contract/execution failures such as:

- inventory SHA mismatch;
- conflicting duplicate inventory rows;
- no inventory variables for a frozen scope;
- unavailable/malformed response relation;
- fewer than **20 total live inventory variables** in a frozen scope;
- invalid/conflicting explicit bucket-authority rows;
- failure to emit exactly 20 unique selections after the deterministic algorithm.

It does **not** block because any diversity bucket has fewer than its target maximum.

## Success condition

Every one of the 35 scopes must produce exactly 20 live variables:

`35 × 20 = 700`

Success terminal:

`FRESH_LIVE_35WAVE_20VAR_SELECTION_BUILT`

Blocked terminal:

`FRESH_LIVE_SELECTION_BLOCKED`

## Outputs

Always/diagnostically:

- `fresh_live_variable_eligibility_35wave_20260814.csv`
- `fresh_live_selection_wave_summary_20260814.csv`
- `fresh_live_selection_manifest_20260814.json`
- `fresh_live_selection_blockers_20260814.csv` when blocked

On successful 35×20 freeze:

- `fresh_live_question_selection_35wave_20var_20260814.csv`

If the old fixture is supplied:

- `fresh_live_selection_old700_crosswalk_20260814.csv`

The final selection records:

- inventory authority fields;
- exact bucket metadata when available, otherwise `UNBUCKETED`;
- bucket metadata source/hash;
- selection reason;
- deterministic seed/order;
- aggregate liveness counts;
- inventory SHA-256;
- response relation used.

## Regression check

```bash
python3 -m py_compile build_fresh_live_20var_selection.py
python3 build_fresh_live_20var_selection.py --self-test
sha256sum build_fresh_live_20var_selection.py
```

The self-test specifically proves that **40 live GSS variables with zero bucket metadata still produce exactly 20 deterministic selections**, and that only 19 live variables is a genuine blocker.
