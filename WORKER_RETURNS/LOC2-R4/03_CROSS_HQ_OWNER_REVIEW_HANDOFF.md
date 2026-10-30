# Cross-HQ owner review handoff — LOC2-R4

## Status

`CANDIDATE_PATCH_ONLY`. This return is not adoption, not owner CAS, not a required-check installation and not a merge. PR521 remains the source under review; the canonical `SESSION_LOCATORS.json` was not mutated by this worker.

## Exact repaired source

| Surface | Before (PR521 `f246eadd…`) | Candidate |
|---|---|---|
| verifier | `1a43988267c589d2198c9f1b8b7faf92967481be` | `9936405646e6b8620ee986fe19658e2024a76602` |
| G1–G6 unittest | absent | `65358f11fe7b6184e435404980e3d3d6167ecc03` |
| template | `2414990807dee39c95cf2331ed58ad29e017c5ae` | `e80fad987d14cc6fab868299e32960b6eabf60ea` |
| session law | `b817092d54236f51565a1739949b2c319bf7f815` | `a5889baca326e9cfcc38f9a477878596ecaaa1d7` |
| workflow | `16f06da5e9d120983491b7dd3984d7fd9c24af17` | `ff0c3afd5154b95390d14a9edc4174674363ecab` |
| canonical registry | `be4965022a13729344f9723d958a1edc458000e2` | **unchanged by this candidate** |

The exact patch and commands are in `02_SESSION_REGISTRY_PATCH_AND_TESTS.md`; the machine-readable before/after is in `01_G1_G6_NEGATIVES_AND_VALID_CASES.json`.

## Review recipe

```sh
git worktree add --detach /tmp/loc2-r4-review f246eaddbeeb86677c3ae67a075390501e233f38
cd /tmp/loc2-r4-review
git apply <the exact patch from 02>
python3 -m py_compile CROSS_HQ_CONTROL_ROOM/verify_session_locators.py \
  CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
python3 CROSS_HQ_CONTROL_ROOM/verify_session_locators.py --selftest --repo .
python3 -m unittest -v CROSS_HQ_CONTROL_ROOM/test_session_locator_integrity_r2.py
python3 CROSS_HQ_CONTROL_ROOM/verify_session_locators.py --repo . \
  --baseline-ref f246eaddbeeb86677c3ae67a075390501e233f38 \
  --require-sha --require-sha-branch
```

Expected: original six witness lines still pass; `PASS G1`–`G6`; `Ran 21 tests ... OK`; canonical 18-row baseline and real SHA/branch readback pass. The reviewer must obtain the SHAs on the declared branches in their own clone; a missing local commit is a typed `SHA_NOT_LOCAL`/HOLD, not a reason to invent a URL or machine.

## Owner decisions required

1. **PR521 maintainer/author:** accept or reject the exact five-file candidate. Preserve the original green six tests; do not revert G1–G6.
2. **Cross-HQ registry owner:** run the repaired verifier against the canonical `SESSION_LOCATORS.json` with a prior baseline. Append QF2 revision 2 (`RETURN-QF2-R2`, supersedes `DISPATCH-QF2-R1`) through your own authorized CAS; do not let this worker write the canonical registry.
3. **PRE-MAIN owner:** install/read back the repaired `--selftest`, 21-test unittest and baseline check as a required context. Branch protection, owner CAS and merge remain separate and are not granted here.
4. **Operator / original authors:** confirm the actual `oldMac`/`mainMac` labels and app-visible titles for rows still `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`. Preserve `UNKNOWN` where the evidence is genuinely absent; never infer the Mac from macOS, x86_64, a path, an account or a model.
5. **Pyat/Sorok/HQ grok owners:** use the repaired fields as discoverability/return custody only. This is not a Rule A/T/C8/C11/C12/Pyat/ADP source permission or a scientific result.
6. **Distinct control reviewer:** review this exact cut; the worker is not the reviewer and does not self-adopt.

## QF2 representation

The exact reported QF2 session is representable without source authority:

- device `oldMac`, evidence `scutil --get ComputerName returned oldMac; hostname Matthews-MBP.lan`
- harness `Codex`, agent name `Codex`, agent mode `Default`
- session title `Review QF2 Sorok fan-in`
- session id `01a18e10-6391-7a52-8950-dec3073e1800`
- suggested title independently recorded
- `session_locator_type=APP_SESSION_ID`, `locator_status=APP_TITLE_AND_SESSION_ID_VERIFIED`
- `source_authority=false`, `adoption=false`
- no model selector or source-owner delegation asserted

The QF2 row is in `01_...json` and in the unittest. It is **not** written into the canonical registry by this worker.

## Exact unresolved gates

- PR521 is draft/unmerged; no protected required check or owner CAS readback.
- The canonical registry still has 17 `UNKNOWN` devices and 9 `SEALED_NOT_LAUNCHED` dispatch rows; operator confirmation remains outstanding.
- Historical session titles/IDs remain unknown for most rows; they must stay `UNKNOWN` with `SESSION_NOT_FOUND__REQUIRES_OPERATOR_CONFIRMATION`, not be invented.
- The repaired verifier is offline consistency only; it cannot authenticate a Mac, user, provider session or source authority.
- No source-native/CAN/ADP/SCI05/Pyat/C11/C12, production consumer or merge is established.
- The exact remote return SHA is reported externally after push; a commit cannot contain its own final SHA.

## No self-adoption

This worker did not merge PR521, modify PRE-MAIN/Pyat/Sorok owner branches, write the canonical registry, issue a source grant or claim the first production consumer. A distinct reviewer and the original owners must decide.
