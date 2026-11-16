# RRIF C3 — selective receiving packet (E4F + independent E4FR)

**Status:** exact six-file sourcefree receiving CANDIDATE; protected PRE-MAIN not mutated. This isolated branch is based on PRE-MAIN `8e44ca9c751049d65e6def47600b5c073ee04b29`. Approval/adoption, source rights and current actor authority are NOT claimed.

## Completed independent gate

- E1 original candidate `ffd03934d0a86c98ed095d973e45587bd5751013`; E4 hostile reviewer `5dc00a1eb0d2881a9d74661b7a94d436cc7b7c60` identified real SAV/DTA `pandas.Timestamp` -> string, aware subclass fallthrough.
- E4F fixed `f2c0af3273d612bff0a7bd2407532b52caf4348b`.
- Independent E4FR review `7cd2206fd976606d3816589e2fce03c03c827f39` explicitly `APPROVE_E4F_PHYSICAL_D01_D02_SOURCEFREE_FANIN`.
- F0 independent receiving preflight `ac9690e70c3129c86d55ea59503a9248c77a3277`: receiving paths E4F and E5 do not overlap; E4F 45 tests PASS, selected 194 pass/1 skip; PRE-MAIN remains baseline. F0's combined gate refused both while reviews were not returned at F0's cut. E4FR has NOW returned; E6 separately holds E5. This packet is only C3, so M2's fixture-owner HOLD does not block preparing C3.

## Exact payload allowlist

- `rawlsing_next/pre553_physical_decoder.py` `4b89c4598f324834de064c1200c63698a20e3c5c`
- `rawlsing_next/pre553_r5_codec.py` `f5f64d9b8b6c9af1d1b755f86b44fe43a8e741b7`
- `rawlsing_next/tests/test_rrif_e1_c3_d01_declared_encoding_admission.py` `625f1d8b1f3fa8c24501addcaff7d70209598596`
- `rawlsing_next/tests/test_rrif_e1_c3_d02_opaque_datetime_carrier.py` `ac5f331322a69dab224eeeda14b05681918b432e`
- `rawlsing_next/tests/test_rrif_e1_c3_current_integration_regressions.py` `bfa20f7a35ef9a399bec5380b6c3e6f9caad0115`
- `rawlsing_next/tests/test_rrif_e4f_d02_real_datetime_subclass.py` `c07c2019455e6264b4297c1c1d782bd887b96bdd`

No E1/E4F return documents, other historical source code, G01 numerical bridge, R9/S06F owner, E5 M2/B5 patch, or source-native permission are included in payload. This packet is the only documentary addition.

## Honest acceptance evidence and known residuals

- E4FR independently reproduced 12 new E4F tests, 33 E1 tests, selected 194 pass/1 skip, real synthetic SAV+DTA date as `opaque` at decoder and test-pinned historical R5 seam. The R5 seam is absent at current PRE-MAIN: test-only pinned Git-object execution is NOT a current production consumer.
- Existing G01 hostile two FAIL are identical on baseline and corrected code; no change or cure asserted.
- E4FR showed two-or-more-level custom `.item()` wrappers containing aware datetime still pass through recursive `_jsonable` to a string. Reviewer scoped this as nonblocking because real pyreadstat source cells are direct pandas Timestamp and accepted D02 scope is direct / one-level only. Preserve this negative; no general claim of aware-value fail-closed over arbitrary wrappers or scalar numpy inputs.
- No raw survey decoded; three D01 allowlist pairs are physical identities only. No source-use licence, historical scientific/semantic authority, external issuer, or G01 numeric authority granted.
- These tests were run on exact E4F and independently on detached sourcefree worktrees, NOT run on this GitHub-authored receiving branch. The branch has been constructed from identical Git blobs; protected integrator must run required tests again (including actual first decoder/EE-P2X consumer) and check blob hashes under the final receiving checkout.

## Required receiving CAS

1. Verify PRE-MAIN still equals `8e44ca9c751049d65e6def47600b5c073ee04b29`, or stop and rebase/re-review material differences without overwrite.
2. Independently confirm diff only the above six paths plus this documentary file; each blob matches exactly and E4FR review SHA is distinct from E4F author.
3. Run E1 33 + E4F 12, selected 194/1 and real sourcefree SAV/DTA consumer tests in the actual receiving tree; preserve G01 two known baseline RED.
4. Only an authorized protected receiving owner may move PRE-MAIN; do not force push, self-adopt or infer source/actor rights.

ENGINEERING: exact independently reviewed sourcefree six-file candidate. SCIENTIFIC: original source/data/meaning HELD. AUTHORITY: protected PRE-MAIN CAS and original issuer rights HELD. RRIF finite terminal closeout still pending M2 fixture-owner decision and protected receiving account.
