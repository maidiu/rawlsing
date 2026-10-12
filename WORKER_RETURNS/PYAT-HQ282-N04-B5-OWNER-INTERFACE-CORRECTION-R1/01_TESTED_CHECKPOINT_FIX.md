# PYAT HQ282 N04 — Tested checkpoint fix

## The defect

The C02J `verify_checkpoint_subject` method in `pre553_b5_owner_held_verifier_candidate.py` calls:

```python
stored = self._m2.subject_exact(subject.release_ref)
```

The M2 `subject_exact` method expects a `release_subject_ref` (the producer subject), not a `release_ref` (the release identity). This mismatch causes valid checkpoint restores to be falsely rejected with:

```
VerifierCheckpointError: checkpoint subject release is absent from the held M2 repository:
RELEASE_SUBJECT_NOT_FOUND: exact producer subject is not registered
```

## The correction

The corrected implementation uses `resolve_subject_exact(repository, release_ref)` which:

1. Resolves the release via `release_exact`
2. Extracts `release.release_subject_ref`
3. Calls `subject_exact` with the correct ref
4. Verifies producer-contract and subject-kind consistency

## Evidence

### Positive: valid checkpoint restoration

```python
# Without overlay
repo, release, m2_subject, subject, verifier, ex = _full_fixture()
ck = ex.export_checkpoint()
restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
assert restored is not None  # PASSES
```

```python
# With corrected overlay
repo, release, m2_subject, subject, verifier, ex = _full_fixture()
ck = ex.export_checkpoint()
with corrected_overlay_active():
    corrected_register_verifier(verifier)
    restored = B5.LearnedProductLifecycleExecutor.from_checkpoint(ck)
    assert restored is not None  # PASSES
```

### Defect reproduction

```python
result = demonstrate_checkpoint_defect()
assert result["defect_reproduced"] is True  # RELEASE_SUBJECT_NOT_FOUND
assert result["correction_works"] is True   # resolve_subject_exact succeeds
```

### Negative: inconsistent records still rejected

| Modification | Raw executor | Corrected overlay |
|---|---|---|
| Truncated history | ACCEPTED (known gap) | REJECTED (CHECKPOINT_UNRESOLVED) |
| Altered state | ACCEPTED (known gap) | REJECTED (CHECKPOINT_UNRESOLVED) |
| Bad hash | REJECTED | REJECTED |
| Incomplete publication | REJECTED | REJECTED |

## Identity mismatch

The root cause is that `release_ref != release.release_subject_ref`:
- `release_ref` is the release identity (e.g., `LearnedProductReleaseCore / urn:rawlsing:pre553:m2:release:sha256:...`)
- `release.release_subject_ref` is the producer subject identity (e.g., `LearnedSemanticProduct / urn:rawlsing:pre553:m2:subject:sha256:...`)

The `subject_exact` method looks up subjects by `release_subject_ref`, not by `release_ref`. The correction resolves the release first, then extracts the correct subject ref.
