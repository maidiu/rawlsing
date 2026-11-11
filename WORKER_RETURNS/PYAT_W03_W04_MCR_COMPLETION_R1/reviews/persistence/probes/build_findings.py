#!/usr/bin/env python3
"""Build W04 review findings JSONL from retained evidence."""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent

COUNTS = {
    "reviewed_head": "605ce4c409857155eaf8dad7ca4e9c2ae0b15638",
    "corrected_anchor": "1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc",
    "prior_source_cut": "46b7325637e68f78ccc7487d4b1abc7009c5ac0b",
    "source_tree_files": 402,
    "selected_tests": "40 passed",
    "facade_tests": "10 passed",
    "focused_completion_tests": "7 passed",
    "poison_revoke_torn_tests": "3 passed",
    "legacy_fallback_cache_writes": 1,
    "dir_fsync_failure_raised": False,
    "dir_fsync_destination_exists": True,
    "benchmark_100k": "NOT_RUN",
}
HASHES = {
    "execution_view_git": "28a27961f32435665b40ba47e54a73aa2516fc42",
    "execution_view_sha256": "e359196c5b42d9c8f54ba1f7b6359f32011edbcbb8a117b27ba39fdfb69758ff",
    "w04_cache_git": "9d4fb2ee7d925156cccad893b02246a36ff329f9",
    "w04_cache_sha256": "e0f6a3a4ec2f56c8f9f14aedba20521f642d23e74d5f2d10a9fa8e0edf61f210",
    "parquet_carrier_git": "b5f8d2cbf90153e382c3a13cdd3ce75d032c7084",
    "parquet_carrier_sha256": "8c85f4b583485078b598c7d86381bf19b8e9df352ce262ea32a1da072bec82ad",
    "completion_test_git": "0df94b3649bbc869fe245bc7185e35218fa4d085",
    "completion_test_sha256": "5aaa6761c47243066bb11e033e3ce1af20fba57ae4884f2462efb1899233265f",
    "prior_execution_view_blob": "986f327aa18053edc61bd837cdded02bbf8388d9",
    "prior_execution_test_blob": "8e8effa58579af0c3326ecd4af7e159947abe4ec",
}
B = "WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/reviews/persistence"

