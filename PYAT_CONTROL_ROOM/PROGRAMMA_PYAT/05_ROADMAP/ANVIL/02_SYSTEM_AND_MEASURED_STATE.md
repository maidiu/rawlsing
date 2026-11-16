# 02 — Plain-language C11 mechanics, actual code, and physical evidence

**This document anchors architecture arguments to the concrete machine.** Treat figures as sourcefree/scoped reports unless separately accepted. The exact source of a measurement matters: an S1-E journal is not a direct S2-C writer, an I02 semantic proof is not an SQLite query index, and a sourcefree test is not a governed wave.

## 1. What the stages mean

| Stage | Human description | On disk / in RAM | Failure rule |
|---|---|---|---|
| Source selection / projection (S01–S03) | Choose an actually authorized file, interpret source-specific questionnaire, respondent frame, question roles and answer codes; make the thirteen kinds of standard records | SAV/DTA source, configured rules, bounded record production | No guessed wave/alias, weight, semantic role, routing law or permission |
| **Stage 2: staged publication** | Build private C11 output while certifying source semantics; prove exact physical fidelity before naming it a completed release | Temporary proof DB, batches, staging files, commits | Failure/interrupt never publishes an incomplete/false release |
| **Stage 3: authenticated canonical C11** | Finished authoritative standardized evidence | Full thirteen-family Parquet/Zstd estate, manifest, hashes, replay/source roots | Physical integrity alone does not grant present rights |
| **Stage 4: prepared analysis** | Efficiently ask many varied scientific questions without rebuilding everything | Temporary or verified persistent access locators, respondent/question indices, prepared conditional populations and downstream outputs | Derived structures are not new authority; exact CURRENT/source/negative/replay semantics remain |

**Canonical** means standardized authoritative source representation *within Rawlsing*, not scientific proof that a survey item correctly measures a structural concept. **Authenticated** means linked to independently trusted source/proof identities and checked physical members; CURRENT asks whether the relevant use remains permitted.

Example: a 100k respondent × 200-question dataset might contain multiple country/wave universes. Query Q17 among unemployed Lebanese 30–40 year olds requires identity, source scope, actual observed answers, routing/asked eligibility, weight design, and a proper denominator. Stage 4 must not treat a question not asked as observed zero.

## 2. The actual physical implementation and costly transformations

