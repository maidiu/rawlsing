# Scoped review verdict and living-Programma interface

## 1. Single decision

**`REVISE_EXACT_DEFECTS`**

R3 is a real source-object and forward-product-link repair. It is not yet
acceptance-grade as the source-exact static O-INDEX map because the required
ACTUAL-consumer provenance negative is accepted, the six product backward
links are still generic, and source-kind/consumer semantics are not
Git-derived. The defects are finite and repairable; this is not a new source
census, a new framework or a request to redo the 102/17 source recovery.

## 2. Three separate courts

### ENGINEERING — `REVISE_EXACT_DEFECTS`

Accepted at this scope:

- 167 manifest rows + 3 references resolve to exact Git objects; 166 blobs + 1
  tree; 21 commits; exact object ids, commit timestamps and R15 tree file list.
- The eight named R2-IR source defects are repaired: B1/B2/B3/BP2P4J blob
  fills, B3A/B3AS/S39_S52 exact paths, R15_V2 tree identity.
- `validate_index.py` PASS with 144/23/4/80/461/3/46/0/66.
- `verify_source_manifest.py` PASS with 167/3/0 errors.
- 21 pytest tests + 4 subtests pass; 21 unittest tests pass.
- Source-object, timestamp, Pyat object, R15 tree-as-blob, removed lineage,
  missing S0/forged S16, product-forward-path and untyped-cycle negatives fail
  for their claimed reasons.
- Six specific forward L0-L5 product chains, owner slots, alternatives and
  falsifiers exist.

Not accepted:

1. **Actual-consumer provenance is not Git-bound.** A fabricated `ACTUAL`
   consumer with a fake or real-but-unrelated Git object in both registry and
   manifest, with a recomputed digest, passes both tools. The current
   `NONE_PROVEN_AT_PREMAIN=135 / ACTUAL=0` state is not a protected invariant.
2. **Source-kind/consumer semantics are not externally anchored.** A joint
   `source_kind` relabel, a joint `required_consumer`/`first_consumer` relabel,
   and a different real source object all pass both tools.
3. **Six product backward links remain generic.** `S5/S7/S11/S13/S14/S15`
   still have `S# -> L1_GOVERNANCE -> L5_S_WORKSTREAM_PRIMARY_SOURCE` in
   `backward_paths`; no product-specific reverse edge/path exists.
4. **Stale notes.** `s0_s16_primary_source_correction.note` and
   `backward_paths["*_limits"]` still reference `L5_SOURCE_HOLD` / a generic
   source hold; `05_VALIDATOR_AND_READBACK.md` says ACTUAL requires
   callable/source evidence but only non-empty fields are checked.

### SCIENTIFIC — `HOLD`

All 17 original S0-S16 questions/outputs are exact in the historical Program
Map. The six specific workstreams now have source-derived candidate forward
paths, owner slots and falsifiers. No workstream output is complete, no
falsifier is run, no human alpha or native person is evidenced, and no
scientific issuance is made. S5/S7/S11/S13/S14/S15 remain
`EXPLORATORY_REQUIREMENT_NOT_ISSUED` or `EXISTING_SOURCEFREE_PARTIAL`. This is
a navigation substrate for HQ, not the HQ scientific/product judgment.

### AUTHORITY — `HOLD`

No original CAN/ADP/SCI05, Pyat N11/N12/C0, C9/C12, native B/A5, owner
adoption, PRE-MAIN merge, PR #559 edit or self-adoption is issued. The four
assets remain author-tested, unadopted candidates. R3 remains
`RETURNED_UNADOPTED` candidate material until a distinct competent owner/HQ
adopts a scoped candidate.

## 3. Precise minimal corrections

### 3.1 Consumer provenance (required)

In `validate_index.py`:

- For every Sorok row and every Pyat row with
  `actual_consumer_state == "ACTUAL"`, require `actual_consumer_evidence` to
  match a separate consumer-evidence manifest, not only the source manifest.
- If this cut intends no ACTUAL rows, hard-fail any `ACTUAL` state and assert
  the exact counts `NONE_PROVEN_AT_PREMAIN == 135` and `ACTUAL == 0`.
- If ACTUAL rows are allowed later, require `commit`, `path`, `object_type`,
  `object_id` and a Git-resolvable consumer object, plus a named consumer
  owner/edge.

In `verify_source_manifest.py`:

- Iterate every non-null `actual_consumer_evidence` (Sorok and Pyat) and
  resolve `commit:path` with `git cat-file -t`, `git rev-parse` and commit
  time. Fail `actual_consumer_evidence` on missing, wrong-type, wrong-id or
  wrong-time evidence.
- Do not silently ignore consumer fields when the source object is valid.

Add at least these negatives:

- fabricated ACTUAL consumer with a fake Git object;
- ACTUAL consumer with a real but unrelated Git object;
- joint registry + manifest + digest change from `NONE_PROVEN` to `ACTUAL`;
- unchanged 135/0 count check.

