# API text/path binding contract

## Public API behavior

`verify_return(commission, returned, candidate_sha, root, *, returned_path=None)`
retains its existing signature. When `returned_path` is supplied:

1. the path is resolved and checked for repository tracking exclusion;
2. the exact path text is read;
3. the text must equal the separately supplied `returned` text;
4. mismatch is `MCR_C_EVIDENCE_TEXT_PATH_MISMATCH`;
5. unreadable/missing/escaping path is `MCR_C_EVIDENCE_PATH_UNREADABLE` or
   `MCR_C_EVIDENCE_PATH_UNAVAILABLE` and the result is RED.

`returned_path=None` remains the existing fail-closed API state
`MCR_C_EVIDENCE_EXTERNALITY_UNVERIFIED`. A caller may therefore continue to use
the old signature, but cannot receive a READY result without the exact external
path text.

The CLI already reads the supplied path and passes that text into the API; the
new equality check preserves CLI behavior and closes the API-only mismatch.

## Preserved boundaries

- No candidate-contained/tracked evidence is accepted.
- Wrong candidate, forged digest, missing/extra/duplicate IDs and insufficient
  grade checks remain unchanged.
- The result ceiling remains documentary author-evidence readiness only;
  `authority` remains `AUTHOR_EVIDENCE_COVERAGE_ONLY__NEVER_SELF_CERTIFIES_COMPLETE`.
- Repository-tracking exclusion is not a timestamp, signer or PR-origin proof.
- Frozen commission/wrapper/12-ID/source tuples/grades/receiving requirements are
  unchanged.

## Limits

No final `RECEIVING_EVIDENCE.md`, delivered IDs, 12 same-head PASS package,
postcommit block, whole-MCR, economic/100k, source/native/science/actor or
protected integration is created or accepted here. Final same-immutable-SHA
external evidence and both independent receivers remain required.
