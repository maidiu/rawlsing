# Negative setup — prepared, not executed

Private altered fixtures are present in the controller-only execution directory:

- `changed_decision.json` — exact decision altered; expected
  `REFUSE_CURRENT_AUTHORITY_MISMATCH`.
- `revoked_scope.json` — status/current scope revoked; expected
  `REFUSE_CURRENT_AUTHORITY`.
- `wrong_release.json` — wrong manifest/source roots; expected
  `REFUSE_RELEASE_OR_SOURCE_MISMATCH`.

No evaluator was run. These fixtures are for the future accepted implementation.
