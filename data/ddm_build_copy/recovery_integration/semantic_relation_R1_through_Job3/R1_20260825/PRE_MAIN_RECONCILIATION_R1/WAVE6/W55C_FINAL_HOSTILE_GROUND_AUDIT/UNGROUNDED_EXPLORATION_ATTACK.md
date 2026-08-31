# Deliberately ungrounded exploration attack

`EXPLORATION_ALLOWED = TRUE`

`DIRECT_PROJECT_ADOPTION = FALSE`

The dedicated protocol permits hypotheses, alternative architectures, vocabularies, prototypes and attacks while expressly denying project authority/adoption/closure. The validator additionally forces `GROUNDING_PASS = false` when `agent_mode == DELIBERATELY_UNGROUNDED_EXPLORATION`, so a packet in that explicit mode cannot pass the adoption gate.

Ruling: no direct-adoption bypass found for the explicit deliberate-exploration mode.

Later grounded reconciliation remains mandatory.
