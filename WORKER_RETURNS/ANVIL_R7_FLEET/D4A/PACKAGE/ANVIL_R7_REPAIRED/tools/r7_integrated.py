#!/usr/bin/env python3
"""Active ANVIL R7 integral investigation and decision gates — D4A guarded copy.

This file is a bounded instrument correction authored in the D4A private package
copy. It adds source-authentication, identity-inventory, T-boundary, release and
actor/world firewall guards. It does NOT authenticate owners, science, H1 or a
real native run. The unpatched original remains at PACKAGE/ANVIL_R7_ORIGINAL.
"""
from __future__ import annotations
import argparse, hashlib, json, pathlib, re, subprocess, sys
from anvil import REQUIRED

SCHEMA = 'ANVIL_R7_INTEGRATED'
HEX40 = re.compile(r'^[a-f0-9]{40}$')
HEX64 = re.compile(r'^[a-f0-9]{64}$')
DOMAINS = ('SOURCE_SEMANTICS', 'C11_PERSISTENCE', 'CURRENT_I03_I05',
           'HISTORICAL_DDM_FUNCTIONS', 'F1_F4_ANALYTICS', 'FIELD_FORGE',
           'SEAM_WORLD_ACTOR', 'AUTHORITY_AND_RECOVERY', 'RESOURCE_ECONOMICS')
BINDS = {'PRESENT_HARD', 'FUTURE_NONPRECLUSION', 'EXTERNAL_OWNER_HELD'}
DISPOS = {'PRESENT_PRESERVED', 'FUTURE_NONPRECLUDED', 'EXACT_OWNER_HOLD', 'BLOCKING_LOSS'}
GRADES = {'CODE_STATIC', 'DOCUMENTARY', 'EXECUTED_SOURCEFREE', 'EXECUTED_NATIVE', 'UNVERIFIED_HELD'}
INVALID = ('todo', 'tbd', 'placeholder', 'to be determined', 'see above', 'n/a', 'not applicable')

FROZEN_CUTS = {
    '31291d08179890852246c8742700e055168e9933': 'LIVE_PROTECTED_31291D',
    '7fc00289dd801d2d0a8ce159986c7595fc27a4d9': 'K3_PROTECTED_7FC',
    '596f1230258ff50f98d8543dec42a80e696720f4': 'SEAM25',
    '796452b8cb788fa5a02f37a7ce86eafce8312dfe': 'SEAM26',
    '3cc09bba3d0e26c226da0ddca4b64c43dd74e493': 'ANVIL15_REVERSE',
    'ca78b6a99a73f4e34790950caeb8d3684c5df94a': 'ANVIL_PR1108',
    'cea2d4d3009e9087d2267e9d1f53bec28b730dc7': 'PRODUCT_BASE',
}
SUPPLIED_ZIP = '526d835d64a98c886a8cbb159fb39f06af7c287ebe1029a93fbbfc9131072332'
IDENTITY_STATES = {'CONSERVED', 'NOT_ADOPTED', 'PROOF_HELD', 'FUTURE_NONPRECLUDED',
                   'OWNER_HELD', 'IDENTITY_ONLY', 'BLOCKING_LOSS'}
IDENTITY_KINDS = {'K3_TSV_ROW', 'DOCUMENTARY_ROW', 'BOUNDARY_CONTRACT', 'TERMINAL_IDENTITY', 'R5_R6_RECORD'}
ANCHOR_CLASSES = {'PROTECTED_K3', 'SEAM_DOCUMENTARY', 'ANVIL_DOCUMENTARY',
                  'SUPPLIED_ZIP', 'R5_R6_ACCEPTED', 'AUTHORED_FIXTURE'}
CONSUMER_RE = re.compile(r'^[A-Za-z0-9_./-]+::[A-Za-z_][A-Za-z0-9_.]*$')


def good(x, n=24):
    return isinstance(x, str) and len(x.strip()) >= n and not any(x.strip().lower() == s for s in INVALID)


def digest(x):
    return hashlib.sha256(json.dumps(x, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False).encode()).hexdigest()


def sha(x):
    return hashlib.sha256(x).hexdigest()


