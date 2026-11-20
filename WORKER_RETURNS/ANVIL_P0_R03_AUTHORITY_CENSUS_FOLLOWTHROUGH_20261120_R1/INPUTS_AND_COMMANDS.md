# Inputs and commands

## Candidate trace inputs

- `HARVEST-001.../source_structure_audits/GSS_1972_GSS1972.csv`
  SHA-256 `f746fdfa831a1f8b13fa66c5985685ce89e0b49ec3117848d77ff4f36f05f82e`
- `HARVEST-003.../masters/drivers_current/questions_master_drivers.csv`
  SHA-256 `d62accad0e956f739eada0718e4fb222429e7a90ed7889fff6f4f292b1a8a011`
- `HARVEST-003.../masters/semantic_old/questions_master_semantic.csv`
  SHA-256 `171d399da7e0f2bbd66dcce08a6c353978e48b69fee8d32ac6b1720d10d70ca5`
- `SRC16.source.config.json`
  SHA-256 `1106de3e086032f5ac0b26fee0b56a147722399c80ac2841b70f0b851dea93b7`
- `HARVEST-002.../SCOPE_BINDING_MECHANICAL_RECEIPT.json`
  SHA-256 `c4d7684f8e3813f2b323f6d7a9e3ef630945afa4c770ebda4f10bbcaa03cde5c`
- H48 commit `359ddabc89d78ceb4c8fa45561588ee4cad7dd11`; exact item-binding
  grade only, no adoption.

## Commands

```bash
cd "$P0_WORKTREE"
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  "$PRIVATE_PROOF_DIR/r03_candidate_binding2.py"
PYTHONPATH=. PYTHONDONTWRITEBYTECODE=1 python3 -B \
  "$PRIVATE_PROOF_DIR/r03_projection_probe.py"
```

Private launcher SHA-256 hashes:

- `r03_candidate_binding2.py`:
  `6b45c860cf7a85cf7cf1b29104560cbcaa51329e694dc79918423cbed56237da`
- `r03_projection_probe.py`:
  `d2039d9e0f62252e7f7e9c75f01fa699a7260819b215c9b4828aebb8354821fb`

No raw SAV, respondent values, private paths, manifests, or rights files were
published. The saved-stream check read `QuestionVariableBinding` metadata only.
