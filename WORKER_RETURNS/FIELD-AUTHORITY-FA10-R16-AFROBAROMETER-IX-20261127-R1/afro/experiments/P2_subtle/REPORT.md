# Afrobarometer IX P2 subtle-differentiation diagnostic

**Status:** executed and blindly reviewed for the six-field source-metadata scope; neutral-output correction separately received at exact candidate SHA. This is not an overall R16 acceptance or scientific result.

Neutral and directed DeepSeek calls used the same six exact Afrobarometer Round 9 rows (Q28, Q29B, Q22B, Q48A, Q48B, Q63B), empty prior context, same model/effort/cap, and one call each. Only the P2 contrastive instruction varied.

The neutral output already distinguished Q29B military-intervention statement choice from Q22B approval of army governance, and Q28 presidential rule-of-law constraint from Q48B presidential accountability attribution. The directed output added explicit false-merge configurations, separated the Q48A/Q48B 93-versus-94 not-asked code asymmetry, and distinguished conditional police/security enforcement in Q63B from army-governance approval.

The separate source-first and blinded comparative calls preceded unblinding. The blind reviewer returned `PASS_SCOPED`, judging the directed output modestly stronger in source-grounded false-merge coverage, but found no decisive accuracy winner. A post-review exact check caught two neutral-output defects the blind reviewer missed: Q28's purported literal quote was not a substring, and Q22B called source code 3 “mixed response” despite its exact label “Neither approve nor disapprove.” A bounded separate two-path repair was independently received `PASS_SCOPED` at candidate SHA `1303221b750c810188f5b970c7fa3dc2ea8c4e75c827e6c86a3d597660002de7`. The frozen original pair and its blind comparison remain unchanged; the repaired neutral copy is supplemental, not a re-scored arm. The first repair worker also proposed an out-of-scope Q48A edit; it was excluded.

The full P2 sequence used seven sequential DeepSeek calls: 20,158 input and 5,685 output tokens, zero reported reasoning/cache reads, and `$0.0064347` OpenCode rate-equivalent accounting. Actual billed use, active human minutes, and Codex cost are unobserved.

No respondent-level observations were used. No source metadata establishes actual co-administration, routing beyond the code-97 label, respondent answers, distributions, or empirical relations. No WVS7 work was performed. This bounded result is not a general capacity/cost advantage, scientific acceptance, or authority. All inputs, raw provider events, responses, hashes, failed repair, exact receiving and controller-only mapping are retained under `experiments/P2_subtle/`.
