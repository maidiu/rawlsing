"""E06I precommitment: write the independent joined-native oracle BEFORE running
the reviewer court.  Numerical expectations are derived from the raw synthetic
source rows (native C11 input) only; permission/clock/cold expectations are
stated from the E04T/E05R semantics and the commission's hostile list.
"""
import json, hashlib, sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]              # reviewer return dir
CAND = Path(sys.argv[1] if len(sys.argv) > 1 else
            '/tmp/e06i/court/WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1')
CAND_SHA = 'f9c52113de38caececc450f0e54c980f64ed3981'
E04T = '79cb8244a5291218bde17142b93fc2419eade396'
E04U = 'f1ca9c530f6f03053ca981b49eefc91b85be47b8'
E05R = '84485d32c0088995f8dc664dc0517b2d27f2563d'
E05S = 'f524f60781e2e7e72278d04d6377fb1da877698a'

def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---- independent numerical derivation from the raw native source rows --------
RT = CAND / 'runtime'
sys.path[:0] = list(map(str, [CAND, CAND / 'repro', RT / 'owners', RT,
                              RT / 'rawlsing_next/tests', RT / 'rawlsing_next']))
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03  # noqa: E402

def _rows(changed=False, support_loss=False):
    rows = [dict(r, responses=dict(r['responses'])) for r in e03.synthetic_world_rows()]
    if changed:
        next(r for r in rows if all(r['responses'][q] == 1 for q in 'ABC') and r['responses']['Y'] == 0)['responses']['Y'] = 1
    if support_loss:
        rows = [r for r in rows if not all(r['responses'][q] == 1 for q in 'ABC')]
    return rows

def _table(rows, target, conditions):
    sel = [r for r in rows if all(r['responses'][q] == v for q, v in conditions)]
    return (sum(1 for r in sel if r['responses'][target] == 1), len(sel))

_base, _changed, _loss = _rows(), _rows(changed=True), _rows(support_loss=True)
fwd = [_table(_base, 'Y', c) for c in [(('A',1),), (('A',1),('B',1)), (('A',1),('B',1),('C',1))]]
mnt = [(t[1] - t[0], t[1]) for t in fwd]
y01 = [_table(_changed, 'Y', c) for c in [(('A',1),), (('A',1),('B',1)), (('A',1),('B',1),('C',1))]]
zs = [_table(_loss, 'Y', c) for c in [(('A',1),), (('A',1),('B',1))]]
zt = {'denominator': _table(_loss, 'Y', (('A',1),('B',1),('C',1)))[1]}
_rev = _table(_base, 'A', (('Y',1),))
_strata = {}
for r in _base:
    k = ''.join(str(r['responses'][q]) for q in 'ABC')
    _strata.setdefault(k, [0, 0])[0 if r['responses']['Y'] == 1 else 1] += 1
deriv = {'base': {'respondents': len(_base), 'c11_events': 4 * len(_base), 'strata': _strata},
         'reverse': {'yes': _rev[0], 'denominator': _rev[1]}}
fwd = [list(t) for t in fwd]; mnt = [list(t) for t in mnt]; y01 = [list(t) for t in y01]
zs = [list(t) for t in zs]

