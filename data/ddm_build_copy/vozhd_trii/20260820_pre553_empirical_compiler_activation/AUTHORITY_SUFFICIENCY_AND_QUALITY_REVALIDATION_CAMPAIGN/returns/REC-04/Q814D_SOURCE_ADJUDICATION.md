# LiTS III q814d — Source Adjudication

## Source contract

`LiTS|III|q814d` asks:

> How many are corrupt - local government representatives

Source response options:

- `1` — None
- `2` — Some of them
- `3` — Most of them
- `4` — All of them
- `-97` — Don't know
- `-94` — Haven't heard enough to say

The substantive ordering is source-semantic and textual: **None → Some → Most → All** answers "How many". It is not inferred from the numeric codes.

## Current defect

The current QRA row is directional on `local_public_integrity`, targets `local_government_representatives`, and carries `item_reversal = true`. It has a negative anchor `All of them` but a blank positive anchor. Current O07 class is `UNSIGNED_ORDERED`.

The blank QRA positive anchor is a response-binding defect. O07's unsigned class is also inconsistent with the source-supported signed geometry once the existing QRA public-integrity axis is respected.

## Bounded successor candidate

Candidate status: `CANDIDATE_ONLY__NOT_INSTALLED`.

- source prevalence geometry: None / Some / Most / All
- existing QRA semantic axis: `local_public_integrity`
- existing QRA reversal: retained
- positive public-integrity anchor: **None**
- negative public-integrity anchor: **All of them**
- intermediate intensity states: Some of them / Most of them
- source-special states excluded: Don't know / Haven't heard enough to say
- O07 successor class candidate at this row: `SIGNED_SCALAR`

The sign is established by the named public-integrity axis plus source wording and the existing reversal, not by numeric ordering.

`REC04_Q814D_QRA_DISPOSITION = SUCCESSOR_CANDIDATE__QRA_ASSERTION_DEFECTIVE`

`REC04_Q814D_O07_DISPOSITION = RECONCILIATION_REQUIRED`
