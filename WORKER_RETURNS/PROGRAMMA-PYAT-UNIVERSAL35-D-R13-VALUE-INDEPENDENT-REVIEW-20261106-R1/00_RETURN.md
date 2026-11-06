# Universal35 D r13 — conditional-value review

**VERDICT: REVISE** at frozen D head `7cafd1fd3830454ad4833ba98a7d68eb1a9e610f`.

- Code: `6c66654c7f2882b94b9ad8a74ee438c77844af2f`
- Prior head: `cca6f2b0b46029b0684f539dd58b0f6b0e6a0d6d`
- Prior G: `dcbb8b1bcfcf7ff2dd34492c55e40ba4f2fca108`
- Published review head: the commit containing this directory; exact SHA reported in final delivery.

## FINDING

### Blocking — the new consumer trusts transport metadata instead of validated envelope/query/profile

`consume_requested_joint_transport` copies `conditioner_item_id`, `target_item_id`,
`fact_refs`, `query_refs`, `joint_operation_id`, and requested values from the
transport row. It does not compare them with the decoded envelope/query or the
accepted E profile. A tampered transport therefore still returns `OK`:

- wrong `conditioner_item_id`/`target_item_id`: both requests `OK`; selection
  material carries the tampered IDs;
- fake backing fact/query refs: both requests `OK`; selection material echoes the
  fake refs;
- empty `conditioner_values`: request returns `OK` with **zero selections**.

Value matching also uses `str(row["condition_state"])` and `str(requested)` rather
than the existing canonical state codec, with no unknown/None guard. This can
create false matches or mask empty selection.

This violates the required request/role/backing-ref binding and the empty/mismatch
failure boundary. The exact fix is to derive role/backing refs from the validated
envelope/query/profile, validate requested values canonically, and refuse empty or
mismatched selections before returning `OK`.

### Axes

- **Joint support/direction: PASS_SCOPED.** Existing engine produces the genuine
  two-target JOINT; B|A and A|B cold profiles match the asymmetric rows.
- **Value-selection: FAIL.** Requested values are carried, but consumer selection
  trusts transport metadata and allows empty-value `OK` zero selections.
- **Cold consumer: FAIL.** Valid envelope path works, but contradictory metadata
  is not checked against actual envelope/query/profile identity.
- **Identity/measure: PARTIAL.** Exact unique RAW/SAMPLE measure and distinct
  selected-result IDs exist; backing refs are not revalidated by the consumer.
- **R10 ordering/permission:** preserved from prior accepted proof.
- **Actual original/native/all35/science:** `NOT_RUN`.

Focused test: 2 passed in 3.02s. The test exercises the happy path and
missing/replay cases but not tampered transport metadata or empty requested
values. No code repair, source read, full-estate/650 s run, or A/C/E/guide/
progress/controller edit.
