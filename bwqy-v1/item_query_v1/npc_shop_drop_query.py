from __future__ import annotations

from dataclasses import dataclass

from .csv_loader import NPC_DROP_SHOP_TABLES, load_selected_tables, resolve_tables_dir
from .query_service import ItemQueryIndex, _to_raw_record
from .types import (
    NpcItemRelationRecord,
    NpcShopDropQueryResult,
    NpcShopDropSection,
    RawRecord,
    TraceValue,
)

_DROP_ITEM_FIELDS = [f"DropItem{i:02d}" for i in range(1, 16)]


def build_npc_shop_drop_index() -> ItemQueryIndex:
    tables = load_selected_tables(
        NPC_DROP_SHOP_TABLES, tables_dir=resolve_tables_dir()
    )

    item_by_tid: dict[str, dict[str, str]] = {}
    item_by_local_name: dict[str, list[dict[str, str]]] = {}

    for row in tables["ItemTable"]:
        tid = row.get("TID", "").strip()
        if tid:
            item_by_tid[tid] = row

        local_name = row.get("LocalName", "").strip()
        if local_name:
            item_by_local_name.setdefault(local_name, []).append(row)

    npc_by_tid: dict[str, dict[str, str]] = {}
    npc_by_local_name: dict[str, list[dict[str, str]]] = {}
    for row in tables["NpcTable"]:
        tid = row.get("TID", "").strip()
        if tid:
            npc_by_tid[tid] = row

        local_name = row.get("LocalName", "").strip()
        if local_name:
            npc_by_local_name.setdefault(local_name, []).append(row)

    sale_items_by_sale_tid: dict[str, list[dict[str, str]]] = {}
    for row in tables["SaleTable"]:
        sale_tid = row.get("SaleTID", "").strip()
        if sale_tid:
            sale_items_by_sale_tid.setdefault(sale_tid, []).append(row)

    drop_rows_by_tid = {
        row["TID"].strip(): row
        for row in tables["ItemDropTable"]
        if row.get("TID", "").strip()
    }

    return ItemQueryIndex(
        tables=tables,
        by_tid=item_by_tid,
        by_local_name=item_by_local_name,
        by_eng_name={},
        item_set_by_tid={},
        set_ability_by_tid={},
        npc_by_tid=npc_by_tid,
        npc_by_local_name=npc_by_local_name,
        sale_items_by_sale_tid=sale_items_by_sale_tid,
        drop_rows_by_tid=drop_rows_by_tid,
    )


def query_npc_or_item(index: ItemQueryIndex, query: str) -> NpcShopDropQueryResult:
    q = query.strip()
    if not q:
        return NpcShopDropQueryResult(query=query, query_kind="unknown", sections=[])

    npc_rows = _match_entities(
        query=q,
        by_tid=index.npc_by_tid,
        by_name=index.npc_by_local_name,
    )
    item_rows = _match_entities(
        query=q,
        by_tid=index.by_tid,
        by_name=index.by_local_name,
    )

    if q.isdigit() and npc_rows and item_rows:
        return NpcShopDropQueryResult(
            query=q,
            query_kind="ambiguous",
            sections=[],
            note="该纯数字输入同时命中 NPC TID 与 Item TID；请改用名称或更明确的对象上下文重新查询。",
        )

    if npc_rows:
        sections = []
        for npc_row in npc_rows:
            sections.extend(_build_npc_sections(index, npc_row))
        return NpcShopDropQueryResult(query=q, query_kind="npc", sections=sections)

    if item_rows:
        sections = []
        for item_row in item_rows:
            sections.extend(_build_item_sections(index, item_row))
        return NpcShopDropQueryResult(query=q, query_kind="item", sections=sections)

    return NpcShopDropQueryResult(query=q, query_kind="unknown", sections=[])


def _match_entities(
    query: str,
    by_tid: dict[str, dict[str, str]],
    by_name: dict[str, list[dict[str, str]]],
) -> list[dict[str, str]]:
    if query.isdigit():
        row = by_tid.get(query)
        return [row] if row else []

    return by_name.get(query, [])


def _build_npc_sections(
    index: ItemQueryIndex, npc_row: dict[str, str]
) -> list[NpcShopDropSection]:
    npc_record = _to_raw_record("NpcTable", npc_row)
    sections: list[NpcShopDropSection] = []
    sections.append(
        NpcShopDropSection(
            relation_type="shop",
            owner_record=npc_record,
            related_records=_collect_shop_relations(index, npc_row),
        )
    )
    sections.append(
        NpcShopDropSection(
            relation_type="drop",
            owner_record=npc_record,
            related_records=_collect_drop_relations(index, npc_row),
        )
    )
    return sections


def _build_item_sections(
    index: ItemQueryIndex, item_row: dict[str, str]
) -> list[NpcShopDropSection]:
    item_record = _to_raw_record("ItemTable", item_row)
    sections = [
        NpcShopDropSection(
            relation_type="shop",
            owner_record=item_record,
            related_records=_reverse_shop_relations(index, item_row),
        ),
        NpcShopDropSection(
            relation_type="drop",
            owner_record=item_record,
            related_records=_reverse_drop_relations(index, item_row),
        ),
    ]
    return sections


