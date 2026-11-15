# Exact one-pass source-backed execution command

## Required execution identity

Checkout/use exactly:

`8e35e9b0d41c6a404a84ea511761d5123323af35`

Do not substitute an older integration head or a later documentary-only return commit.

## Required environment inputs

- `LITS_SOURCE_PATH`: exact local canonical LiTS-I source file authorized for the execution.
- `FIABC_LITS_WORK_ROOT`: fresh candidate-neutral work root with no Candidate A/B/C state.

## Command

```bash
git checkout 8e35e9b0d41c6a404a84ea511761d5123323af35

PYTHONHASHSEED=0 python -m rawlsing_next.fiabc_final_oracle_freeze_producers produce-lits \
  --repo-root "$PWD" \
  --source "$LITS_SOURCE_PATH" \
  --work-root "$FIABC_LITS_WORK_ROOT" \
  --output "$FIABC_LITS_WORK_ROOT/court/oracle_producers/LITS_I/current_standard_lits_oracle.json" \
  --checkpoint-output "$FIABC_LITS_WORK_ROOT/court/oracle_producers/LITS_I/current_i05_materialization_checkpoint_v3.json"
```

## Execution law

Do **not** run a separate pre-command SHA-256 pass over the source. The producer itself enforces the exact canonical LiTS source SHA before decoding and reports the fresh source access envelope.

The intended single fresh materialization path is:

- one candidate-neutral LiTS source-backed pass;
- one decoder call;
- zero Candidate A/B/C processes;
- checkpoint v3 written before later zero-source resume;
- standard candidate-neutral LiTS oracle frozen from current material;
- ASTRA historical regression may run as a bounded projection if present, without becoming checkpoint ontology.

Do not run Candidate A/B/C, measured P2X, P3, or FF02 in this command.