def load(root, ptr, errors, code):
    if not isinstance(ptr, dict):
        errors.append(code + ':NO_POINTER'); return None
    rel = ptr.get('path'); expected = ptr.get('sha256')
    if not isinstance(rel, str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts or not isinstance(expected, str) or not HEX64.fullmatch(expected):
        errors.append(code + ':INVALID_LOCATOR'); return None
    base = pathlib.Path(root).resolve() if root else None
    if base is None:
        errors.append(code + ':NO_ROOT'); return None
    path = (base / rel).resolve()
    if not path.is_relative_to(base) or not path.is_file() or path.is_symlink():
        errors.append(code + ':UNSAFE_OR_ABSENT'); return None
    data = path.read_bytes()
    if sha(data) != expected:
        errors.append(code + ':BYTES_CHANGED'); return None
    try:
        return json.loads(data)
    except (UnicodeDecodeError, ValueError):
        errors.append(code + ':MALFORMED_JSON'); return None


def _git_verify(commit, git_path, blob, wanted, git_root, errors, code, fixture_mode=False):
    if not isinstance(git_path, str) or not git_path or git_path.startswith('/') or '..' in pathlib.PurePosixPath(git_path).parts:
        errors.append(code + ':INVALID_GIT_PATH'); return
    if not HEX40.fullmatch(commit) or not HEX40.fullmatch(blob):
        errors.append(code + ':INVALID_GIT_ANCHOR'); return
    if commit not in FROZEN_CUTS and not fixture_mode:
        errors.append(code + ':COMMIT_NOT_FROZEN'); return
    if git_root is None:
        errors.append(code + ':GIT_ANCHOR_UNVERIFIED'); return
    try:
        actual = subprocess.check_output(['git', '-C', str(git_root), 'rev-parse', commit + ':' + git_path],
                                         stderr=subprocess.DEVNULL, text=True, timeout=8).strip()
        if actual != blob:
            errors.append(code + ':GIT_BLOB_MISMATCH'); return
        body = subprocess.check_output(['git', '-C', str(git_root), 'cat-file', '-p', blob],
                                       stderr=subprocess.DEVNULL, timeout=8)
        if sha(body) != wanted:
            errors.append(code + ':GIT_BYTES_DO_NOT_MATCH_SHA'); return
    except (OSError, subprocess.SubprocessError):
        errors.append(code + ':GIT_ANCHOR_UNREADABLE')


def source_ref(item, root, errors, code, git_root=None, fixture_mode=False):
    """Content pin, exact quote and frozen Git/ZIP anchor. NOT owner authentication."""
    if not isinstance(item, dict):
        errors.append(code + ':NO_SOURCE'); return
    rel = item.get('path'); wanted = item.get('sha256'); quote = item.get('exact_excerpt')
    if (not isinstance(rel, str) or not rel or rel.startswith('/') or '\\' in rel or '..' in pathlib.PurePosixPath(rel).parts
            or not isinstance(wanted, str) or not HEX64.fullmatch(wanted) or not good(quote, 20)):
        errors.append(code + ':INVALID_SOURCE_PIN'); return
    if root is None:
        errors.append(code + ':NO_SOURCE_ROOT'); return
    base = pathlib.Path(root).resolve(); p = (base / rel).resolve()
    if not p.is_relative_to(base) or not p.is_file() or p.is_symlink():
        errors.append(code + ':SOURCE_NOT_FOUND'); return
    body = p.read_bytes()
    if sha(body) != wanted or quote.encode() not in body:
        errors.append(code + ':SOURCE_HASH_OR_QUOTE_DISAGREES'); return
    klass = item.get('source_class')
    if fixture_mode and klass == 'AUTHORED_FIXTURE':
        return
    if klass not in ANCHOR_CLASSES:
        errors.append(code + ':SOURCE_CLASS_MISSING_OR_UNKNOWN'); return
    if item.get('git_commit'):
        _git_verify(str(item.get('git_commit', '')), item.get('git_path'), str(item.get('git_blob', '')), wanted, git_root, errors, code, fixture_mode)
    elif item.get('zip_sha256'):
        if item.get('zip_sha256') != SUPPLIED_ZIP and not fixture_mode:
            errors.append(code + ':ZIP_NOT_SUPPLIED_ORIGINAL'); return
    elif not fixture_mode:
        errors.append(code + ':SOURCE_ANCHOR_MISSING')


def _check_record(rid, entry, group, errors, source_root, git_root=None, fixture_mode=False):
    for key in ('source_semantics', 'consumer_or_hold', 'negative_meaning', 'architecture_effect', 'why'):
        if not good(entry.get(key), 12):
            errors.append('HISTORY:SEMANTIC_OR_CONSUMER_LOSS:' + rid + ':' + key)
    if not isinstance(entry.get('evidence_ids'), list) or not entry['evidence_ids']:
        errors.append('HISTORY:NO_EVIDENCE:' + rid)
    if entry.get('source_kind') not in IDENTITY_KINDS:
        errors.append('HISTORY:UNKNOWN_SOURCE_KIND:' + rid)
    source_ref(entry.get('source_anchor'), source_root, errors, 'HISTORY:ANCHOR:' + rid, git_root, fixture_mode)
    if group == 'PYAT_PC':
        if entry.get('adopted') is not False or entry.get('necessity') != 'HISTORICAL_NOT_ADOPTED':
            errors.append('HISTORY:FALSE_PROSPECTIVE_ADOPTION:' + rid)
        sem = (entry.get('source_semantics', '') + ' ' + entry.get('architecture_effect', '')).upper()
        if re.search(r'(?<!NOT_)ADOPT', sem):
            errors.append('HISTORY:NOT_ADOPTED_ROW_REWRITTEN_AS_ADOPTED:' + rid)
    if group == 'P4R':
        if entry.get('closed') is not False or entry.get('necessity') != 'HISTORICAL_PROOF_HELD':
            errors.append('HISTORY:FALSE_PROOF_CLOSURE:' + rid)
        sem = (entry.get('source_semantics', '') + ' ' + entry.get('architecture_effect', '')).upper()
        if re.search(r'(?<!NOT_)CLOSED', sem):
            errors.append('HISTORY:HELD_ROW_REWRITTEN_AS_CLOSED:' + rid)
    if group in ('K1_CAP', 'PYAT_PC', 'P4R'):
        want = entry.get('source_anchor')
        if not isinstance(want, dict):
            want = {}
        if want.get('source_class') != 'PROTECTED_K3':
            errors.append('HISTORY:K3_ANCHOR_NOT_PROTECTED:' + rid)
        # exact raw row byte check against the pinned TSV snapshot
        p = pathlib.Path(source_root).resolve() / str(want.get('path', ''))
        if not p.is_file():
            errors.append('HISTORY:K3_SNAPSHOT_ABSENT:' + rid)
        else:
            rows = p.read_bytes().splitlines()
            h = entry.get('row_sha256')
            if not isinstance(h, str) or not any(sha(r) == h for r in rows):
                errors.append('HISTORY:K3_ROW_BYTES_ALTERED_OR_UNANCHORED:' + rid)
            else:
                raw = next(r for r in rows if sha(r) == h).decode()
                neg = entry.get('negative_meaning')
                if isinstance(neg, str) and neg not in raw:
                    errors.append('HISTORY:K3_NEGATIVE_NOT_FROM_SOURCE_ROW:' + rid)
                sem = entry.get('source_semantics', '')
                if not isinstance(sem, str):
                    sem = ''
                if group == 'PYAT_PC' and ' :: ' in sem:
                    if not all(part in raw for part in sem.split(' :: ')):
                        errors.append('HISTORY:K3_SEMANTICS_NOT_FROM_SOURCE_ROW:' + rid)
                elif sem not in raw:
                    errors.append('HISTORY:K3_SEMANTICS_NOT_FROM_SOURCE_ROW:' + rid)
                cons = [x for x in entry.get('consumer_or_hold', '').split(' :: ') if x]
                if cons and not any(x in raw for x in cons):
                    errors.append('HISTORY:K3_CONSUMER_NOT_FROM_SOURCE_ROW:' + rid)


def check_history(obj, errors, source_root=None, git_root=None, fixture_mode=False):
    if not isinstance(obj, dict) or obj.get('schema') not in ('ANVIL_R7_INHERITED_CONSERVATION', 'ANVIL_R7_SOURCE_AUTHENTICATED_IDENTITY_INVENTORY'):
        errors.append('HISTORY:WRONG_SCHEMA'); return
    origin = obj.get('source_authentication_origin')
    if origin == 'ACCEPTED_R5_R6_ARTIFACT':
        anchor = obj.get('accepted_spine_anchor')
        source_ref(anchor, source_root, errors, 'HISTORY:ACCEPTED_SPINE_ANCHOR', git_root, fixture_mode)
    elif origin == 'AUTHORED_SYNTHETIC_FIXTURE':
        if not fixture_mode:
            errors.append('HISTORY:SYNTHETIC_FIXTURE_CANNOT_SUPPORT_ACCEPTANCE')
    elif origin is None and obj.get('schema') == 'ANVIL_R7_INHERITED_CONSERVATION':
        errors.append('HISTORY:NO_SOURCE_AUTHENTICATION_ORIGIN')
    coverage = obj.get('coverage', obj.get('groups', {}))
    if not isinstance(coverage, dict) or set(coverage) != set(REQUIRED):
        errors.append('HISTORY:GROUPS_NOT_INHERITED'); return
    count = 0
    for group, ids in REQUIRED.items():
        rows = coverage.get(group, {})
        if not isinstance(rows, dict) or set(rows) != set(ids):
            errors.append('HISTORY:ID_SET_DRIFT:' + group); continue
        for rid, entry in rows.items():
            count += 1
            if not isinstance(entry, dict):
                errors.append('HISTORY:NO_RECORD:' + rid); continue
            _check_record(rid, entry, group, errors, source_root, git_root, fixture_mode)
    if count != sum(map(len, REQUIRED.values())):
        errors.append('HISTORY:COUNT_DRIFT')
    if obj.get('source_authentication') not in ('NOT_AUTHENTICATED_BY_LOCAL_CHECK', 'EXACT_GIT_ZIP_BYTES_CHECKED_LOCALLY_NOT_OWNER_SCIENCE'):
        errors.append('HISTORY:FALSE_SOURCE_AUTHENTICATION')


def check_frame(frame, evidence_root, source_root, git_root=None, fixture_mode=False):
    e = []
    if not isinstance(frame, dict) or frame.get('schema') != SCHEMA or frame.get('stage') != 'COMMON_FRAME':
        return {'status': 'RED', 'errors': ['FRAME:BAD_SCHEMA']}
    if frame.get('workflow') != 'ONE_INTEGRATED_INVESTIGATION_OPTIONAL_TARGETED_DUELS':
        e.append('FRAME:DIVIDED_ARCHITECT_WORKFLOW_FORBIDDEN')
    if frame.get('phase') != 'BEFORE_ARCHITECTURE_SELECTION':
        e.append('FRAME:WRONG_CHRONOLOGY')
    if frame.get('architecture_selected') is not False:
        e.append('FRAME:ARCHITECTURE_PRESELECTED')
    if frame.get('mandatory_rival_architecture') is not False:
        e.append('FRAME:RIVAL_NOT_OPTIONAL')
    if frame.get('A_B_method') != 'OPTIONAL_SAME_QUESTION_SAME_EVIDENCE':
        e.append('FRAME:DUEL_METHOD_DISTORTED')
    if frame.get('scope') not in ('C11_QUERY_DESIGN', 'F1_F4_CONSUMER_DESIGN', 'FF_FIRST_EFFECT_DESIGN'):
        e.append('FRAME:INVALID_SCOPE')
    for name in ('source_cut', 'protected_head'):
        if not isinstance(frame.get(name), str) or not HEX40.fullmatch(frame[name]):
            e.append('FRAME:UNPINNED_' + name)
    for name in ('user_priority_source', 'first_real_consumer', 'currentness_gap_or_exact_verified_state',
                 'science_authority_boundary', 'whole_program_mission', 'source_currentness'):
        if not good(frame.get(name), 35):
            e.append('FRAME:UNDERDEFINED_' + name)
    if frame.get('source_grades_authentic_by_local_test') is not False:
        e.append('FRAME:FALSE_SOURCE_AUTHORITY')
    # Source release register and revocation denial
    rel = load(evidence_root, frame.get('release_register'), e, 'FRAME:RELEASE')
    if rel is not None:
        if rel.get('schema') not in ('ANVIL_R7_SOURCE_RELEASE_REGISTER',):
            e.append('FRAME:RELEASE_BAD_SCHEMA')
        current = rel.get('current')
        revoked = rel.get('revoked')
        if not isinstance(current, list) or not current:
            e.append('FRAME:RELEASE_NO_CURRENT_PIN')
        if not isinstance(revoked, list):
            e.append('FRAME:RELEASE_REVOKED_NOT_LIST')
        revoked_shas = {x.get('sha256') for x in revoked if isinstance(x, dict)} if isinstance(revoked, list) else set()
    else:
        revoked_shas = set()
    rows = frame.get('requirements')
    if not isinstance(rows, list):
        rows = []; e.append('FRAME:REQUIREMENTS_NOT_LIST')
    seen = set(); have = set()
    for row in rows:
        if not isinstance(row, dict):
            e.append('FRAME:BAD_REQUIREMENT'); continue
        key = row.get('id'); domain = row.get('domain'); have.add(domain)
        if not isinstance(key, str) or not key or key in seen:
            e.append('FRAME:DUPLICATE_OR_MISSING_ID')
        seen.add(key)
        if domain not in DOMAINS:
            e.append('FRAME:UNRECOGNIZED_DOMAIN:' + str(domain))
        if row.get('binding') not in BINDS:
            e.append('FRAME:BAD_BINDING:' + str(key))
        for k in ('substantive_requirement', 'why_needed', 'loss_if_missing', 'first_consumer',
                  'architectural_consequence', 'proof_or_owner_hold'):
            if not good(row.get(k), 28):
                e.append('FRAME:VACUOUS_' + str(key) + ':' + k)
        source_ref(row.get('evidence'), source_root, e, 'FRAME:EVIDENCE:' + str(key), git_root, fixture_mode)
        ev = row.get('evidence') or {}
        if ev.get('sha256') in revoked_shas or ev.get('zip_sha256') in revoked_shas:
            e.append('FRAME:REVOKED_EVIDENCE_USED:' + str(key))
        if row.get('binding') == 'EXTERNAL_OWNER_HELD' and not good(row.get('authority_owner'), 10):
            e.append('FRAME:OWNER_NOT_NAMED:' + str(key))
    for domain in DOMAINS:
        if domain not in have:
            e.append('FRAME:WHOLE_MISSION_DOMAIN_MISSING:' + domain)
    # Historical identity conservation: accepted SPINE OR source-authenticated inventory
    history = None
    if frame.get('historical_inventory') is not None:
        history = load(evidence_root, frame.get('historical_inventory'), e, 'FRAME:INVENTORY')
        if history is not None:
            if history.get('schema') != 'ANVIL_R7_SOURCE_AUTHENTICATED_IDENTITY_INVENTORY':
                e.append('FRAME:INVENTORY_BAD_SCHEMA')
            if history.get('total') != 118:
                e.append('FRAME:INVENTORY_TOTAL_NOT_118')
            if history.get('source_authentication') != 'EXACT_GIT_ZIP_BYTES_CHECKED_LOCALLY_NOT_OWNER_SCIENCE':
                e.append('FRAME:INVENTORY_FALSE_SOURCE_AUTHORITY')
            check_history(history, e, source_root, git_root, fixture_mode)
    elif frame.get('historical_conservation') is not None:
        history = load(evidence_root, frame.get('historical_conservation'), e, 'FRAME:HISTORY')
        if history is not None:
            check_history(history, e, source_root, git_root, fixture_mode)
            original = load(evidence_root, frame.get('historical_source_spine'), e, 'FRAME:SOURCE_SPINE')
            if original is not None:
                if original.get('schema') not in ('ANVIL_SPINE_R5', 'ANVIL_SPINE_R6'):
                    e.append('FRAME:SOURCE_SPINE_NOT_EXISTING_R5_R6')
                if original.get('coverage') != history.get('coverage'):
                    e.append('FRAME:HISTORICAL_TRANSFER_NOT_BYTE_EQUIVALENT_TO_SOURCE_COVERAGE')
                if history.get('source_spine_sha256') != frame['historical_source_spine'].get('sha256'):
                    e.append('FRAME:HISTORICAL_TRANSFER_NOT_PINNED_TO_ORIGINAL_SPINE')
    else:
        e.append('FRAME:HISTORY:NO_POINTER')
    # T1-T7 exact boundary contracts from the supplied ZIP
    bc = load(evidence_root, frame.get('boundary_contract'), e, 'FRAME:BOUNDARY')
    if bc is not None:
        if bc.get('schema') != 'ANVIL_BOUNDARIES_R3' or len(bc.get('boundaries', [])) != 7:
            e.append('FRAME:BOUNDARY_SET_NOT_EXACT')
        supplied = {b.get('id'): b for b in bc.get('boundaries', []) if isinstance(b, dict)}
        claimed = frame.get('boundary_contracts')
        if not isinstance(claimed, list) or {b.get('id') for b in claimed if isinstance(b, dict)} != set(supplied):
            e.append('FRAME:T_BOUNDARIES_MISSING_OR_EXTRA')
        else:
            for b in claimed:
                src = supplied.get(b.get('id'), {})
                pairs = (('producer', 'producers'), ('receiver', 'receivers'), ('must_preserve', 'must_preserve'),
                         ('expected_first_effect', 'first_effect'), ('veto', 'veto'), ('time_class', 'time_class'),
                         ('owner', 'owners'))
                for k, sk in pairs:
                    if b.get(k) != src.get(sk):
                        e.append('FRAME:T_BOUNDARY_REWRITTEN:' + str(b.get('id')) + ':' + k)
    if frame.get('duel_required') is not False:
        e.append('FRAME:UNNECESSARY_DUEL_REQUIRED')
    status = 'RED' if e else ('PASS_LOCAL_AUTHORED_FIXTURE_NOT_ACCEPTANCE' if fixture_mode else 'PASS_LOCAL_SOURCE_AUTHENTICATED_PENDING_C')
    return {'status': status, 'errors': sorted(set(e)), 'requirements': len(rows), 'domains': len(have & set(DOMAINS))}


def check_duel(duel, frame_sha, errors):
    if not isinstance(duel, dict) or duel.get('schema') != 'ANVIL_R7_TARGETED_DUEL':
        errors.append('DECISION:DUEL_BAD_SCHEMA'); return
    if duel.get('shared_frame_sha256') != frame_sha:
        errors.append('DECISION:DUEL_DIFFERENT_PREMISES')
    if not good(duel.get('single_decision_question'), 40):
        errors.append('DECISION:DUEL_NOT_SINGLE_QUESTION')
    if not good(duel.get('why_independence_is_needed'), 40):
        errors.append('DECISION:DUEL_NO_JUSTIFICATION')
    if not good(duel.get('shared_evidence_description'), 40):
        errors.append('DECISION:DUEL_MISSING_SHARED_EVIDENCE')
    investigators = duel.get('investigators')
    if not isinstance(investigators, list) or len(investigators) != 2 or len({i.get('id') for i in investigators if isinstance(i, dict)}) != 2:
        errors.append('DECISION:DUEL_NOT_TWO_DISTINCT_PEERS'); return
    if any(i.get('shared_frame_sha256') != frame_sha or i.get('evidence_access') != 'SAME_FULL_EVIDENCE' or not good(i.get('analysis'), 40) for i in investigators):
        errors.append('DECISION:DUEL_DIVIDED_EVIDENCE_OR_NO_ANALYSIS')
    if any(i.get('assignment') not in ('SAME_EXACT_QUESTION_INDEPENDENT_ANALYSIS',) for i in investigators):
        errors.append('DECISION:DUEL_SPLIT_ASSIGNMENTS_FORBIDDEN')
    if not good(duel.get('integrated_adjudication'), 50):
        errors.append('DECISION:DUEL_NOT_INTEGRATED')
    if duel.get('independence_proven_by_local_check') is not False:
        errors.append('DECISION:DUEL_SELF_CERTIFIES_INDEPENDENCE')


def check_decision(decision, evidence_root, source_root, git_root=None, fixture_mode=False):
    e = []
    if not isinstance(decision, dict) or decision.get('schema') != SCHEMA or decision.get('stage') != 'INTEGRATED_DECISION':
        return {'status': 'RED', 'errors': ['DECISION:BAD_SCHEMA']}
    frame = load(evidence_root, decision.get('common_frame'), e, 'DECISION:FRAME')
    if frame is None:
        return {'status': 'RED', 'errors': sorted(set(e))}
    fr = check_frame(frame, evidence_root, source_root, git_root, fixture_mode)
    if fr['status'] == 'RED':
        e.extend('DECISION:INVALID_FRAME:' + v for v in fr['errors'])
    frozen_sha = digest(frame)
    if decision.get('frame_sha256') != frozen_sha:
        e.append('DECISION:FRAME_NOT_FROZEN')
    if decision.get('first_real_consumer') != frame.get('first_real_consumer'):
        e.append('DECISION:FIRST_CONSUMER_DRIFT')
    if decision.get('decision_process') != 'ONE_SYNTHESIS_NO_MANDATORY_RIVAL':
        e.append('DECISION:WRONG_PROCESS')
    if decision.get('basis') not in ('ANALYTICAL_SOURCE_GROUNDED', 'EXECUTED_EXISTING_CODE', 'BOUNDED_DISCRIMINATOR', 'TARGETED_DUEL'):
        e.append('DECISION:UNKNOWN_BASIS')
    if decision.get('grade') not in ('AUTHOR_PROPOSED_PENDING_C', 'CONDITIONAL_DIRECTION', 'EXACT_HOLD'):
        e.append('DECISION:FALSE_AUTHORITY_GRADE')
    for k in ('architecture_description', 'entire_source_to_actor_dataflow', 'algorithm_and_data_structures', 'resource_cost_reasoning',
              'historical_function_conservation', 'scientific_boundary_and_nonpreclusion', 'strongest_surviving_objection',
              'why_selected_over_feasible_alternatives', 'next_actual_engineering_operation'):
        if not good(decision.get(k), 55):
            e.append('DECISION:UNDERARGUED_' + k)
    if not good(decision.get('single_selected_strategy'), 10) and decision.get('grade') != 'EXACT_HOLD':
        e.append('DECISION:NO_PROPOSED_STRATEGY')
    alternatives = decision.get('alternatives_considered')
    if not isinstance(alternatives, list) or not alternatives:
        e.append('DECISION:ALTERNATIVES_NOT_ANALYTICALLY_CONSIDERED')
    else:
        for j, a in enumerate(alternatives):
            if not isinstance(a, dict) or not good(a.get('technical_approach'), 20) or not good(a.get('why_not_selected_or_held'), 45) or a.get('state') not in ('RULED_OUT_BY_REASON', 'VIABLE_NOT_SELECTED', 'UNRESOLVED_HOLD'):
                e.append('DECISION:ALTERNATIVE_UNREASONED:' + str(j))
    reversers = decision.get('choice_reversers')
    if not isinstance(reversers, list):
        e.append('DECISION:NO_REVERSER_ACCOUNTING')
    elif decision.get('grade') == 'AUTHOR_PROPOSED_PENDING_C' and any(isinstance(r, dict) and r.get('status') == 'UNRESOLVED_CHOICE_CHANGING' for r in reversers):
        e.append('DECISION:CHOICE_CHANGING_UNCERTAINTY_HIDDEN')
    if decision.get('requires_full_A_B_comparison') is not False:
        e.append('DECISION:COMPETITION_REQUIRED')
    if decision.get('architecture_claims_independent_acceptance') is not False:
        e.append('DECISION:UNAUTHORIZED_ACCEPTANCE')
    # Historical 118 semantic dispositions (not merely requirement rows)
    inventory = None
    if frame.get('historical_inventory') is not None:
        inventory = load(evidence_root, frame.get('historical_inventory'), e, 'DECISION:INVENTORY')
    expected_ids = set()
    if inventory:
        for group, recs in inventory.get('groups', {}).items():
            expected_ids |= set(recs)
    hd = decision.get('historical_identity_dispositions')
    if not isinstance(hd, list):
        e.append('DECISION:NO_HISTORICAL_IDENTITY_DISPOSITIONS')
    else:
        dmap = {x.get('id'): x for x in hd if isinstance(x, dict)}
        if set(dmap) != expected_ids or len(hd) != len(expected_ids):
            e.append('DECISION:HISTORICAL_118_DISPOSITION_INCOMPLETE')
        for rid, x in dmap.items():
            st = x.get('disposition')
            if st not in IDENTITY_STATES:
                e.append('DECISION:BAD_IDENTITY_DISPOSITION:' + str(rid)); continue
            if x.get('negative_preserved') is not True:
                e.append('DECISION:NEGATIVE_NOT_PRESERVED:' + str(rid))
            if not good(x.get('consumer'), 12):
                e.append('DECISION:IDENTITY_CONSUMER_MISSING:' + str(rid))
            source_ref(x.get('evidence'), source_root, e, 'DECISION:IDENTITY_EVIDENCE:' + str(rid), git_root, fixture_mode)
            if inventory:
                for group, recs in inventory.get('groups', {}).items():
                    if rid in recs:
                        if group == 'PYAT_PC' and st != 'NOT_ADOPTED':
                            e.append('DECISION:PROSPECTIVE_PROPOSAL_PROMOTED:' + rid)
                        if group == 'P4R' and st != 'PROOF_HELD':
                            e.append('DECISION:HELD_PROOF_DECLARED_CLOSED:' + rid)
                        if group == 'K1_CAP' and st not in ('CONSERVED', 'OWNER_HELD', 'BLOCKING_LOSS'):
                            e.append('DECISION:K1_CAPABILITY_NOT_CONSERVED:' + rid)
                        break
    # Source/actor/world firewall
    aw = decision.get('actor_world_boundary')
    if not isinstance(aw, dict):
        e.append('DECISION:NO_ACTOR_WORLD_BOUNDARY')
    else:
        for flag in ('survey_implies_actor_knowledge', 'fictional_mutates_source', 'source_implies_material_power'):
            if aw.get(flag) is not False:
                e.append('DECISION:ACTOR_WORLD_FIREWALL_BREACH:' + flag)
        if not good(aw.get('owner_held_instead'), 20):
            e.append('DECISION:ACTOR_WORLD_HOLD_NOT_NAMED')
    if decision.get('protected_h1_claimed') is not False:
        e.append('DECISION:FABRICATED_PROTECTED_H1')
    if decision.get('source_authentication_claimed') is not False:
        e.append('DECISION:FALSE_SOURCE_AUTHENTICATION')
    # requirement crosswalk
    reqs = frame.get('requirements', [])
    covers = decision.get('requirement_dispositions', [])
    if not isinstance(covers, list):
        covers = []; e.append('DECISION:NO_REQUIREMENT_DISPOSITIONS')
    rids = {r['id'] for r in reqs if isinstance(r, dict) and isinstance(r.get('id'), str)}
    dmap = {x.get('requirement_id'): x for x in covers if isinstance(x, dict)}
    if set(dmap) != rids or len(covers) != len(rids):
        e.append('DECISION:INCOMPLETE_REQUIREMENT_RECONCILIATION')
    for row in reqs:
        if not isinstance(row, dict):
            continue
        rid = row.get('id'); x = dmap.get(rid, {})
        state = x.get('disposition')
        if state not in DISPOS:
            e.append('DECISION:BAD_DISPOSITION:' + str(rid))
        if row.get('binding') == 'PRESENT_HARD' and state not in ('PRESENT_PRESERVED', 'BLOCKING_LOSS'):
            e.append('DECISION:HARD_PRESENT_RELABELED_FUTURE:' + str(rid))
        if row.get('binding') == 'EXTERNAL_OWNER_HELD' and state == 'PRESENT_PRESERVED' and x.get('evidence_grade') not in ('EXECUTED_SOURCEFREE', 'EXECUTED_NATIVE'):
            e.append('DECISION:HELD_SCIENCE_PROMOTED:' + str(rid))
        for k in ('actual_design_effect', 'specific_first_consumer_path', 'conservation_or_refusal_witness'):
            if not good(x.get(k), 38):
                e.append('DECISION:VACUOUS_DISPOSITION:' + str(rid) + ':' + k)
        if x.get('evidence_grade') not in GRADES:
            e.append('DECISION:BAD_EVIDENCE_GRADE:' + str(rid))
        if state in ('PRESENT_PRESERVED', 'FUTURE_NONPRECLUDED'):
            source_ref(x.get('evidence'), source_root, e, 'DECISION:UNPROVED_PRESERVATION:' + str(rid), git_root, fixture_mode)
    if decision.get('grade') == 'AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition') == 'BLOCKING_LOSS' for x in covers if isinstance(x, dict)):
        e.append('DECISION:READY_WHILE_LOSING_REQUIRED_FUNCTION')
    if decision.get('grade') == 'AUTHOR_PROPOSED_PENDING_C' and any(x.get('disposition') == 'EXACT_OWNER_HOLD' for x in covers if isinstance(x, dict)
              and any(r.get('id') == x.get('requirement_id') and r.get('binding') == 'PRESENT_HARD' for r in reqs)):
        e.append('DECISION:READY_WITH_PRESENT_HARD_HOLD')
    if decision.get('basis') == 'TARGETED_DUEL':
        duel = load(evidence_root, decision.get('targeted_duel'), e, 'DECISION:OPTIONAL_DUEL')
        if duel is not None:
            check_duel(duel, frozen_sha, e)
    elif decision.get('targeted_duel') is not None:
        e.append('DECISION:DUEL_PRESENT_WITHOUT_GROUNDED_NEED')
    if decision.get('competing_implementations_mandatory') is not False:
        e.append('DECISION:MANDATORY_BACKEND_BAKEOFF')
    status = 'RED' if e else ('PASS_LOCAL_AUTHORED_FIXTURE_NOT_ACCEPTANCE' if fixture_mode else 'PASS_LOCAL_INTEGRATED_DECISION_PENDING_C')
    return {'status': status, 'errors': sorted(set(e)), 'covered': len(covers), 'requirement_total': len(rids)}


