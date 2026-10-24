# S40 plan E1 identity closure — ACCEPT_SCOPED

Decision: **ACCEPT_SCOPED**.

## Exact cut

- Corrected candidate: `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.
- Branch: `codex/sorok-s40-generated-native-speech`.
- Prior rejected cut: `1d6f89b2ef60f4713741c9432c63940737248984`.
- Base: accepted S39 `e41513fa65601a37e7b3b430d26c626ae0217d90`.
- Reviewed in a disposable clone. No product edits, provider/model calls,
  controller-attachment changes, native/science action, or accepted-boundary
  reopening.

## Reproduced checks

```text
PYTHONPATH=<S40 return> M35_JOIN_E_RETURN=<warm JOIN-E> \
  python3 -B -m pytest -q <S40 return>/tests -p no:cacheprovider
8 passed in 2.45s
```

The preserved reviewer oracle `SOROK_REVIEW/S40/oracles/s40_e1_plan_binding.py`
was run against checkout `79b0357` and returns **1 PASS / 0 FAIL**. It now sees
the actual E1 event ID `TEST_ONLY_BP2_E1_OCC-0001`, its separate hash, the C8
occurrence `OCC-0001`, and the C8 state digest in the plan's `ADMITTED_E1`
public fact. The oracle's static cut metadata still names the prior candidate;
the actual checkout used was `79b0357c7af9b66ad8a28f5b77b46b0348094a23`.

## Repair verification

The producer obtains the actual E1 event ID/hash and C8 occurrence/state before
wording and passes that identity into the plan. The S40 reader now checks the
plan's public E1 fact against the actual session/C8 binding, validates the C8
journal/content hash and the actual C9 E1 hash, and rejects a wrong public E1
fact on both warm read and cold reopen. The authorized plan/native/English
artifacts remain bound to the same event.

The 8 focused tests retain generated native request and refusal, nonverbal
`ATTEND_OBJECT`, denied request with no speech/valid-empty C9, OPEN no-action,
zero target proposals/rows, `NO_CHANGE/NO_PROPOSAL`, same-event plan/native/
English view, competence refusal/restore, and equivalence strengthening refusal.
No broad campaign or speculative assurance work was performed.

## Receipt

- 8-test output: `evidence/s40-79b-tests8.out` SHA-256 `85d31c5b…`.
- Preserved oracle output: `evidence/s40-79b-e1.json` SHA-256 `608a8fb1…`;
  1 PASS / 0 FAIL.
- Corrected `s40/language.py` SHA-256 `7b960516…`; `s40/reader.py` SHA-256
  `cf88464b…`; `s40/performer.py` SHA-256 `094c8786…`; `s40/session.py`
  SHA-256 `abe771cc…`.
- Preserved oracle SHA-256 `c38ed92f…`.
- No live provider/domain/native/production action was performed.
