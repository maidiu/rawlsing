# ANVIL engineering cut1 — owner ACK

## Status

**`ACK_SCOPED_TWO_FILE_PREPARED_SAVED_BATCH_CUT1`**

- Owner session: `ses_e3120ba7affeNBHUoX1HIP3G4r`
- Owner worktree: `ANVIL_ENGINEERING_EXECUTION_20261117/OWNER`
- Owner branch: `agent/anvil-engineering-cut1-owner-20261117-r1`
- Baseline: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7` (parentless local snapshot)
- Prior ACK: `b32f215660def205762f0e9d0eafa2c3dfaa0c36` — terminal G5 closed; **not silently extended**
- Protected observed: `5d387a9a8c72c68e6ef87a671d6d486bfd1fc43e`, paired rev11; no protected writes
- Product code edited by this ACK: **none**
- Source/test/native actions by this ACK: **none**

## Exact pins

| File | Blob | SHA-256 |
|---|---|---|
| `rawlsing_next/pre553_saved_workload_integration.py` | `cc8aa32512378261406d765f0b049c748cb3e11f` | `5f885a5d34f8363dd474b691aafb4b22c6bff4f886825cccbbb30cf12aa5e07b` |
| `rawlsing_next/pre553_batch_runner.py` | `49e3974c658d66a270815d9faa3798b40d4488b1` | `96fe6c6574be8f6641252d07a8b09349126a369e53d4f892a840f4ea5070701e` |
| `rawlsing_next/pre553_prepared_saved_i03.py` | `bcb146edae680028e027e47cae45891693f63526` | `fbc60cb65e159c820d25f70052130e1256689bf1655053ff9b0751f0e968cf78` |
| `rawlsing_next/pre553_saved_c11_admission.py` | `22749addc1fca5f0b90e12728847c390aafa7a84` | `93299f5c0100d132bb2bef07b321af1755726a5e90ee3b488a11dc1b6028c526` |

## Observed baseline red

Read from the implementer’s own baseline evidence, not rerun by owner:

- `prepared_abi_red.txt`: 2 witness tests pass, proving the current exact prepared
  subclass is rejected by both the saved I03 wrapper and
  `BatchExecutionRunner.__init__`.
- `baseline_cut1.txt`: 58 passed.
- `batch_court.txt`: 23 passed.

The proposed cut is the exact repair for that observed prepared-subclass
rejection.

## Granted scope

### File 1 — `rawlsing_next/pre553_saved_workload_integration.py`

Allowed symbols only:

- `execute_saved_i03`
- `execute_saved_i05`
- `execute_saved_batch`

Allowed private helpers: only those directly required for exact prepared-type
dispatch/import, one prepared-context lifecycle, and saved Batch unit dispatch.
No new public symbols. No change to `execute_saved_normal`,
`execute_saved_completed`, `execute_saved_partial`, `execute_saved_absent`, or
any resume/checkpoint function.

### File 2 — `rawlsing_next/pre553_batch_runner.py`

Allowed symbols only:

- `BatchExecutionRunner.__init__`
- indispensable exact `PreparedSavedC11Admission` class import and exact
  saved-admission/release-guard helper only.

No change to `run`, schedule/unit order, state machine, receipts, summary or
failure behavior.

## Required invariants

- Exact class whitelist only: `SavedC11Admission` and
  `PreparedSavedC11Admission`. **No generic `isinstance`, duck repository, fake
  `C11Repository`, fabricated release/seal or monkeypatched guard.**
- The prepared subclass inherits the exact `SavedC11Admission` release identity
  and `resolve_release_exact`; **no new release identity type**.
- `execute_saved_batch` uses **one** prepared context for all actual Batch units
  of a `PreparedSavedC11Admission`, closes on success, refusal and exception, and
  never reuses a prepared session across mismatched release/universe/predicate/
  weight scopes.
- Per-unit CURRENT checks, actual Batch receipts/fates, full facts/risk/
  denominator member refs/used refs/replay must equal the one-shot baseline.
- Plain `SavedC11Admission` and legitimate `C11Repository` behavior remain
  unchanged. The legacy path remains supported.
- No S2-C writer, prepared module, base admission, native evaluator, issuer,
  Batch scheduler/receipt machine, NORMAL/resume/checkpoint or scientific owner
  is changed.

## Read-only surfaces

- `pre553_prepared_saved_i03.py` — `PreparedSavedC11Admission`,
  `PreparedI03Session`
- `pre553_saved_c11_admission.py` — base admission, release identity, current
  checks
- S2-C writer, actual direct reader/writer
- Existing native I03/I05 evaluators and issuer
- `BatchExecutionRunner.run`, scheduler, state/receipt machine, summary/failure
- `pre553_issued_workload.py` NORMAL/COMPLETED/PARTIAL/ABSENT/resume/checkpoint
- Existing tests, prior returns, protected/control/source/private data

## Receiving identity and lease

- Implementer: existing S2-D A `ses_e3120ba1cffeO1w43uU5MLh4yq`
- Worktree: `ANVIL_ENGINEERING_EXECUTION_20261117/IMPLEMENTER`
- Branch: `agent/anvil-engineering-cut1-20261117-r1`
- Baseline: `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`
- Mode: exclusive serial product-owner implementer for this exact two-file cut
- Competing writes: none granted by this ACK
- Expiry: valid only through frozen nonauthor review at the exact cut1 candidate
  SHA; no subsequent engineering, files, science or protected rights

## Required decisive tests

- Baseline exact rejection of prepared subclass at wrapper and Batch runner.
- One real saved sourcefree fixture; four distinct selected / F2 forward / true
  same-respondent F4 k>=3 / raw operations through saved wrappers and actual
  Batch; one `DirectEstateI03Session._build` for the prepared workload.
- Exact full facts/risk/denominator/used refs/replay and actual Batch
  receipts/fates identical to the one-shot baseline.
- Arbitrary subclass/wrong release/wrong source/forged admission refuses before
  protected work or positive receipt.
- CURRENT revoked before/during batch, changed root/manifest binding refuses.
- Repeated/ranked occurrences and UNKNOWN/zero/routing remain distinct.
- Cleanup on success/refusal/exception; exact restoration; legitimate legacy
  path.
- Bounded cut1 wall/CPU/RSS/retained/scratch/output/build-count measurements.
- New focused `test_anvil_prepared_saved_batch_cut1.py` and own return only.
  Existing tests read-only. No 100k/full-matrix claim.

## Grantor role basis

This is an inherited S1-D/Batch functional allocation under the current parent
user cut1 GO plus the prior `b32f2156` inherited-maintainer ACK. During the
prior ACK the saved-integration surface was expressly read-only; this is a
**new cut1-specific parent-user allocation** for the exact prepared saved Batch
bridge, not an extension of the old terminal G5 and not a claim of personal R16
Batch authorship or S2-D packet authorship. S2-D A remains the receiving
implementer/product owner; accepted S2-E scientific ownership remains separate.

No new owner, issuer, licence, source/science/CURRENT/completion/Batch fact or
generic user approval request is created by this ACK.

## Boundaries

No protected merge/CAS, production CURRENT, original35/native source, science/
actor/issuer, W03/W04/Q3, subagents, model/provider/host/account switch or
heavy benchmark. This ACK does not start the implementer or execute source.
