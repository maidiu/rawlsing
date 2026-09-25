from __future__ import annotations

import hashlib
import importlib.metadata
import importlib.util
import json
import os
from pathlib import Path
import platform
import py_compile
import subprocess
import sys
import tempfile

import pytest


ROOT = Path(__file__).resolve().parents[2]
HELPER = ROOT / "HQ_HANDOFF" / "launchers" / "FIABC_PYTHON_CACHE_NEUTRALITY_SUCCESSOR.py"
LAUNCHER = ROOT / "HQ_HANDOFF" / "launchers" / "RUN_DISPOSITIVE_FIABC_SIX_CELL.sh"
ENVELOPE = ROOT / "rawlsing_next" / "ee_p2x_candidate_process_envelope.py"
STAGE_BACKEND = ROOT / "rawlsing_next" / "ee_p2x_darwin_stage_backend.py"
BINDING_PATH = ROOT / "WORKER_RETURNS" / "EE-P2X" / "10C_DARWIN_DRIVER_SUCCESSOR_BINDING.json"
HISTORICAL_BINDING = ROOT / "WORKER_RETURNS" / "EE-P2X" / "10B_DARWIN_DRIVER_RECEIPT_BINDING.json"
EPOCH_PATH = ROOT / "WORKER_RETURNS" / "FIABC-CACHE-NEUTRAL-JOINED-SUCCESSOR-R1" / "01_CACHE_NEUTRAL_PHYSICAL_EPOCH.json"
EPOCH_ID = "fc6afc9bc7b287f8fd0654e1da546faee7e6c85491e6735ebe4a161b0db3de35"
HISTORICAL_10B_BLOB = "24311d54ca92a3255dcbbf05e7bc2b8d3ef19cb0"
WORKER_E_HELPER_BLOB = "0822b4e185fee4022a9a6920216fda423aa26a28"


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def _neutral_env(work: Path) -> tuple[dict[str, str], Path]:
    prefix = (work / "court" / "_python_cache_neutral_prefix").resolve()
    prefix.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONPYCACHEPREFIX"] = str(prefix)
    env["RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR"] = "1"
    env["RAWLSING_EE_P2X_PHYSICAL_EPOCH_IDENTITY"] = EPOCH_ID
    env["PYTHONPATH"] = str(ROOT)
    return env, prefix


