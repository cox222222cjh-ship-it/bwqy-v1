from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .npc_shop_drop_query import build_npc_shop_drop_index, query_npc_or_item
from .query_service import ItemQueryIndex, build_item_query_index, query_item
from .quest_query import (
    QuestQueryIndex,
    QuestQueryResult,
    build_quest_query_index,
    query_quest,
)
from .types import ItemQueryResult, NpcShopDropQueryResult

UnifiedDomain = Literal["item", "npc", "quest"]
UnifiedStatus = Literal["exact_match", "ambiguous", "not_found"]
_ALLOWED_DOMAIN_HINTS = {"item", "npc", "quest"}


@dataclass(frozen=True)
class UnifiedQueryRequest:
    raw_query: str
    domain_hint: str | None = None


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
    domain_hint: str | None = None,
) -> UnifiedQueryResponse:
    request = UnifiedQueryRequest(raw_query=raw_query, domain_hint=domain_hint)
    validation_error = _validate_domain_hint(request)
    if validation_error is not None:
        return validation_error

    if request.domain_hint is not None:
        return _route_with_domain_hint(index, request)
    return _route_without_domain_hint(index, request)


def _validate_domain_hint(request: UnifiedQueryRequest) -> UnifiedQueryResponse | None:
    if request.domain_hint is None:
        return None

    if request.domain_hint in _ALLOWED_DOMAIN_HINTS:
        return None

    return UnifiedQueryResponse(
        query=request.raw_query.strip(),
        domain=None,
        status="ambiguous",
        primary_payload=None,
        notes=[
            "无效的 domain_hint；仅支持 item、npc、quest。",
        ],
    )


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
    item_response = _normalize_item_result(query_item(index.item_index, q))
    npc_response = _normalize_npc_result(query_npc_or_item(index.npc_index, q))
    quest_response = _normalize_quest_result(query_quest(index.quest_index, q))

    if npc_response.status == "ambiguous" and npc_response.domain is None:
        return npc_response

    matched_by_domain: dict[UnifiedDomain, list[UnifiedQueryResponse]] = {}
    for response in (item_response, npc_response, quest_response):
        if response.status == "not_found" or response.domain is None:
            continue
        matched_by_domain.setdefault(response.domain, []).append(response)

    if not matched_by_domain:
        return UnifiedQueryResponse(
            query=q,
            domain=None,
            status="not_found",
            primary_payload=None,
            notes=["未在 Item / NPC / Quest 白名单域中找到匹配结果。"],
        )

    exact_by_domain = {
        domain: _pick_preferred_response(responses, "exact_match")
        for domain, responses in matched_by_domain.items()
        if any(response.status == "exact_match" for response in responses)
    }
    ambiguous_by_domain = {
        domain: _pick_preferred_response(responses, "ambiguous")
        for domain, responses in matched_by_domain.items()
        if any(response.status == "ambiguous" for response in responses)
    }

    if len(exact_by_domain) == 1 and not ambiguous_by_domain:
        return next(iter(exact_by_domain.values()))

    if not exact_by_domain and len(ambiguous_by_domain) == 1:
        return next(iter(ambiguous_by_domain.values()))

    candidate_domains = sorted({*exact_by_domain.keys(), *ambiguous_by_domain.keys()})
    return UnifiedQueryResponse(
        query=q,
        domain=None,
        status="ambiguous",
        primary_payload=None,
        notes=[
            "该查询同时命中多个运营主域；请显式指定 domain_hint=item|npc|quest 以消除歧义。",
            f"候选域: {', '.join(candidate_domains)}",
        ],
    )


def _pick_preferred_response(
    responses: list[UnifiedQueryResponse],
    status: UnifiedStatus,
) -> UnifiedQueryResponse:
    filtered = [response for response in responses if response.status == status]
    for response in filtered:
        if response.domain == "item" and _is_canonical_item_response(response):
            return response
    return filtered[0]


def _is_canonical_item_response(response: UnifiedQueryResponse) -> bool:
    if response.primary_payload is None or response.primary_payload.result is None:
        return False
    return isinstance(response.primary_payload.result, ItemQueryResult)


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
