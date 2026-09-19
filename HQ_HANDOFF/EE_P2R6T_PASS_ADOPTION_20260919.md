# EE-P2R6T PASS ADOPTION — 2026-09-19

Status: `R6T_ADOPTED_PASS__REPAIRED_BACKEND_READY_FOR_SELECTIVE_P2X_FANIN`

Decision:

`HQD-2026-09-19-079`

Semantic PRE-MAIN remains:

`1dcd2a79dd6d4208738f655ab7fe4e71c219e354`

## Governed return

EE-P2R6T final return head:

`d9785085cf7a5ac4b220627f0dfef39dbaf56345`

Terminal:

`EE_P2R6T_PASS__LITS_AS2A_PINNED_AUTHORITY_PATH_REF_REPAIRED__EXACT_BANKED_AUTHORITY_BYTES_PRESERVED__READY_FOR_HQ_SELECTIVE_BACKEND_FANIN_AND_P2X_RESUME`

Disposition:

`PASS__ADOPTED_REPAIRED_BACKEND_BLOB__SELECTIVE_FANIN_REQUIRED`

## Exact repair

Prior backend blob:

`ca32b9c8ec6bfcbbdc039fba0a10646dcc5357e2`

Repaired backend blob:

`fb30167ebc060939e17eb15c71b93c000033eb4f`

Backend contract remains:

`RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0`

Pinned authority commit remains:

`3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f`

Exact repaired path component:

`banked_as2a`

The repair changes only the pinned authority path reference from the absent canonical-name directory to the existing exact banked path.

No fallback, fuzzy, latest or alternate authority lookup was introduced.

## Preserved authority bytes

Ledger blob:

`c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c`

Ledger SHA-256:

`65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60`

Package blob:

`174b931e8aa89111086e3d46159b47154bed7f16`

Part-A projection authority hash:

`9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06`

LiTS source SHA-256 remains:

`7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`

No authority content was changed.

## Qualification

- run: `35424699308`
- job: `105848513942`
- bounded R6T court: `6/6 PASS`
- protocol court: `20/20 PASS`
- artifact: `10579135204`
- digest:
  `sha256:3a4dce583165ae90ee18002da1ada4e513b4d9e4de25173fc22995c1b0b5f00c`

Hostile missing-path, substituted-ledger and substituted-package cases all fail closed.

The transient `.rabochii/court_spec.json` was restored to the commissioned-head state: absent.

No measured P2X execution, Library/carrier access, empirical outcomes or performance measurements occurred.

## Integration law

HQ adopts the exact repaired backend blob only:

`fb30167ebc060939e17eb15c71b93c000033eb4f`

Qualification tests and EE-P2R6T return files remain evidence and are not required on P2X for runtime.

The existing P2X branch remains stopped at:

`d0187a01f21959f4834a7f774f92d06187f1efb3`

and:

`LITS_I/A/S02_C11_REACHABILITY`

Next lawful operation:

`SELECTIVE_FANIN_REPAIRED_BACKEND_BLOB_fb30167e_TO_EXISTING_P2X_BRANCH`

P2X remains held until that exact fan-in commit is verified and resume authority is sealed.

Terminal:

`R6T_ADOPTED__REPAIRED_BACKEND_SELECTIVE_FANIN_READY__P2X_HELD_AT_S02`
