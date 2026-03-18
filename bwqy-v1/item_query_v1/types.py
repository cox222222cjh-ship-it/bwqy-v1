from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

ValueStatus = Literal["direct", "derived", "pending_confirmation"]


@dataclass(frozen=True)
class TraceValue:
    """可追溯的字段值表示。"""

    source_table: str
    source_field: str
    raw_value: str
    status: ValueStatus
    note: str | None = None


@dataclass(frozen=True)
class RawRecord:
    """保留原始行内容，便于后续 UI 层做二次映射。"""

    table: str
    values: dict[str, TraceValue]


@dataclass(frozen=True)
class ItemQueryResult:
    """Task 3 的稳定查询结果结构。"""

    query: str
    query_type: Literal["item_id", "item_name"]
    matched_items: list[RawRecord]
    candidates: list[RawRecord]
    set_chain: dict[str, list[RawRecord]]


@dataclass(frozen=True)
class NpcItemRelationRecord:
    relation_type: Literal["drop", "shop"]
    npc_record: RawRecord
    item_record: RawRecord
    source_path: str
    trace_records: list[RawRecord]
    status: ValueStatus
    note: str | None = None


@dataclass(frozen=True)
class NpcShopDropSection:
    relation_type: Literal["drop", "shop"]
    owner_record: RawRecord
    related_records: list[NpcItemRelationRecord]


@dataclass(frozen=True)
class NpcShopDropQueryResult:
    query: str
    query_kind: Literal["npc", "item", "unknown", "ambiguous"]
    sections: list[NpcShopDropSection]
    note: str | None = None
