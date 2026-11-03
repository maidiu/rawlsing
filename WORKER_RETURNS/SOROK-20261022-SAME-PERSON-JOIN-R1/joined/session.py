"""Sourcefree J product connected to E admission without a second product root."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from .imports import install
install()
from r31j.build import c9_only, product as build_product
from r31e.session import R31ESession
from r30a.first_session import SessionRefusal
from .b_event import (BINDING_KIND, B_EVENT_CONTRACT, BSourceUnavailable,
                      PERFORMED, binding_from_receipt, performed_scenario,
                      persisted_binding, refused_scenario, validate_binding,
                      validate_receipt)
from .closure import audit_loaded, source_manifest_sha256
from .lineage import ROOT_BRANCH, create_fork, validate as validate_lineage
from .provenance import validate_join
from .readonly import ReadOnlyR31JProduct



def _load_meta(state_root: Path) -> dict:
    if not state_root.exists() or not state_root.is_dir():
        raise SessionRefusal('SESSION_NOT_FOUND', str(state_root))
    path = state_root / 'session.json'
    if not path.is_file():
        raise SessionRefusal('SESSION_NOT_FOUND', str(path))
    return json.loads(path.read_text(encoding='utf8'))


def _canonical_product_root(state_root: Path, meta: dict) -> Path:
    recorded_state = meta.get('state_root')
    if recorded_state and Path(recorded_state).resolve() != state_root:
        raise SessionRefusal('SESSION_ROOT_MOVED',
                             f'{recorded_state} != {state_root}')
    product_root = Path(meta.get('product_root', '')).resolve()
    expected = (state_root / 'product').resolve()
    if product_root != expected:
        raise SessionRefusal('FOREIGN_PRODUCT_ROOT',
                             f'{product_root} != {expected}')
    return product_root


def _guard_binding(product_root: Path) -> dict:
    path = product_root / 'bp2_join.json'
    if not path.is_file():
        raise SessionRefusal('J_BINDING_MISSING', str(path))
    document = json.loads(path.read_text(encoding='utf8'))
    if not document.get('r31j_source') or not document.get('r31j_actor_snapshot'):
        raise SessionRefusal('J_BINDING_MISSING', 'r31j source/actor snapshot absent')
    return document


class JoinedSession(R31ESession):
    """One persistent same-person session over the J product and E admission."""

    @classmethod
    def start(cls, state_root, *, perform='e2', attention='focused',
              variant='A_REPAIR_LONG', b_disposition=PERFORMED):
        state_root = Path(state_root).resolve()
        state_root.mkdir(parents=True, exist_ok=True)
        if (state_root/'session.json').exists():
            raise SessionRefusal('SESSION_EXISTS__NO_AUTOMATIC_REROLL')
        if (state_root/'product').exists() or (state_root/'bp2').exists():
            raise SessionRefusal('ORPHAN_PRODUCT_ROOT')
        if perform not in ('e2', 'omit'):
            raise SessionRefusal('UNKNOWN_PERFORMANCE')
        if b_disposition != PERFORMED:
            raise SessionRefusal(
                'TARGETLESS_B_EVENT_REQUIRES_REFUSAL_SESSION', str(b_disposition))
        scenario = performed_scenario(e2=perform == 'e2')
        receipt = scenario['b_performer_receipt']
        product, built, producer = build_product(
            state_root, gm01=scenario['gm01'], case=scenario['case'],
            variant=variant)
        producer.close()
        try:
            if perform == 'e2':
                product.material_inspect()
            else:
                product.record_omission()
            root_verify = product.c12_verify('root')
            if not root_verify.get('ok'):
                raise SessionRefusal('ROOT_C12_VERIFY_FAILED',
                                     json.dumps(root_verify.get('errors', [])))
            source = dict(product.source)
            if source.get('b_operation') != 'SHARE_TOOL' or not source.get('b_performed'):
                raise SessionRefusal('J_SOURCE_NOT_POSITIVE', json.dumps(source, sort_keys=True))
            receipt_check = validate_receipt(receipt, source)
            if not receipt_check.get('ok'):
                raise SessionRefusal(
                    'B_SOURCE_RECEIPT_MISMATCH',
                    json.dumps(receipt_check.get('checks', {}), sort_keys=True))
            session = cls._attach_new(product, state_root, scenario='available',
                                      attention=attention, variant=variant)
            binding = binding_from_receipt(receipt, source)
            product._append_episode(
                session.branch_id, 'B', BINDING_KIND,
                product._world(session.branch_id).clock, binding)
            seed = product.seed.public()
            session.meta.update(
                schema='SOROK_SAME_PERSON_JOIN@1',
                grade='TEST_ONLY_SOURCEFREE_NOT_NATIVE',
                material_performance=perform,
                root_branch_id='root',
                branch_lineage=None,
                j_source_ref='64fec28c374d8f77fb0b412d0c934d798ede03e8',
                e_source_ref='a2760d3687b063513fe0a5b9589c56c998d4ccb5',
                j_source=source,
                j_c8_state_digest=built['c8_state_digest'],
                j_e1_event_hash=built['e1_event_hash'],
                j_target_id=built['target_id'],
                b_event_contract=B_EVENT_CONTRACT,
                j_b_disposition=PERFORMED,
                b_performer_receipt=receipt,
                source_actor_map={
                    'TEST_ONLY_R31J_A': seed['actor_a'],
                    'TEST_ONLY_R31J_B': seed['actor_b'],
                },
                source_manifest_sha256=source_manifest_sha256(),
                expression_port='R31E_EXPRESSION_PORT@1',
                actor_model='LIVE_ACTOR_MODEL_NOT_RUN',
            )
            session._save_join_meta()
            closure = audit_loaded()
            if not closure.get('ok'):
                raise SessionRefusal('IMPORT_CLOSURE_INVALID',
                                     ';'.join(closure.get('problems', [])))
            provenance = validate_join(product, session.meta, session.branch_id)
            if not provenance.get('ok'):
                raise SessionRefusal('J_PROVENANCE_MISMATCH',
                                     json.dumps(provenance.get('checks', {}), sort_keys=True))
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            return session
        except Exception:
            product.close()
            raise

    def _save_join_meta(self):
        (self.state_root/'session.json').write_text(
            json.dumps(self.meta, indent=2, sort_keys=True) + '\n',
            encoding='utf8')

    @classmethod
    def open(cls, state_root, *, attention=None):
        state_root = Path(state_root).resolve()
        meta = _load_meta(state_root)
        if meta.get('schema') != 'SOROK_SAME_PERSON_JOIN@1':
            raise SessionRefusal('WRONG_PRODUCT_LINEAGE')
        if 'j_source' not in meta:
            raise SessionRefusal('JOIN_META_INCOMPLETE__J_SOURCE_MISSING')
        product_root = _canonical_product_root(state_root, meta)
        _guard_binding(product_root)
        branch = meta.get('branch_id')
        try:
            product = ReadOnlyR31JProduct.reopen(product_root, branch_id=branch)
        except Exception as exc:
            raise SessionRefusal('COLD_REOPEN_REFUSED',
                                 type(exc).__name__ + ':' + str(exc)) from exc
        try:
            if product.source != meta.get('j_source'):
                raise SessionRefusal('J_SOURCE_IDENTITY_CHANGED')
            try:
                persisted = persisted_binding(product, branch)
            except BSourceUnavailable as exc:
                raise SessionRefusal(
                    'J_PROVENANCE_MISMATCH',
                    type(exc).__name__ + ':' + str(exc)) from exc
            binding_check = validate_binding(meta, persisted, product.source)
            if not binding_check.get('ok'):
                raise SessionRefusal(
                    'J_PROVENANCE_MISMATCH',
                    json.dumps(binding_check.get('checks', {}), sort_keys=True))
            lineage_result = validate_lineage(meta, branch, product.store)
            if not lineage_result.get('ok'):
                raise SessionRefusal(
                    'BRANCH_LINEAGE_MISMATCH',
                    json.dumps(lineage_result.get('checks', {}), sort_keys=True))
            root_verify = product.c12_verify('root')
            if not root_verify.get('ok'):
                raise SessionRefusal('ROOT_C12_VERIFY_FAILED',
                                     json.dumps(root_verify.get('errors', [])))
            branch_verify = product.c12_verify(branch)
            if not branch_verify.get('ok'):
                raise SessionRefusal('BRANCH_C12_VERIFY_FAILED',
                                     json.dumps(branch_verify.get('errors', [])))
            provenance = validate_join(product, meta, branch)
            if not provenance.get('ok'):
                raise SessionRefusal('J_PROVENANCE_MISMATCH',
                                     json.dumps(provenance.get('checks', {}), sort_keys=True))
            session = cls(product, state_root, meta)
            if attention and attention != session.meta.get('attention'):
                session.meta['attention'] = attention
                session._save_join_meta()
            verification = session.verify()
            if not verification.get('ok'):
                raise SessionRefusal('C12_VERIFY_FAILED', str(verification))
            closure = audit_loaded()
            if not closure.get('ok'):
                raise SessionRefusal('IMPORT_CLOSURE_INVALID',
                                     ';'.join(closure.get('problems', [])))
            return session
        except Exception:
            product.close()
            raise

    @classmethod
    def probe_refusal(cls, state_root, *, variant='A_REPAIR_LONG'):
        """Return the typed no-target boundary; never fabricate a C9 target."""
        state_root = Path(state_root).resolve()
        root = state_root / 'refusal'
        root.mkdir(parents=True, exist_ok=True)
        scenario = refused_scenario(e2=False)
        partial, producer = c9_only(
            root, gm01=scenario['gm01'], case=scenario['case'], variant=variant)
        producer.close()
        return {
            'schema': 'SOROK_JOIN_E_REFUSAL_PROBE@1',
            'status': 'HOLD',
            'code': 'JOIN_REFUSAL_NO_TARGET__OWNER_CONTRACT_REQUIRED',
            'source': partial['gm01_source'],
            'c8_state_digest': partial['c8_state_digest'],
            'e1_event_hash': partial['e1_event_hash'],
            'c9': partial['c9'],
            'target_id': '',
            'j_b_disposition': 'REFUSED',
            'b_performer_receipt': scenario['b_performer_receipt'],
            'owner_contract': {
                'request': ('The original BP2P4 consumer requires a committed C9 '
                            'CREATE target before it can assemble a product; the '
                            'E first-neighbor session requires a product root. A '
                            'derived targetless C12 representation is available '
                            'in joined.refusal for the refusal path.'),
                'required_decision': ('Provide a lawful no-target C10/C12 '
                                      'representation, or accept this typed HOLD.'),
                'owner': 'BP2P4/C9 consumer owner with C12/C10 owner',
                'unaffected_paths': ('share+E2, share+omit, E expression, '
                                     'attention, privacy, cold positive'),
            },
        }

    def _lineage_result(self):
        return validate_lineage(self.meta, self.branch_id, self.product.store)

    def verify(self) -> dict:
        result = super().verify()
        root = self.product.c12_verify('root')
        lineage_result = self._lineage_result()
        result['root'] = root
        result['lineage'] = lineage_result
        result['ok'] = (bool(result.get('ok')) and bool(root.get('ok'))
                        and bool(lineage_result.get('ok')))
        return result

    def fork_alt(self, new_branch_id='alt'):
        lineage_result = self._lineage_result()
        if not lineage_result.get('ok'):
            raise SessionRefusal(
                'BRANCH_LINEAGE_MISMATCH',
                json.dumps(lineage_result.get('checks', {}), sort_keys=True))
        parent = self.branch_id
        try:
            fork, lineage = create_fork(
                self.product, parent, new_branch_id,
                self.meta.get('branch_lineage'))
        except Exception as exc:
            code = getattr(exc, 'code', type(exc).__name__)
            raise SessionRefusal('FORK_REFUSED', code + ':' + str(exc)) from exc
        self.branch_id = new_branch_id
        self.meta['branch_id'] = new_branch_id
        self.meta['branch_lineage'] = lineage
        self.product.use(new_branch_id)
        self._save_join_meta()
        return fork

    def status(self) -> dict:
        lineage_result = self._lineage_result()
        if not lineage_result.get('ok'):
            raise SessionRefusal(
                'BRANCH_LINEAGE_MISMATCH',
                json.dumps(lineage_result.get('checks', {}), sort_keys=True))
        result = super().status()
        result['j_source_ref'] = self.meta.get('j_source_ref')
        result['e_source_ref'] = self.meta.get('e_source_ref')
        result['j_target_id'] = self.meta.get('j_target_id')
        result['root_branch_id'] = self.meta.get('root_branch_id')
        result['material_performance'] = self.meta.get('material_performance')
        result['j_b_disposition'] = self.meta.get('j_b_disposition')
        result['b_performer_receipt'] = self.meta.get('b_performer_receipt')
        result['branch_lineage'] = self.meta.get('branch_lineage')
        return result
