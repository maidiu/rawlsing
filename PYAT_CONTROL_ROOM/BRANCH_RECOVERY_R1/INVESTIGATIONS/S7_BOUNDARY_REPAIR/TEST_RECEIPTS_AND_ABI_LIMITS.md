# S7-FIX test receipts and ABI limits

**Schema:** `PYAT_S7FIX_TEST_RECEIPTS_AND_ABI_LIMITS@1`  
**Branch:** `agent/pyat-s7-six-boundary-function-family-repair-20261031-r1`  
**Worktree:** `/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s7-six-boundary-function-family-repair-20261031-r1`  
**Independent session:** `ses_e6f7c46f8ffeJ808JJfoBH3866`  
**Model/variant:** `opencode-go/deepseek-v4.1-flash`, variant `max`, agent `build`; MAX verified from process argv and session DB.  
**Python:** CPython 3.11.3 on mainMac.

## 1. Exact inputs, PRE-MAIN recheck, and session provenance

```text
$ git branch --show-current
agent/pyat-s7-six-boundary-function-family-repair-20261031-r1

$ git rev-parse HEAD
87755f02ec5c37499b09e80db6fbdcc9316a6b15

$ git rev-parse origin/integration/pre-main-reconciliation-r1
d0342290b257f85c3e8931f9962e0aecabc84ed3

$ git rev-parse 87755f02ec5c37499b09e80db6fbdcc9316a6b15:rawlsing_next \
               d0342290b257f85c3e8931f9962e0aecabc84ed3:rawlsing_next
1d88d3fbb1d18dadfda946d9cd7f309d84afa479
1d88d3fbb1d18dadfda946d9cd7f309d84afa479
```

The actual PRE-MAIN is exactly the dispatch value `d0342290b257f85c3e8931f9962e0aecabc84ed3`; the delta from STARTUP `87755f02ec5c37499b09e80db6fbdcc9316a6b15` is three audit/workflow files only, with identical `rawlsing_next` tree. No merge or production mutation was performed.

```text
$ sqlite3 -separator ' | ' 'file:$HOME/.local/share/opencode/opencode.db?mode=ro' \
  "select id, directory, title, model, agent from session where id='ses_e6f7c46f8ffeJ808JJfoBH3866';"
ses_e6f7c46f8ffeJ808JJfoBH3866 | /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s7-six-boundary-function-family-repair-20261031-r1 | PYAT S7-FIX six boundary family repairs | {"id":"deepseek-v4.1-flash","providerID":"opencode-go","variant":"max"} | build
```

This session is not S7 `ses_e700ee99affet8V64XRG9BwxGt`, not S1/H1/H03 `ses_e7285576bffeqo0lE8N0HYK6gc`, and not an S6 author session.

Exact source SHAs read from Git objects: S6 `2c5cf86beb12b7dbeda5532614784737ad30d89d`; S7 `026ca72c24d564d4dc203f68385df8c75b4bd3a7`; S1 `6a658ad347ad0a714f40cbce04b5cd6d1f5b5ab5`; S2 `3042fca8a2165e07871d408118e1741686020cdc`; S3 `ebdb51a5c79209b2e552cfce648f7847b19386c2`; S4 `d93e8c2441dfa394e56fc1f5bcf43a0b4388adcb`; S5 `32dac59b3741dcc54f507321c7826e65174af372`; evidence law `f50651a2bb0758e9fe6d6a2852441dcc782344be`.

## 2. Exact-object AST identity test — PASS

The exact-object checker read module blobs from Git and recomputed `sha1(ast.dump(node, include_attributes=False))` for each S4 boundary ID, and exact AST qualnames for the S5 representations. It did not execute historical code.