def _check_builder_receipt(card, receipt_root, errors):
    if card.get('grade') != 'EXECUTED_FIRST_READER_PROOF':
        return
    proof = load(receipt_root, card.get('executed_test_receipt'), errors, 'C:BUILDER_RECEIPT')
    if proof is None:
        return
    if proof.get('schema') != 'ANVIL_R7_EXECUTION_TEST_RECEIPT':
        errors.append('C:BUILDER_RECEIPT_BAD_SCHEMA')
    if proof.get('command') != card.get('test_command'):
        errors.append('C:BUILDER_RECEIPT_COMMAND_MISMATCH')
    if proof.get('exit_code') != 0:
        errors.append('C:BUILDER_RECEIPT_NONZERO')
    if proof.get('execution_kind') == 'SYNTHETIC_TEST':
        errors.append('C:BUILDER_SYNTHETIC_TEST_NOT_FIRST_READER')
    for field in ('stdout_sha256', 'log_sha256', 'command_argv', 'started_utc', 'host', 'runner_code_head'):
        if not proof.get(field):
            errors.append('C:BUILDER_RECEIPT_MISSING_' + field)
    if not isinstance(proof.get('command_argv'), list) or not proof['command_argv']:
        errors.append('C:BUILDER_RECEIPT_ARGV_NOT_EXECUTABLE')
    if isinstance(proof.get('log_path'), str) and isinstance(proof.get('log_sha256'), str):
        lp = pathlib.Path(receipt_root).resolve() / proof['log_path']
        if not lp.is_file() or sha(lp.read_bytes()) != proof['log_sha256']:
            errors.append('C:BUILDER_RECEIPT_RAW_LOG_UNPINNED')
    else:
        errors.append('C:BUILDER_RECEIPT_RAW_LOG_MISSING')
    if isinstance(proof.get('stdout'), str) and isinstance(proof.get('stdout_sha256'), str):
        if sha(proof['stdout'].encode()) != proof['stdout_sha256']:
            errors.append('C:BUILDER_RECEIPT_STDOUT_HASH_MISMATCH')
    if not HEX40.fullmatch(str(proof.get('runner_code_head', ''))):
        errors.append('C:BUILDER_RECEIPT_UNPINNED_RUNNER_HEAD')


