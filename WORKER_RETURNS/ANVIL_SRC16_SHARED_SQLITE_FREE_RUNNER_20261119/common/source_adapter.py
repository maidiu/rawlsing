"""Source-profile adapter: exact config/binding/current selection for common operator."""
from __future__ import annotations
import importlib.util, json, os
from pathlib import Path
from rawlsing_next.pre553_r157_projection_adapter import (
    SourceConfig, load_source_config, canonical_config_hash, source_read_request_from_config,
)

class AdapterRefusal(RuntimeError):
    def __init__(self, code, detail=''):
        super().__init__(code + (f': {detail}' if detail else '')); self.code=code

class Profile:
    def __init__(self, path):
        self.path=Path(path).absolute(); self.data=json.loads(self.path.read_text())
        self.kind=self.data['kind']
        if self.kind not in ('sourcefree','src16','src16-denied'):
            raise AdapterRefusal('UNKNOWN_SOURCE_ADAPTER_KIND',self.kind)
        self.config=load_source_config(Path(self.data['config']).absolute())
        self.source_path=Path(self.data['source']).absolute() if self.kind=='sourcefree' else Path(self.data['source_path']).absolute()
        self.resolver=None; self.request=None; self.grant_ref=None; self.decision_ref=None
        if self.kind in ('src16','src16-denied'):
            bd=Path(self.data['binding_dir']).absolute()
            rp=bd/'SRC16.exact_resolver.py'; bp=bd/'SRC16.construction.binding.json'
            spec=importlib.util.spec_from_file_location('src16_resolver_adapter',rp)
            mod=importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            self.resolver=mod.ExactSrc16Resolver(bp); self.request=self.resolver.request
            self.grant_ref=self.resolver.decision.source_permission_refs[0]
            self.decision_ref=self.resolver.decision.decision_ref
            if self.kind=='src16-denied':
                import dataclasses
                self.request=dataclasses.replace(self.request,purpose='DENIED_TEST_PURPOSE')
            if self.config.source_id!='SRC16' or self.config.active_source_sha256!='e368fc0f1d141b201900185c919c48ab1de1c4c7815bccf83a6e4fb224293204':
                raise AdapterRefusal('SRC16_CONFIG_IDENTITY_DRIFT')
            d=self.config.document
            if (d['binding']['row_count'],len(d['physical_slots']),len(d['response_slots']),len(d['coordinate_slots']),len(d['weight_slots']))!=(1613,216,157,2,0):
                raise AdapterRefusal('SRC16_CONFIG_SHAPE_DRIFT')
            # Source path must match the private exact grant before any decode.
            grant=json.loads((bd/'SRC16.construction.grant.json').read_text())
            if str(self.source_path)!=str(Path(grant['source_path']).absolute()):
                raise AdapterRefusal('SRC16_SOURCE_PATH_NOT_EXACT_GRANT')
            expected=source_read_request_from_config(
                self.config,host=self.request.host,purpose=self.request.purpose,
                consumer_use=self.request.consumer_use,semantic_use_scope=self.request.semantic_use_scope)
            if expected!=self.request:
                raise AdapterRefusal('SRC16_CONFIG_REQUEST_MISMATCH')
    def resolve_before_source(self):
        if self.kind=='sourcefree':
            return None
        d=self.resolver.resolve_current(self.request)
        if d.currentness!='CURRENT_GRANTED' or d.revocation_ref is not None:
            raise AdapterRefusal('SRC16_CURRENT_OR_REVOCATION_REFUSED')
        return d
