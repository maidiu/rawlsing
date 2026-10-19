# Supplemental custody court, frozen before first supplemental execution

Source inspection after the first hostile court reveals that evaluate_target constructs a full semantic record but returns only its digest; CandidateStore reconstructs a smaller row. Test these additional boundary assertions without modifying the candidate:

S1. A committed/cold-reopened record retains the qualified semantic object, effective time and causal parents, rather than only a claimed record hash.
S2. An explicit target_middle_state_id selected/validated by CAN011 is the actual committed identity consumed downstream.
S3. A caller-constructed TargetDecision with invented record_hash/permission and no evaluator provenance cannot bypass independent target evaluation to publish an effect.

These are required boundary assertions and may remain RED. No weakened expectations, no native execution, no new issuance. Existing first-court outcomes remain frozen.