def check_C(packet, evidence_root, source_root, git_root=None, fixture_mode=False):
    e = []
    if not isinstance(packet, dict) or packet.get('schema') != SCHEMA or packet.get('stage') != 'INDEPENDENT_C':
        return {'status': 'RED', 'errors': ['C:BAD_SCHEMA']}
    decision = load(evidence_root, packet.get('integrated_decision'), e, 'C:DECISION')
    if decision is not None:
        verdict = check_decision(decision, evidence_root, source_root, git_root, fixture_mode)
        if verdict['status'] == 'RED':
            e.extend('C:DEFECTIVE_DECISION:' + x for x in verdict['errors'])
        if packet.get('integrated_decision_sha256') != digest(decision):
            e.append('C:DECISION_NOT_PINNED')
        if packet.get('first_consumer') != decision.get('first_real_consumer'):
            e.append('C:CONSUMER_CHANGED')
    for k in ('independent_reverse_walk_of_whole_frame', 'strongest_choice_reversing_objection',
              'scientific_and_owner_boundary', 'actual_first_consumer_assessment', 'historical_no_loss_assessment'):
        if not good(packet.get(k), 60):
            e.append('C:INSUFFICIENT_' + k)
    cards = packet.get('builder_cards')
    if not isinstance(cards, list) or len(cards) != 2 or {c.get('domain') for c in cards if isinstance(c, dict)} != {'CURRENT_FIRST_CONSUMER', 'FUTURE_NONPRECLUSION'}:
        e.append('C:REQUIRES_PRESENT_AND_FUTURE_BUILDER_CARDS')
    else:
        from r7_stage import check_builder
        for card in cards:
            e.extend('C:BUILDER:' + v for v in check_builder(card, source_root, evidence_root))
            fc = card.get('first_consumer')
            if not isinstance(fc, str) or not CONSUMER_RE.fullmatch(fc):
                e.append('C:BUILDER_FIRST_CONSUMER_NOT_EXECUTABLE_SYMBOL')
            _check_builder_receipt(card, evidence_root, e)
        present = next(c for c in cards if c['domain'] == 'CURRENT_FIRST_CONSUMER')
        if packet.get('verdict') == 'C_CONDITIONALLY_ADMIT_DESIGN' and present.get('grade') == 'EXACT_BUILDER_HOLD':
            e.append('C:ADMIT_WITHOUT_CURRENT_BUILDER')
    if packet.get('reviewer_relationship') != 'DISTINCT_NONAUTHOR_ASSERTION_PENDING_EXTERNAL_VERIFICATION':
        e.append('C:SELF_CERTIFIED_INDEPENDENCE')
    if packet.get('choice_reversing_objection_survives') is not False and packet.get('verdict') == 'C_CONDITIONALLY_ADMIT_DESIGN':
        e.append('C:ACCEPTS_SURVIVING_REVERSER')
    if packet.get('verdict') not in ('C_CONDITIONALLY_ADMIT_DESIGN', 'C_HOLD_EXACT'):
        e.append('C:FALSE_C_GRADE')
    if packet.get('original_source_granted_by_local_check') is not False or packet.get('owner_granted_by_local_check') is not False:
        e.append('C:FALSE_AUTHORITY')
    if packet.get('protected_h1_claimed') is not False:
        e.append('C:FABRICATED_PROTECTED_H1')
    status = 'RED' if e else ('PASS_LOCAL_AUTHORED_FIXTURE_NOT_ACCEPTANCE' if fixture_mode else 'PASS_LOCAL_C_PACKET_ONLY_INDEPENDENCE_UNVERIFIED')
    return {'status': status, 'errors': sorted(set(e))}


