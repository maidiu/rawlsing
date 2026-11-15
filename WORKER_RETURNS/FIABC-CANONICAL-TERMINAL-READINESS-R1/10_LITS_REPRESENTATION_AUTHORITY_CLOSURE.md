# LiTS-I Representation Authority Closure

## Evidence accepted

The candidate-neutral diagnostic receipt has SHA-256:

`74fc2c53610ad2af5867e4c36728604a812cf9ad3d7b0e4bceebda68fe4ac74b`

It binds the exact LiTS-I source SHA, CPython 3.11.3, pyreadstat 1.3.6,
`decode_dta(..., encoding="latin1")`, 29,002 rows, 1,198 variables, and only
`q301_2`/ordinal 194 plus `q301_7`/ordinal 199.

The receipt reports 58,004 response cells in 16 exact representation classes:

- 57,989 observed cells are float64 tokens for exactly `1.0` through `7.0`;
- 15 cells are the already-matching exact system-missing form (`None`, no
  source missing declaration);
- no observed float64 response cell matches the current Decimal-keyed rules;
- the historical `Decimal(str(value))` helper also matches none under the
  current R5 typed-key law because it yields Decimal exponent `-1`, whereas
  the governed rule tokens use exponent `0`.

This confirms a representation-contract transition, not a newly discovered
response-semantic rule.

## Bounded successor authority

`rawlsing_next/fiabc_lits_i_representation_authority.py` admits only:

- source SHA `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`;
- `q301_2`/194 and `q301_7`/199;
- the seven literal float64 bit patterns observed for codes 1 through 7;
- the exact accepted banked Decimal tokens `1.0` through `7.0`;
- exact system missing as `None` with no declaration;
- historical owner commit `0b96b8de9aac774566f872cf0630ebd4ddeb70e6`, blob
  `7c509c2098d0030f253344eb3f682471378812a8`;
- accepted projection, C11 release, and C11 replay identities.

Authority content hash:

`9fce3b606413c2a5d3e9a05eda967067d191fbb31ff869d445d962bdf321393d`

Authority snapshot hash:

`9ac03b6d6e1464da29018ad1e6e803c490ff652a1ec4d9b18691b3e82d98ec7b`

## Production route

The LiTS candidate-neutral oracle producer now loads the exact historical
physical-key owner by commit and blob, converts the already-validated current
banked projection into that compatible owner class without changing its cache
identity, and applies only the enumerated representation bridge. It then
fails closed unless both the accepted C11 release and replay identities are
reproduced exactly.

The global `PRE553_PHYSICAL_VALUE_BINDING@2.0.0` law is unchanged. No generic
int/float/Decimal equality was added.

## Negative limits

This closure grants no authority for other variables, sources, waves, values,
types, missing states, labels, frequencies, response-semantic remapping,
canonical question mapping, candidate output, oracle truth derived from a
candidate, T3 freeze, or measured P2X.

## Holding

Production code changed. Source-backed continuation remains forbidden until
the complete governed source-free qualification is green at the exact repair
head.