```text
$ python3 /var/folders/78/60jhm3cd26vfr4mp4kvwk2840000gn/T/opencode/s7fix/exact_ast_check.py
{
 "s4_exact_ast_hash_ok": 12,
 "s4_bad": [],
 "s5_outer_exact_qualname_ok": 5,
 "s5_bad": [],
 "join_exact_qualname_hits": 4,
 "join_hits": [
  {"blob":"5a21bdbf314f240a8718fe64b6db734e839a8581","qualname":"PhysicalSourceIncidence.iter_batches.emit","ast_sha1":"4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445"},
  {"blob":"d3d828c171ea9fdd0e90563aff6ef705f5aae2cf","qualname":"PhysicalSourceIncidence.iter_batches.emit","ast_sha1":"4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445"},
  {"blob":"8e7a6a997f3f0a765dd7bac506a0c06af82555a0","qualname":"PhysicalSourceIncidence.iter_batches.emit","ast_sha1":"4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445"},
  {"blob":"b406d45fae419c0249b3e5c4955838542de88037","qualname":"PhysicalSourceIncidence.iter_batches.emit","ast_sha1":"4f7cd7ccb7a06b3d6a4f75f19c65dd16d6911445"}
 ],
 "status": "PASS"
}
EXIT=0
```

Checker script SHA-256: `8ce2a9765f2abdba30f8b3a3b7d5abb9d9d4067e05d05bfa3529afd4a82b8d52`. This test proves source/AST identity only; it is not behavioral equivalence.

## 3. Sourcefree membership validator — baseline PASS

```text
$ python3 PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR/SOURCEFREE_MEMBERSHIP_VALIDATOR.py --json
{
 "status": "PASS",
 "checks": [
  "corrected_family_count",
  "function_id_custody",
  "corrected_family_membership",
  "old_group_map",
  "external_zero_member_cases",
  "split_repairs",
  "join_repair",
  "review_negative_preservation",
  "first_consumer_preservation",
  "branch_identity_custody",
  "counts_and_external_cases"
 ],
 "counts": {"function_ids": 3135, "old_groups": 1881, "corrected_families": 1885, "branches": 845},
 "digests": {
  "function_ids": "5917b3bd58bb56f101d0daa35a0259761234a58a6c4bf9adaf6f0586d3593a68",
  "negative_records": "93cdb8e28653e42aebc7fe2b2c511333e85320eecee2710a37fe833fb80122f7",
  "first_consumer_records": "79a135e0910568007357083187ffb0ae337b729b94890440f29dbc5c3474e533",
  "branches": "c781d59aafff7154726f8d6d4c0c61e9f2ae409df7643ad4b2d3cbea3063ca0e",
  "inherited_branches": "5c586812883afd4333cbdae95a9ad83b68e2a774340fee9d637f7a8cb8fa2bb9"
 }
}
EXIT=0
```

## 4. Sourcefree membership validator — fail-capability self-test PASS

```text
$ python3 PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR/SOURCEFREE_MEMBERSHIP_VALIDATOR.py --self-test
PASS:
  baseline: PASS (11 checks)
  missing mapping ID: detected
  duplicate mapping ID: detected
  outer/nested mis-nesting: detected
  false join identity: detected
  lost adverse review: detected
  invented first consumer: detected
  branch roster drift: detected
  old group map drift: detected
EXIT=0
```

This demonstrates fail-capability for each required red condition: missing/duplicate IDs, lost adverse review, outer/nested mis-nesting, false join, invented first consumer, and branch/count drift.

## 5. Static ABI/import boundary test — PASS

```text
$ python3 - <<'PY'
import ast,json
p='PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR/SOURCEFREE_MEMBERSHIP_VALIDATOR.py'
t=ast.parse(open(p).read())
mods=[]
for n in ast.walk(t):
 if isinstance(n,ast.Import): mods += [a.name for a in n.names]
 if isinstance(n,ast.ImportFrom): mods.append(n.module)
print(json.dumps({'imports':sorted(set(mods)),'historical_code_imports':[m for m in sorted(set(mods)) if m and not m.split('.')[0] in {'argparse','copy','hashlib','json','os','sys'}]},indent=1))
PY
{
 "imports": ["argparse", "copy", "hashlib", "json", "os", "sys"],
 "historical_code_imports": []
}
EXIT=0
```

The validator imports only Python standard-library modules. It reads the seven artifact files and does not import or execute historical, production, or branch code.

## 6. Compile and file custody

