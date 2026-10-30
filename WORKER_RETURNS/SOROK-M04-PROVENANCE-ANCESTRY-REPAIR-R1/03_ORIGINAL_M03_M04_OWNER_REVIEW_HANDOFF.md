# M04 original-owner and independent-review handoff

## Exact lineage

- M04 sealed startup: `342164a09e10aa70812299c12386ed0923308228`.
- Assigned return branch base: `187a9dcf69dc75b00c2875ee1fbe83d3524e0426`.
- F3 source/test cut: `6477a89bb9160eba1dd10607c47534fa4dce6cc2`.
- Original M03 author cut: `e1f7a74e51201b9614bcc578348b4e9db7be7bd3`.
- Original independent M04 reviewer: `3a993abcc0a9f6bd3a1bb003d298d293be199ea6`; return blob `5840b2f3f551903d61ce00654b8b964c0ea3a545`.
- Original candidate `cell.py`: `3eb2d02aee8dc840e7cac1f99230d7c69adc2f58`.
- Original candidate `claim_provenance.py`: `2434bda6f4b00e6ea5881291f5422227e8045e74`.
- Frozen reviewer test: `8add06c66b347e324443c1263771755f6898c7e2`.
- Candidate PRE-MAIN: `299f41e97a43c67be9cc76a79fa49b48f4e12e54`; unchanged.

## What this return does

It supplies a bounded sourcefree repair candidate for the three provenance defects independently identified at the original cut:

- 4 cross-cell owner-substitution RED;
- 4 partial-rollback/non-terminal-transition RED;
- 2 forged-pre-state ancestry RED.

The patch binds checkpoint/read acceptance to the journaled `ADP017_COMMIT` pre-state and to the terminal transition snapshot. It preserves 587/587 inherited positives and 51/51 fresh tests in two cold reconstructions. It does not touch native code or tests.

## What remains with original owners

- **Original M03/M04 author and CAN3 owner:** decide whether the candidate patch is the correct sourcefree repair, whether any native CAN3 rule/issuance is implicated, and whether the nine historical CAN3 failures are in scope for a separate court. This return does not issue or reclassify them.
- **Original independent M04 reviewer:** may reproduce the 51/51 and 587/587 results and inspect the patch. This return is not that reviewer's acceptance.
- **Distinct new reviewer:** required at the exact pushed SHA before any fan-in. The author of this return cannot be the accepting reviewer.
- **Incumbent Sorok HQ:** logs the returned evidence and decides any scoped adoption or integration. No source, actor, scientific or production authority transfers.

## Independent-review requirements

A competent reviewer should:

1. Read the four return artifacts and the exact candidate blob `5ba929f51870b111ca54ca87fdf97338e4295625`.
2. Reproduce the baseline 41/51 and the patched 51/51 at the same frozen test blob `8add06c6...`.
3. Reproduce 413/413, 100/100 and 74/74 after the patch; confirm the nine CAN3 failures remain nine.
4. Attempt the three forged-ancestry classes independently, including a cross-cell owner swap, a partial rollback with the later transition retained, and a fully rehashed pre-state.
5. Classify engineering, scientific and authority separately. The expected result is engineering candidate acceptance if and only if the exact tests and counterexamples hold; scientific and authority remain HOLD.

## No self-adoption

This return does not merge, adopt, promote, issue or self-review. It does not modify canonical PRE-MAIN, PR #514/#516/#519, original source branches, original reviewers, or any other live worker/owner branch. The final remote return-branch SHA is reported by the committing worker after push; it is not self-embedded in this file.
