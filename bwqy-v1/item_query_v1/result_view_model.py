from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .types import ItemQueryResult, RawRecord, TraceValue, ValueStatus


@dataclass(frozen=True)
class FieldDisplayItem:
    """面向展示的字段项，保留来源与可信状态。"""

    key: str
    label: str
    value: str
    source_table: str
    source_field: str
    status: ValueStatus
    note: str | None = None


@dataclass(frozen=True)
class SectionModel:
    name: Literal[
        "basic_information",
        "classification",
        "source_information",
        "trust_status",
        "equipment_chain",
    ]
    fields: list[FieldDisplayItem]


@dataclass(frozen=True)
class EquipmentChainSectionModel:
    section: SectionModel
    state: Literal["available", "not_applicable", "empty"]
    set_records: list[RawRecord]
    set_ability_records: list[RawRecord]


@dataclass(frozen=True)
class ItemResultPageModel:
    query: str
    query_type: Literal["item_id", "item_name"]
    basic_information: SectionModel
    classification: SectionModel
    source_information: SectionModel
    trust_status: SectionModel
    equipment_chain: EquipmentChainSectionModel


@dataclass(frozen=True)
class CandidateResultModel:
    query: str
    query_type: Literal["item_id", "item_name"]
    candidates: list[ItemResultPageModel]


ResultViewModel = ItemResultPageModel | CandidateResultModel

_BASIC_FIELDS: list[tuple[str, str]] = [
    ("TID", "物品ID"),
    ("LocalName", "物品名称"),
    ("EngName", "英文键"),
    ("Level", "Level（待确认含义）"),
    ("Grade", "Grade（待确认含义）"),
    ("LocalDesc", "物品描述"),
]

_CLASSIFICATION_FIELDS: list[tuple[str, str]] = [
    ("Type", "Type"),
    ("Kind", "Kind"),
    ("Property", "Property"),
]


def build_result_view_model(raw_result: ItemQueryResult) -> ResultViewModel:
    if raw_result.matched_items:
        return _build_item_page(
            raw_result, raw_result.matched_items[0], raw_result.set_chain
        )

    candidate_pages = [
        _build_item_page(
            raw_result, candidate, {"ItemSetTable": [], "ItemSetAbilityTable": []}
        )
        for candidate in raw_result.candidates
    ]
    return CandidateResultModel(
        query=raw_result.query,
        query_type=raw_result.query_type,
        candidates=candidate_pages,
    )


def _build_item_page(
    raw_result: ItemQueryResult,
    item_record: RawRecord,
    set_chain: dict[str, list[RawRecord]],
) -> ItemResultPageModel:
    basic_fields = [
        _map_existing_field(item_record, key, label) for key, label in _BASIC_FIELDS
    ]

    classification_fields = [
        _map_existing_field(item_record, key, label)
        for key, label in _CLASSIFICATION_FIELDS
    ]
    is_equipment = _derive_is_equipment(item_record)
    classification_fields.append(is_equipment)
    classification_fields.append(
        FieldDisplayItem(
            key="category_name_zh",
            label="category_name_zh",
            value="待确认",
            source_table="ItemTable",
            source_field="Type|Kind|Property",
            status="pending_confirmation",
            note="缺少可验证编码字典，不能将中文分类名当作确定值。",
        )
    )

    displayed = [*basic_fields, *classification_fields]
    source_fields = [
        FieldDisplayItem(
            key=f"{field.key}_source",
            label=field.key,
            value=f"{field.source_table}.{field.source_field}",
            source_table=field.source_table,
            source_field=field.source_field,
            status=field.status,
            note=field.note,
        )
        for field in displayed
    ]

    trust_fields = [
        FieldDisplayItem(
            key=f"{field.key}_trust",
            label=field.key,
            value=field.status,
            source_table=field.source_table,
            source_field=field.source_field,
            status=field.status,
            note=field.note,
        )
        for field in displayed
    ]

    equipment_section = _build_equipment_chain_section(is_equipment, set_chain)

    return ItemResultPageModel(
        query=raw_result.query,
        query_type=raw_result.query_type,
        basic_information=SectionModel(name="basic_information", fields=basic_fields),
        classification=SectionModel(
            name="classification", fields=classification_fields
        ),
        source_information=SectionModel(
            name="source_information", fields=source_fields
        ),
        trust_status=SectionModel(name="trust_status", fields=trust_fields),
        equipment_chain=equipment_section,
    )


