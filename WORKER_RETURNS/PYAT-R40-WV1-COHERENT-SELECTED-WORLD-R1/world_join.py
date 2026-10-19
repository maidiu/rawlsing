"""Bounded WV1 binding of actual E04L learned release to T35/R13 selected world.

Original owner/client modules remain byte-identical. Proposal and N9 empirical
permissions remain held. This module provides no scientific or actor authority.
"""
from copy import deepcopy
from dataclasses import replace
from unittest.mock import patch
import bootstrap
from fixture import prepare
from readthrough import ReadThroughService, ReleaseReadThroughProvider, ReadThroughError, require
from rawlsing_next import pre553_learned_world_composition as i4
import two_epoch_world as t35
from product.world import SelectedWorldCatalog
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_empirical_objects import semantic_hash

class LearnedIdentityCatalog(SelectedWorldCatalog):
    """Extend snapshot identity with the exact selected learned product binding."""
    def empirical_identity(self):
        result = super().empirical_identity()
        result['selected_learned_product'] = deepcopy(self.learned_binding)
        return result

class CoherentService(ReadThroughService):
    def __init__(self, prepared):
        super().__init__(prepared)
        self.provider.cache = {}  # R13 transient-cache interface; facts remain exact catalog reads.

    def structural(self, snapshot, key, consumer):
        selected = self.catalog.read(snapshot, key)
        if selected['state'] == 'SUPPORTED_TEST_ONLY':
            record = self.catalog._select_record(key, snapshot.material['valid_at'],
                                                  snapshot.material['published_asof'])
            require(record is not None, 'SELECTED_STRUCTURAL_RECORD_UNAVAILABLE')
            try:
                fresh = self.catalog._resolve(record)
            except KeyError as exc:
                raise ReadThroughError('STRUCTURAL_OWNER_UNAVAILABLE') from exc
            require(fresh == selected, 'SELECTED_STRUCTURAL_OWNER_CHANGED_OR_UNAVAILABLE')
        return super().structural(snapshot, key, consumer)

    def possibilities(self, snapshot, **kwargs):
        require(snapshot.material['empirical']['selected_learned_product'] == self.catalog.learned_binding,
                'SNAPSHOT_LEARNED_SELECTION_MISMATCH')
        require(self.catalog.empirical is self.provider.world, 'EMPIRICAL_WORLD_OBJECT_MISMATCH')
        return super().possibilities(snapshot, **kwargs)

