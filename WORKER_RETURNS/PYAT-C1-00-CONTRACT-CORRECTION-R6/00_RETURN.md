# PYAT C1-00 contract correction R6 return

Disposition: `PATCH_READY__EXECUTION_CAPABILITY_BLOCKED`

HQ's normative fixture-only R6 convention has been implemented forward. Historical R2/R3/R5 opaque hashes were not reverse-engineered or fitted.

Frozen recomputed identities:
- forward query: `8f7444dbae4250cdda8a7a4c89bb331bd1f960072a97e8b11f05c4bd68c770d9`
- reverse query: `2909672ca01a2b5fcb5d07351f8691bb10bf82d3e794d92f73981d2e70fc4f0e`
- forward witness: `f4123258625589513da2afc0d4f10a2438b6238b0b4f0a5338acb03ef8932da5`
- reverse witness: `a5410dd09f9a16ada260b6d18e902e5a101b7b41346a407f17283de8d726fdb0`
- forward evidence: `c5e5930b6b368605c6828b70de02bf00ca77b9636c890706ac755b0074f61374`
- reverse evidence: `0cd3b5b868852db956a079835c5052c206561b0fe2a7480931e6de0dc5d81844`

The active C1 test now reconstructs the accepted AT07 source-free fixture, asserts the frozen producer identities, constructs the two normative R6 consumer queries and closed 16-field witnesses, invokes the public empirical producer -> frozen analytical adapter -> public positioned-subject consumer, checks 54/60 and 54/62, checks the R6 evidence identities, checks stale-witness mutation failure, and checks hostile relation mismatch timing before evidence/consumer invocation.

Execution is not claimed. The present agent surface exposes GitHub reads/writes but no repository Python runtime; no workflow run was created by the branch push. Required pytest remains the exact commission command.

Raw survey source reads: 0. Candidate A/B/C: not run. Measured P2X: not run. Real-source C11: not run. Production implementation: not edited.