def _build_equipment_chain_section(
    is_equipment: FieldDisplayItem,
    set_chain: dict[str, list[RawRecord]],
) -> EquipmentChainSectionModel:
    set_records = set_chain.get("ItemSetTable", [])
    set_ability_records = set_chain.get("ItemSetAbilityTable", [])

    if is_equipment.value == "非装备或未知":
        fields = [
            FieldDisplayItem(
                key="equipment_chain_state",
                label="装备链路状态",
                value="不适用",
                source_table=is_equipment.source_table,
                source_field=is_equipment.source_field,
                status=is_equipment.status,
                note="依据 v1 装备判定规则。",
            )
        ]
        return EquipmentChainSectionModel(
            section=SectionModel(name="equipment_chain", fields=fields),
            state="not_applicable",
            set_records=[],
            set_ability_records=[],
        )

    if set_records or set_ability_records:
        fields = [
            FieldDisplayItem(
                key="set_chain_rows",
                label="套装链路记录数",
                value=str(len(set_records)),
                source_table="ItemSetTable",
                source_field="TID|ItemTID|SetAbilityTID",
                status="direct",
            ),
            FieldDisplayItem(
                key="set_ability_rows",
                label="套装效果记录数",
                value=str(len(set_ability_records)),
                source_table="ItemSetAbilityTable",
                source_field="TID|ReqTotal|LocalDesc",
                status="direct",
            ),
        ]
        return EquipmentChainSectionModel(
            section=SectionModel(name="equipment_chain", fields=fields),
            state="available",
            set_records=set_records,
            set_ability_records=set_ability_records,
        )

    fields = [
        FieldDisplayItem(
            key="equipment_chain_state",
            label="装备链路状态",
            value="无可用套装链路",
            source_table="ItemSetTable",
            source_field="TID|ItemTID|SetAbilityTID",
            status="pending_confirmation",
            note="当前物品被判定为可能装备，但未命中最小套装链路数据。",
        )
    ]
    return EquipmentChainSectionModel(
        section=SectionModel(name="equipment_chain", fields=fields),
        state="empty",
        set_records=[],
        set_ability_records=[],
    )


def _map_existing_field(
    item_record: RawRecord, key: str, label: str
) -> FieldDisplayItem:
    trace = item_record.values.get(key) or _missing_trace(key)
    return FieldDisplayItem(
        key=key,
        label=label,
        value=trace.raw_value,
        source_table=trace.source_table,
        source_field=trace.source_field,
        status=trace.status,
        note=trace.note,
    )


def _missing_trace(field: str) -> TraceValue:
    return TraceValue(
        source_table="ItemTable",
        source_field=field,
        raw_value="",
        status="pending_confirmation",
        note="字段缺失，待确认。",
    )


def _derive_is_equipment(item_record: RawRecord) -> FieldDisplayItem:
    set_tid = _raw(item_record, "SetTID")
    stat_fields = ["AP", "DP", "BP", "CP"]
    has_stat = any(
        _is_nonzero_numeric(_raw(item_record, field)) for field in stat_fields
    )
    has_set = _is_positive_integer(set_tid)

    if has_set or has_stat:
        value = "可能是装备"
    else:
        value = "非装备或未知"

    return FieldDisplayItem(
        key="is_equipment",
        label="是否装备（推断）",
        value=value,
        source_table="ItemTable",
        source_field="SetTID|AP|DP|BP|CP",
        status="derived",
        note="依据 v1 规则：SetTID>0 或 AP/DP/BP/CP 任一非 0。",
    )


def _raw(item_record: RawRecord, field: str) -> str:
    trace = item_record.values.get(field)
    if not trace:
        return ""
    return trace.raw_value.strip()


def _is_positive_integer(value: str) -> bool:
    try:
        return int(value) > 0
    except ValueError:
        return False


def _is_nonzero_numeric(value: str) -> bool:
    if not value:
        return False
    try:
        return float(value) != 0
    except ValueError:
        return False
