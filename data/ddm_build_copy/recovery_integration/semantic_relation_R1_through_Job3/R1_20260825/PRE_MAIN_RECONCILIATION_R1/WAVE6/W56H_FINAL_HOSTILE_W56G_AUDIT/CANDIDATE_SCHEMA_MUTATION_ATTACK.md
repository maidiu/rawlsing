# CANDIDATE HOSTILE-AUDIT SCHEMA MUTATION ATTACK

The predecessor gate does not load its trusted hostile-audit schemas from `Path.read_text`, candidate SHA paths, or the current checkout as governance authority.

`canonical_schema_check()` obtains schema objects via `canonical_json(live, rel)`, and `canonical_json()` obtains bytes through `canonical_text(live, rel)`, which performs `git show <live>:<rel>`.

Therefore candidate mutations to authorization/result schemas allowing arbitrary candidates, branches, rulings, missing nonce, extra fields, `READY`, or malformed authorization have zero direct data-level effect when the predecessor interpreter/runtime is authentic.

Classification: `SAFE_AT_TRUSTED_DATA_GRAIN`.

Global integration eligibility nevertheless remains blocked because Python import provenance is not isolated.