class SelectedWorld:
    def __init__(self, *, release='base', rules='two_epoch', support_loss=False):
        require(release in ('base', 'alternate'), 'UNKNOWN_SELECTED_RELEASE')
        self.prepared = p = prepare(same_marginals=release=='alternate', support_loss=support_loss)
        # T35's actual publication code runs on the SAME native source/service,
        # rather than constructing a second coincident empirical world.
        with patch.object(t35, 'GenericSelectedWorldService', return_value=p.service):
            original = t35.make_adapter(variant=rules)
        self.service = CoherentService(p)
        self.service.catalog.learned_binding = dict(
            release_ref=p.composition.m2_artifacts.release.ref.as_dict(),
            selection_key_ref=p.composition.b5_selection_receipt.selection_key_ref.as_dict(),
            selection_receipt_ref=p.composition.b5_selection_receipt.ref.as_dict(),
            subject_ref=p.composition.m1_disposition.ref.as_dict(),
            permission='NONPARENT_OPTIONS_TEST_ONLY')
        self.service.catalog.__class__ = LearnedIdentityCatalog
        self.service.catalog.catalog_hash = semantic_hash(dict(
            records=self.service.catalog.records, empirical=self.service.catalog.empirical_identity()))
        self.release_bank = {release: p}
        self.adapter = t35.E.N9SelectedWorldAdapter(service=self.service, registry=original.registry)

    def stage_release(self, label):
        require(label == 'alternate' and label not in self.release_bank, 'EXACT_ALTERNATE_REQUIRED')
        p = prepare(same_marginals=True)
        p.repository = self.prepared.repository
        p.lifecycle = self.prepared.lifecycle
        # Store the second actual M2 closure before the control; no selection side effect.
        staged = i4.compose_learned_world(
            replace(p.contract, lifecycle_actions=()),
            m2_repository=p.repository, lifecycle_executor=p.lifecycle,
            m1_disposition=p.composition.m1_disposition)
        require(staged.receipt.terminal_state == 'RULE_SATISFIED', 'ALTERNATE_STAGING_REFUSED')
        self.release_bank[label] = p

    def select_release(self, label):
        require(label in self.release_bank, 'UNREGISTERED_RELEASE_SELECTION')
        p = self.release_bank[label]
        prior = self.prepared.composition.b5_selection_receipt
        p.contract = replace(p.contract, lifecycle_actions=('REGISTER', 'PUBLISH', 'SELECT_CURRENT'),
                             expected_previous_selection_receipt_ref=prior.ref)
        p.composition = i4.compose_learned_world(
            p.contract, m2_repository=p.repository, lifecycle_executor=p.lifecycle,
            m1_disposition=p.composition.m1_disposition)
        require(p.composition.receipt.terminal_state == 'RULE_SATISFIED', 'ALTERNATE_SELECTION_REFUSED')
        self.prepared = p
        self.service.provider = ReleaseReadThroughProvider(p)
        self.service.provider.cache = {}
        catalog = self.service.catalog
        catalog.empirical = p.native_provider.world
        catalog.learned_binding = dict(
            release_ref=p.composition.m2_artifacts.release.ref.as_dict(),
            selection_key_ref=p.composition.b5_selection_receipt.selection_key_ref.as_dict(),
            selection_receipt_ref=p.composition.b5_selection_receipt.ref.as_dict(),
            subject_ref=p.composition.m1_disposition.ref.as_dict(),
            permission='NONPARENT_OPTIONS_TEST_ONLY')
        catalog.catalog_hash = semantic_hash(dict(records=catalog.records,
                                                  empirical=catalog.empirical_identity()))

    def epoch(self, clock):
        request = t35.make_request(clock)
        snapshot = self.adapter.build_snapshot(request)
        acceptance = self.adapter.accept(request, snapshot)
        result = consume(self.service, snapshot)
        return dict(clock=clock.binding(), snapshot=snapshot.material,
                    snapshot_hash=snapshot.snapshot_hash,
                    acceptance=acceptance.binding(), acceptance_hash=acceptance.acceptance_hash,
                    nonparent=result, proposal=self.proposal(snapshot),
                    learned_binding=deepcopy(self.service.catalog.learned_binding),
                    structural_trace=deepcopy(self.service.catalog.trace),
                    empirical_trace=deepcopy(self.service.provider.trace),
                    F6P=dict(state='AVAILABLE_TEST_ONLY_EVIDENCE', join='NO_AUTHORIZED_JOIN',
                             source_commit='912467aaacb715fd6e80ebc8c2bdd7285c26120b',
                             reason='NO_MATCHED_SOURCE_ESTIMAND_OR_TRANSPORT_CONTRACT'),
                    R13_serve='HOLD_N9_SELECTED_WORLD_EMPIRICAL_PERMISSION')

    def proposal(self, snapshot):
        try:
            evaluate(self.service, snapshot, t35.PROPOSALS)
        except ReadThroughError as exc:
            return dict(state='HOLD', reason=str(exc), consumer='CONCEPTION_SCENARIO_PROPOSALS')
        raise AssertionError('UNAUTHORIZED_PROPOSAL_PERMISSION_ESCALATION')

    def snapshot(self, clock):
        return self.adapter.build_snapshot(t35.make_request(clock))

def product():
    world = SelectedWorld()
    return dict(schema='WV1_COHERENT_TEST_ONLY_SELECTED_WORLD@1',
                grade='AUTHOR_SOURCEFREE_POSITIVE_NONPARENT__PROPOSAL_AND_R13_SERVE_HOLD',
                epochs={'2026':world.epoch(t35.E1), '2027':world.epoch(t35.E2)},
                source_method_authority='SYNTHETIC_TEST_ONLY; NO_ORIGINAL_SOURCE_OR_METHOD_ISSUANCE')

if __name__ == '__main__':
    import json
    print(json.dumps(product(), sort_keys=True, indent=2))
