# PYAT HQ280 F8D-R — INDEPENDENT C1→M2/B5 RUNTIME AND HOSTILE REVIEW R1

**Disposition:** `F8DR_EXECUTION_HOLD_AND_SOURCE_VISIBLE_TECHNICAL_GAPS__NO_OPERATIVE_C1_OR_G0B_ADOPTION`.
**Required terminal:** `HQ280_F8DR_INDEPENDENT_C1_M2_B5_PYTEST_AND_HOSTILE_RETURNED__NO_OPERATIVE_C1_OR_G0B_ADOPTION`.
**Law:** `HQD-2026-10-10-280`.
**Reviewer sealed startup:** `3dadce2e35c6c9d7e84e225090bf7cac3a63f129`.
**Inspected candidate:** `69bb0fc69175b2f6048b00cfa47dc852593798c0`, Git tree `3af7edd93601d16b1a802ba12c4ed64c0890b8f2`.
**Candidate code/test blobs:** `2f6ab22c5f079b24fe81a3611bb21dcce7b9854f` / `2c4617e132293dfae459ded56b2d0f79d211c5f3`. Existing C1/C1-03R/M2/B5 owner blobs match candidate commission.

## Runtime — execution HOLD, never a PASS

Independent runtime has Python 3.13.5 and pytest 9.0.2. Candidate Git contents were inspected read-only through the private GitHub connection, but **the exact Git tree is not available in the Python filesystem**. `git ls-remote https://github.com/maidiu/rawlsing.git` failed (exit 128, DNS cannot resolve github.com). Attempting the prescribed `python -m pytest -q -vv rawlsing_next/tests/test_pre553_c1_immutable_release_binding.py` in isolated local checkout location returned exit **4** with **zero collected** and **file not found**. This did **not** execute the actual 15-test suite. Five positive and ten negative authored cases are **all UNRUN**; zero observed PASS, zero observed case FAIL. No candidate-commit GitHub status or PR workflow run was observed. B2-R's separate 8/8 was not borrowed.

## Static owner inspection

F8D's build function does use accepted C1 typed `AnalyticalCompositionResult`, native evidence preimage hashing, real M2 repository/subject/five closures/release, C1-03R registration, and real B5 lifecycle subject construction. The resulting contract is nonissuing: `grant=None`, `external_issuer=None`, `authorizing=False`, `REPLAY_BLOCKED_MISSING_AUTHORITY`, `REBUILD_BLOCKED`, historical-only C1-03R replay. B5's original subject would be stageable/registerable and refused for publication at its blocked replay state *by control-flow inspection only*. No operative permission, published CURRENT or G1 serving claim follows.

## Five owner-contract technical gaps not covered by the authored tests

**H01 — q1/q2 label/condition/target spoof.** `_ALLOWED_CELLS` checks only conditioner count and denominator (q1:1/2; q2:2/1). The wrapper does not pin original q1 = `q(C|A=1)`, q2 = `q(C|A=1,B=0)`, or target `C` to the G1 owner-held expected identities. Genuinely computed wrong-condition C1 objects with correct count/denominator can be relabeled.

**H02 — q2 numerator value identity missing.** Frozen four-row source: R00=(0,0,0), R01=(0,1,1), R10=(1,0,1), R11=(1,1,0). Legitimate q1 uses R10/R11: n=2, C0=1,C1=1. Legitimate q2 uses R10: n=1, C0=0,C1=1. Alien q2 A=1,B=1 uses R11: n=1, C0=1,C1=0. Authored P01 only sorts supports `[0,1]`, so the reversed alien result satisfies its numerical assertion. No fixed-value oracle exists in F8D `_verify`.

**H03 — risk member cross-preimage absent.** `_verify` checks `geometry.denominator.risk_set_ref` and `denominator_member_refs`, but never checks `geometry.denominator.risk_set_member_refs == composition.risk_set_member_refs`. A recomputed composition hash can carry altered risk-member refs while native evidence geometry stays unchanged. N03 only changes `risk_set_ref` without rehashing; N04 tests duplicate denominator refs.

**H04 — consumed model/walkback authority closure gap.** `PositionedSubjectPossibilityModelRule.model_authority_ref` and `.walkback_authority_ref` are mandatory consumed model authorities. F8D's `auths` union comes only from empirical C1 composition/evidence authorities, not these consumer rule authorities, so they are not explicitly in M2 AUTHORITY, B5 authority snapshots, or C1-03R authority edges. The model-rule *hash* in DETERMINANT is not the same as an authority revision edge.

**H05 — C1-03R graph underprojects exact determinants.** Registration stores `determinant_exact_refs=determinants` but sets `dependency_edges_from=dependencies` (a narrower set). The accepted `AnalyticalDependencyRegistry.build_graph` emits edges only from `dependency_edges_from`, not `determinant_exact_refs`. It therefore misses at least the F8D-generated model-rule exact ref and other added determinant identities. P02 tests existence of registration, not completeness of graph edges / affected-set changes. The separate B5 determinant graph does not prove the C1-03R graph complete.

**Additional trust-boundary limitation:** B5 stage/register/publication methods accept opaque caller-supplied lifecycle records; its publication gate tests replay state, not a cryptographically verified producer credential. Original F8D records are explicitly blocked. This is no evidence of an actual unauthorized publication, but also no universal issuer/currentness guarantee.

**The listed hostiles were derived from source-control flow and the independently calculated fixture oracle. They were NOT dynamically invoked.** Source-visible logical gaps remain to be tested on a real repository runner. No accepted C1/M2/B5/G1/I4 code was modified.

## Exact outstanding gates

1. Acquire pinned candidate checkout and execute all 15 pytest cases with full per-case logs, then additional original-vs-alien predicate, numerator-label, risk-member rehash, model authority revocation, graph affected-set and replay-state spoof hostiles.
2. Fix or prove owner-pinned C1 q1/q2 predicate, target, denominator, response-label, authority/determinant closure and graph completeness; independently review the producer candidate. This review does **not** approve narrow development-level technical adoption.
3. Locate a competent independent C1 immutable-product issuer, exact source/semantic producer custody and adopted immutable release/retained replay permission. Current candidate contract remains non-issuing.
4. Establish actual B5 publication/CURRENT/as-of selection and independently qualified source-free selected B5→owner-authenticated G1 origin/service. Historical C1-03R narration is not fresh-process.
5. Keep I4 M1-only. Keep EE14 G0b operative grant HELD pending separately competent model/use signer, exact allowed identity tuple and HQ adoption. No real-source, N10W, actor or V3 escalation.

**HQ recommendation:** `F8D_RUNTIME_HOLD__TECHNICAL_CLOSURE_INCOMPLETE__C1_OWNER_ISSUER_HOLD__B5_SELECTED_G1_UNPROVED__OPERATIVE_G0B_HELD`. This is a review recommendation, not an HQ decision or adoption.
