"""Bounded parent-funded purchase/refusal over the existing P2 world material.

The buyer is the registered C02 parent; its cash/free-hours are spent, not the
B01 fixed-A household cash. The object must exist in a source-qualified P2
market inventory before transfer. Ownership is one P2 world material fact, not a
second household database. No bp4 event vocabulary is edited and no public
event or Nadia perception is fabricated; the stock/ownership consumer is the
actual later reader.
"""
from __future__ import annotations

from contextlib import contextmanager
import fcntl
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import RecursionRefusal, detached, digest
from developmental_recursion.p2_owner import (
    branch_is_ancestor, material_fact_source, write_material_fact,
)
from developmental_recursion.parent_activity import (
    PARENT_GRADE, PARENT_MATERIAL_SCHEMA, _StoreWrite, _material_content,
    _material_document, _parent_write_lock, _read_material,
    parent_feasible_actions, read_parent_material,
)
from developmental_recursion.supporting_actor import read_supporting_actor

try:
    import house as p6_house
except ImportError:  # pragma: no cover - caller must put P6 on sys.path
    p6_house = None

try:
    import historical_period as hp
except ImportError:  # pragma: no cover - B02 is optional for a B04-only cut
    hp = None

MARKET_SLOT = "p6_market_inventory"
OWNED_SLOT = "p6_owned_objects"
MARKET_SCHEMA = "SOROK_MARKET_INVENTORY@1"
MARKET_READ_SCHEMA = "SOROK_MARKET_INVENTORY_READ@1"
OWNED_SCHEMA = "SOROK_OWNED_OBJECTS@1"
OWNED_READ_SCHEMA = "SOROK_OWNED_OBJECTS_READ@1"
PURCHASE_RECEIPT_SCHEMA = "SOROK_PARENT_PURCHASE_RECEIPT@1"
PURCHASE_KIND = "P2_PARENT_PURCHASE"
GRADE = "SOURCEFREE_S2_ONLY"
FIXTURE_GRADE = "SOURCEFREE_FIXTURE"
CURRENCY = "sourcefree_currency_unit"
PURCHASE_HOURS = 1
MARKET_FIELDS = frozenset({"schema", "grade", "currency_unit", "items"})
MARKET_STORED_FIELDS = frozenset({*MARKET_FIELDS, "root", "branch", "epoch", "source"})
ITEM_FIELDS = frozenset({"object_id", "kind", "quantity", "unit_price"})
OWNED_FIELDS = frozenset({"schema", "grade", "objects"})
OWNED_STORED_FIELDS = frozenset({*OWNED_FIELDS, "root", "branch", "epoch", "source"})
OWNED_OBJECT_FIELDS = frozenset({
    "acquisition_id", "object_id", "kind", "owner_actor_id", "quantity",
    "market_source", "purchase_source", "currency_unit", "unit_price",
})
READ_BOUNDARY = {
    "psyche_store": "NOT_READ",
    "psychology_state": "NOT_WRITTEN",
    "class_to_trait": "NOT_APPLIED",
    "model_prose": "NOT_READ",
}


