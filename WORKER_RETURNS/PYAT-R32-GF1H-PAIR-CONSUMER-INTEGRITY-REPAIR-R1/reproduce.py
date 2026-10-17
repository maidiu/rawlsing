"""Rebuild and run the exact GF1H source-free court in a fresh isolated stage."""
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
STAGE = Path(tempfile.mkdtemp(prefix="gf1h-r32-"))
E = "WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-GF1-GENERIC-NATIVE-PAIR-RELATION-R1"
G = "WORKER_RETURNS/PYAT-R29-GF1G-FRESH-I2-PAIR-CONSUMER-R1"
F = "WORKER_RETURNS/PYAT-R28-GF1F-IMPLEMENTED-NATIVE-CONSUMER-INDEPENDENT-R1"
I = "WORKER_RETURNS/PYAT-R18-GF1I-INDEPENDENT-GENERIC-PAIR-R1"
COURT, GF1G, GF1F, GF1I = (STAGE / path for path in (E, G, F, I))


def archive(sha, *paths, dest=STAGE):
    data = subprocess.check_output(["git", "archive", sha, *paths], cwd=REPO)
    with tarfile.open(fileobj=io.BytesIO(data)) as tar:
        for member in tar.getmembers():
            assert not member.issym() and not member.islnk()
            assert (dest / member.name).resolve().is_relative_to(dest.resolve())
        tar.extractall(dest)


def run(name, args, cwd, expected=0, env=None):
    p = subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True)
    (STAGE / (name + ".log")).write_text(p.stdout + p.stderr)
    assert p.returncode == expected, (name, p.returncode, expected, p.stdout[-1200:], p.stderr[-1200:])
    print(name, "exit", p.returncode)


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
pytest = [sys.executable, "-m", "pytest", "-q"]
run("original44_before", pytest + ["test_gf1_generic_pair.py", "--junitxml=" + str(STAGE / "original44_before.xml")], COURT / "court/repro")
run("gf1g_before", pytest + [str(GF1G / "phase_a/test_gf1g_precommitted.py"), "--junitxml=" + str(STAGE / "gf1g_before.xml")], COURT / "court/repro", 1, gf_env)
run("gf1f100_before", pytest + ["tests/test_gf1f_independent_consumer.py", "--import-mode=importlib", "-p", "no:cacheprovider", "--junitxml=" + str(STAGE / "gf1f100_before.xml")], GF1F)

for target in (COURT / "court/runtime_root/gf1_pair_support_consumer.py",
               GF1F / "candidate/court/runtime_root/gf1_pair_support_consumer.py",
               GF1I / "court/runtime_root/gf1_pair_support_consumer.py"):
    shutil.copyfile(HERE / "gf1_pair_support_consumer.py", target)

run("original44_after", pytest + ["test_gf1_generic_pair.py", "--junitxml=" + str(STAGE / "original44_after.xml")], COURT / "court/repro")
run("gf1g_after", pytest + [str(GF1G / "phase_a/test_gf1g_precommitted.py"), "--junitxml=" + str(STAGE / "gf1g_after.xml")], COURT / "court/repro", env=gf_env)
run("gf1h_new", pytest + [str(HERE / "test_gf1h_adversarial.py"), "--junitxml=" + str(STAGE / "gf1h_new.xml")], HERE, env=h_env)
run("gf1f100_after", pytest + ["tests/test_gf1f_independent_consumer.py", "--import-mode=importlib", "-p", "no:cacheprovider", "--junitxml=" + str(STAGE / "gf1f100_after.xml")], GF1F, 1)
run("gf1i19_after", pytest + ["test_gf1i_independent.py", "--junitxml=" + str(STAGE / "gf1i19_after.xml")], GF1I / "court", 1)
for n in (0, 1):
    p = subprocess.run([sys.executable, str(HERE / "cold_child.py")], cwd=HERE, env=h_env,
                       text=True, capture_output=True, check=True)
    (STAGE / f"cold_{n}.json").write_text(p.stdout)
run("package_evidence", [sys.executable, str(HERE / "package_evidence.py")], HERE,
    env=dict(h_env, GF1H_STAGE_ROOT=str(STAGE)))
print("stage", STAGE)
