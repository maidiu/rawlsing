# Replay and Determinism Receipt

## M1 replay gate

Before M1->M2 adaptation, I4 calls `verify_m1_disposition_replay(disposition)`.

It then requires exact identity conservation for:

- disposition ref;
- determinant manifest ref;
- explanation ref;
- replay ref;
- determinant/explanation receipt ref.

The M2 replay closure carries the exact M1 replay root and records only the conservative grade `HISTORICAL_EXPLANATION_ONLY` plus `m1_replay_verified = true`. I4 does not claim live-source reexecution.

## B5 replay gate

When explicit lifecycle actions occur, I4 invokes B5's existing `audit_replay()`. The resulting exact `LifecycleReplayReceipt.ref` is included in the composition receipt.

Full T01 therefore proves an exact lifecycle checkpoint can be exported, reconstructed, and rehashed identically after explicit REGISTER -> PUBLISH -> SELECT_CURRENT.

## Determinism

T25 proves:

same exact M1 disposition + same exact product contract + no lifecycle effects
=> same M2 release ref + same composition receipt ref.

T26 proves:

constitutive contract change
=> new contract ref + new composition receipt ref.

It simultaneously proves that a consumer-purpose-only change does not rewrite the producer-owned M2 release identity.

T29 proves B5 rejects a tampered determinant-set hash.

## Governed evidence

- semantic candidate: `f6da31f9f6df315486c574f42c4469639cb79ff8`
- evidence execution tip: `59b223533e05f7005f41e891e214ceef1a0169f0`
- workflow run: `36331313683`
- job: `108653665456`
- court artifact: `10935678224`
- protocol self-tests: `20 passed in 0.07s`
- combined I4 + owner regressions: `135 passed in 15.19s`
- result: PASS

The evidence-only court-spec change was reverted at `0400c6d18276226b248942c9a19995d39a101093`.
