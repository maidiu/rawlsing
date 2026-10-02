# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT AT17/N10E SUCCESSOR REQUALIFICATION + C1-03 LARGE JOIN RERUN — R1
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq166-at17-requal-c1-03-join-rerun-r1`

Exact branch base:
`8b2c45d754a0ff3922a7b60c510c9e96df995bc5`

This base is the historical failed large-join return. Its court was:
`434 passed / 1 failed / 435 collected`

The sole failure was the stale R8 AT07 composed-result identity assertion.

## Governing accepted successor oracle

Accepted branch:
`integration/pyat-hq166-at07-successor-spine-accepted-r1 @ 069ac61b5c90486e5b7bb633135b4743dfbd55df`

Oracle freeze:
`92ddee2241a78b46394665d325e5ebf0e75adf40`

Independent review:
`2a454f4cd6359d149269dbbbe5497ea1c263f9c8`

Governing Astra decision:
`a2e7767ecec9ecb6d241861628759f2e933920d5`

Adopted successor identities:

Forward:
`01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`

Reverse:
`a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca`

Historical R8 identities remain historical only:

Forward:
`03610f9d91b23cfb6f862dc91b5de92c7f4e4b8e44a53b9efdacb1cf73af6b9e`

Reverse:
`1202822cf98d802c04440328496dc64ee02e6d6030a3da6c9bf10ef1a6490a3c`

## Mission

Perform **one combined job**:

1. bring the HQ-adopted successor-spine package into the historical joined tree;
2. narrowly requalify AT17/N10E current identity binding against the adopted successor oracle in both directions;
3. preserve the R8 spine as historical C1-01 evidence;
4. rerun the entire C1-03 large join and all accepted/join-specific courts;
5. return one integrated result.

Do not split this into an AT17-only return and a later join return.

A PASS here still requires one independent integration review. Do not self-adopt.

---

# PHASE 0 — exact ancestry and accepted-blob lock

Before editing:

1. Verify branch base exactly:
   `8b2c45d754a0ff3922a7b60c510c9e96df995bc5`.

2. Verify historical tested join commit:
   `39046d22db18eb69cb9cdd3ce1865e7bc8dec1f0`.

3. Verify the historical failed run:
   - 413 accepted baseline cases;
   - 22 join-specific cases;
   - 435 collected;
   - 434 pass;
   - 1 fail;
   - sole failure = stale R8 current composed-result identity assertion.

4. Verify the four frozen production blobs remain:

   - A state/route:
     `3a5e3db8a0897900d0b2606813bda7c3f586d46e`

   - AT17 provider:
     `23167aa25291fb148b1e3cf210ac33fe7769b783`

   - R authority maintenance:
     `547e6bf20354f38179a0e2600de64c7cb2260ea0`

   - R replay dependency:
     `47e65aad5e0a8df7af6fda72fc8807a002e556ce`

5. Verify current analytical-composition owner blob:
   `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`.

If any exact identity differs, stop:
`SUCCESSOR_REQUALIFICATION_PROVENANCE_DRIFT__HQ_ADJUDICATION_REQUIRED`.

---

# PHASE 1 — merge the accepted successor oracle

Ancestry-preservingly merge:

`integration/pyat-hq166-at07-successor-spine-accepted-r1 @ 069ac61b5c90486e5b7bb633135b4743dfbd55df`

into this worker branch.

This merge exists to bring the accepted oracle package and HQ adoption record into the joined tree.

After the merge:

- verify the accepted successor package is byte-identical;
- verify no production owner changed because of the merge;
- verify all historical R8 artifacts remain unchanged;
- record exact merge base and merge commit.

Do not copy only the two digest strings into a test file and discard the oracle package.

---

# PHASE 2 — preserve historical R8 truth explicitly

Astra requires the old R8 assertion to remain as historical evidence.

Do **not** delete, skip, xfail, weaken, or silently rewrite the historical claim.

Correct the old conflation between:
- historical C1-01 identity truth; and
- current C1-02 identity truth.

Create/retain an explicit historical regression proving:

- R8 spine blob is still exactly:
  `462bb282ddc2cc9667f1890f2d65f2fae9a3a72c`;
- historical forward digest remains:
  `03610f9d...`;
- historical reverse digest remains:
  `1202822c...`;
- the historical spine still binds the same historical source/query/witness/evidence identities it originally recorded;
- the historical spine is not treated as the current expected composed-result digest under the C1-02 owner.

The previous failing P7 obligation may be renamed/restructured only if its historical assertion remains equally strong and explicit.

---

# PHASE 3 — current AT17 successor requalification, BOTH directions

Using the real public provider path and existing accepted source-free fixtures, execute:

### Forward
POSITION=P1 -> ANSWER

Expected:
- denominator 60;
- cells yes=54, no=6;
- exact fraction yes=9/10;
- consumer state `EXACT_SUPPORTED`;
- composed-result identity exactly:
  `01c381d3f3c386cfc22fd2f57b8e2c244771ddf1529d4f8ab8c7b1cf41bd50dd`.

### Reverse
ANSWER=yes -> POSITION

Expected:
- denominator 62;
- cells P1=54, P2=8;
- exact fraction P1=27/31;
- consumer state `EXACT_SUPPORTED`;
- composed-result identity exactly:
  `a3bd7e85ae14babb5ac5a12b0bcc57a8cdf3eccf8f43394895903dc43aca40ca`.

For **each** direction prove the actual production `composition_result.identity_material()` canonicalizes to the independently adopted successor preimage, not merely that its final digest matches.

At minimum compare:

- all 38 conserved historical fields;
- all six successor additions;
- complete canonical preimage;
- final digest.

The six current direct-path additions must be exactly:

- `discovery_receipt_refs=[]`
- `discovery_frontier_ref=None`
- `recursive_handoff_refs=[]`
- `recursive_lineage_refs=[]`
- `joint_component_count=1`
- `joint_order_semantics="SEMANTIC_ORDERED"`

No field may be fit to production output. The expected preimage comes only from the adopted successor oracle.

---

# PHASE 4 — AT17 semantic/custody preservation

Requalify both directions through the real chain:

`provider -> composition -> generated evidence -> named positioned-subject consumer`

Verify unchanged:

- exact source law;
- universe/release scope;
- query authority;
- predicate/query identities where conserved;
- 16-field witness custody;
- evidence geometry;
- raw support and exact fractions;
- generated evidence identity where the successor law says it is conserved;
- consumer result semantics;
- refusal behavior;
- anti-handwritten/precomputed geometry law;
- changed-source P6 law;
- replay behavior;
- fresh-process provider replay.

A changed composed-result digest is allowed **only** because of the adopted six-field preimage expansion. Do not treat this as a blanket waiver for any other downstream identity drift.

If any other previously accepted identity changes without exact derivation from the successor law, stop:
`AT17_REQUALIFICATION_UNEXPLAINED_IDENTITY_DRIFT__HQ_ADJUDICATION_REQUIRED`.

---

# PHASE 5 — AT17 regression surface

The historical accepted provider suite had 30 tests.

Preserve all existing semantic obligations.

Add explicit successor tests, including at minimum:

1. historical R8 forward identity preserved as historical;
2. historical R8 reverse identity preserved as historical;
3. current forward complete preimage equals adopted successor;
4. current reverse complete preimage equals adopted successor;
5. current forward digest equals adopted successor;
6. current reverse digest equals adopted successor;
7. wrong successor direction fails;
8. one six-field omission fails;
9. one six-field wrong value fails;
10. old R8 digest cannot masquerade as current C1-02 digest.

Do not reduce the old provider test surface merely to keep total counts tidy.

Record old count, new count and exact delta.

---

# PHASE 6 — rerun the large C1-03 join on successor-qualified AT17

The previous 22 join-specific courts all passed and remain authoritative obligations.

Rerun them all.

Additionally prove the joined tree now uses the successor-qualified AT17 identities:

- the real AT17 composition dependent used by lifecycle integration carries the current successor composed identity, not the historical R8 identity;
- any graph-dependent exact ref derived from the composition uses the successor content hash where that contract binds it;
- historical R8 refs never become CURRENT merely because they remain retained evidence;
- replacement / explicit noncurrent / unaffected CURRENT behavior remains unchanged;
- zero-release known dependent remains `NOT_GOVERNED / NO_GOVERNING_RELEASE`;
- unknown dependent remains `NOT_GOVERNED / OWNER_UNKNOWN_DEPENDENT`;
- A negative analytical states remain distinct from R lifecycle states;
- mutation / rollback / replay remain green.

Add join-specific successor cases if the existing 22 do not explicitly prove those points.

---

# PHASE 7 — replay/fresh-process grades and known bridge limitation

Preserve the accepted distinction among:

- serialization replay;
- explanatory replay;
- fresh-process product replay;
- fresh empirical recomputation.

Run:

- AT17 accepted fresh-process provider replay;
- R accepted checkpoint/replay courts;
- join-specific fresh-process lifecycle reconstruction.

The previously recorded limitation remains explicit:

There is no accepted single fresh-process bridge that carries
`provider recomputation -> named consumer -> lifecycle restore`
as one end-to-end owner contract.

Do not fabricate such a bridge.

This limitation is nonblocking at the current declared grain unless the current work uncovers a concrete reason it prevents lawful join acceptance.

If closing it would require new owner semantics, return the exact obstruction to HQ/Astra rather than inventing one.

---

# PHASE 8 — production blob conservation

No accepted production implementation is authorized to change.

At final HEAD verify byte identity for at least:

- `rawlsing_next/pre553_analytical_state_and_route.py`
  = `3a5e3db8a0897900d0b2606813bda7c3f586d46e`

- `rawlsing_next/pre553_empirical_possibility_provider.py`
  = `23167aa25291fb148b1e3cf210ac33fe7769b783`

- `rawlsing_next/pre553_authority_maintenance.py`
  = `547e6bf20354f38179a0e2600de64c7cb2260ea0`

- `rawlsing_next/pre553_analytical_replay_dependency.py`
  = `47e65aad5e0a8df7af6fda72fc8807a002e556ce`

- `rawlsing_next/pre553_analytical_composition.py`
  = `604c8d591d4cc2b646e9b149cdb233fc9d69cf6b`

Allowed implementation terrain is **tests/fixtures only**.

If lawful requalification appears to require production-owner mutation, stop:
`ACCEPTED_OWNER_CHANGE_REQUIRED__HQ_ADJUDICATION_REQUIRED`.

---

# PHASE 9 — full final court

The historical unique accepted baseline was:

`413 tests across 14 accepted suites`

The historical join-specific court was:

`22 tests`

The previous total was:

`435`

The provider suite will now gain declared successor-requalification tests; the join suite may gain declared successor-integration tests.

Final execution must include:

1. all fourteen accepted suite files;
2. the complete provider suite after requalification;
3. the complete join-specific suite after successor integration;
4. all fresh-process runners invoked by those suites.

Before running, construct the test-file list from the filesystem and assert every path exists. Do not hand-type a fragile list that can silently produce a false-green no-tests run.

Required final result for PASS:

- zero failed;
- zero errors;
- zero skipped;
- zero xfail unless already historically present and explicitly reconciled;
- exact per-file counts;
- exact old→new test-count delta;
- exit status 0;
- clean final tree;
- exact final commit tested.

The old `434/1` run remains historical failed evidence. Do not rewrite it.

---

# PHASE 10 — return package

Write:

`WORKER_RETURNS/PYAT-AT17-SUCCESSOR-REQUAL-C1-03-JOIN-RERUN-R1/**`

Required:

- `00_RETURN.md`
- `01_LINEAGE_AND_ORACLE_ADOPTION_RECEIPT.json`
- `02_AT17_FORWARD_REQUALIFICATION.json`
- `03_AT17_REVERSE_REQUALIFICATION.json`
- `04_HISTORICAL_R8_CONSERVATION.json`
- `05_AT17_CUSTODY_AND_REPLAY_MATRIX.json`
- `06_JOIN_SUCCESSOR_INTEGRATION_RECEIPT.json`
- `07_PRODUCTION_BLOB_CONSERVATION.json`
- `08_EXECUTION_RECEIPT.json`
- `09_FINAL_DISPOSITION.json`

## Allowed dispositions

- `PASS_AT17_SUCCESSOR_REQUAL_AND_C1_03_JOIN_RERUN__INDEPENDENT_INTEGRATION_REVIEW_REQUIRED`
- `AT17_REQUALIFICATION_UNEXPLAINED_IDENTITY_DRIFT__HQ_ADJUDICATION_REQUIRED`
- `ACCEPTED_OWNER_CHANGE_REQUIRED__HQ_ADJUDICATION_REQUIRED`
- `SUCCESSOR_REQUALIFICATION_PROVENANCE_DRIFT__HQ_ADJUDICATION_REQUIRED`
- `INTEGRATION_CONTRACT_GAP__HQ_ADJUDICATION_REQUIRED`
- `ARCHITECTURE_WARRANT`

No self-adoption.
No control merge.
No C1-R.
No Omega-1 yet.
No C4/live production.
No raw sources.
No C7.
No PRE-V3→V3 actor/person implementation.

Terminal:
`AT17_SUCCESSOR_REQUAL_C1_03_JOIN_RERUN_RETURNED__HQ_ADJUDICATION_REQUIRED`