```text
$ PYTHONPYCACHEPREFIX=<temp> python3 -m py_compile \
    PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR/SOURCEFREE_MEMBERSHIP_VALIDATOR.py
COMPILE_EXIT=0

$ wc -l FUNCTION_ID_TO_CORRECTED_FAMILY.jsonl OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl \
        REVIEW_NEGATIVE_AND_VARIANT_PRESERVATION.md 00_RETURN.md
3135 FUNCTION_ID_TO_CORRECTED_FAMILY.jsonl
1881 OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl
 380 REVIEW_NEGATIVE_AND_VARIANT_PRESERVATION.md
  99 00_RETURN.md
```

SHA-256 of the substantive artifacts (excluding this receipts file, whose hash would be self-referential):

```text
c40df2dc317e8e828d25ed0efff9d424913f238aad8a45490c56cf3d02cca219  00_RETURN.md
f7b7d4eeca135295f3d29571a13e076486be31ffab314e7308ae5e68316a71df  CORRECTED_RECEIVER_AND_INTEGRATABILITY.json
32bbf3db8666d7330b4f475b251c8f92fc90be7cea86958c1dbc45b2df05d0e1  FUNCTION_ID_TO_CORRECTED_FAMILY.jsonl
bb6f89fd98ededc502a7018a8ba3f7190918be9d7813e56d817b2b97d05af0d9  OLD_TO_NEW_S6_S7_FAMILY_MAP.jsonl
7e7f06dc314c5e740e8ef7603adf182da8a2a8d2e0e21e8aadfd4603e5769abe  REVIEW_NEGATIVE_AND_VARIANT_PRESERVATION.md
d9d0e7a23ef1c25046468ff8d669524d50eda8ae6856f4edc330c6e1e1615560  SOURCEFREE_MEMBERSHIP_VALIDATOR.py
```

`git diff --check` exit: `0`. No `__pycache__` or extra files are committed under `S7_BOUNDARY_REPAIR`.

## 7. Pass/fail summary

| Test | Result | Exact count |
|---|---|---|
| Exact-object S4 boundary AST hashes | PASS | 12/12 |
| Exact S5 outer qualnames | PASS | 5/5 |
| S5 join representation exact qualname | PASS | 4/4 variant blobs, same AST SHA-1 |
| Sourcefree validator baseline | PASS | 11/11 checks; 3,135 IDs; 1,881 old groups; 1,885 families; 845 branches |
| Sourcefree validator self-test | PASS | 8/8 mutations detected plus baseline |
| Static ABI/import boundary | PASS | 0 historical-code imports |
| Validator compile | PASS | exit 0 |
| `git diff --check` | PASS | exit 0 |

## 8. ABI limits and explicit NOT_RUN

- This is **Python AST/source identity** and **static/sourcefree membership** evidence only.
- No historical/production Python module was imported, executed, or ABI-tested.
- No C or JavaScript ABI test was run. 104 S5 rows are native C/JS (`64` `.c`, `40` `.mjs`) and are marked `NON_PYTHON__AST_NOT_APPLICABLE`.
- The C3 physical-decoder 55-test receipt is preserved as E2 author/reviewer evidence; it was **NOT_RUN** by S7-FIX.
- F7/P07 hostile attack artifacts and the HQ232/HQ236 negatives are preserved as source/review evidence; they were **NOT_RUN** by S7-FIX.
- No current production consumer was executed. First-consumer evidence is preserved source evidence, not execution.
- No ABI/schema/ownership/consumer compatibility was promoted. No behavioral equivalence or scientific issuance is claimed.
- Introducing commits for non-defect S1-S4 rows are explicitly **UNKNOWN** where only branch-tip/presence evidence was retained; no full object-history walk was performed for those rows.
- No merge, adoption, source/science/actor/world/N11/N12 authority, self-review, or PRE-MAIN mutation was performed.

## 9. Reproduction

```text
cd /Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-s7-six-boundary-function-family-repair-20261031-r1/PYAT_CONTROL_ROOM/BRANCH_RECOVERY_R1/INVESTIGATIONS/S7_BOUNDARY_REPAIR
python3 SOURCEFREE_MEMBERSHIP_VALIDATOR.py --json
python3 SOURCEFREE_MEMBERSHIP_VALIDATOR.py --self-test
PYTHONPYCACHEPREFIX=/tmp/s7fix-pyc python3 -m py_compile SOURCEFREE_MEMBERSHIP_VALIDATOR.py
```

The final commit SHA is reported externally because a commit cannot contain its own hash.
