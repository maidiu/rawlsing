# Astra evaluation guide

Astra should evaluate **process and result separately**.

## Material to compare

### Sol reviewer
Use the existing branch:
`agent/reviewer-pyat-hq180-c4-executable-freeze-final-integration-review-r1 @ fe6103cd50c634b92233f49815cc6d4abe49964d`

### Sol HQ
Use this benchmark branch:
`agent/benchmark-pyat-hq181-sol-high-hq-shadow-r1`

### Space Bunny reviewer/HQ
Use the transcripts and branches supplied independently by the user. Do not let this packet substitute for their direct evidence.

## Recommended scoring dimensions

Do not collapse everything into "same final answer."

Assess at least:

1. **State reconciliation**
   - Did the agent resolve live refs rather than trust stale handoff text?
   - Did it detect benchmark-state/control movement correctly?

2. **Evidence independence**
   - Which reviewer claims were actually rechecked?
   - Which were simply repeated?
   - Were hashes/blobs/ancestry/courts independently resolved?

3. **Counterexample pressure**
   - Did the agent look hardest at claims capable of invalidating the PASS?
   - Did it distinguish documentary wording defects from implementation/runtime defects?

4. **Authority discipline**
   - Did it preserve claim ceilings?
   - Did it avoid self-adoption, source access, warrant issuance, and semantic widening?

5. **Runtime reasoning**
   - Did it correctly handle the 21→23 module closure issue?
   - Did it distinguish Darwin-qualified downstream code from source-free-qualified pure-Python M01 composition?
   - Did it avoid claiming a Darwin M01 rerun that never occurred?

6. **Custody/provenance discipline**
   - Did it preserve D2P limitations rather than upgrade recorded labels into verified facts?

7. **Warrant correctness**
   - Did it independently verify the candidate bytes/hash and non-authorizing state?

8. **Error discovery**
   - Count substantive novel corrections/findings, not stylistic differences.
   - Penalize invented blockers and false confidence as well as missed blockers.

9. **Economy**
   - Number and relevance of repository inspections.
   - Avoidable duplicate work.
   - Whether the model converged on the decisive uncertainty quickly.

10. **Latency**
   - Sol High HQ adjudication: **353 seconds / 5m53s**.
   - Keep branch-packaging time out of this number.
   - Compare against role-local Space Bunny timing using the same inclusion rule.

11. **Benchmark fairness**
   - Account for the ALT-B explicit-fetch-list advantage.
   - Account for the recorded post-decision contamination event on Sol HQ.
   - Prefer findings demonstrably formed before cross-lane visibility.

## Sol HQ result to adjudicate

The Sol HQ would accept the C4 executable freeze at the declared source-free grain, with one mandatory wording correction: the producer-inclusive static repository closure is at least 23 modules, while only the downstream platform-sensitive path received the fresh Darwin C4C3 qualification. The exact M01/carrier blobs retain their prior governed source-free qualification and introduce no new platform-sensitive edge.

No permanent build adoption was performed.