FINDINGS = [
    {
        "FINDING_ID": "W04-F01",
        "SEVERITY": "P1",
        "STATUS": "REPAIR_REQUIRED",
        "SUBJECT": "Legacy environment fallback masquerades as policy authorization",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_w04_cache.py:142-198; rawlsing_next/_pre553_c11_execution_view.py:205-218; probes/adversarial_probe.py",
        "EVIDENCE": "In an ordinary Python process (not pytest), setting PYTEST_CURRENT_TEST and RAWLSING_C11_ACCELERATOR_DIR made load_policy() return an accepted policy with authorization_id=PYTEST_TEMP_ROOT_EXPLICIT and NONRESPONDENT_SOURCEFREE, and _execute(_fixture()) wrote one c11-events-*.parquet under the chosen temp root. The fallback also created an absent root. PYTEST_CURRENT_TEST is an ordinary environment variable and is not proof of a pytest process. This contradicts the lane claim that a bare legacy directory variable is test-only and cannot become a deployment grant.",
        "MINIMUM_EXACT_REPAIR": "Remove the RAWLSING_C11_ACCELERATOR_DIR/PYTEST_CURRENT_TEST fallback from production load_policy. Migrate the existing test cache helper to an explicit private policy file under RAWLSING_C11_ACCELERATOR_POLICY in tmp_path (the new completion tests already use this pattern). Do not substitute another environment marker. If a test-only injection remains, use a non-environment test API unavailable to deployment, and re-review any changed prior accepted test blob.",
        "LIMIT": "The probe wrote only a sourcefree fixture cache under the review lease temp root; no original respondent/source bytes or deployment root grant.",
    },
    {
        "FINDING_ID": "W04-F02",
        "SEVERITY": "P2",
        "STATUS": "REPAIR_REQUIRED",
        "SUBJECT": "Directory fsync failure is swallowed and reported as success",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_w04_cache.py:296-311; rawlsing_next/pre553_parquet_carrier.py:46-52,246,256,282-286; probes/adversarial_probe.py",
        "EVIDENCE": "The probe patched _pre553_w04_cache.os.fsync to raise OSError. fsync_dir returned normally, atomic_replace placed the destination, the destination existed, and no exception was raised. A failed directory fsync is therefore indistinguishable from success. For the disposable cache this can become a safe miss/rebuild after a crash; for ParquetC11Carrier.persist, the method can return a target and report success after a failed parent-directory fsync, so the claimed file+directory durability is not fail-closed. Replace-failure tests do not cover this branch.",
        "MINIMUM_EXACT_REPAIR": "Make fsync_dir fail closed (raise or return success/failure). Cache callers treat failure as safe miss/abort and remove the new cache if needed; ParquetC11Carrier.persist raises and cleans up/leaves no accepted target rather than returning success. Add focused fsync-failure tests for both cache and canonical publication.",
        "LIMIT": "No new store or engine is needed; this is a durability/error-propagation repair.",
    },
    {
        "FINDING_ID": "W04-F03",
        "SEVERITY": "P3",
        "STATUS": "REPAIR_RECOMMENDED",
        "SUBJECT": "Crash-orphaned hidden cache staging file survives retention and is not budgeted",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_w04_cache.py:25,220-264,300-313; probes/adversarial_probe.py",
        "EVIDENCE": "The cache writer stages with prefix .c11-events- while retention globs c11-events-*.parquet. A .c11-events-orphan file with old mtime remained after prune under a max_files=1/max_age_seconds=1 policy. A hard process crash between staging and commit can therefore leave hidden source-derived cache bytes that are neither reclaimed by retention nor counted against max_bytes/max_files. Normal abort/replace tests do not cover a hard crash.",
        "MINIMUM_EXACT_REPAIR": "Prune stale hidden .c11-events-* staging files by policy age (or a short staging grace period), or stage in a dedicated staging subdirectory cleaned on policy load; include them in the retention accounting. They must never be accepted as cache (already true).",
        "LIMIT": "Disposable cache only; no false SUPPORTED fact. Resource/cleanup gap, not a canonical-store defect.",
    },
    {
        "FINDING_ID": "W04-P01",
        "SEVERITY": "INFO",
        "STATUS": "PASS_EXCEPT_F01",
        "SUBJECT": "Policy-file activation and path/owner/permission edges",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_w04_cache.py:57-139; rawlsing_next/tests/test_pre553_w03_w04_completion.py:69-125; probes/adversarial_probe.py",
        "EVIDENCE": "With an explicit policy file: authorized private root activates; absent/invalid policy, relative/missing/0755 root, final-component root symlink, policy-file symlink, group/world-writable policy file, missing authorization id/budget, simulated owner mismatch and legacy root outside temp are rejected; invalid configured policy does not fall back to legacy; max_files/max_age prune leaves one cache file. The persistent cache is reached through the actual Route B facade and I03/I05 consumers.",
        "MINIMUM_EXACT_REPAIR": "None beyond W04-F01.",
    },
    {
        "FINDING_ID": "W04-P02",
        "SEVERITY": "INFO",
        "STATUS": "PASS",
        "SUBJECT": "Cache key/envelope, poison/rehash and revocation",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_c11_execution_view.py:228-298,441-468; rawlsing_next/tests/test_pre553_c11_execution_view.py:59-145; rawlsing_next/tests/test_pre553_w03_w04_completion.py:128-150",
        "EVIDENCE": "Key/envelope bind schema, source, decoder/transport, projection, authority root, release, release manifest, replay, trusted policy root and member root. _read_bodies checks the expected envelope/key and every body SHA-256 against selector refs; body poison/rehash under the unchanged key is a safe miss/rebuild; revoked workload and stale/torn cache tests refuse before the warmed accelerator. The 40-case selected suite and 3 focused poison/revoke/torn tests passed.",
        "MINIMUM_EXACT_REPAIR": "None for the tested scope.",
    },
    {
        "FINDING_ID": "W04-P03",
        "SEVERITY": "INFO",
        "STATUS": "PASS_WITH_F02_F03_GAPS",
        "SUBJECT": "Atomic cache/canonical lifecycle; canonical/disposable separation",
        "FILE_OR_RECORD": "rawlsing_next/_pre553_c11_execution_view.py:300-351,469-507; rawlsing_next/pre553_parquet_carrier.py:237-289; rawlsing_next/tests/test_pre553_w03_w04_completion.py:152-233",
        "EVIDENCE": "Staged private cache file, fsync, atomic replace; canonical carrier fsyncs members/manifest/payload and atomically replaces; interrupted cache/canonical publication keeps previous/safe miss; 4 concurrent builders share one exact release; deletion/rebuild and corruption/trusted rebuild pass; canonical Parquet survives accelerator deletion and exact I03/I05 material is preserved. Gaps: swallowed directory-fsync failure (W04-F02) and hidden crash-orphan staging cleanup (W04-F03).",
        "MINIMUM_EXACT_REPAIR": "Apply W04-F02/W04-F03; no second store/engine.",
    },
    {
        "FINDING_ID": "W04-P04",
        "SEVERITY": "INFO",
        "STATUS": "PASS",
        "SUBJECT": "Actual caller and exact typed facts",
        "FILE_OR_RECORD": "rawlsing_next/pre553_route_b_production.py:495-570; rawlsing_next/pre553_source_backed_c11_facade.py:656-685; rawlsing_next/tests/test_pre553_c11_cold_reopen_i03.py; rawlsing_next/tests/test_pre553_w03_w04_completion.py:217-233",
        "EVIDENCE": "execute_route_b_production -> build_source_backed_c11_repository -> _compact_public_objects; tests exercise actual I03/I05 consumers. _consumer_material compares full typed facts, discovery receipts, source releases and repository snapshot identity across cold reopen, missing optional weight and valid-empty fixtures. Cache stores event bodies only; non-event objects/authority/weights/occurrences/ranks/zero remain canonical.",
        "MINIMUM_EXACT_REPAIR": "None for the tested scope.",
    },
    {
        "FINDING_ID": "W04-L01",
        "SEVERITY": "INFO",
        "STATUS": "UNPROVED",
        "SUBJECT": "Memory/resource/economic utility",
        "FILE_OR_RECORD": "MCR W03-COLD-HIGHWATER / W34-RESOURCE-ECONOMY; review scope",
        "EVIDENCE": "No 100000-event benchmark, paired process cold RSS, wall/CPU/disk/amortization measurement or economic acceptance was run in this lane. Test counts are not economic acceptance. Resource utility remains UNPROVED until the integrated candidate 100k measures.",
        "MINIMUM_EXACT_REPAIR": "Separate benchmark/economic lane at the integrated candidate head; no claim now.",
    },
    {
        "FINDING_ID": "W04-L02",
        "SEVERITY": "INFO",
        "STATUS": "RETAINED_NOT_FINAL",
        "SUBJECT": "PR895 prior capital and whole-12 boundary",
        "FILE_OR_RECORD": "PYAT_W03_W04_MCR_C_Commission.md; WORKER_RETURNS/PYAT_W03_W04_MCR_COMPLETION_R1/lanes/persistence/00_RETURN.md",
        "EVIDENCE": "PR895/source 46b7325637e68f78ccc7487d4b1abc7009c5ac0b and its prior 43-pass sourcefree run are retained as prior capital, not final proof. This review covers only the W04 persistence lane; whole 12-ID MCR-C, cross-lane integration, independent economic review and protected receiving remain open. PR895 and protected terrain were untouched.",
        "MINIMUM_EXACT_REPAIR": "No merge or whole-goal acceptance; final whole-12 same-head code + economic receiving still required.",
    },
]