def check(stage, packet, evidence_root, source_root=None, git_root=None, fixture_mode=False):
    if stage == 'FRAME':
        return check_frame(packet, evidence_root, source_root, git_root, fixture_mode)
    if stage == 'DECISION':
        return check_decision(packet, evidence_root, source_root, git_root, fixture_mode)
    if stage == 'C_INTEGRATED':
        return check_C(packet, evidence_root, source_root, git_root, fixture_mode)
    return {'status': 'RED', 'errors': ['ACTIVE_STAGE_UNKNOWN']}


def main():
    ap = argparse.ArgumentParser(description='Active ANVIL integral workflow, NOT autonomous accreditation')
    ap.add_argument('stage', choices=['FRAME', 'DECISION', 'C_INTEGRATED'])
    ap.add_argument('packet')
    ap.add_argument('--evidence-root', required=True)
    ap.add_argument('--source-root', required=True)
    ap.add_argument('--git-root', default=None)
    ap.add_argument('--fixture-mode', action='store_true')
    arg = ap.parse_args()
    try:
        out = check(arg.stage, json.loads(pathlib.Path(arg.packet).read_text()), arg.evidence_root, arg.source_root, arg.git_root, arg.fixture_mode)
    except Exception as exc:
        out = {'status': 'RED', 'errors': ['UNHANDLED_MALFORMED_PACKET:' + repr(exc)]}
    print(json.dumps(out, indent=2))
    return 2 if out['status'] == 'RED' else 0


if __name__ == '__main__':
    sys.exit(main())