Relevant code at `b830458c3ebfe0a3f0e2d18e516e68b90324c88a` (sourcefree corrective branch, not protected):
- [`pre553_source_saved_body_bridge.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/pre553_source_saved_body_bridge.py): S1-E qualified source bridge journals thirteen JSONL families, then reconstructs typed objects for S2-C consumption. This is **upstream integrated-path cost**.
- [`pre553_source_direct_parquet_estate.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/pre553_source_direct_parquet_estate.py): **direct** writer consumes thirteen family iterators, writes canonical `body_json` plus typed selector columns, constructs I02 proof, emits Parquet/Zstd, independently rereads physical families and verifies typed-vs-body projections before atomic publication. Do **not** blame 100k direct-writer runtime on the bridge journals.
- [`_pre553_direct_i02_sourcefree.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/_pre553_direct_i02_sourcefree.py) and [`_pre553_external_i02_certificate.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/_pre553_external_i02_certificate.py): temporary SQLite semantic uniqueness/identity/referential joins, ordering/root construction and certification; not interchangeable with I03 postings database.
- [`pre553_direct_estate_i03.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/pre553_direct_estate_i03.py): cold reader builds per-session private SQLite `events` and `members` physical locators, holds scoped respondent identity, reads row-groups/selected bodies and supplies native I03. Its event postings favor respondent lookups; no general question-major analysis substrate is proven.
- [`_pre553_query_eval.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/_pre553_query_eval.py) and [`_pre553_query_predicate.py`](https://github.com/maidiu/rawlsing/blob/b830458c3ebfe0a3f0e2d18e516e68b90324c88a/rawlsing_next/_pre553_query_predicate.py): native respondent-scanning risk/condition/target/weight calculation, evidence collection and result/replay.

**body_json has a reason to exist:** existing typed columns are not a fully proved reversible canonical representation for all thirteen families. Removing it is a semantic/schema migration requiring its own rigorous codec and replay/reader proof—not automatically an optimization.

## 3. Measured resource failures and progress

| Cut/workload | Reported outcome | What can be inferred |
|---|---|---|
| Older W03 saved artifact, 100k rows/200k events | Peak **6,468,513,792 B RSS**, greater than 6GiB | Old eager/packed attempt failed physical resource ceiling; not a current direct-writer benchmark |
| Direct sourcefree 100k respondents, ~3.245 events/person | Writer **3,033.723s**; retained **310.16MB**; staging **5.26GB**; temporary I02 **4.39GB** | Direct writer and proof economics are a severe target; tiny question width makes this insufficient as realistic wide-survey certification |
| Same sourcefree cold native session | Temporary I03 postings **~1.30GB** | Session construction can be materially expensive at scale |
| Pre-W05 selected 100k cold query | **562.362s** on selected experiment | Historical before physical-order correction; must not claim current post-W05 latency from this number |
| J5 128 respondents×5Q, 100 *distinct* queries | Baseline 213.456s/100 builds/28,076 reads/97.6MB RSS vs local prepared 126.424s/1 build/17,384 reads/89.1MB RSS | Author-reported 1.69×; exact 100/100 parity claimed; tiny fixture remains expensive |
| J5 64 respondents×30Q, 20 distinct queries | Baseline 142.996s/20 builds/121,882 reads/263.9MB RSS vs prepared 83.873s/1 build/71,304 reads/162.9MB RSS | Author-reported 1.70×; 20/20 full fact/replay/parity claimed; not realistic full-width proof |
| Same 64×30 construction | 29.954s writer + 3.196s fixture; ~39.6MB retained; 1,638 events; 1,920 routing facts; 64 weights | Important to measure construction, retrieval and emitted output separately |
| Prepared candidate author run | **80 PASS** focused; 8/8 I05 receipt/frontier parity; 100k/6GiB NOT_RERUN | Author tests do not substitute independent review or authorized real-source use |

**Prepared-session publication correction:** Earlier dialogue recorded local unpushed `cea2d4d3009e9087d2267e9d1f53bec28b730dc7`. Later GitHub inspection verified [the commit now exists remotely](https://github.com/maidiu/rawlsing/commit/cea2d4d3009e9087d2267e9d1f53bec28b730dc7) and its branch `implementation/pyat-p0-c11-operable-20261115-r1` exists. This changes **PUBLISHED**, not **INDEPENDENTLY_ACCEPTED** or **PROTECTED**. `pre553_prepared_saved_i03.py` retains the original evaluator and existing source/current checks, but still constructs an index per prepared process, and does not add group-core reuse.

**Caution about metric arithmetic:** Raw disk sizes cannot be equated with process RSS or full downstream output cost. Small-fixture read counts are not proof of large-wave performance. “~1.7×” is a measured author ratio, **not a projected general speedup**.

## 4. Source and semantic distinctions that cost optimizations must preserve

- All thirteen families, full response occurrences, native vs canonical refs, exact raw representation and typed missing/unknown/not asked semantics.
- Original questionnaire role/option/scale/overlay selection, QUC/QRA rules where applicable, actual source editions, country/wave/household/respondent scope and no source-specific guessed golden path.
- One vs many respondents, actual weights/strata/clusters and legal estimands; RAW vs selected governed weighted; absent design information yields held/unknown uncertainty, not invented confidence.
- Full physical member integrity and independent source-I02 proof, duplicate/ref/locator poisoning refusals, atomic publish/rollback/replay, lawful held negatives.
- CURRENT and revocation before and during repeated operations, with no covert stale index or wrong-as-of reuse.
- Correct F2 forward/reverse direction and denominators; F4 genuine 3+ same-person tuple rather than product of marginals; F3 recursive/minority history and out-of-domain/zero statuses.

## 5. Three *different* performance problems

1. **Construction**: decoding, canonicalization, staging, semantic proof, compression, physical readback, publication.
2. **Access and computation**: cold member authentication, index building, per-person event selection, routing/predicate evaluation, respondent-aligned joins, weight aggregation.
3. **Output/evidence volume**: large explicit member refs, used objects/authority closures, full cell distributions, replay hashes and downstream stored derived products.

Improving one does not establish the others. The decisive system benchmark must eventually include source→C11→many distinct I03/I05/F1–F4→Field Forge/learned consumer, not merely a cheap Parquet file or a single cached query.

## 6. Facts that remain unproved

- Full source-authorized real SAV/DTA width, country/wave combinations, present field use rights and native original35 science.
- All-stage 100k/6GiB process-tree economics (including writer, cold read, derived products, recovery, full results); acceptable runtime/size targets remain undecided.
- Sourcefree joined #998 independent complete first-consumer; materialized field/world/person pilot #1009/#1011.
- Exact current protected adoption and independent G5 for the latest prepared-session code.
- Whether a proposed output-witness representation can preserve all v1 consumer and replay invariants; no such migration is selected.