def _collect_shop_relations(
    index: ItemQueryIndex,
    npc_row: dict[str, str],
) -> list[NpcItemRelationRecord]:
    sale_tid = npc_row.get("SaleTID", "").strip()
    if not _is_valid_link_id(sale_tid):
        return []

    related: list[NpcItemRelationRecord] = []
    for sale_row in index.sale_items_by_sale_tid.get(sale_tid, []):
        item_tid = sale_row.get("ItemTID", "").strip()
        item_row = index.by_tid.get(item_tid)
        if not item_row:
            continue
        related.append(
            NpcItemRelationRecord(
                relation_type="shop",
                npc_record=_to_raw_record("NpcTable", npc_row),
                item_record=_to_raw_record("ItemTable", item_row),
                source_path="NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID",
                trace_records=[
                    _trace_only_record("NpcTable", "SaleTID", sale_tid),
                    _to_raw_record("SaleTable", sale_row),
                ],
                status="direct",
            )
        )
    return related


def _collect_drop_relations(
    index: ItemQueryIndex,
    npc_row: dict[str, str],
) -> list[NpcItemRelationRecord]:
    drop_tid = npc_row.get("ItemDropTID", "").strip()
    if not _is_valid_link_id(drop_tid):
        return []

    drop_row = index.drop_rows_by_tid.get(drop_tid)
    if not drop_row:
        return []

    related: list[NpcItemRelationRecord] = []
    for field in _DROP_ITEM_FIELDS:
        item_tid = drop_row.get(field, "").strip()
        if not _is_valid_link_id(item_tid):
            continue
        item_row = index.by_tid.get(item_tid)
        if not item_row:
            continue
        related.append(
            NpcItemRelationRecord(
                relation_type="drop",
                npc_record=_to_raw_record("NpcTable", npc_row),
                item_record=_to_raw_record("ItemTable", item_row),
                source_path=f"NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.{field} -> ItemTable.TID",
                trace_records=[
                    _trace_only_record("NpcTable", "ItemDropTID", drop_tid),
                    _trace_only_record("ItemDropTable", field, item_tid),
                    _to_raw_record("ItemDropTable", drop_row),
                ],
                status="direct",
            )
        )
    return related


def _reverse_shop_relations(
    index: ItemQueryIndex,
    item_row: dict[str, str],
) -> list[NpcItemRelationRecord]:
    item_tid = item_row.get("TID", "").strip()
    related: list[NpcItemRelationRecord] = []
    for npc_row in index.npc_by_tid.values():
        sale_tid = npc_row.get("SaleTID", "").strip()
        if not _is_valid_link_id(sale_tid):
            continue
        for sale_row in index.sale_items_by_sale_tid.get(sale_tid, []):
            if sale_row.get("ItemTID", "").strip() != item_tid:
                continue
            related.append(
                NpcItemRelationRecord(
                    relation_type="shop",
                    npc_record=_to_raw_record("NpcTable", npc_row),
                    item_record=_to_raw_record("ItemTable", item_row),
                    source_path="NpcTable.SaleTID -> SaleTable.SaleTID -> SaleTable.ItemTID -> ItemTable.TID",
                    trace_records=[
                        _trace_only_record("NpcTable", "SaleTID", sale_tid),
                        _to_raw_record("SaleTable", sale_row),
                    ],
                    status="direct",
                )
            )
    return related


def _reverse_drop_relations(
    index: ItemQueryIndex,
    item_row: dict[str, str],
) -> list[NpcItemRelationRecord]:
    item_tid = item_row.get("TID", "").strip()
    related: list[NpcItemRelationRecord] = []
    for npc_row in index.npc_by_tid.values():
        drop_tid = npc_row.get("ItemDropTID", "").strip()
        if not _is_valid_link_id(drop_tid):
            continue
        drop_row = index.drop_rows_by_tid.get(drop_tid)
        if not drop_row:
            continue
        for field in _DROP_ITEM_FIELDS:
            if drop_row.get(field, "").strip() != item_tid:
                continue
            related.append(
                NpcItemRelationRecord(
                    relation_type="drop",
                    npc_record=_to_raw_record("NpcTable", npc_row),
                    item_record=_to_raw_record("ItemTable", item_row),
                    source_path=f"NpcTable.ItemDropTID -> ItemDropTable.TID -> ItemDropTable.{field} -> ItemTable.TID",
                    trace_records=[
                        _trace_only_record("NpcTable", "ItemDropTID", drop_tid),
                        _trace_only_record("ItemDropTable", field, item_tid),
                        _to_raw_record("ItemDropTable", drop_row),
                    ],
                    status="direct",
                )
            )
    return related


def _trace_only_record(table: str, field: str, value: str) -> RawRecord:
    return RawRecord(
        table=table,
        values={
            field: TraceValue(
                source_table=table,
                source_field=field,
                raw_value=value,
                status="direct",
            )
        },
    )


def _is_valid_link_id(value: str) -> bool:
    stripped = value.strip()
    return bool(stripped and stripped != "0")
