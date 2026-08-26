# Nine-source canary archive truth audit

Status: **PASS_STATIC_CANARY_ARCHIVE_TRUTH_AUDIT**

- Exact source-wave-country scopes: 9
- Configured joint items: 26
- Schemas containing respondent identifiers: 0
- Schemas containing aggregate `n_respondents`: 99

## Governing conclusion

The archive is sufficient for exact scope recovery, question binding, response-semantics audit, and reuse of preserved V551 relation atoms.
It is **not** a respondent-level V550J substrate: no packaged schema exposes `respondent_id` or `respondent_id_norm`.
The large `indicator_answer_matrix` tables are aggregate question/answer distributions carrying counts such as `n_respondents`; those counts cannot be inverted into respondent co-occurrence patterns.
Real V550J execution must therefore use the live respondent database/view (or a separately governed prepared substrate) on the receiving host.

This gate prevents marginal distributions from being silently counterfeited as joint-response evidence.