def main() -> int:
    records = [{"RECORD_TYPE": "FINDING", **f, "COUNTS": COUNTS, "HASHES": HASHES} for f in FINDINGS]
    records.append({
        "RECORD_TYPE": "VERIFICATION",
        "VERDICT": "REVISE",
        "REVIEWED_HEAD": "605ce4c409857155eaf8dad7ca4e9c2ae0b15638",
        "CORRECTED_ANCHOR": "1b0c8dc4c4c6350aa77f70fea9470f5b18aa21dc",
        "PRIOR_SOURCE_CUT": "46b7325637e68f78ccc7487d4b1abc7009c5ac0b",
        "COUNTS": COUNTS,
        "HASHES": HASHES,
        "DEFECTS": ["W04-F01", "W04-F02", "W04-F03"],
        "POSITIVE_SCOPE": ["W04-P01 except F01", "W04-P02", "W04-P03 with F02/F03 gaps", "W04-P04"],
        "BOUNDARY": "W04 persistence lane only; no whole 12-ID, economic, native/S3/science/actor, protected merge or deployment host grant.",
        "LIMITS": {
            "no_source_respondent_sav_dta_db_read": True,
            "no_native_s3_science_actor": True,
            "no_environment_install": True,
            "no_100k_benchmark": True,
            "no_production_existingtest_author_hq_peer_protected_write": True,
            "no_merge": True,
            "quota": "UNKNOWN",
        },
    })
    text = "\n".join(json.dumps(r, sort_keys=True) for r in records) + "\n"
    (REVIEW / "FINDINGS.jsonl").write_text(text)
    print(f"wrote {len(records)} records to {REVIEW / 'FINDINGS.jsonl'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