This closes the exact R2-IR requirement to "require evidence for the actual
`first_consumer`/edge" and the commission's acceptance-grade consumer check.

### 3.2 Source-type and consumer semantics (required if claimed as verified)

- Derive `source_kind` from `object_type` and repository path class, or mark it
  explicitly as authored metadata with no Git-authenticated status.
- Derive or externally anchor `required_consumer`/`first_consumer`; a joint
  relabel must not pass.
- If provenance substitution to a different real object must fail, add an
  owner-signed per-row source anchor independent of `source_manifest.json`.
  Otherwise state the proof limit: the manifest proves object existence, not
  historical/owner authenticity.

Add the joint-tamper negatives for `source_kind` and consumer labels.

### 3.3 Product backward links (required)

In `02_L0_L5_LINKED_ORCHESTRATION_INDEX.json`:

- For S5/S7/S11/S13/S14/S15, add a product-specific backward path or reverse
  edge that traverses the specific `L1_S*`, `L3_S*`, `L4_S*`, `L5_S*` and
  `L0_S*` nodes, not only `L1_GOVERNANCE`.
- Keep the existing forward chains; do not replace them.

In `validate_index.py`:

- For each of the six, assert the backward path contains the specific
  `l1`, `l3`, `l4` and `l5` nodes and does not route only through
  `L1_GOVERNANCE`.
- Add a negative that removes the specific backward link.

### 3.4 Documentation cleanup

- Replace the `L5_SOURCE_HOLD` / generic source-hold notes with
  `L5_S_WORKSTREAM_PRIMARY_SOURCE`.
- Change the `05_VALIDATOR_AND_READBACK.md` ACTUAL wording to state exactly
  what is checked (non-empty fields and registry/manifest equality) until the
  Git consumer resolver is added.
- Prefix the seven `NONE_PROVEN` prose `first_consumer` labels containing
  "actual" with `REQUIRED_ONLY:` or add `current_importer: NONE_PROVEN`.

## 4. What a scoped acceptance would have covered

If the engineering corrections above are made and independently re-executed,
the index can be accepted only as:

- a static, source-exact navigation map of 102 inherited definitions, 17
  historical S0-S16 exploratory workstreams, 23 separate Pyat rows and four
  author-tested, unadopted assets;
- a navigation aid with explicit holds and no native/science/priority claim;
- a bounded input to the living Programma, not the living Programma itself.

Even then it would not be PRE-MAIN adoption, owner adoption, scientific
issuance, a real Pyat native world or generated human alpha.

## 5. Living-Programma interface

- The proposed Programma Rawlsing living-reference implementation may read R3
  only as `RETURNED_UNADOPTED` candidate material.
- It must not treat the 219-node / 461-edge map as the living Programma, an
  automatically updated versioned work program, live worker status, gap
  prioritization or a roadmap.
- It must not treat the six forward paths as implemented product functions or
  the four assets as adopted consumers.
- If this review's corrections are made and the candidate is scoped-accepted,
  the living reference still needs explicit owner adoption before any
  canonical-status change.
- No priority is implied. `PRIORITY`, `JOINT_TEST`, `S0_S16_SOURCE`, `F1CR_PATCH`
  and `V3_ZIP_CONTAINER` remain owner/HQ questions, not index decisions.

## 6. I3 handoff

The exact returned branch tip must be examined by a distinct competent
owner/HQ. The handoff asks for one of:

1. a bounded R4 engineering repair of the four items in section 3, followed by
   an independent re-execution of the full receipt; or
2. a deliberately narrower scoped acceptance that excludes ACTUAL-consumer
   provenance and product backward links and states those limits explicitly.

This reviewer does not select the option, does not self-adopt, does not merge,
does not alter PR #559 and does not dispatch future work.

## 7. Proof limits

The returned artifact, even at full GREEN, is static index engineering:

- not an automatically updated versioned work program;
- not live worker status or a live queue;
- not gap prioritization, roadmap or priority ranking;
- not a real Pyat native world or native N11/N12/C11;
- not scientific issuance, native science or generated human alpha;
- not owner adoption, PRE-MAIN merge or canonical Programma status;
- not an external source-owner signature over historical provenance;
- not proof that a named/required `first_consumer` is a current importer.

## 8. Final SHA and decision readback

`FINAL_SHA: PENDING_TERMINAL_READBACK` — the exact 40-hex branch tip is read
with `git rev-parse HEAD` after the non-force push and reported in the terminal
response. A file cannot contain the SHA of the commit that contains it.

**Single decision:** `REVISE_EXACT_DEFECTS`
**ENGINEERING:** `REVISE_EXACT_DEFECTS`
**SCIENCE:** `HOLD`
**AUTHORITY:** `HOLD`
