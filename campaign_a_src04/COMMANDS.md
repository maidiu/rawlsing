# Campaign A1 commands and evidence

Run from the repository root with the frozen existing owners.

```sh
# 1. Focused non-building checks
PYTHONPATH=. python3 -m pytest campaign_a_src04/tests -q -o addopts=

# 2. Actual authorized original read, negatives, and positive C11 slice release
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode primary

# 3. Fresh-process cold replay of grant, source identity, selection and release
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode replay

# 4. Assemble the final campaign return
PYTHONPATH=. python3 campaign_a_src04/run_campaign_a_src04.py --mode return \
  --artifact-commit <code-commit>
```

Expected primary result: a `C11LogicalRelease` for the selected 42-slot /
2-coordinate slice, 7,337 source rows, with no canonical values emitted and no
weight facts. Expected negatives:

- wrong source decision -> `SOURCE_READ_SOURCE_SHA256_MISMATCH` before source I/O
- full configured release -> exact unbound observed-value refusal
- canonical retained slice -> exact `DEFER` positive-authority refusal

Expected cold replay: identical release ref/hash/source-manifest hash and local
bundle hashes. Actual source-read approval is the pinned `USER_GRANT.json`
(`feb8320a149315fdfe74ae97f0aa91a3720aa141e5a1d5cbd5e2b97746c594f1`) under
control commit `2d2814df614018dbca5687839fe562d16bf900e7`; the governing program
hash is `9e292a10df7052afb6db503a96c4b1721472d9030ab33094f8681b6bc8e49b50`.
