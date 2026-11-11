# Validator repair

The allowed protected validator `GOVERNANCE_PROTOCOLS_R1/tools/validate_enforcement_candidate_from_canonical.py` is the only governance protocol executable modified by W56N.

The repair replaces four W56M-exposed authority seams:

1. unverified `cat-file` commit/blob acceptance -> expected-type read plus independent Git-object hash rebind;
2. `commit:path` governance reads -> verified commit/root-tree/child-tree/blob path traversal;
3. unverified raw-parent traversal -> verified commit payload before parent headers are trusted;
4. trust-bearing `diff-tree` and `rev-parse --verify` provenance -> verified tree-difference construction plus direct bounded loose/packed ref resolution.

The process trust established by W56L is retained: built-in `sys` is the only import before the `-I -S` isolation barrier; post-barrier imports are stdlib; the repository root and Git executable are explicit absolute host inputs; the trusted Git executable is outside the repository and fingerprinted before/after; Git children receive no inherited PATH; the repository and `.git` roots are pinned; replacements/grafts/alternates/shallow and common-dir indirection remain fail-closed.

No Rawlsing runtime/helper import is introduced. No external diff/textconv/pager/alias authority is introduced. No second bootstrap path exists.

`GOVERNANCE_ENFORCEMENT_CHANGE_PROTOCOL.md` and `GOVERNANCE_ENFORCEMENT_PROTECTED_PATHS.tsv` remain unchanged because the validator was already a protected predecessor dependency and the W56N repair requires no new executable dependency. Avoiding gratuitous edits keeps the protected change grain minimal.

Intermediate implementation commit: `f8d262830e474adfacc2910212907d9f6efa2a7b`. The final W56N terminal additionally contains only the bounded evidence and append-only ledger correction required by the mission.