def _run_attestation(work: Path, *, phase: str = "SOURCE_FREE_QUALIFICATION"):
    env, prefix = _neutral_env(work)
    code = (
        "import json, pathlib;"
        "from rawlsing_next.ee_p2x_candidate_process_envelope import attest_cache_neutral_runtime;"
        f"print(json.dumps(attest_cache_neutral_runtime(pathlib.Path({str(work)!r}),phase={phase!r}),sort_keys=True))"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return proc, prefix


def _valid_timestamp_pyc_then_mutate(source: Path, cached_text: str, source_text: str) -> Path:
    assert len(cached_text.encode()) == len(source_text.encode())
    source.write_text(cached_text, encoding="utf-8")
    stamp = source.stat().st_mtime_ns
    pyc = Path(
        py_compile.compile(
            str(source),
            doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
    )
    source.write_text(source_text, encoding="utf-8")
    os.utime(source, ns=(stamp, stamp))
    return pyc


def test_exact_darwin_runtime_when_qualification_gate_is_enabled():
    if os.environ.get("FIABC_REQUIRE_EXACT_DARWIN_RUNTIME") != "1":
        pytest.skip("exact Darwin runtime gate is exercised only by the qualification job")
    assert platform.python_implementation() == "CPython"
    assert platform.python_version() == "3.11.3"
    assert platform.system() == "Darwin"
    assert platform.machine() == "x86_64"
    expected = {
        "pyreadstat": "1.3.6",
        "pyarrow": "25.0.1",
        "pandas": "2.3.1",
        "numpy": "2.3.2",
    }
    assert {name: importlib.metadata.version(name) for name in expected} == expected


def test_epoch_receipt_identity_and_measurement_law_are_deterministic():
    epoch = json.loads(EPOCH_PATH.read_text(encoding="utf-8"))
    identity = epoch.pop("receipt_identity")
    canonical = json.dumps(epoch, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    assert hashlib.sha256(canonical).hexdigest() == identity == EPOCH_ID
    assert epoch["measurement_law"]["historical_pre_cache_neutral_physical_metrics_are_successor_measurements"] is False
    assert epoch["measurement_law"]["semantic_candidate_identities_changed"] is False
    assert epoch["measurement_law"]["startup_build_open_cpu_wall_rss_may_change"] is True
    assert epoch["measurement_law"]["joined_and_split_must_bind_same_epoch"] is True
    assert epoch["measurement_law"]["absolute_cross_source_physical_metric_comparison_permitted"] is False


def test_worker_e_helper_is_ported_exactly_and_precompiled_substitution_remains_forbidden():
    assert git_blob_sha1(HELPER) == WORKER_E_HELPER_BLOB
    spec = importlib.util.spec_from_file_location("_fiabc_cache_neutral_helper", HELPER)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        env = module.prepare_environment(work)
        assert env["PYTHONDONTWRITEBYTECODE"] == "1"
        assert env["RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR"] == "1"
        assert module.cache_prefix(work).is_dir()
        assert tuple(module.cache_prefix(work).rglob("*")) == ()


def test_process_cache_attestation_passes_in_fresh_non_candidate_subprocess_and_prefix_stays_empty(tmp_path):
    work = tmp_path / "work"
    proc, prefix = _run_attestation(work)
    assert proc.returncode == 0, proc.stderr
    doc = json.loads(proc.stdout)
    assert doc["status"] == "PASS__CACHE_NEUTRAL_RUNTIME_ATTESTED"
    assert doc["sys_dont_write_bytecode"] is True
    assert Path(doc["sys_pycache_prefix"]).resolve() == prefix
    assert doc["environment"]["RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR"] == "1"
    assert doc["environment"]["RAWLSING_EE_P2X_PHYSICAL_EPOCH_IDENTITY"] == EPOCH_ID
    assert doc["redirected_prefix_descendants"] == []
    assert tuple(prefix.rglob("*")) == ()


def test_process_cache_attestation_rejects_nonempty_redirected_prefix(tmp_path):
    work = tmp_path / "work"
    env, prefix = _neutral_env(work)
    (prefix / "rogue.pyc").write_bytes(b"rogue")
    code = (
        "import pathlib;"
        "from rawlsing_next.ee_p2x_candidate_process_envelope import attest_cache_neutral_runtime;"
        f"attest_cache_neutral_runtime(pathlib.Path({str(work)!r}),phase='HOSTILE_NONEMPTY')"
    )
    proc = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert proc.returncode != 0
    assert "cache-neutral prefix has descendants" in proc.stderr


def test_valid_warm_spec_pyc_is_ignored_under_cache_neutral_law_and_no_new_cache_is_written(tmp_path):
    source = tmp_path / "sample_cache_probe.py"
    cached_text = "VALUE = 'cachex'\n"
    source_text = "VALUE = 'source'\n"
    pyc = _valid_timestamp_pyc_then_mutate(source, cached_text, source_text)
    assert pyc.is_file()
    code = (
        "import importlib.util,json,pathlib,sys;"
        "p=pathlib.Path(sys.argv[1]);"
        "spec=importlib.util.spec_from_file_location('probe',p);"
        "m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);"
        "print(json.dumps({'value':m.VALUE,'prefix':sys.pycache_prefix,'dont_write':sys.dont_write_bytecode}))"
    )
    ordinary = subprocess.run([sys.executable, "-c", code, str(source)], stdout=subprocess.PIPE, text=True, check=True)
    assert json.loads(ordinary.stdout)["value"] == "cachex"

    work = tmp_path / "neutral-work"
    env, prefix = _neutral_env(work)
    neutral = subprocess.run([sys.executable, "-c", code, str(source)], env=env, stdout=subprocess.PIPE, text=True, check=True)
    doc = json.loads(neutral.stdout)
    assert doc["value"] == "source"
    assert doc["dont_write"] is True
    assert Path(doc["prefix"]).resolve() == prefix
    assert tuple(prefix.rglob("*")) == ()


def test_valid_warm_package_pyc_is_ignored_under_cache_neutral_law(tmp_path):
    pkgroot = tmp_path / "repo_like"
    pkg = pkgroot / "fixturepkg"
    pkg.mkdir(parents=True)
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    mod = pkg / "mod.py"
    cached_text = "VALUE = 'cachex'\n"
    source_text = "VALUE = 'source'\n"
    pyc = _valid_timestamp_pyc_then_mutate(mod, cached_text, source_text)
    assert pyc.is_file()
    code = "import json,fixturepkg.mod as m;print(json.dumps({'value':m.VALUE}))"
    ordinary_env = dict(os.environ)
    ordinary_env["PYTHONPATH"] = str(pkgroot)
    ordinary = subprocess.run([sys.executable, "-c", code], env=ordinary_env, stdout=subprocess.PIPE, text=True, check=True)
    assert json.loads(ordinary.stdout)["value"] == "cachex"

    work = tmp_path / "neutral-work"
    env, prefix = _neutral_env(work)
    env["PYTHONPATH"] = str(pkgroot)
    neutral = subprocess.run([sys.executable, "-c", code], env=env, stdout=subprocess.PIPE, text=True, check=True)
    assert json.loads(neutral.stdout)["value"] == "source"
    assert tuple(prefix.rglob("*")) == ()


@pytest.mark.parametrize("standin", ["work_root", "exact_owner", "repository", "site_or_stdlib"])
def test_preseeded_cache_standins_are_nonparticipants(standin, tmp_path):
    root = tmp_path / standin
    root.mkdir()
    source = root / "probe.py"
    cached_text = "VALUE = 'cachex'\n"
    source_text = "VALUE = 'source'\n"
    assert _valid_timestamp_pyc_then_mutate(source, cached_text, source_text).is_file()
    work = tmp_path / ("neutral_" + standin)
    env, prefix = _neutral_env(work)
    code = (
        "import importlib.util,json,pathlib,sys;"
        "p=pathlib.Path(sys.argv[1]);"
        "s=importlib.util.spec_from_file_location('standin_probe',p);"
        "m=importlib.util.module_from_spec(s);s.loader.exec_module(m);"
        "print(json.dumps({'value':m.VALUE}))"
    )
    proc = subprocess.run([sys.executable, "-c", code, str(source)], env=env, stdout=subprocess.PIPE, text=True, check=True)
    assert json.loads(proc.stdout)["value"] == "source"
    assert tuple(prefix.rglob("*")) == ()


def test_real_repository_warm_pyc_is_left_in_place_but_cannot_participate(tmp_path):
    real_source = ROOT / "rawlsing_next" / "fiabc_live_terminal_control.py"
    warmed_pyc = Path(
        py_compile.compile(
            str(real_source),
            doraise=True,
            invalidation_mode=py_compile.PycInvalidationMode.TIMESTAMP,
        )
    )
    assert warmed_pyc.is_file()
    work = tmp_path / "real-repo-neutral"
    env, prefix = _neutral_env(work)
    code = (
        "import json,pathlib;"
        "import rawlsing_next.fiabc_live_terminal_control as m;"
        "print(json.dumps({'file':m.__file__,'cached':m.__cached__}))"
    )
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=True,
    )
    doc = json.loads(proc.stdout)
    assert Path(doc["file"]).resolve() == real_source.resolve()
    assert Path(doc["cached"]).resolve().is_relative_to(prefix)
    assert warmed_pyc.is_file()
    assert tuple(prefix.rglob("*")) == ()


def test_process_envelope_handshake_dynamically_binds_cache_neutral_fields_without_candidate_owner(tmp_path):
    work = tmp_path / "court-probe"
    env, prefix = _neutral_env(work)
    backend = tmp_path / "source_free_probe_backend.py"
    backend.write_text(
        "BACKEND_CONTRACT='RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0'\n"
        "_SESSIONS={}\n"
        "def run_stage(context, services):\n"
        "    raise RuntimeError('qualification probe must never run a stage')\n",
        encoding="utf-8",
    )
    source, candidate, cell_key = "COURT", "ALL", "COURT/ALL"
    freeze_sha = "f" * 64
    env.update({
        "RAWLSING_EE_P2X_CELL_SOURCE": source,
        "RAWLSING_EE_P2X_CELL_CANDIDATE": candidate,
        "RAWLSING_EE_P2X_CELL_KEY": cell_key,
        "RAWLSING_EE_P2X_UPSTREAM_FREEZE_SHA256": freeze_sha,
    })
    proc = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "rawlsing_next.ee_p2x_candidate_process_envelope",
            "--child",
            "--backend-spec",
            str(backend),
            "--context-mode",
            "SIMPLE_TEST_ONLY",
        ],
        cwd=ROOT,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdin is not None and proc.stdout is not None
    start = {
        "schema": "RAWLSING_FIABC_P2X_CELL_PROCESS_PROTOCOL@1.0.0",
        "op": "START",
        "source": source,
        "candidate": candidate,
        "cell_key": cell_key,
        "parent_envelope_start_monotonic_ns": 1,
        "freeze_receipt_sha256": freeze_sha,
        "work_root": str(work),
    }
    proc.stdin.write(json.dumps(start, sort_keys=True) + "\n")
    proc.stdin.flush()
    line = proc.stdout.readline().strip()
    protocol_prefix = "RAWLSING_FIABC_CELL_PROCESS "
    assert line.startswith(protocol_prefix), line
    handshake = json.loads(line[len(protocol_prefix):])
    assert handshake["op"] == "HANDSHAKE"
    att = handshake["cache_neutral_attestation"]
    assert att["phase"] == "MAIN_CELL_CHILD_PRE_BACKEND_IMPORT"
    assert att["sys_dont_write_bytecode"] is True
    assert Path(att["sys_pycache_prefix"]).resolve() == prefix
    assert att["redirected_prefix_descendants"] == []

    proc.stdin.write(json.dumps({
        "schema": "RAWLSING_FIABC_P2X_CELL_PROCESS_PROTOCOL@1.0.0",
        "op": "STOP",
        "cell_key": cell_key,
        "reason": "SOURCE_FREE_QUALIFICATION_COMPLETE",
    }, sort_keys=True) + "\n")
    proc.stdin.flush()
    stop_line = proc.stdout.readline().strip()
    assert stop_line.startswith(protocol_prefix), stop_line
    stopped = json.loads(stop_line[len(protocol_prefix):])
    assert stopped["op"] == "STOPPED"
    assert stopped["cache_neutral_attestation"]["phase"] == "MAIN_CELL_CHILD_STOP"
    proc.stdin.close()
    assert proc.wait(timeout=20) == 0
    assert tuple(prefix.rglob("*")) == ()


def test_process_envelope_attests_before_backend_import_and_at_cell_stop():
    source = ENVELOPE.read_text(encoding="utf-8")
    child = source[source.index("def _child_main"):source.index("class ProcessIsolationController")]
    assert child.index('phase="MAIN_CELL_CHILD_PRE_BACKEND_IMPORT"') < child.index("backend = _load_backend")
    assert '"cache_neutral_attestation": cache_attestation' in child
    assert 'phase="MAIN_CELL_CHILD_STOP"' in child
    controller = source[source.index("class ProcessIsolationController"):]
    assert 'phase="PARENT_PRE_CELL_START"' in controller
    assert 'phase="PARENT_PRE_CELL_STOP"' in controller
    assert 'phase="PARENT_POST_CELL_STOP"' in controller
    assert '"parent_pre_cell_start_cache_attestation"' in controller
    assert '"parent_post_cell_stop_cache_attestation"' in controller
    assert 'env = dict(os.environ)' in controller
    assert 'env.pop("PYTHONPYCACHEPREFIX"' not in controller
    assert 'env.pop("PYTHONDONTWRITEBYTECODE"' not in controller


def test_s15_fresh_replay_attests_in_child_before_semantic_work_and_parent_after_replay():
    source = STAGE_BACKEND.read_text(encoding="utf-8")
    cli = source[source.index("def _fresh_replay_cli"):source.index("def _s15")]
    assert cli.index("cache_attestation=attest_cache_neutral_runtime") < cli.index("from rawlsing_next.ee_p2x_darwin_court_driver import DriverServices")
    assert '"cache_neutral_attestation":cache_attestation' in cli
    s15 = source[source.index("def _s15"):source.index("def _s16")]
    assert 'phase="S15_PARENT_PRE_FRESH_REPLAY"' in s15
    assert 'expected_phase="FRESH_REPLAY_CHILD_PRE_SEMANTIC_WORK"' in s15
    assert 'phase="S15_PARENT_POST_FRESH_REPLAY"' in s15
    assert '"cache_neutral_attestation":doc.get("cache_neutral_attestation")' in s15
    popen = s15[s15.index("p=subprocess.Popen"):s15.index("out,_=p.communicate")]
    assert "env=" not in popen


def test_joined_launcher_establishes_cache_neutral_epoch_immediately_before_measured_driver():
    source = LAUNCHER.read_text(encoding="utf-8")
    export_pos = source.index("export PYTHONDONTWRITEBYTECODE=1")
    driver_pos = source.index('"$PYTHON_BIN" -m rawlsing_next.ee_p2x_darwin_court_driver')
    assert export_pos < driver_pos
    assert source.index('CACHE_PREFIX="$WORK_ROOT/court/_python_cache_neutral_prefix"') < export_pos
    assert 'export PYTHONPYCACHEPREFIX="$CACHE_PREFIX"' in source[export_pos:driver_pos]
    assert "export RAWLSING_EE_P2X_CACHE_NEUTRAL_SUCCESSOR=1" in source[export_pos:driver_pos]
    assert f'PHYSICAL_EPOCH_IDENTITY="{EPOCH_ID}"' in source
    assert source.count('find "$CACHE_PREFIX" -mindepth 1 -print -quit') >= 3
    assert "git merge-base --is-ancestor \"$SUCCESSOR_COMMISSION\" HEAD" in source
    assert 'EXPECTED_BRANCH="agent/rabochii-fiabc-cache-neutral-joined-successor-r1"' in source
    assert "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09" in source
    assert "2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d" in source


def test_driver_successor_repo_and_runtime_gate_close_exact_target():
    from rawlsing_next import ee_p2x_darwin_court_driver as driver

    assert driver.EXECUTION_BRANCH == "agent/rabochii-fiabc-cache-neutral-joined-successor-r1"
    assert driver.P2X_BRANCH == "agent/rabochii-prev3-ee-p2x-final-abc-equal-work-execution-r1"
    assert driver.EXPECTED_RUNTIME == {
        "implementation": "CPython",
        "python": "3.11.3",
        "pyreadstat": "1.3.6",
        "pyarrow": "25.0.1",
        "pandas": "2.3.1",
        "numpy": "2.3.2",
        "system": "Darwin",
        "machine": "x86_64",
    }
    if os.environ.get("FIABC_REQUIRE_EXACT_DARWIN_RUNTIME") == "1":
        driver.verify_runtime_gate(driver.observe_host())


def test_10c_successor_binding_closes_exact_blobs_and_10b_is_immutable():
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    assert git_blob_sha1(HISTORICAL_BINDING) == HISTORICAL_10B_BLOB
    assert binding["hq_authority"]["historical_10b_git_blob_sha1"] == HISTORICAL_10B_BLOB
    assert binding["schema"] == "RAWLSING_EE_P2X_DARWIN_DRIVER_SUCCESSOR_BINDING@1.0.0"
    assert git_blob_sha1(ROOT / binding["driver"]["path"]) == binding["driver"]["git_blob_sha1"]
    for item in binding["successor_surfaces"].values():
        assert git_blob_sha1(ROOT / item["path"]) == item["git_blob_sha1"]
    assert binding["physical_epoch"]["receipt_identity"] == EPOCH_ID
    assert git_blob_sha1(ROOT / binding["physical_epoch"]["path"]) == binding["physical_epoch"]["git_blob_sha1"]
    assert git_blob_sha1(ROOT / binding["six_cell_execution_manifest"]["path"]) == binding["six_cell_execution_manifest"]["git_blob_sha1"]
    assert binding["implementation_binding_scheme"]["ancestor_required"] == "79b10777df2c8733edee56f6a18d880b3c664779"


def test_10c_terminal_vocabulary_preserves_repaired_t5_joined_nonpass_semantics():
    binding = json.loads(BINDING_PATH.read_text(encoding="utf-8"))
    vocab = binding["terminal_vocabulary"]
    assert vocab["pass_status"] == "COURT_SEQUENCE_COMPLETE__S17_VERIFIED"
    assert vocab["candidate_local_nonpass"].endswith("S17_SUCCESS_VERIFIER_NOT_RUN")
    assert vocab["common_source_nonpass"].endswith("S17_SUCCESS_VERIFIER_NOT_RUN")
    assert vocab["success_verifier_must_not_run_after_any_nonpass"] is True
