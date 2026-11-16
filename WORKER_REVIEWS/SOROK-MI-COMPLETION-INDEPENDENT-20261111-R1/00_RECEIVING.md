# Mechanism I completion — independent code receiving

**Verdict: REVISE_EXACT_DEFECT**

**Reviewed author SHA:** `634b75d6e321952e9a917c83ccf62ae7c30e0680`
**References:** frozen MI implementation `83de56d24c2be2bc69bc596abd26aa808c26cf42`; protected `811dd32b04b017d98fe898dd7416cbf82e5d5fd1`.
**Scope:** sourcefree Mechanism I implementation and actual current consumers; no native, actor, root, product, live-provider, or protected authority claimed.

## Executed evidence

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mi-review-state" \
  rawlsing_next/tests/test_sorok_history_*.py

# 90 passed in 313.57s
```

The suite covered H1 admission/atomicity, graph and cold index behavior, source withholding/restore, T2/idle ordering, joined P4/P5/P6 behavior, provider mocks/timeouts, and ordinary S46 activity.

Independent adverse probe:

```text
PYTHONDONTWRITEBYTECODE=1 /private/tmp/rawlsing-oct28-p1r1/venv/bin/python \
  -m pytest -q -p no:cacheprovider --basetemp "$PWD/.mi-review-state" \
  WORKER_REVIEWS/SOROK-MI-COMPLETION-INDEPENDENT-20261111-R1/test_h1_source_time.py

# 1 failed: test_h1_source_ref_cannot_postdate_effective_time
# AssertionError: assert 'INDEX_READY' != 'INDEX_READY'
```

## Concrete defect

An H1 occurrence can cite a `source_refs` event whose clock is later than the occurrence's `effective_time`, and the owner still commits `INDEX_READY`.

Reproducer: `WORKER_REVIEWS/SOROK-MI-COMPLETION-INDEPENDENT-20261111-R1/test_h1_source_time.py`. It takes a valid experimental H1 candidate, selects a packet event ref with a clock after the proposed effective time, and commits through `HistoricalWorld`.

Relevant source:
- `rawlsing_next/sorok_history/admission.py:594-596` validates source refs only for membership in `packet_refs`; it does not check their event time.
- `rawlsing_next/sorok_history/admission.py:695-730` checks chronology for `causal_parents`, but not `source_refs`.
- `WORKER_RETURNS/.../bp4/world.py:191-219` validates `causal_parents` timing but does not validate `source_refs` chronology before `admit_material_history` appends the H1 event.

This is a sourcefree H1 source/time qualification defect, not a missing native grant. The smallest correction is to require each admitted source ref to resolve in the packet and have `event.clock <= effective_time` (or a typed later-source rule if one is intentionally supported), then add this negative regression.

## Positive findings

- Existing sourcefree H1 tests pass: world-owner insertion, group atomicity, actor/place/role checks, unrelated H0 survival, cold graph/index restoration, T2 coalescing, bounded idle work, provider timeout custody, and joined P4/P5/P6 readers.
- H1 source absence and restoration, no hidden-history actor/user disclosure, and `H1_OWNER_NOT_GRANTED` holds are exercised.
- The default path has no H1 permission; explicit experimental policy remains test-only.
- No native science, actor memory/knowledge effects, root-public pre-contact write, product authority, or live provider result is claimed.

## Limits

- Live provider was not run; provider tests use injected/mock transport and are not live inference.
- Native/actor/root/product permissions remain genuinely unissued and are not counted as engineering defects.
- No protected merge or author implementation edit was made.
