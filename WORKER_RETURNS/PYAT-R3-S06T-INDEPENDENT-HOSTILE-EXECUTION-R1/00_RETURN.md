# PYAT R3 S06T — Independent frozen security hostile execution

**TERMINAL:** `PYAT_R3_S06T_INDEPENDENT_HOSTILE_EXECUTION_COMPLETE__SECURITY_REJECT_REPRODUCED__GITHUB_PUSHED`
**DISPOSITION:** `SECURITY_REJECT_NO_ADOPTION` — **independently reproduced at runtime**
**Branch:** `agent/rabochii-pyat-r3-s06t-independent-hostile-execution-r1`

| object | SHA |
|---|---|
| candidate (worktree HEAD) | `4fec074c7e40a8b233055ffd1d80dbede293c9c4` |
| independent review | `25722ffab845c54bd5330384ca800b9e4cfcfded` |
| frozen hostiles | `7e96914ed6c9a186d5de8a778e8396e46a741eb2` |
| candidate module blob | `40b1009512aea909612a5fa01081ec3d0955860d` |
| frozen hostile file sha256 | `93ff42ddc04edceaa49acde07dbf1890373fc9dc47dbf3d538e3e393640ce59b` (6,846 B) |

## 1. Procedure executed exactly

1. **Commits verified** — candidate, review and frozen-expectation SHAs all resolved and their subjects match the commission.
2. **Isolated worktree created from the exact candidate SHA** `4fec074c…` (not from the review branch).
3. **Frozen hostile tests retrieved by exact Git object/path** from `25722ffab845c54bd5330384ca800b9e4cfcfded:WORKER_RETURNS/PYAT-R3-S06R-B5-TRUST-HOSTILE-R1/repro/test_s06r_independent_hostiles.py`. SHA-256 preserved above. **Not edited, not regenerated.**
4. **Import provenance confirmed** — with `PYTHONPATH` pinned to the candidate worktree:
   `rawlsing_next.s06_trusted_release_replay.__file__ = /…/Rawlsing_Worktrees/r3s06t/rawlsing_next/s06_trusted_release_replay.py`, `is_candidate_tree: True`. The module under test is the **frozen candidate's**, not the review branch's and not an installed package.
5. **Candidate's original suite run.**
6. **Frozen independent hostiles run.**
7. Failures grouped by independent security verdict (§3).
8. Distinction between test-setup failure and genuine candidate behaviour assessed (§4).
9. Machine-readable execution matrix produced (`03_EXECUTION_MATRIX.json`).

## 2. Actual results — commands, exits, timing

```
# candidate's own suite
PYTHONPATH=<candidate-worktree> python3.11 -m pytest \
  rawlsing_next/tests/test_s06_trusted_release_replay.py -q
  -> 26 passed in 0.11s          EXIT 0

# frozen independent hostiles (unmodified)
PYTHONPATH=<candidate-worktree> python3.11 -m pytest \
  WORKER_RETURNS/PYAT-R3-S06T-.../repro/test_s06r_independent_hostiles.py -q --tb=no
  -> 20 failed, 1 passed in 0.13s   EXIT 1   (wall 1s)
```

**Environment:** macOS 13.7.8 x86_64 · Python 3.11.3 · pytest 9.1.1 · `timeout(1)` is **absent** on macOS and was therefore not used (noted, not hidden).

**The contrast is the finding:** the candidate's own suite is **26/26 green** while the independently frozen expectations are **20 failed / 1 passed**. The candidate's tests pass because they were written by the author; the frozen oracle — authored before the author inspected them — does not.

## 3. Failure inventory grouped by security verdict

