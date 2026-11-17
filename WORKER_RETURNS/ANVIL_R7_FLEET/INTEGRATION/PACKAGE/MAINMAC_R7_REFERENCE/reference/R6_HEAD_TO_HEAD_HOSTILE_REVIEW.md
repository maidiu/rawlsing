# ANVIL R6 — Independent hostile head-to-head review

**Objects:** user-provided `oldMac_ANVIL_R6.zip` versus assistant-authored `ANVIL_R6_FINAL.zip`.

**Scope:** Review both as campaign *plans* for choosing the strongest feasible architecture. Neither is an executed architecture choice or an independent science/actor/owner accreditation. The findings below are synthetic structural attacks against the packages' actual code and documents, not claims that any production system is currently compromised.

## Executive ruling

**Neither R6 is suitable for an unconditional architectural-decision launch unchanged.** The oldMac package is **RED as shipped** because its own quality command cannot find a baseline manifest it explicitly requires. More significantly, both designs still allow a substantively discovered, potentially choice-reversing architecture criterion to be administratively neutralized instead of changing or holding the actual decision.

**There is no clean winner.** At package/preflight level, the assistant R6 is better: smaller, consolidated, and passes its supplied tests as delivered. At comparative-evidence and original-R5-conservation level, oldMac is stronger: finer metric floors, actual receipt-byte hashing and richer inherited test coverage. At source-value claim discipline, the assistant R6 is stronger: it requires `DOCUMENTED_RESPONDENT_RESPONSE`, an original code reference and a selected respondent record, rather than permitting a substantive source observation to arise from an instrument-consequence classification. At independent C-adjudication structure, oldMac is stronger: its stage checker requires a documented strongest surviving objection.

**Preferred basis for a single corrected R6:** retain the assistant's compact controlling operating texts and stricter respondent-claim typing, but adopt oldMac's complete material cost floor, raw measurement-byte authentication, stronger C objection gate and full inherited R5 baseline. Correct oldMac's packaging and both designs' B-discovery loophole. This is a bounded integration of useful work, not a new R7 campaign.

## Executed package tests

| Check | oldMac | Assistant |
|---|---|---|
| Archive ZIP integrity | ZIP CRC clean | ZIP CRC clean |
| Contents | 100 files, 1,389,692 uncompressed bytes | 34 files, 247,738 uncompressed bytes |
| Own archive manifest | 99/99 listed payloads hash-match; manifest omits the required nested R5 manifest | 33/33 payloads hash-match |
| Own primary quality command *as delivered* | `python3 tools/run_quality.py`: **RED_LOCAL_TEST_FAILURE**, exit 2 | `python3 tools/test_r6.py`: **38/38 PASS**, `python3 tools/preflight.py`: PASS |
| Isolated oldMac baseline repair | Restored unchanged `ANVIL_R5/MANIFEST.json` only in a disposable extracted copy; **9/9 tools/run_quality.py component commands PASS** | No repair necessary for baseline tests |
| Real A/B physical performance / original survey | NOT RUN | NOT RUN |
| Independent reviewer/owner receipt | NOT ESTABLISHED | NOT ESTABLISHED |

The absence of the nested R5 manifest is a delivery defect, not evidence that oldMac's underlying nine test suites are generally defective. The 44 inherited R5 payload files present in oldMac matched the corresponding original R5 archive contents. Repaired-copy results do not retroactively make the submitted ZIP green.

## Cross-executed hostile mutations

All outcomes below were rerun against the contained Python modules, with controlled synthetic fixtures. `PASS` means the local checker accepted the input at its documented structural scope, **not** that an external reviewer, scientific issuer or GitHub has approved it.

| Attack | oldMac R6 | Assistant R6 | Implication |
|---|---|---|---|
| A verified baseline numeric fixture wins | `A_DOMINATES_FULL_MATERIAL_DIMENSIONS` | `A_ADVANTAGE_AT_COMPLETE_SCOPE` | Both positive paths work synthetically |
| B discovers potentially decisive new criterion, which is not genuinely adjudicated or measured | **Still A dominates** after `PROVED_IMMATERIAL_WITH_COURT` text | **Still A advantage** after accepted amendment with no added cell | **Shared critical failure:** discovery can fail to change a verdict |
| Promote instrument-consequence classification into substantive `ORIGINAL_OBSERVATION` without individual original code/record | **Accepted** | Equivalent original respondent-value route requires original record/code; generic provenance guard is stronger | oldMac claim-meaning gate is underconstrained |
| Use fabricated receipt references | Raw A/B comparator requires actual byte files and matching SHA when evidence root supplied | A still wins with all receipt paths deliberately replaced by nonexistent files and updated self-attested evidence | assistant comparison authenticity gate is underconstrained |
| Claim C-scoped acceptance without a strongest surviving objection | R6 C stage explicitly demands objection and `could_reverse=NO` evidence | **Accepted with no objection field** | assistant independent terminal review is weaker in executable schema |
| Claim H1 received using unverified C/CAS evidence | **Accepted arbitrary C-file bytes** if supplied SHA matches; content is not parsed | **Accepted self-attested non-existent C/CAS references** with SHA-shaped metadata | Both need external authentication; oldMac is stricter on byte existence but not receipt semantics |
| Mandatory material cost coverage | 15 required case×metric cells; includes sparse 1/10/100, dense retained/scratch | 11 required cells; **zero required 1-query latency** or scratch metrics | oldMac better physical floor; both omit dense 100-query latency |

