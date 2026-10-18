"""GF1K reproduce.py — stage exact pinned Git sources and run every frozen court.

Stages the true native 74-module producer closure and the GF1H/GF1G/GF1F/GF1I
sources, seats the GF1H consumer first (to reproduce GF1J's two REDs), then seats
the GF1K consumer and runs original44, GF1G26, GF1H26, GF1K native-identity,
GF1F100, GF1I19 and two fresh cold processes. No frozen test is mutated.
"""
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
STAGE = Path(tempfile.mkdtemp(prefix="gf1k-r33-"))
E = "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"
G = "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1"
F = "WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1"
I = "WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1"
COURT, GF1G, GF1F, GF1I = (STAGE / p for p in (E, G, F, I))


def archive(sha, *paths, dest=STAGE):
    data = subprocess.check_output(["git", "archive", sha, *paths], cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk()
            assert (dest / member.name).resolve().is_relative_to(dest.resolve())
        tar.extractall(dest)


OUT = HERE / "03_REAL_FROZEN_COURTS_JUNIT_COLD"


def run(name, args, cwd, expected=0, env=None):
    p = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
    (OUT / (name + ".log")).write_text(p.stdout + p.stderr)
    ok = p.returncode == expected
    print(name, "exit", p.returncode, "expected", expected, "OK" if ok else "MISMATCH")
    return p.returncode

archive("eeb726357204653b22458dc267dd70ba0009bd77", E)
archive("ec5dddfcb3476c01ceb8e7f5122c5e5259b936f7", G + "/phase_a", G + "/01_FROZEN_ORACLE.json")
archive("3dcc7d7dddfff4f1be8b4293cab92e5b4275007d", F)
archive("c6a55f0dd5b327c40d64f96e0705ab5485559e90", I)
preg = STAGE / "pregf1e"
preg.mkdir()
archive("9f4a23cef1482e0a81afb1e7a65df90879931465", E + "/court", dest=preg)
shutil.copytree(preg / E / "court", GF1I / "court", dirs_exist_ok=True)

gf_env = dict(os.environ, GF1G_COURT=str(COURT), GF1G_ORACLE=str(GF1G / "01_FROZEN_ORACLE.json"))
h_env = dict(gf_env, GF1H_COURT=str(COURT), GF1H_GF1G=str(GF1G))
k_env = dict(gf_env, GF1K_COURT=str(COURT), GF1K_GF1G=str(GF1G))
pytest = [sys.executable, "-B", "-m", "pytest", "-q", "-p", "no:cacheprovider"]
targets = (COURT / "court/runtime_root/gf1_pair_support_consumer.py",
           GF1F / "candidate/court/runtime_root/gf1_pair_support_consumer.py",
           GF1I / "court/runtime_root/gf1_pair_support_consumer.py")

# ---- Phase 1: reproduce GF1J's two REDs against the GF1H consumer ----
for t in targets:
    shutil.copyfile(HERE / "before/gf1_pair_support_consumer.py", t)
run("gf1j_two_reds_before_gf1h",
    pytest + [str(HERE / "test_gf1k_native_identity.py"),
              "-k", "red1 or red2",
              "--junitxml=" + str(OUT / "gf1j_two_reds_before_gf1h.xml")],
    COURT / "court/repro", 1, k_env)

# ---- Phase 2: seat GF1K consumer and run every court ----
for t in targets:
    shutil.copyfile(HERE / "gf1_pair_support_consumer.py", t)

run("original44", pytest + ["test_gf1_generic_pair.py",
                            "--junitxml=" + str(OUT / "original44.xml")],
    COURT / "court/repro", 0)
run("gf1g26", pytest + [str(GF1G / "phase_a/test_gf1g_precommitted.py"),
                        "--junitxml=" + str(OUT / "gf1g26.xml")],
    COURT / "court/repro", 0, gf_env)
run("gf1h26", pytest + [str(HERE / "test_gf1h_adversarial.py"),
                        "--junitxml=" + str(OUT / "gf1h26.xml")],
    HERE, 0, h_env)
run("gf1k_native_identity", pytest + [str(HERE / "test_gf1k_native_identity.py"),
                                      "--junitxml=" + str(OUT / "gf1k_native_identity.xml")],
    COURT / "court/repro", 0, k_env)
run("gf1j_two_reds_after_gf1k",
    pytest + [str(HERE / "test_gf1k_native_identity.py"),
              "-k", "red1 or red2",
              "--junitxml=" + str(OUT / "gf1j_two_reds_after_gf1k.xml")],
    COURT / "court/repro", 0, k_env)
run("gf1f100", pytest + ["tests/test_gf1f_independent_consumer.py",
                         "--import-mode=importlib",
                         "--junitxml=" + str(OUT / "gf1f100.xml")],
    GF1F, 1, k_env)
run("gf1i19", pytest + ["test_gf1i_independent.py",
                        "--junitxml=" + str(OUT / "gf1i19.xml")],
    GF1I / "court", 1, k_env)

# ---- cold processes ----
cold_json = []
for n in (0, 1):
    p = subprocess.run([sys.executable, str(HERE / "cold_child.py")],
                       cwd=HERE, env=k_env, text=True, capture_output=True, check=True)
    cold_json.append(p.stdout.strip())
    (OUT / f"cold_{n}.json").write_text(p.stdout)

print("STAGE", STAGE)
