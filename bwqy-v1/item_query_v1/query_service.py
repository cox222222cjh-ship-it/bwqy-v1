from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import Iterable

from .csv_loader import load_allowed_tables, resolve_tables_dir
from .types import ItemQueryResult, RawRecord, TraceValue


@dataclass
class ItemQueryIndex:
    tables: dict[str, list[dict[str, str]]]
    by_tid: dict[str, dict[str, str]]
    by_local_name: dict[str, list[dict[str, str]]]
    by_eng_name: dict[str, list[dict[str, str]]]
    item_set_by_tid: dict[str, dict[str, str]]
    set_ability_by_tid: dict[str, dict[str, str]]
    npc_by_tid: dict[str, dict[str, str]] = field(default_factory=dict)
    npc_by_local_name: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    sale_items_by_sale_tid: dict[str, list[dict[str, str]]] = field(default_factory=dict)
    drop_rows_by_tid: dict[str, dict[str, str]] = field(default_factory=dict)


def build_item_query_index() -> ItemQueryIndex:
    tables_dir = resolve_tables_dir()
    tables = load_allowed_tables(tables_dir)

    by_tid: dict[str, dict[str, str]] = {}
    by_local_name: dict[str, list[dict[str, str]]] = {}
    by_eng_name: dict[str, list[dict[str, str]]] = {}

    for row in tables["ItemTable"]:
        tid = row.get("TID", "").strip()
        if tid:
            by_tid[tid] = row

        local_name = row.get("LocalName", "").strip()
        if local_name:
            by_local_name.setdefault(local_name, []).append(row)

        eng_name = row.get("EngName", "").strip()
        if eng_name:
            by_eng_name.setdefault(eng_name, []).append(row)

    item_set_by_tid = {
        row["TID"].strip(): row
        for row in tables["ItemSetTable"]
        if row.get("TID", "").strip()
    }
    set_ability_by_tid = {
        row["TID"].strip(): row
        for row in tables["ItemSetAbilityTable"]
        if row.get("TID", "").strip()
    }

    return ItemQueryIndex(
        tables=tables,
        by_tid=by_tid,
        by_local_name=by_local_name,
        by_eng_name=by_eng_name,
        item_set_by_tid=item_set_by_tid,
        set_ability_by_tid=set_ability_by_tid,
    )


def _to_raw_record(table_name: str, row: dict[str, str]) -> RawRecord:
    values = {
        field: TraceValue(
            source_table=table_name,
            source_field=field,
            raw_value=value,
            status="direct",
        )
        for field, value in row.items()
    }
    return RawRecord(table=table_name, values=values)


def _empty_set_chain() -> dict[str, list[RawRecord]]:
    return {
        "ItemSetTable": [],
        "ItemSetAbilityTable": [],
    }


def _collect_set_chain_rows(index: ItemQueryIndex, item_rows: Iterable[dict[str, str]]) -> dict[str, list[RawRecord]]:
    set_rows: list[RawRecord] = []
    ability_rows: list[RawRecord] = []

    for item_row in item_rows:
        set_tid = item_row.get("SetTID", "").strip()
        if not set_tid or set_tid in {"0", ""}:
            continue

        set_row = index.item_set_by_tid.get(set_tid)
        if not set_row:
            continue

        set_rows.append(_to_raw_record("ItemSetTable", set_row))

        ability_tid_field = set_row.get("SetAbilityTID", "").strip()
        for ability_tid in [x.strip() for x in ability_tid_field.split("|") if x.strip()]:
            ability_row = index.set_ability_by_tid.get(ability_tid)
            if ability_row:
                ability_rows.append(_to_raw_record("ItemSetAbilityTable", ability_row))

    return {
        "ItemSetTable": set_rows,
        "ItemSetAbilityTable": ability_rows,
    }


def query_item(index: ItemQueryIndex, query: str) -> ItemQueryResult:
    q = query.strip()
    if not q:
        return ItemQueryResult(
            query=query,
            query_type="item_name",
            matched_items=[],
            candidates=[],
            set_chain=_empty_set_chain(),
        )

    if q.isdigit():
        item = index.by_tid.get(q)
        matched = [_to_raw_record("ItemTable", item)] if item else []
        chain = _collect_set_chain_rows(index, [item] if item else [])
        return ItemQueryResult(
            query=q,
            query_type="item_id",
            matched_items=matched,
            candidates=[],
            set_chain=chain,
        )

    local_matches = index.by_local_name.get(q, [])
    eng_matches = index.by_eng_name.get(q, [])
    merged = []
    seen_tid: set[str] = set()

    for row in [*local_matches, *eng_matches]:
        tid = row.get("TID", "")
        if tid in seen_tid:
            continue
        seen_tid.add(tid)
        merged.append(row)

    if len(merged) == 1:
        matched_records = [_to_raw_record("ItemTable", merged[0])]
        chain = _collect_set_chain_rows(index, merged)
        return ItemQueryResult(
            query=q,
            query_type="item_name",
            matched_items=matched_records,
            candidates=[],
            set_chain=chain,
        )

    candidates = [_to_raw_record("ItemTable", row) for row in merged]
    return ItemQueryResult(
        query=q,
        query_type="item_name",
        matched_items=[],
        candidates=candidates,
        set_chain=_empty_set_chain(),
    )
