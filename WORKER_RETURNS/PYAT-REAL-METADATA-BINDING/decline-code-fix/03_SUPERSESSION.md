# Historical tally supersession — q101 only

## Preserved accepted receipt

- Tally product: `d9d7f43b090c599d987a3f4957a321d26701b2ee175b8f9cf71ec033588abfc0`
- Tally ref: `87e297bb8795ae3628603a730c83ca0b90107556236c9e1cb7dba27858722022`
- Replay ref: `8c7205dc775fd9123ab09985e61b91671f38127e0ae22a6ae3d58e39dfd41b4f`
- Focused review: PASS, `D1_OBSERVED_SAMPLE_DESCRIPTIVE_TALLY_ACCEPTED`

The historical receipt is not rewritten. It is superseded only at q101.

## q101 supersession

| Field | Historical | Corrected |
|---|---:|---:|
| Valid answer | 7162 | 7129 |
| Explicit nonresponse | 171 | 204 |
| Missing | 4 | 4 |
| Source records | 7337 | 7337 |

The delta is exactly 33 code-99 `Decline to Answer` responses: they move from
`SUBSTANTIVE_RESPONSE` to `REFUSAL`. DK remains 171 and missing remains 4.

## Scope

- Only q101 is superseded.
- Other 41 selected fields retain their historical values.
- No accepted historical file was edited.
- No routing, eligibility denominator or policy is changed.
- Routing remains `ROUTING_UNKNOWN`.

## Exact authority

The response-option authority row for q101/code 99 has:

```text
option_group = special
is_substantive = False
is_refusal = True
is_missing = True
response_kind = special_missing
```

No dedicated response-state classifier exists in the current owners; the exact
option-authority fields are the classification authority used by this correction.