### OldMac critical finding O1 — delivered packet fails its own quality procedure

`tools/test_conservation.py` reads `R5_BASELINE/MANIFEST.json` unconditionally, while this exact file is absent from `oldMac_ANVIL_R6.zip`. The top-level manifest does not identify it as a payload. Therefore `tools/run_quality.py` returns `RED_LOCAL_TEST_FAILURE` (8 component passes, one component crash). Test-only restoration of the exact R5 manifest causes all nine component commands to pass. **Fix the archive and rehash; do not waive a broken launch command.**

### OldMac critical finding O2 — `PROVED_IMMATERIAL_WITH_COURT` does not entail a court

`tools/r6_comparator.py` requires fields describing a new B-discovered discriminator, but it accepts `disposition=PROVED_IMMATERIAL_WITH_COURT` based on strings, without authenticating a corresponding independent C finding or linking the disposition to an actual measurement/effect on the winner. In my test a discovered reverser that was not tested or verified left A's full-material domination untouched. The original R5 decision-frame failure survives in a new form. **A new potential reverser must either generate a measured comparison cell, carry a verifiable independent finding of nonmateriality, or force a conditional verdict.**

### OldMac major scientific finding O3 — original-source value claim does not require an original record

In `tools/r5_contract.py`, a source case with `legal_claim_kind=ORIGINAL_OBSERVATION`, asked/released/eligible/value facets, and `source_status=OBSERVED_INSTRUMENT_CONSEQUENCE` passes without a selected respondent-record ref or original-code ref. I reproduced this mutation and got zero validation errors. An observed consequence of the instrument's design is not necessarily an original respondent response. The claim model should require exact record/option evidence and a distinct `DOCUMENTED_RESPONDENT_RESPONSE` grade for respondent-level values, retaining design consequences as their own valid class.

### OldMac major receiving finding O4 — bytes are checked, C's meaning is not

`tools/check_stage.py` verifies the `authenticated_C_receipt.path` file's SHA, but does not parse its contents to reconcile the actual verdict, P2 cut, reviewer/builder grade and scope with the asserted metadata. A file containing arbitrary text passed as C receipt when its checksum matched. This is not a cryptographic break; it is a missing semantic readback. It is important precisely because the H1 grade is meant to depend on what C really concluded.

### OldMac strategic finding O5 — stronger material floor still not a whole-economic proof

`20_R6_MATERIAL_DECISION_CONSTITUTION.json` mandates 15 cells but W-D dense source workloads have no mandatory `query_100_wall_s`; W-J does not require dense higher-order 100-operation latency. The accepted matrix could omit a bottleneck capable of reversing the decision. The B-discovered-discriminator mechanism is supposed to address exactly this; see O2. **No fixed minimum is a substitute for substantive adversarial workload selection.**

### Assistant critical finding A1 — nonexistent source-run receipts can support READY

`tools/r6.py` accepts `independent_checked=true`, `raw_receipt_ref`, grade, source ref and 40-hex code HEAD without locating or hashing any raw evidence file. I replaced every A/B comparison receipt path with `/does/not/exist/unverifiable.txt`; the comparator still returned `A_ADVANTAGE_AT_COMPLETE_SCOPE` and the synthetic `DESIGN_READY_SCOPED` spine passed the local validator. This is a stronger attack than an absence of independent review: it demonstrates that the supposedly verified evidence is treated as a *boolean assertion*. **Real ready evidence must fail closed when the referenced bytes are unavailable.**

### Assistant critical finding A2 — B's pre-result discovery need not change the experiment

The assistant's `plan_errors` verifies an amendment's version, parent digest and presence of B-discovery text. But it does not require a newly identified discriminator to have a new cell or an explicit independently substantiated immateriality disposition. A new B source-justified choice-reverser may be recorded without adding anything to the matrix. The amended comparator still returns A victory. **This is the same central R5 failure as oldMac O2.**

### Assistant major finding A3 — mandatory evidence dimensions are too thin

