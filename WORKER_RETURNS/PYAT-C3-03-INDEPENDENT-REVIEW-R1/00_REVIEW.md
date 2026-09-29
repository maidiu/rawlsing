# PYAT C3-03 — independent bounded repair review under execution-capability block — R1

STATIC_REPAIR_DISPOSITION:

`PASS_AT_DECLARED_GRAIN`

EXECUTION_QUALIFICATION_DISPOSITION:

`BLOCKED_EXECUTION_CAPABILITY`

Overall:

`STATIC_PASS__EXECUTION_CAPABILITY_PENDING`

Reviewer branch:
`agent/reviewer-pyat-hq126-c3-03-physical-repair-r1`

Commission tip:
`eb0193fbb8b48b3fe455de553a88cc44b5a61170`

Reviewed worker return:
`ede7d350be23d0a340bed221da272d8c0124e049`

Reviewed semantic candidate:
`901e3e77f905847d3ef8d86b458280d8fe422dd0`

Reviewed execution-only commit:
`283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`

## Static holding

The C3-03 repair is correct at the declared bounded grain.

From prior independent review head `c874a134077e6eb416b584157d0209eabdd0d723` to semantic candidate, the only net changes are:
- the inherited C3-03 commission document;
- `rawlsing_next/pre553_physical_decoder.py`;
- `rawlsing_next/tests/test_closed35_d02_opaque_datetime_carrier.py`.

The actual repair commit from C3-03 commission tip `a68fb242e8a000a4b06037118e8eb804ee3365b5` to semantic candidate is exactly one commit changing only the decoder and D02 test.

### D02 exception boundary

The decoder now catches only failure of `value.item()` extraction. A successfully unwrapped exact built-in date/datetime/time is normalized in the `else` block outside the broad exception guard. Therefore `R5CodecError` from timezone-aware datetime/time carrier rejection propagates and cannot fall through to stringification through this item-unwrapped path.

No type widening was introduced: the branch still checks exact built-in `datetime.datetime`, `datetime.date`, and `datetime.time` types.

### Semantic-test environment ownership

The D02 test no longer imports `importlib.util`, `subprocess`, or `sys`, and contains no `pip` invocation or package-install bootstrap.

The test now contains explicit item-wrapper hostile coverage for:
- timezone-aware `datetime`;
- timezone-aware `time`.

Both require the same `R5CodecError` carrier-authority rejection as the direct path.

### Preserved holdings

The semantic candidate retains:
- G01 authority blob `31a9afd7d91ed4cb2fb1c1aab3ef86a5fdda1f85`;
- D01 test blob `8fc05965386055a208e5b3988112e67a2e6333e2`;
- source-backed C11 facade blob `8a761119e4a8d68eb291fc4edfadb52e027f8284`.

Those are identical to the prior C3-02 reviewed identities.

No historical CLOSED35 census harness, qualified-census receipt tree, or historical decoder infrastructure appears in the semantic-candidate tree.

### Execution-only separation

Semantic candidate -> execution commit is exactly one commit and changes only:
- `.rabochii/court_spec.json`;
- `.github/workflows/pyat-c3-03-physical-repair-source-free.yml`.

The court spec binds exactly semantic candidate `901e3e77f905847d3ef8d86b458280d8fe422dd0` and the exact six-file court.

The dedicated workflow satisfies the static contract:
- push trigger only on the assigned C3-03 branch;
- `ubuntu-latest`;
- CPython 3.11;
- pinned `pytest==9.1.1` and `pandas==2.3.3` provisioned before pytest collection;
- exact Python/pytest/pandas/pip capture;
- sorted `pip freeze --all`;
- SHA-256 of the freeze snapshot;
- protocol self-test;
- bounded court-spec validation;
- exact six-file governed court;
- separate receipt and environment-evidence artifacts.

Static disposition: `PASS_AT_DECLARED_GRAIN`.

## Independent execution retry

The commission allowed at most one independent retry of existing run `36627731035` at execution SHA `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`.

The reviewer used that one retry, creating attempt 4.

Attempt 4:
- run: `36627731035`;
- job: `109643559497`;
- head SHA: `283d2c5d2b187c4e62ae1aecb236a0b51ddeffb1`;
- conclusion: `failure`;
- `steps=[]`;
- `runner_id=0`;
- `runner_name=""`;
- no pytest collection;
- no protocol execution;
- no court execution;
- no artifacts.

This reproduces the same execution-capability condition as attempts 1–3. No source-free semantic/test result was produced by attempt 4.

Execution disposition: `BLOCKED_EXECUTION_CAPABILITY`.

## Adoption boundary

Static PASS is not execution PASS.

This review does not approve C3 adoption, does not certify the source-free qualification, and does not convert earlier historical C3-02 runs into C3-03 evidence.

No raw survey source was accessed.

## Terminal

`C3_03_STATIC_REVIEW_COMPLETE__EXECUTION_CAPABILITY_PENDING__HQ_ADJUDICATION_REQUIRED`
