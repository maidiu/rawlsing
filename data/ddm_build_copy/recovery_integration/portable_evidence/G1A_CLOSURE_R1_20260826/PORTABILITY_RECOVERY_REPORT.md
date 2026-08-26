# G1A Portability Agent B historical recovery report

Status: `G1A_PORTABILITY_AGENT_B_SHA_RECOVERY_DENOMINATOR_COMPLETE`

Authority ceiling: `EVIDENCE_RECOVERY_ONLY__NO_C1_C6_ADJUDICATION__NO_G1A_CLOSURE`

## Git identity

- Repository: `maidiu/rawlsing`
- Required coordination branch at dispatch: `agent/vozhd-to-vozhdy-inheritance-integration-r1`
- Exact starting commit: `9b65e0232916f660d9a0bc343b01e94e438e2cbb`
- Live coordination branch observed before writes: `f805c6a0f79f00f66e1ecd7949a8bf05f707249c`
- Recovery branch: `agent/g1a-github-portability-recovery-r1`
- Exact resulting branch HEAD: recorded and independently verified in the terminal cross-agent return after push. A tracked file cannot embed the SHA of the commit that contains that file because changing the embedded SHA changes the commit SHA.

The live coordination branch movement was not consumed. The recovery branch was created in a fresh clone directly from the user-pinned commit.

## Denominator disposition

The SHA-pinned historical recovery denominator contains 26 objects:

- `PRESENT_EXACT`: 24
- `NOT_FOUND`: 1
- `EXCLUDED_BY_GOVERNING_SEARCH_LAW`: 1

Of the 24 exact objects, 23 were newly installed and the exact itinerary was already present at the pinned Git base and therefore was verified without duplication.

The only unresolved required SHA is:

- `266d82216bcd6351de19ada84377d56fcf8b48fba1d29eb208a399fda012e816` — `Rawlsing_9family_after_manual_authority_bridge_repair_handoff_TIGHT_20260729T083708Z.zip` — `NOT_FOUND`

Its bounded negative receipt is `PORTABILITY_NEGATIVE_SEARCH_RECEIPTS/C1_9FAMILY_ARCHIVE_SEARCH_RECEIPT.md`. The supplied complete member index was preserved as locator evidence by the supplied portability corpus, but it cannot reproduce the missing ZIP bytes.

The exact runtime carrier SHA `9eb13f928a9e2fc64d54a97991f6091fe3ed4ffb3cebf60fb2433b76a78b5323` was found locally and independently verified. It is dispositioned `EXCLUDED_BY_GOVERNING_SEARCH_LAW` because the manifest explicitly makes it optional unless uniquely required, its 194,784,692-byte binary exceeds the ordinary Git limit, and the exact local retrieval route is recorded. This is not a representation of the original object and no derived projection was substituted.

## Exact recovery validation

- All 24 `PRESENT_EXACT` objects independently match their expected SHA-256.
- The HARVEST-003 packet passes ZIP CRC testing and all 252 entries in its internal `SHA256SUMS.txt`.
- Both C4 R2/R3 historical archives pass ZIP CRC testing.
- The R184 Git bundle passes `git bundle verify` as complete history.
- The R184 database dump passes `pg_restore --list`.
- `repository.tar.zst` passes `zstd -t`.
- No installed ordinary Git object is 95 MiB or larger.

## Same-name and misleading candidates

Yes. Same-name/different-SHA objects could mislead a later agent:

- `ddm_survey_identity.py` has three required historical SHA identities; they are installed in separate `aug17`, `aug16`, and `historical` directories.
- `questions_master_drivers.csv` has distinct V525b and d62 identities; neither was selected by recency.
- `questions_master_semantic.csv` has distinct V525b and later identities; neither was treated as automatic successor authority.
- Generic `manifest.yaml` produced five distinct candidate SHA values; only `27aaabf...` matched the target.
- `repository.tar.zst` produced a 60,858,407-byte candidate at SHA `b673b11e...` in addition to the exact 47,193,953-byte R184 target at `6c5f1e71...`.
- Three same-family nine-family ZIPs at SHA `27fbbb3b...` did not match the missing C1 archive.

The full physical provenance and candidate-disambiguation ledgers are under `99_PROVENANCE/`.

No portability completion, C1-C6 outcome, successor authority, retirement, P9 execution, or cross-agent merge is claimed.

`G1A_PORTABILITY_AGENT_B_COMPLETE__RETURN_FOR_CROSS_AGENT_ADJUDICATION__NO_G1A_CLOSURE`
