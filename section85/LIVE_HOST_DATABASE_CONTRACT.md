# Live-host respondent database contract

The R184 authority database is not the respondent database. Pointing the canary runner only at `rawlsing_p3c_work` is insufficient.

V550J requires a live DDM database exposing one of:

- `public.v_ddm_response_long_facet_ready_authority` (preferred when present), or
- `public.v_ddm_response_long_facet_ready`.

For each canary scope the compiler performs a bounded query equivalent to:

```sql
SELECT *
FROM <facet_ready_view>
WHERE source = <source>
  AND canonical_wave = <wave>
  AND country_code = <country>
  AND upper(var_code) IN (<configured canary variables>)
ORDER BY var_code, respondent_id;
```

The returned surface must contain real respondent identifiers and response rows. The prepared-substrate contract expects, at minimum, resolvable values for:

- source, wave/canonical_wave, country_code;
- respondent_id;
- var_code/question_id;
- raw or normalized response value/label;
- missingness/special-response state where applicable;
- weight value/status where applicable.

The compiler then harmonizes and caches a governed prepared substrate containing `respondent_id_norm`, `var_code_norm`, semantic response roles, target resolution, directionality, and provenance.

## Required distinction

- R184 PostgreSQL: canonical proposition authority and provenance.
- Live DDM PostgreSQL: respondent-level answers used to compile joint patterns.

Do not merge them by copying aggregate V550 artifacts into the respondent view. Do not restore the R184 dump over the live pipeline database.

## Pre-execution proof

Run `code/check_live_respondent_database.py` against the live pipeline database before generating or executing the J-chain plan. It must return `PASS_LIVE_RESPONDENT_DATABASE_CONTRACT` for all nine scopes. This is a fail-closed gate against accidentally pointing the runner at the R184 authority-only database or an aggregate-output store.
