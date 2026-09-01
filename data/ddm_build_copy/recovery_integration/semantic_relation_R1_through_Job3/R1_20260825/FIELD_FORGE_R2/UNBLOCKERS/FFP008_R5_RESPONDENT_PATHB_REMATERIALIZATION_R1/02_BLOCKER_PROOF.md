# FFP008 — PREDICATE-INPUT BLOCKER PROOF

## C04-owned semantics

C04 freezes the Q73D predicate symbol and source condition, not a respondent measurement mapping. Its compiler branch is literally:

```python
if 'has paid employment' in s.lower():
    a={'field':'RESPONDENT_HAS_PAID_EMPLOYMENT','op':'eq','value':True}
```

The resulting predicate sidecar records `RESPONDENT_HAS_PAID_EMPLOYMENT`, but neither the sidecar nor the compiler names Q96 as its empirical carrier.

## Source-owned measurements

- Q73D condition: paid employment; income tax deducted from **wages by your employer**.
- Q73E condition: **self employed**; tax on earnings from **your business or job**.
- Q96: whether respondent has **a job that pays a cash income**, and whether full-time/part-time.

No current evidence recovered in this bounded court authorizes `Q96 in {2,3} == RESPONDENT_HAS_PAID_EMPLOYMENT`. Empirical convenience is not semantic authority.

## Why this is the first blocker

Source bytes, row count, respondent grain, `(COUNTRY, RESPNO)` identity, qimpl→Q73D, and predicate specification are all proved. Predicate execution on a real respondent cannot begin until every predicate symbol is bound to an exact governed respondent fact. `RESPONDENT_HAS_PAID_EMPLOYMENT` is the first missing binding.

`UNRESOLVED_INPUT != FALSE` and response state is not used to repair the gap.