oracle = {
    "schema": "E06I_INDEPENDENT_PRECOMMITTED_JOINED_NATIVE_ORACLE@1",
    "grade": "PRECOMMITTED_BEFORE_INDEPENDENT_REVIEWER_COURT_EXECUTION",
    "reviewer": {
        "role": "independent hostile cross-owner reviewer; not E06 author, issuer, HQ or installer",
        "branch": "agent/reviewer-pyat-20261016-r18-e06i-full-bridge-independent-r1",
        "sealed_startup": "6aea052f09ef01205aff1c38cd8c68197b762447",
        "commission": "WORKER_COMMISSIONS/PYAT-R18-E06I-INDEPENDENT-FULL-BRIDGE-R1/00_COMMISSION.md",
    },
    "candidate": {
        "branch": "agent/userdirect-pyat-20261016-r17-e06-e04e05-native-bridge-r1",
        "sha": CAND_SHA,
        "pins": {"E04T": E04T, "E04U": E04U, "E05R": E05R, "E05S": E05S},
        "bridge_sha256": sha(CAND / 'bridge.py'),
        "frozen_contract_sha256": sha(CAND / '01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json'),
        "frozen_contract_git_object": "14f247b75",
        "author_tests_sha256": sha(CAND / 'tests' / 'test_bridge.py'),
        "source_manifest_len": len(json.loads((CAND / 'source_manifest.json').read_text())),
        "author_claimed_cases": 40,
    },
    "independent_source_derivation": {
        "method": "python import of rawlsing_next.pre553_n9_n10w_progressive_candidate.synthetic_world_rows() (native C11 input) with the exact build_source transforms; independent of bridge.py and of the candidate product JSON",
        "respondents": deriv['base']['respondents'],
        "c11_events": deriv['base']['c11_events'],
        "source_strata": deriv['base']['strata'],
    },
    "numerical_expectations": {
        "forward_Y_given_A_AB_ABC": fwd,
        "minority_cell0": mnt,
        "reverse_A_given_Y16": [deriv['reverse']['yes'], deriv['reverse']['denominator']],        "Y0to1_counterfactual": y01,
        "zero_support_early": zs,
        "zero_support_terminal_denominator": zt['denominator'],
        "zero_support_terminal_state": "ZERO_SUPPORT",
        "gss": {"numerator": 2388192, "denominator": 3288063,
                "electricity_subtypes_sum": 2388192, "publication": "2022-02-24",
                "unit": "RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING", "geography": "GHANA_RURAL"},
        "nca": {"active_subscriptions": 23414527, "publication": "2022-07-08",
                "unit": "ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS", "geography": "GHANA_NATIONAL"},
        "current_struct": {"training_access": False, "exit_cost": 8},
        "historical_struct": {"training_access": True, "exit_cost": 2},
    },
    "positive_path_expectation": {
        "id": "A01/A05",
        "predicted": "NativeBridge(rows,enabled=True).prepare+read returns state SELECTED_WORLD_VALUES_SERVED with exactly 2 consumers (NONPARENT_OPTIONS OPTIONS_AND_SOURCE_SUPPORT_PRODUCED, CONCEPTION_SCENARIO_PROPOSALS FINITE_PROPOSALS_EVALUATED), both over the same snapshot_hash, with the numerical expectations above and two separately native field units",
        "rationale": "commission requires a positive current-grant joined consumer path, not refusal-only green",
    },
    "permission_and_clock_expectations": [
        {"id": "B01", "hypothesis": "warm positive then remove exact query authority from the attached registry; next read on the same prepared request",
         "predicted": "state DEPENDENT_EMPIRICAL_USE_REFUSED, fresh_empirical_use_authorized False, empirical_values None, both warm clients deny with fresh_receipt False, E05R partial has no cells/evidence, structural + native field readset unchanged"},
        {"id": "B02", "hypothesis": "repeat the withdrawn read (cache now cold)",
         "predicted": "no positive empirical cells or evidence on the repeat either; state must not be SELECTED_WORLD_VALUES_SERVED; fresh_empirical_use_authorized must not be True"},
        {"id": "B03", "hypothesis": "brand-new bridge with the query grant never attached",
         "predicted": "no positive empirical cells/evidence"},
        {"id": "B04", "hypothesis": "warm bridge, withdraw grant, then a different empirical condition key (cold cache key)",
         "predicted": "no positive empirical cells/evidence; cache-miss path must not bypass the query grant"},
        {"id": "B05", "hypothesis": "restore only the exact legitimate fixture grants under the same acceptance",
         "predicted": "state SELECTED_WORLD_VALUES_SERVED and selected_world_receipt byte-equal to the original positive receipt"},
        {"id": "B06", "hypothesis": "the refusal path must not auto-issue or renew authority",
         "predicted": "world source authorities, qauth and attached registry contents unchanged across the refusal"},
        {"id": "B07", "hypothesis": "an old receipt is archival, not a grant",
         "predicted": "archive()['archival_only'] True and ['fresh_use_authorized'] False in both states"},
        {"id": "B08", "hypothesis": "same-label successor grant (new version/content hash) substituted for qauth",
         "predicted": "warm: refusal envelope or typed no-values partial; cold: no positive values"},
        {"id": "B09", "hypothesis": "same ref, forged governed_operations/decision_state/issuer",
         "predicted": "warm: refusal; cold: integrity error or no positive values; never positive empirical cells"},
        {"id": "B10", "hypothesis": "a source-release authority snapshot is put in DENY",
         "predicted": "no positive empirical cells/evidence"},
        {"id": "B11", "hypothesis": "one source-release authority snapshot is removed from the registry",
         "predicted": "no positive empirical cells/evidence"},
        {"id": "C01", "hypothesis": "a prior-process public cache projection injected into a fresh bridge before its first prepare",
         "predicted": "ValueError UNATTESTED_NATIVE_CACHE_ENTRY; never accepted as owner evidence"},
        {"id": "C02", "hypothesis": "attacker mutates a warm cache entry and recomputes its content_hash",
         "predicted": "ValueError NATIVE_OWNER_CACHE_PROJECTION_MISMATCH propagates as an integrity error; it is not laundered into the grant-loss envelope"},
        {"id": "C03", "hypothesis": "a projection from a bridge with a different source binding replaces a warm entry",
         "predicted": "ValueError NATIVE_OWNER_CACHE_PROJECTION_MISMATCH"},
        {"id": "C04", "hypothesis": "prepared handoff read by a different bridge instance",
         "predicted": "ValueError E06_FOREIGN_PREPARED_HANDOFF"},
        {"id": "D01", "hypothesis": "release_ref replaced by a foreign ExactRef after a valid acceptance",
         "predicted": "ValueError (binding changed / provider source changed), no positive values"},
        {"id": "D02", "hypothesis": "same release ref, foreign release object in the repository",
         "predicted": "ValueError ACCEPTED_NATIVE_SOURCE_REPLACED"},
        {"id": "D03", "hypothesis": "risk refs or permission root mutated",
         "predicted": "ValueError, no positive values"},
        {"id": "D04", "hypothesis": "supplied consumer material with a tampered native field readset",
         "predicted": "N9SelectedWorldRefusal CONSUMER_MATERIAL_NOT_EXACT_ORIGINAL_OUTPUT"},
        {"id": "D05", "hypothesis": "one native field role revoked in the adapter registry",
         "predicted": "typed partial, exactly one value removed, empirical/structural/consumers unchanged"},
        {"id": "D06", "hypothesis": "explicit adapter.invalidate(role)",
         "predicted": "refusal reason SOURCE_REVOKED, distinct from rekey (UNKNOWN_EXACT_FIELD_REF) and from NOT_PUBLISHED_AT_SELECTED_ASOF"},
        {"id": "E01", "hypothesis": "published_asof precedes the empirical source publication",
         "predicted": "no prewarm: provider cache/accepted/trace empty; empirical_steps empty; empirical_state UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK"},
        {"id": "E02", "hypothesis": "after a clock-denied request, a current request on the same bridge",
         "predicted": "full positive current path (denial does not poison or pre-grant)"},
        {"id": "E03", "hypothesis": "serve a different clock's request against an existing acceptance/snapshot",
         "predicted": "N9SelectedWorldRefusal, no receipt"},
        {"id": "F01", "hypothesis": "after a valid E05 acceptance, downgrade adapter.service to the original GenericSelectedWorldService (E04R factory)",
         "predicted": "ValueError E06_PINNED_E04T_PROVIDER_SUBSTITUTED"},
        {"id": "F02", "hypothesis": "replace service.provider with product.empirical.GenericProgressiveProvider",
         "predicted": "ValueError E06_PINNED_E04T_PROVIDER_SUBSTITUTED"},
        {"id": "F03", "hypothesis": "mutate the live catalog records in place",
         "predicted": "ValueError (CATALOG_CONTENT_CHANGED / FOREIGN_SNAPSHOT_SUBSTITUTION), no positive service"},
        {"id": "F04", "hypothesis": "construct the bridge without literal enabled=True",
         "predicted": "BridgeDisabled before any native source evidence is produced"},
        {"id": "G01", "hypothesis": "the imported producer is the exact E04T owner, not product.empirical",
         "predicted": "e04t_empirical.__file__ == runtime/owners/e04t_empirical.py with git blob from the E04T commit; product.empirical module distinct and separately imported"},
        {"id": "G02", "hypothesis": "no installation/issuance occurs",
         "predicted": "installed_OC05 current_applicability NOT_YET_APPLICABLE and consumer_seam None; issued_N5N6/issued_EE13 False; operative_N9/OC05 False"},
        {"id": "H01", "hypothesis": "two fresh cold OS processes replay a persisted restored current-grant ledger",
         "predicted": "distinct PIDs, bit-identical serialized results, restored result equals the original positive selected-world receipt"},
        {"id": "H02", "hypothesis": "two fresh cold OS processes replay a persisted withdrawn ledger (stale permission)",
         "predicted": "distinct PIDs, bit-identical, no positive empirical cells/evidence, and no foreign public projection accepted as owner evidence"},
    ],
    "excluded_from_independence": {
        "author_40": "executed separately as regression evidence only; not counted as independent acceptance",
        "prior_E04U_E05S": "referenced as component acceptances; neither accepted this composition",
    },
}
(HERE / '01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json').write_text(json.dumps(oracle, indent=1, sort_keys=True) + '\n')
print('wrote', HERE / '01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json')
print('candidate bridge sha', oracle['candidate']['bridge_sha256'][:16],
      'tests sha', oracle['candidate']['author_tests_sha256'][:16])
print('numerical', fwd, mnt, y01, zs, zt['denominator'])
