# Rawlsing agent communication guidance

This repository is software-engineering, CI, provenance, validation, governance, and code-review work. Describe it using neutral engineering terminology.

## Required terminology discipline

- Prefer terms such as: independent review, validation case, boundary condition, mutation case, negative test, provenance check, malformed-input case, compatibility check, implementation review, state-transition check, and CI evidence.
- Do not unnecessarily recast ordinary repository work as cybersecurity work.
- When an existing branch name, filename, command, terminal, test name, historical artifact, or other exact repository identifier contains specialized wording, preserve that wording only when quoting the exact identifier. Use neutral engineering language in surrounding prose.
- Describe concrete behavior directly. For example, say that a retained client must remain stable after module-state changes, that malformed inputs must fail closed, or that a review must verify provenance and immutability, rather than adding unrelated security framing.
- Preserve the substantive rigor of tests and reviews. This guidance changes wording only; it does not weaken validation requirements, independence requirements, evidence requirements, or repository governance.

## Scope

Apply this guidance to agent chat responses, repository-authored review packets, command prose, commit messages, PR titles/descriptions, issue text, CI summaries, and newly authored documentation wherever exact historical identifiers do not require literal reproduction.