@contextmanager
def _purchase_lock(session):
    """Serialize market/ownership transfer reads and writes.

    This is a state-root lock over the existing P2/C12 writers, not a new
    scheduler or ledger.  It prevents two purchases from reading the same
    stock/ownership sources before either commits.
    """
    root = Path(session.state_root)
    root.mkdir(parents=True, exist_ok=True)
    with (root / "material_operations.lock").open("a") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def _text(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _nonneg_int(value: Any) -> bool:
    return type(value) is int and value >= 0


def _hash_text(value: Any) -> bool:
    if not isinstance(value, str) or len(value) != 64:
        return False
    try:
        int(value, 16)
    except ValueError:
        return False
    return True


def default_market_items() -> list[dict]:
    return [
        {"object_id": "object:junior-drum-kit", "kind": "junior_drum_kit",
         "quantity": 2, "unit_price": 40},
        {"object_id": "object:acoustic-drum-kit", "kind": "acoustic_drum_kit",
         "quantity": 1, "unit_price": 180},
    ]


def _provenance(stored_branch: str, current_branch: str) -> dict:
    inherited = stored_branch != current_branch
    return {
        "stored_branch": stored_branch,
        "current_branch": current_branch,
        "inherited": inherited,
        "scope": "P6_MATERIAL_STOCK_ONLY",
        "fork_state": ("C12_FORK_WITHOUT_S46_INTERVAL_STATE"
                       if inherited else "CURRENT_BRANCH"),
    }


def _validate_items(items: Any) -> list[dict]:
    if not isinstance(items, list) or not items:
        raise RecursionRefusal("P6_MARKET_SCHEMA")
    rows, ids, kinds = [], set(), set()
    for item in items:
        if not isinstance(item, Mapping) or set(item) != ITEM_FIELDS:
            raise RecursionRefusal("P6_MARKET_ITEM_SCHEMA")
        row = detached(item)
        if (not _text(row.get("object_id")) or not _text(row.get("kind"))
                or not _nonneg_int(row.get("quantity"))
                or not _nonneg_int(row.get("unit_price"))):
            raise RecursionRefusal("P6_MARKET_ITEM_SCHEMA")
        if row["object_id"] in ids or row["kind"] in kinds:
            raise RecursionRefusal("P6_MARKET_ITEM_DUPLICATE")
        ids.add(row["object_id"])
        kinds.add(row["kind"])
        rows.append(row)
    return rows


def _market_content(items: Any = None) -> dict:
    return {
        "schema": MARKET_SCHEMA,
        "grade": FIXTURE_GRADE,
        "currency_unit": CURRENCY,
        "items": _validate_items(default_market_items() if items is None else items),
    }


def _document(session, content: Mapping[str, Any]) -> dict:
    world = session.world()
    document = {**detached(content), "root": session.read_root()["root_hash"],
                "branch": session.branch_id, "epoch": world.clock}
    document["source"] = material_fact_source(document)
    return document


def _read_market_document(document: Any, world, root: str, branch: str, *,
                          branch_ok=None) -> dict:
    if not isinstance(document, dict) or set(document) != MARKET_STORED_FIELDS:
        raise RecursionRefusal("P6_MARKET_SCHEMA")
    if document.get("schema") != MARKET_SCHEMA or document.get("grade") != FIXTURE_GRADE:
        raise RecursionRefusal("P6_MARKET_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_MARKET_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_MARKET_SOURCE_OR_ROOT_MISMATCH")
    if document.get("source") != material_fact_source(document):
        raise RecursionRefusal("P6_MARKET_SOURCE_OR_ROOT_MISMATCH")
    if document.get("currency_unit") != CURRENCY:
        raise RecursionRefusal("P6_MARKET_CURRENCY")
    items = _validate_items(document.get("items"))
    material_hash = digest({"root": root, "branch": branch, "clock": world.clock,
                            "epoch": epoch, "source": document["source"],
                            "currency_unit": CURRENCY, "items": items})
    return {
        "schema": MARKET_READ_SCHEMA,
        "grade": FIXTURE_GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": document["source"],
        "material_hash": material_hash,
        "currency_unit": CURRENCY,
        "items": items,
        "provenance": _provenance(stored_branch, branch),
    }


def read_market_inventory(session) -> dict:
    world = session.world()
    document = world.resources.get(MARKET_SLOT)
    if document is None:
        raise RecursionRefusal("P6_MARKET_ABSENT")
    root_row = session.read_root()
    return _read_market_document(
        document, world, root_row["root_hash"], session.branch_id,
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )


def _establish_market_inventory(session, *, items: Any = None) -> dict:
    document = _document(session, _market_content(items))
    _read_market_document(document, session.world(),
                          session.read_root()["root_hash"], session.branch_id)
    existing = session.world().resources.get(MARKET_SLOT)
    if existing is not None:
        if existing != document:
            raise RecursionRefusal("P6_MARKET_ALREADY_ESTABLISHED")
        return read_market_inventory(session)
    write_material_fact(session, slot=MARKET_SLOT, document=document)
    return read_market_inventory(session)


def establish_market_inventory(session, *, items: Any = None) -> dict:
    with _purchase_lock(session):
        return _establish_market_inventory(session, items=items)


def _validate_owned_objects(objects: Any) -> list[dict]:
    if not isinstance(objects, list):
        raise RecursionRefusal("P6_OWNED_SCHEMA")
    rows, ids = [], set()
    for item in objects:
        if not isinstance(item, Mapping) or set(item) != OWNED_OBJECT_FIELDS:
            raise RecursionRefusal("P6_OWNED_OBJECT_SCHEMA")
        row = detached(item)
        if (not _text(row.get("acquisition_id")) or not _text(row.get("object_id"))
                or not _text(row.get("kind")) or not _text(row.get("owner_actor_id"))
                or type(row.get("quantity")) is not int or row["quantity"] < 1
                or not _hash_text(row.get("market_source"))
                or not _hash_text(row.get("purchase_source"))
                or row.get("currency_unit") != CURRENCY
                or not _nonneg_int(row.get("unit_price"))):
            raise RecursionRefusal("P6_OWNED_OBJECT_SCHEMA")
        if row["acquisition_id"] in ids:
            raise RecursionRefusal("P6_OWNED_OBJECT_DUPLICATE")
        ids.add(row["acquisition_id"])
        rows.append(row)
    return rows


def _owned_content(objects: Any = None) -> dict:
    return {
        "schema": OWNED_SCHEMA,
        "grade": FIXTURE_GRADE,
        "objects": _validate_owned_objects([] if objects is None else objects),
    }


def _read_owned_document(document: Any, world, root: str, branch: str, *,
                         branch_ok=None) -> dict:
    if not isinstance(document, dict) or set(document) != OWNED_STORED_FIELDS:
        raise RecursionRefusal("P6_OWNED_SCHEMA")
    if document.get("schema") != OWNED_SCHEMA or document.get("grade") != FIXTURE_GRADE:
        raise RecursionRefusal("P6_OWNED_SCHEMA")
    stored_branch = document.get("branch")
    if (document.get("root") != root
            or (stored_branch != branch
                and not (branch_ok is not None
                         and branch_ok(stored_branch, document.get("epoch"))))):
        raise RecursionRefusal("P6_OWNED_SOURCE_OR_ROOT_MISMATCH")
    epoch = document.get("epoch")
    if (isinstance(epoch, bool) or not isinstance(epoch, int)
            or epoch < 0 or epoch > world.clock):
        raise RecursionRefusal("P6_OWNED_SOURCE_OR_ROOT_MISMATCH")
    if document.get("source") != material_fact_source(document):
        raise RecursionRefusal("P6_OWNED_SOURCE_OR_ROOT_MISMATCH")
    objects = _validate_owned_objects(document.get("objects"))
    totals = {}
    for row in objects:
        key = (row["owner_actor_id"], row["object_id"], row["kind"])
        totals[key] = totals.get(key, 0) + row["quantity"]
    total_rows = [
        {"owner_actor_id": owner, "object_id": object_id, "kind": kind,
         "quantity": quantity}
        for (owner, object_id, kind), quantity in sorted(totals.items())
    ]
    material_hash = digest({"root": root, "branch": branch, "clock": world.clock,
                            "epoch": epoch, "source": document["source"],
                            "objects": objects})
    return {
        "schema": OWNED_READ_SCHEMA,
        "grade": FIXTURE_GRADE,
        "root": root,
        "branch": branch,
        "clock": world.clock,
        "epoch": epoch,
        "source": document["source"],
        "material_hash": material_hash,
        "objects": objects,
        "totals": total_rows,
        "provenance": _provenance(stored_branch, branch),
    }


def read_owned_objects(session) -> dict:
    world = session.world()
    document = world.resources.get(OWNED_SLOT)
    if document is None:
        return {
            "schema": OWNED_READ_SCHEMA, "grade": FIXTURE_GRADE,
            "status": "ABSENT", "root": session.read_root()["root_hash"],
            "branch": session.branch_id, "clock": world.clock, "epoch": None,
            "source": "", "material_hash": "", "objects": [], "totals": [],
            "provenance": _provenance(session.branch_id, session.branch_id),
            "read_boundary": detached(READ_BOUNDARY),
        }
    root_row = session.read_root()
    result = _read_owned_document(
        document, world, root_row["root_hash"], session.branch_id,
        branch_ok=lambda stored, epoch: branch_is_ancestor(session, stored, epoch),
    )
    result["status"] = "READ"
    result["read_boundary"] = detached(READ_BOUNDARY)
    return result



def _period_ref(session) -> dict:
    if hp is None:
        return {"status": "B02_NOT_COMPOSED"}
    try:
        plan = hp.read_period_plan(session)
        current_date = hp._date_from_clock(plan, session.clock()).isoformat()
        read = hp.read_material_period(session, current_date)
        return {
            "status": "B02_MATERIAL_PERIOD_READ",
            "period_id": read["period"]["period_id"],
            "as_of_date": current_date,
            "as_of_relation": read["as_of_relation"],
            "interval_status": read["interval_status"],
            "interval_status_detail": read["interval_status_detail"],
        }
    except RecursionRefusal:
        return {"status": "B02_NOT_AVAILABLE"}


def _purchase_episodes(session, alias: str, operation_id: str) -> list[dict]:
    return [
        row for row in session.product.store.episodes(session.branch_id)
        if row.get("actor_id") == alias and row.get("kind") == PURCHASE_KIND
        and (row.get("body") or {}).get("operation_id") == operation_id
    ]


def _refusal(session, *, operation_id: str, parent_id: str, alias: str,
             owner_actor_id: str, request: dict, reasons: list[str],
             market_source: str, owned_source: str, parent_source: str,
             household_source: str, dwelling_source: str,
             feasibility: dict) -> dict:
    receipt = {
        "schema": PURCHASE_RECEIPT_SCHEMA,
        "grade": GRADE,
        "status": "REFUSED",
        "operation_id": operation_id,
        "parent_id": parent_id,
        "parent_alias": alias,
        "buyer": "REGISTERED_PARENT",
        "owner_actor_id": owner_actor_id,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": session.clock(),
        "request": detached(request),
        "object_id": "",
        "quantity": 0,
        "unit_price": 0,
        "currency_unit": request.get("currency_unit"),
        "reasons": list(reasons),
        "b03_feasibility": {
            "status": feasibility.get("status"),
            "reasons": list(feasibility.get("reasons") or []),
            "unknowns": list(feasibility.get("unknowns") or []),
            "dwelling_source": dwelling_source,
            "household_source": household_source,
        },
        "parent_material_source_before": parent_source,
        "parent_material_source_after": parent_source,
        "market_source_before": market_source,
        "market_source_after": market_source,
        "owned_source_before": owned_source,
        "owned_source_after": owned_source,
        "household_source": household_source,
        "dwelling_source": dwelling_source,
        "period": _period_ref(session),
        "event_effect": "NONE",
        "public_event": "NOT_EMITTED_HELD_PAIR3_VOCABULARY",
        "possession": "NONE",
        "actual_reader": "material_operations.read_owned_objects",
        "read_boundary": detached(READ_BOUNDARY),
    }
    store = session.product.store
    with _StoreWrite(store):
        store.append_episode(
            session.branch_id, actor_id=alias, kind=PURCHASE_KIND,
            clock=session.clock(),
            body={
                "schema": PURCHASE_RECEIPT_SCHEMA, "grade": GRADE,
                "root": receipt["root"], "branch": receipt["branch"],
                "operation_id": operation_id, "actor_id": parent_id,
                "alias": alias, "status": "REFUSED", "receipt": receipt,
            },
        )
    return receipt


def _purchase_drum_kit(session, parent_id: str, *, operation_id: str,
                      owner_actor_id: str, request: Any = None,
                      expected_clock: int | None = None) -> dict:
    """Purchase one source-qualified object for an explicit owner using parent cash."""
    if p6_house is None:
        raise RecursionRefusal("P6_HOUSE_READER_UNAVAILABLE")
    if not _text(operation_id) or not _text(owner_actor_id):
        raise RecursionRefusal("PURCHASE_SCHEMA")
    try:
        material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    except RecursionRefusal as exc:
        raise RecursionRefusal("PURCHASE_PARENT_UNAVAILABLE") from exc
    alias = material["alias"]
    if expected_clock is not None and expected_clock != material["clock"]:
        raise RecursionRefusal("PURCHASE_CLOCK_MISMATCH")
    request = detached(p6_house.DRUM_KIT_REQUESTS["junior"]
                       if request is None else request)
    if not isinstance(request, dict) or request.get("currency_unit") != CURRENCY:
        raise RecursionRefusal("PURCHASE_CURRENCY_MISMATCH")
    market = read_market_inventory(session)
    owned = read_owned_objects(session)
    household = p6_house.read_household(session)
    dwelling = p6_house.read_dwelling(session)
    feasibility = p6_house.material_feasibility(session, request)
    if owner_actor_id not in (
            session.world().actor_state.get("A", {}).get("actor_id"), parent_id):
        raise RecursionRefusal("PURCHASE_OWNER_UNKNOWN")
    if market["provenance"]["inherited"]:
        raise RecursionRefusal("PURCHASE_FORK_NOT_SUPPORTED")

    episodes = _purchase_episodes(session, alias, operation_id)
    if len(episodes) > 1:
        raise RecursionRefusal("PURCHASE_OPERATION_DUPLICATE")
    if episodes:
        body = episodes[0].get("body") or {}
        receipt = dict(body.get("receipt") or {})
        if (body.get("actor_id") != parent_id
                or receipt.get("owner_actor_id") != owner_actor_id
                or receipt.get("request") != request):
            raise RecursionRefusal("PURCHASE_OPERATION_REUSE_MISMATCH")
        if receipt.get("status") == "ADMITTED":
            if (material["source"] != receipt.get("parent_material_source_after")
                    or market["source"] != receipt.get("market_source_after")
                    or owned["source"] != receipt.get("owned_source_after")):
                raise RecursionRefusal("PURCHASE_REPLAY_STALE")
        elif (material["source"] != receipt.get("parent_material_source_before")
              or market["source"] != receipt.get("market_source_before")
              or owned["source"] != receipt.get("owned_source_before")):
            raise RecursionRefusal("PURCHASE_REPLAY_STALE")
        receipt["status"] = "REPLAY"
        return receipt

    material_reasons = [reason for reason in feasibility.get("reasons") or []
                        if reason != "REFUSED_AFFORDABILITY"]
    if feasibility.get("status") == "UNKNOWN" or material_reasons:
        return _refusal(
            session, operation_id=operation_id, parent_id=parent_id, alias=alias,
            owner_actor_id=owner_actor_id, request=request,
            reasons=material_reasons or ["MATERIAL_UNKNOWN"],
            market_source=market["source"], owned_source=owned["source"],
            parent_source=material["source"], household_source=household["source"],
            dwelling_source=dwelling["source"], feasibility=feasibility,
        )
    item = next((row for row in market["items"]
                 if row["kind"] == request.get("kind")), None)
    if item is None or item["quantity"] < 1:
        return _refusal(
            session, operation_id=operation_id, parent_id=parent_id, alias=alias,
            owner_actor_id=owner_actor_id, request=request,
            reasons=["PURCHASE_STOCK_UNAVAILABLE"],
            market_source=market["source"], owned_source=owned["source"],
            parent_source=material["source"], household_source=household["source"],
            dwelling_source=dwelling["source"], feasibility=feasibility,
        )
    if (item["unit_price"] != request.get("purchase_price")
            or item["unit_price"] < 0):
        raise RecursionRefusal("PURCHASE_PRICE_MISMATCH")
    fields = material["material"]
    parent_currency = fields.get("currency_unit")
    market_currency = market.get("currency_unit")
    request_currency = request.get("currency_unit")
    if (not _text(parent_currency) or not _text(market_currency)
            or not _text(request_currency)
            or not (parent_currency == market_currency == request_currency)):
        raise RecursionRefusal("PURCHASE_CURRENCY_INCOMPATIBLE")
    if fields["cash_units"] < item["unit_price"]:
        return _refusal(
            session, operation_id=operation_id, parent_id=parent_id, alias=alias,
            owner_actor_id=owner_actor_id, request=request,
            reasons=["PURCHASE_INSUFFICIENT_FUNDS"],
            market_source=market["source"], owned_source=owned["source"],
            parent_source=material["source"], household_source=household["source"],
            dwelling_source=dwelling["source"], feasibility=feasibility,
        )
    if fields["free_hours"] < PURCHASE_HOURS:
        return _refusal(
            session, operation_id=operation_id, parent_id=parent_id, alias=alias,
            owner_actor_id=owner_actor_id, request=request,
            reasons=["PURCHASE_TIME_UNAVAILABLE"],
            market_source=market["source"], owned_source=owned["source"],
            parent_source=material["source"], household_source=household["source"],
            dwelling_source=dwelling["source"], feasibility=feasibility,
        )
    after_content = _material_content({
        **fields,
        "schema": PARENT_MATERIAL_SCHEMA,
        "grade": PARENT_GRADE,
        "actor_id": parent_id,
        "source_ref": material["source_ref"],
        "cash_units": fields["cash_units"] - item["unit_price"],
        "free_hours": fields["free_hours"] - PURCHASE_HOURS,
    })
    after_parent = _material_document(session, parent_id, after_content)
    after_items = detached(market["items"])
    for row in after_items:
        if row["object_id"] == item["object_id"]:
            row["quantity"] -= 1
    after_market = _document(session, _market_content(after_items))
    owned_rows = [] if owned["status"] == "ABSENT" else detached(owned["objects"])
    purchase_source = digest({
        "schema": PURCHASE_RECEIPT_SCHEMA,
        "operation_id": operation_id,
        "parent_id": parent_id,
        "owner_actor_id": owner_actor_id,
        "object_id": item["object_id"],
        "unit_price": item["unit_price"],
        "market_source": market["source"],
        "parent_before": material["source"],
        "parent_after": after_parent["source"],
    })
    owned_rows.append({
        "acquisition_id": operation_id,
        "object_id": item["object_id"],
        "kind": item["kind"],
        "owner_actor_id": owner_actor_id,
        "quantity": 1,
        "market_source": market["source"],
        "purchase_source": purchase_source,
        "currency_unit": CURRENCY,
        "unit_price": item["unit_price"],
    })
    after_owned = _document(session, _owned_content(owned_rows))
    _read_owned_document(after_owned, session.world(),
                         session.read_root()["root_hash"], session.branch_id)
    receipt = {
        "schema": PURCHASE_RECEIPT_SCHEMA,
        "grade": GRADE,
        "status": "ADMITTED",
        "operation_id": operation_id,
        "parent_id": parent_id,
        "parent_alias": alias,
        "buyer": "REGISTERED_PARENT",
        "owner_actor_id": owner_actor_id,
        "root": session.read_root()["root_hash"],
        "branch": session.branch_id,
        "clock": session.clock(),
        "request": request,
        "object_id": item["object_id"],
        "kind": item["kind"],
        "quantity": 1,
        "unit_price": item["unit_price"],
        "currency_unit": CURRENCY,
        "reasons": [],
        "b03_feasibility": {
            "status": feasibility.get("status"),
            "reasons": list(feasibility.get("reasons") or []),
            "unknowns": list(feasibility.get("unknowns") or []),
            "dwelling_source": dwelling["source"],
            "household_source": household["source"],
        },
        "parent_material_source_before": material["source"],
        "parent_material_source_after": after_parent["source"],
        "parent_cash_before": fields["cash_units"],
        "parent_cash_after": after_content["cash_units"],
        "parent_free_hours_before": fields["free_hours"],
        "parent_free_hours_after": after_content["free_hours"],
        "market_source_before": market["source"],
        "market_source_after": after_market["source"],
        "owned_source_before": "" if owned["status"] == "ABSENT" else owned["source"],
        "owned_source_after": after_owned["source"],
        "household_source": household["source"],
        "household_material_hash": household["material_hash"],
        "dwelling_source": dwelling["source"],
        "dwelling_material_hash": dwelling["material_hash"],
        "purchase_source": purchase_source,
        "period": _period_ref(session),
        "event_effect": "NONE",
        "public_event": "NOT_EMITTED_HELD_PAIR3_VOCABULARY",
        "possession": "OBJECT_STOCK_AND_OWNERSHIP_WRITTEN",
        "currency_basis": "PARENT_MARKET_REQUEST_CURRENCY_UNIT_EQUAL",
        "parent_currency_unit": parent_currency,
        "market_currency_unit": market_currency,
        "request_currency_unit": request_currency,
        "actual_reader": "material_operations.read_owned_objects",
        "read_boundary": detached(READ_BOUNDARY),
    }
    store = session.product.store
    world = session.world()
    with _StoreWrite(store):
        store.append_episode(
            session.branch_id, actor_id=alias, kind=PURCHASE_KIND,
            clock=world.clock,
            body={
                "schema": PURCHASE_RECEIPT_SCHEMA, "grade": GRADE,
                "root": receipt["root"], "branch": receipt["branch"],
                "operation_id": operation_id, "actor_id": parent_id,
                "alias": alias, "status": "ADMITTED", "receipt": receipt,
            },
        )
        world.actor_state[alias]["material"] = after_parent
        world.resources[MARKET_SLOT] = after_market
        world.resources[OWNED_SLOT] = after_owned
        session.product._checkpoint(session.branch_id, world.clock, world)
    return receipt


def purchase_drum_kit(session, parent_id: str, *, operation_id: str,
                      owner_actor_id: str, request: Any = None,
                      expected_clock: int | None = None) -> dict:
    """Serialize one registered-parent purchase and its material history."""
    with _purchase_lock(session):
        with _parent_write_lock(session):
            return _purchase_drum_kit(
                session, parent_id, operation_id=operation_id,
                owner_actor_id=owner_actor_id, request=request,
                expected_clock=expected_clock,
            )


def _purchase_read_provenance(session, episode: Mapping[str, Any],
                              receipt: Mapping[str, Any], *, parent_id: str,
                              alias: str, operation_id: str) -> str:
    root = session.read_root()["root_hash"]
    branch = session.branch_id
    body = episode.get("body") or {}
    if (body.get("schema") != PURCHASE_RECEIPT_SCHEMA
            or body.get("grade") != GRADE
            or body.get("root") != root
            or body.get("branch") != branch
            or body.get("actor_id") != parent_id
            or body.get("alias") != alias
            or body.get("operation_id") != operation_id):
        raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
    if (receipt.get("schema") != PURCHASE_RECEIPT_SCHEMA
            or receipt.get("grade") != GRADE
            or receipt.get("root") != root
            or receipt.get("branch") != branch
            or receipt.get("operation_id") != operation_id
            or receipt.get("parent_id") != parent_id
            or receipt.get("parent_alias") != alias
            or receipt.get("buyer") != "REGISTERED_PARENT"):
        raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
    status = receipt.get("status")
    if status not in {"ADMITTED", "REFUSED"} or body.get("status") != status:
        raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
    if receipt.get("clock") != episode.get("clock"):
        raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
    return status


def _purchase_source_expected(receipt: Mapping[str, Any], operation_id: str,
                              parent_id: str) -> str:
    return digest({
        "schema": PURCHASE_RECEIPT_SCHEMA,
        "operation_id": operation_id,
        "parent_id": parent_id,
        "owner_actor_id": receipt.get("owner_actor_id"),
        "object_id": receipt.get("object_id"),
        "unit_price": receipt.get("unit_price"),
        "market_source": receipt.get("market_source_before"),
        "parent_before": receipt.get("parent_material_source_before"),
        "parent_after": receipt.get("parent_material_source_after"),
    })


def read_purchase(session, parent_id: str, operation_id: str, *,
                  as_actor: str | None) -> dict:
    if as_actor != parent_id:
        raise RecursionRefusal("PARENT_SELF_READ_REQUIRED")
    registration = read_supporting_actor(session, parent_id)
    alias = registration["alias"]
    episodes = _purchase_episodes(session, alias, operation_id)
    if len(episodes) != 1:
        raise RecursionRefusal("PURCHASE_NOT_FOUND")
    receipt = dict((episodes[0].get("body") or {}).get("receipt") or {})
    status = _purchase_read_provenance(
        session, episodes[0], receipt, parent_id=parent_id, alias=alias,
        operation_id=operation_id)
    market = read_market_inventory(session)
    owned = read_owned_objects(session)
    acquisition = next(
        (row for row in owned.get("objects") or []
         if row.get("acquisition_id") == operation_id), None)
    if status == "ADMITTED":
        if acquisition is None:
            raise RecursionRefusal("PURCHASE_READ_STALE")
        holder = session.world().actor_state.get("A", {}).get("actor_id")
        if receipt.get("owner_actor_id") not in (holder, parent_id):
            raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
        expected_source = _purchase_source_expected(receipt, operation_id, parent_id)
        if receipt.get("purchase_source") != expected_source:
            raise RecursionRefusal("PURCHASE_READ_PROVENANCE_MISMATCH")
        if (acquisition.get("purchase_source") != receipt.get("purchase_source")
                or acquisition.get("market_source") != receipt.get("market_source_before")
                or acquisition.get("object_id") != receipt.get("object_id")
                or acquisition.get("owner_actor_id") != receipt.get("owner_actor_id")
                or acquisition.get("unit_price") != receipt.get("unit_price")
                or acquisition.get("currency_unit") != receipt.get("currency_unit")):
            raise RecursionRefusal("PURCHASE_READ_STALE")
    elif acquisition is not None:
        raise RecursionRefusal("PURCHASE_READ_STALE")
    material = None
    parent_status = "READ"
    parent_error = None
    try:
        material = _read_material(session, parent_id=parent_id, as_actor=parent_id)
    except RecursionRefusal as exc:
        parent_status = "REFUSED:" + str(exc)
        parent_error = exc
    if status == "ADMITTED" and material is None:
        raise RecursionRefusal("PURCHASE_READ_PARENT_MISMATCH") from parent_error
    feasible = None
    feasible_status = "READ"
    try:
        feasible = parent_feasible_actions(
            session, parent_id, as_actor=parent_id)
    except RecursionRefusal as exc:
        feasible_status = "REFUSED:" + str(exc)
    if material is None:
        historical = None
    elif receipt.get("status") == "ADMITTED":
        historical = (
            material["source"] != receipt.get("parent_material_source_after")
            or market["source"] != receipt.get("market_source_after")
            or owned["source"] != receipt.get("owned_source_after"))
    else:
        historical = (
            material["source"] != receipt.get("parent_material_source_before")
            or market["source"] != receipt.get("market_source_before")
            or owned["source"] != receipt.get("owned_source_before"))
    return {
        "schema": PURCHASE_RECEIPT_SCHEMA,
        "grade": GRADE,
        "status": "READ",
        "operation_id": operation_id,
        "historical": historical,
        "receipt": receipt,
        "parent_material": material,
        "parent_material_status": parent_status,
        "parent_feasible_actions": feasible,
        "parent_feasible_actions_status": feasible_status,
        "parent_material_source": material["source"] if material else None,
        "market_source": market["source"],
        "owned_source": owned["source"],
        "owned_totals": owned["totals"],
        "purchase_is_typed": True,
        "purchase_history_hook": (
            "C02_PARENT_HISTORY_KIND_PENDING" if parent_status != "READ"
            else "C02_PARENT_HISTORY_READ"),
        "read_boundary": detached(READ_BOUNDARY),
    }


__all__ = [
    "MARKET_SLOT", "OWNED_SLOT", "MARKET_SCHEMA", "MARKET_READ_SCHEMA",
    "OWNED_SCHEMA", "OWNED_READ_SCHEMA", "PURCHASE_RECEIPT_SCHEMA",
    "PURCHASE_KIND", "GRADE", "FIXTURE_GRADE", "CURRENCY", "PURCHASE_HOURS",
    "default_market_items", "establish_market_inventory",
    "read_market_inventory", "read_owned_objects", "purchase_drum_kit",
    "read_purchase",
]
