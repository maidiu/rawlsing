# Product documentation and capability uncertainty

[Start](README.md) · [Runtime routing](02_CAPABILITIES_AND_ROUTING.md)

Official sources were consulted on 2026-09-29. Their scope is product/model documentation, not proof of this user's enabled browser environment.

- [GPT-5.6 Sol model documentation](https://developers.openai.com/api/docs/models/gpt-5.6-sol) lists High reasoning support and API tool capabilities. These do not establish which tools a specific ChatGPT browser agent has, its session persistence, CI permissions or account usage treatment.
- [GPT-5.6 model guidance](https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6) recommends representative workload comparisons rather than assuming maximal effort always optimizes quality/cost. The plan's specific role allocation and escalation thresholds are engineering recommendations, not published model benchmarks.
- [ChatGPT Computer Use documentation](https://learn.chatgpt.com/docs/computer-use) documents limits for that feature, including automating terminal apps or ChatGPT itself. This does not imply that separately exposed supported shell/CI/agent tools are unavailable. Use the receiving environment's actual supported tools; do not conflate a GUI-control restriction with all execution capability.

User-supplied premises: substantial Library resources, full GitHub write tooling, browser Sol High preferred because it does not consume the user's finite Codex usage; Codex 5.6/6.0 available when necessary. These premises guide routing. They are not a verified statement that every operation is free, every resource is authorized, or every browser session exposes the same capabilities.

The capability census therefore checks each actual route once on necessary work. It avoids both blanket underestimation of browser agents and invented guarantees about their runtime.
