from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .npc_shop_drop_query import build_npc_shop_drop_index, query_npc_or_item
from .query_service import build_item_query_index, query_item
from .quest_query import (
    QuestQueryIndex,
    QuestQueryResult,
    build_quest_query_index,
    query_quest,
)
from .query_service import ItemQueryIndex
from .types import ItemQueryResult, NpcShopDropQueryResult

UnifiedDomain = Literal["item", "npc", "quest"]
UnifiedStatus = Literal["exact_match", "ambiguous", "not_found"]


@dataclass(frozen=True)
class UnifiedQueryRequest:
    raw_query: str
    domain_hint: UnifiedDomain | None = None


@dataclass(frozen=True)
class UnifiedQueryPayload:
    record: object | None
    result: object | None


@dataclass(frozen=True)
class UnifiedQueryResponse:
    query: str
    domain: UnifiedDomain | None
    status: UnifiedStatus
    primary_payload: UnifiedQueryPayload | None
    notes: list[str]


@dataclass(frozen=True)
class UnifiedQueryRouterIndex:
    item_index: ItemQueryIndex
    npc_index: ItemQueryIndex
    quest_index: QuestQueryIndex


def build_unified_query_router_index() -> UnifiedQueryRouterIndex:
    return UnifiedQueryRouterIndex(
        item_index=build_item_query_index(),
        npc_index=build_npc_shop_drop_index(),
        quest_index=build_quest_query_index(),
    )


def route_operator_query(
    index: UnifiedQueryRouterIndex,
    raw_query: str,
    domain_hint: UnifiedDomain | None = None,
) -> UnifiedQueryResponse:
    request = UnifiedQueryRequest(raw_query=raw_query, domain_hint=domain_hint)
    if request.domain_hint is not None:
        return _route_with_domain_hint(index, request)
    return _route_without_domain_hint(index, request)


def _route_with_domain_hint(
    index: UnifiedQueryRouterIndex,
    request: UnifiedQueryRequest,
) -> UnifiedQueryResponse:
    if request.domain_hint == "item":
        return _normalize_item_result(query_item(index.item_index, request.raw_query))
    if request.domain_hint == "npc":
        return _normalize_npc_result(query_npc_or_item(index.npc_index, request.raw_query))
    return _normalize_quest_result(query_quest(index.quest_index, request.raw_query))


def _route_without_domain_hint(
    index: UnifiedQueryRouterIndex,
    request: UnifiedQueryRequest,
) -> UnifiedQueryResponse:
    q = request.raw_query.strip()
    item_result = query_item(index.item_index, q)
    npc_result = query_npc_or_item(index.npc_index, q)
    quest_result = query_quest(index.quest_index, q)

    candidates: list[UnifiedQueryResponse] = []
    candidate_notes: list[str] = []

    item_response = _normalize_item_result(item_result)
    if item_response.status != "not_found":
        candidates.append(item_response)

    npc_response = _normalize_npc_result(npc_result)
    if npc_response.status == "ambiguous":
        return npc_response
    if npc_response.status != "not_found":
        candidates.append(npc_response)

    quest_response = _normalize_quest_result(quest_result)
    if quest_response.status != "not_found":
        candidates.append(quest_response)

    if not candidates:
        return UnifiedQueryResponse(
            query=q,
            domain=None,
            status="not_found",
            primary_payload=None,
            notes=["未在 Item / NPC / Quest 白名单域中找到匹配结果。"],
        )

    exact_candidates = [candidate for candidate in candidates if candidate.status == "exact_match"]
    if len(exact_candidates) == 1:
        return exact_candidates[0]

    domains = [candidate.domain for candidate in exact_candidates if candidate.domain]
    if domains:
        candidate_notes.append(
            "该查询同时命中多个运营主域；请显式指定 domain_hint=item|npc|quest 以消除歧义。"
        )
        candidate_notes.append(f"候选域: {', '.join(domains)}")

    return UnifiedQueryResponse(
        query=q,
        domain=None,
        status="ambiguous",
        primary_payload=None,
        notes=candidate_notes,
    )


def _normalize_item_result(result: ItemQueryResult) -> UnifiedQueryResponse:
    if result.matched_items:
        return UnifiedQueryResponse(
            query=result.query,
            domain="item",
            status="exact_match",
            primary_payload=UnifiedQueryPayload(
                record=result.matched_items[0],
                result=result,
            ),
            notes=[],
        )

    if result.candidates:
        return UnifiedQueryResponse(
            query=result.query,
            domain="item",
            status="ambiguous",
            primary_payload=UnifiedQueryPayload(record=None, result=result),
            notes=[f"Item 名称命中 {len(result.candidates)} 个候选，请改用更精确名称或 TID。"],
        )

    return UnifiedQueryResponse(
        query=result.query,
        domain="item",
        status="not_found",
        primary_payload=None,
        notes=[],
    )


def _normalize_npc_result(result: NpcShopDropQueryResult) -> UnifiedQueryResponse:
    if result.query_kind == "ambiguous":
        return UnifiedQueryResponse(
            query=result.query,
            domain=None,
            status="ambiguous",
            primary_payload=None,
            notes=[result.note] if result.note else [],
        )

    if result.query_kind == "unknown":
        return UnifiedQueryResponse(
            query=result.query,
            domain="npc",
            status="not_found",
            primary_payload=None,
            notes=[],
        )

    owner_record = result.sections[0].owner_record if result.sections else None
    domain: UnifiedDomain = "npc" if result.query_kind == "npc" else "item"
    return UnifiedQueryResponse(
        query=result.query,
        domain=domain,
        status="exact_match",
        primary_payload=UnifiedQueryPayload(record=owner_record, result=result),
        notes=[result.note] if result.note else [],
    )


def _normalize_quest_result(result: QuestQueryResult) -> UnifiedQueryResponse:
    if result.status == "ok":
        return UnifiedQueryResponse(
            query=result.query,
            domain="quest",
            status="exact_match",
            primary_payload=UnifiedQueryPayload(record=result.quest, result=result),
            notes=result.notes,
        )
    if result.status == "ambiguous":
        return UnifiedQueryResponse(
            query=result.query,
            domain="quest",
            status="ambiguous",
            primary_payload=UnifiedQueryPayload(record=None, result=result),
            notes=result.notes,
        )
    return UnifiedQueryResponse(
        query=result.query,
        domain="quest",
        status="not_found",
        primary_payload=None,
        notes=result.notes,
    )