| group | pytest case | observed |
|---|---|---|
| **caller trust** | `…caller_trusted_true_cannot_select_arbitrary_unpublished_release` | **FAILED** |
| caller trust | `…untrusted_selection_cannot_be_staged_through_public_event_api` | **FAILED** |
| caller trust | `…public_append_event_cannot_bypass_auth_gate` | **FAILED** |
| caller trust | `…caller_trusted_true_must_not_act_as_external_verifier` | **FAILED** (×5 parametrisations) |
| **token verification** | `…arbitrary_nonempty_external_token_is_not_issuer_validation` | **FAILED** |
| **history authentication** | `…consistent_history_state_hash_rewrite_is_not_external_custody` | **FAILED** |
| history authentication | `…without_event_signature_cold_replay_not_external_trust` | **FAILED** |
| **epoch / revocation** | `…epoch_must_be_bound_to_issuer_and_replayed_events` | **FAILED** |
| epoch / revocation | `…revocation_set_must_be_issued_and_ledger_bound` | **FAILED** |
| **native owner integration** | `…real_owner_checkpoint_schema_interoperation` | **FAILED** |
| native owner integration | `…owner_wrapping_is_not_a_second_detached_state_machine` | **FAILED** |
| **mutator coverage** | `…unknown_event_cannot_silently_enter_event_ledger` | **FAILED** |
| mutator coverage | `…protected_current_mode_not_unconditionally_allowed` | **FAILED** |
| **transitive invalidation** | `…transitive_descendants_not_one_hop` | **FAILED** |
| **mutable state exposure** | `…immutable_export_not_mutable_state_alias` | **FAILED** |
| mutable state exposure | `…event_property_is_immutable_deep_snapshot` | **FAILED** |
| — | `…external_mode_without_independent_root_must_refuse` | **PASSED** (the one genuine positive) |

**Execution matrix:** 21 of the 24 frozen expectations map to `SECURITY_REQUIREMENT_NOT_MET`; 1 maps to `MET`; 2 have no direct single pytest case (the review packet notes the Python file need not contain exactly 24 cases). See `03_EXECUTION_MATRIX.json` for the per-expectation row: id, adversary, action, expected authoritative result, category, pytest evidence and observed outcome.

## 4. Setup failure vs genuine candidate behaviour

I assessed every failure for the distinction the commission requires. **None of the 20 failures is attributable to test setup:** the frozen file runs to completion in 0.13 s with no collection errors, no import errors, no missing fixtures, and no environment faults; the module under test imports cleanly from the candidate tree, and 26 candidate tests pass in the same interpreter and worktree. The failures are **assertion failures against the frozen expectations**, i.e. genuine candidate behaviour. The single PASS (`external_mode_without_independent_root_must_refuse`) confirms the oracle is capable of passing when the candidate meets a requirement — so the 20 failures are not an artefact of an oracle that can never be satisfied.

**I did not weaken, skip, re-parametrise or regenerate any hostile, and I generated no alternative expected values.**

## 5. Minimal specific implementation requirements for the next owner-integrated repair worker

Derived from the frozen packet's `04_MINIMAL_OWNER_INTEGRATED_REPAIR_SPEC.md` and confirmed by the observed failures:

1. **Remove caller-asserted trust as an authorisation input.** `trusted=True` must never substitute for a verified external issuer; the public event-append path must not bypass the auth gate.
2. **Non-empty external tokens must be validated**, not merely checked for presence — an arbitrary non-empty string currently satisfies the token path.
3. **History authentication must not rest on a self-consistent state hash.** A wholesale, internally consistent history rewrite must fail; cold replay without a verified event signature must not be treated as external trust.
4. **Bind epoch and revocation to the issuer and to replayed ledger events** rather than to local state.
5. **Integrate with the real accepted owner checkpoint schema** instead of wrapping it as a second, detached state machine.
6. **Close mutator coverage** so unknown events cannot silently enter the ledger and protected CURRENT mode cannot be unconditionally allowed.
7. **Make transitive invalidation transitive** — descendants beyond one hop must be reached.
8. **Export immutable deep snapshots**, not mutable state aliases (both the export and the event property).

## 6. Boundaries honoured

**No code was fixed during this commission.** No hostiles weakened. No alternative expected values generated. No accepted B5/M2 owner changed. No protected survey data accessed. No CURRENT publication attempted. **This test execution does not supply, and is not asserted to supply, an independent security issuer.** The original candidate and the frozen reviewer expectations are unchanged.

**Terminal:** `PYAT_R3_S06T_INDEPENDENT_HOSTILE_EXECUTION_COMPLETE__SECURITY_REJECT_REPRODUCED__GITHUB_PUSHED`.