`contracts/policy.json` requires 11 case×metric cells across the seven workload shapes. None requires `query_1_wall_s`; none requires `scratch_peak_bytes`, despite both being strategically relevant. The system can therefore report a fully compared scope while skipping cold-start-first-query cost and scratch blowups. This is a tangible weakness relative to oldMac's 15-cell policy, although oldMac too needs substantive B-discovered checks.

### Assistant major finding A4 — C and H1 gates are weaker than promised

The assistant `check_stage('C',...)` accepted `C_ACCEPT_SCOPED` with all three local review booleans set to true but with **no strongest-surviving-objection record at all**. `check_stage('H1',...)` also accepted `H1_RECEIVED_SCOPED` with self-asserted protected CAS and C receipt references not backed by actual files. Its prose instructs real independent verification, but the executable gate does not yet preserve the distinction. Adopt oldMac's strongest-objection schema and a byte-readback discipline, then verify C receipt *content*, not only filenames and hashes.

### Assistant continuity finding A5 — clean replacement risks lost inherited nuance

The assistant package is smaller and the operative documents are consolidated, a real advantage for worker comprehension. But it does **not** bundle the full original R5 baseline and its old tested APIs. It stores 118 IDs and source references, which conserves navigation but not independently all the inherited contracts. oldMac's explicit `22_R6_VALUE_AND_FUNCTION_CONSERVATION.md` and embedded R5 baseline are stronger historical-audit assets once the manifest is repaired. Keep full inherited source available as immutable reference, while preventing the old instructions from becoming controlling launch text.

## Strategy and organization comparison

| Category | Advantage | Reason |
|---|---|---|
| Launchability *as delivered* | Assistant | Own preflight green; oldMac quality command RED |
| Historical/R5 obligation nonloss | oldMac after one-file repair | Exact retained baseline + separate function-conservation map |
| Workload comparison floors | oldMac | More mandatory cells and clearer dense retained/scratch and sparse query-1/10/100 coverage |
| Raw measurement-file integrity | oldMac | Can verify file presence and SHA before winner; assistant metadata cannot |
| Source observation-claim semantics | Assistant | Original respondent value requires a response record/original code and documented respondent source |
| Independent C substantive objection | oldMac | Strongest surviving objection has an explicit acceptance gate |
| H1 receipt checks | oldMac, narrowly | C byte presence and hash verified, though semantic receipt readback still missing |
| Clean launch instructions and cognitive economy | Assistant | 34 compact files vs 100 R5-derived/overlapping files; one governing policy schema |
| Existing R5 tooling compatibility | oldMac | Retains prior validators, render pipeline and historical test suite |
| Decision-changing B discoveries | **Neither** | Both can neutralize a newly discovered reverser without real adjudication |
| Actual scientific/native empirical or builder proof | **Neither** | Both are planning packages with only local synthetic checks |

## Required bounded closure before launch

1. **Restore oldMac's one missing manifest and rebuild its archive.** Do not treat the repaired-copy pass as a pass of the submitted ZIP.
2. **Use one admissible-discriminator ledger:** every B-origin choice reverser must have (a) an inserted frozen comparison cell with matched evidence, (b) an independently authenticated C conclusion explaining precisely why it cannot affect the selected scope, or (c) a terminal conditional/hold. No author assertion, fluent paragraph, `decision_reverser=false`, or `PROVED_IMMATERIAL_WITH_COURT` string can discharge it.
3. **Upgrade comparison evidence to real immutable inputs:** required case×metric floor, exact source/shape/rights, A and B matched raw receipt bytes, source/performance falsifiers, no false dominance from excluded or unrunnable material cases. Keep a specific high-density repeated-query and first-query concern visible.
4. **Strengthen original-value claim typing:** documented respondent response + exact selected record/original-code ref, separate instrument consequence/design and interpretation, correct target unit/attribution/wave/country and negative propagation; one fresh instrument ambiguity beyond frozen fixture examples.
5. **Make C/H1 real readbacks:** C explicitly answers strongest surviving objection and builder-first-consumer readiness. H1 reads C's content at the frozen HEAD and checks meaning, not merely the hash of arbitrary bytes; real CAS/authority remains externally authenticated. No sourcefree test grants native/science/actor rights.
6. **Ship one coherent operating package and one immutable evidence archive:** keep the shorter controlling instructions with unambiguous verdict vocabulary; retain R5 as independently verifiable, nonoperative reference. Preserve 118 inherited identifiers with their statuses, source meanings and first-consumer rules, not 118 new builds.

**Final disposition:** `BOTH_REVISE_EXACT_DEFECTS__NO_ARCHITECTURE_WINNER__NO_LAUNCH_OF_UNCONDITIONAL_SELECTION`. This ruling does not forbid lawful current sourcefree C11 engineering or other ongoing first-consumer work. It states only that neither R6 package is ready to claim a reliable unconditional architecture selection. The next step should be one direct corrected campaign, not another new commission/fleet/R7 philosophical review.
