# FINITE FAN-IN OR HOLD DECISION

## One binary answer

**HOLD.**

Named hold:

`HOLD_E5_LOCAL_SOURCEFREE_FANIN_PENDING_OWNER_AUTHORIZED_VERSIONED_M2_FIXTURE_AMENDMENT`

This is not a rejection of E5's local sourcefree engineering merit and not a finding of a new runtime defect. It is a governance/contract hold: E5 leaves two accepted M2 tests byte-unchanged and RED, adds new reconciled tests, but supplies no accepted-M2 owner permission for a versioned fixture amendment. Under the E6 launch that permission cannot be invented.

## Exact defect

`rawlsing_next/tests/test_pre553_learned_product_release.py` remains byte-identical to PRE-MAIN and fails 2/28 on E5:

- `test_17_binding_cannot_resolve_different_release` fails at foreign `register_representation` with `M2ReleaseError: RELEASE_UNAVAILABLE`.
- `test_18_endpoint_failover_only_among_same_release` fails at foreign `register_binding` with `M2ReleaseError: RELEASE_UNAVAILABLE`.

The unfiltered court is `179 passed, 14 failed, exit 1`; the 14 are exactly these 2 plus the 12 historical S06FR `OBSERVED` defect-presence tests. A 14-deselected selection result of `179 passed, 14 deselected, exit 0` is not a green full court and is not adoption evidence.

The early refusal itself is lawful at the public M2 boundary:

- the published M2 operations already required `release_exact`;
- the accepted tests bypass those operations through class storage methods;
- after lawful foreign subject/closure/release import, the original `PUBLICATION_BINDING_MISMATCH` oracle is preserved in both independent scenarios.

But the accepted fixture contract still needs an owner decision. Neither E5 nor E6 may silently convert the two RED accepted tests into accepted reality.

## Per-hunk disposition

| Hunk | Disposition |
|---|---|
| B5 recursive payload immutability and detached export | MERIT; no blocker |
| B5 owner lock, transaction, reader lock and rollback | MERIT; no blocker |
| B5 native checkpoint history and semantic replay | MERIT at local consistency scope; no external-completeness claim |
| B5 saved-helper and unwrapped-body refusal | MERIT; same-process bypass remains documented |
| M2 repository transaction, read lock, instance `_insert`, rollback | MERIT; private ABI delta only |
| M2 direct writer exact-release validation | MERIT at the public-boundary reading; causes the two accepted fixture conflicts |
| `LOCAL_UNAUTHENTICATED` / `EXTERNAL_ISSUER_HOLD` | CORRECT AND HONEST |
| S06G fixtures and S06F-named helper shim | TEST-ONLY MERIT; no S06F acceptance program transplanted |

## What would change the answer

The accepted-M2 owner must issue an explicit **versioned fixture amendment** that does one of the following:

1. Authorizes the two accepted scenarios to lawfully import the foreign subject, closures and release before registering the foreign representation/binding, while retaining `PUBLICATION_BINDING_MISMATCH` as the asserted oracle; or
2. Formally supersedes the two fixtures with versioned replacements that make the same point.

The amendment must not weaken `release_exact` or edit accepted tests in place without owner authority. After the amendment, the exact resulting SHA must be re-run through the full court and re-reviewed by a distinct reviewer.

If the owner instead determines that direct foreign-record registration is a supported lower-level contract, then the M2 `register_representation`/`register_binding` early-refusal hunks must be rejected, while the independent B5 transaction/immutability/replay and M2 transaction hunks can be considered separately.

## Grades

- ENGINEERING: `POSITIVE_LOCAL_SOURCEFREE_REPAIR_MERIT__FANIN_HELD_BY_TWO_ACCEPTED_M2_FIXTURES_AND_MISSING_OWNER_AMENDMENT`
- SCIENTIFIC: `HOLD__NO_SOURCE_NATIVE_ACTOR_OR_EXTERNAL_VALIDATION`
- AUTHORITY: `HOLD__NO_EXTERNAL_ISSUER_OS_KILL_MULTIPROCESS_PROTECTED_CURRENT_OR_PREMAIN_ADOPTION`

## Non-actions

- No production patch on this reviewer branch.
- No accepted test edited, skipped, xfailed or deselected as acceptance.
- No `release_exact` weakening.
- No owner permission invented.
- No PRE-MAIN/main/Sorok mutation, merge, force-push or branch deletion.
- No source-native, survey, actor, N11/N12, C11/C12 or PROGRAMMA work.
- No self-review, self-adoption or automatic fan-in.
