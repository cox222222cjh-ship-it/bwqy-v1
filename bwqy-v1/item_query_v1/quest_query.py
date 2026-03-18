from __future__ import annotations

from dataclasses import dataclass

from .csv_loader import load_selected_tables, resolve_tables_dir

QUEST_V1_TABLES = {
    "QuestTable": "QuestTable.csv",
    "QuestMissionTable": "QuestMissionTable.csv",
    "QuestRewardTable": "QuestRewardTable.csv",
    "QuestDropTable": "QuestDropTable.csv",
    "ItemTable": "ItemTable.csv",
    "NpcTable": "NpcTable.csv",
}

CONFIRMED = "confirmed"
MISSING = "missing"
PENDING = "pending_confirmation"


@dataclass(frozen=True)
class QuestLink:
    tid: int
    name: str | None
    status: str


@dataclass(frozen=True)
class QuestGiveItem:
    slot: str
    item_tid: int
    item_name: str | None
    count: int
    status: str


@dataclass(frozen=True)
class QuestMissionRecord:
    mission_tid: int
    fields: dict[str, str]
    status: str


@dataclass(frozen=True)
class QuestRewardRecord:
    reward_tid: int
    type: str
    value: int
    count: int
    is_select: bool
    resolved_item_tid: int | None
    resolved_item_name: str | None
    status: str
    note: str | None = None


@dataclass(frozen=True)
class QuestDropRecord:
    quest_tid: int
    npc_tid: int
    npc_name: str | None
    item_tid: int
    item_name: str | None
    drop_rate: int
    drop_stack: int
    drop_all: bool
    status: str
    note: str | None = None


@dataclass(frozen=True)
class QuestSummary:
    tid: int
    name: str


@dataclass(frozen=True)
class QuestQueryPayload:
    tid: int
    name: str
    prev_quest: QuestLink
    next_quest: QuestLink
    give_items: list[QuestGiveItem]
    missions: list[QuestMissionRecord]
    rewards: list[QuestRewardRecord]
    quest_drops: list[QuestDropRecord]
    related_items: list[QuestSummary]
    related_npcs: list[QuestSummary]


@dataclass(frozen=True)
class QuestQueryResult:
    query: str
    domain: str
    status: str
    quest: QuestSummary | None
    candidates: list[QuestSummary]
    payload: QuestQueryPayload | None
    notes: list[str]


@dataclass
class QuestQueryIndex:
    quest_by_tid: dict[str, dict[str, str]]
    quests_by_name: dict[str, list[dict[str, str]]]
    mission_by_tid: dict[str, dict[str, str]]
    rewards_by_tid: dict[str, list[dict[str, str]]]
    drops_by_quest_tid: dict[str, list[dict[str, str]]]
    items_by_tid: dict[str, dict[str, str]]
    npcs_by_tid: dict[str, dict[str, str]]


def build_quest_query_index() -> QuestQueryIndex:
    tables = load_selected_tables(QUEST_V1_TABLES, resolve_tables_dir())

    quest_by_tid: dict[str, dict[str, str]] = {}
    quests_by_name: dict[str, list[dict[str, str]]] = {}
    for row in tables["QuestTable"]:
        tid = row.get("TID", "").strip()
        if tid:
            quest_by_tid[tid] = row
        name = _quest_name(row)
        if name:
            quests_by_name.setdefault(name, []).append(row)

    return QuestQueryIndex(
        quest_by_tid=quest_by_tid,
        quests_by_name=quests_by_name,
        mission_by_tid={row["TID"].strip(): row for row in tables["QuestMissionTable"] if row.get("TID", "").strip()},
        rewards_by_tid=_group_by(tables["QuestRewardTable"], "TID"),
        drops_by_quest_tid=_group_by(tables["QuestDropTable"], "QuestTID"),
        items_by_tid={row["TID"].strip(): row for row in tables["ItemTable"] if row.get("TID", "").strip()},
        npcs_by_tid={row["TID"].strip(): row for row in tables["NpcTable"] if row.get("TID", "").strip()},
    )


def query_quest(index: QuestQueryIndex, query: str) -> QuestQueryResult:
    q = query.strip()
    if not q:
        return QuestQueryResult(query=query, domain="quest", status="not_found", quest=None, candidates=[], payload=None, notes=[])

    matches = _match_quests(index, q)
    if not matches:
        return QuestQueryResult(query=q, domain="quest", status="not_found", quest=None, candidates=[], payload=None, notes=["未在 QuestTable 中找到匹配任务。"])

    if len(matches) > 1:
        candidates = [_to_summary(row) for row in matches]
        return QuestQueryResult(query=q, domain="quest", status="ambiguous", quest=None, candidates=candidates, payload=None, notes=["名称命中多个 Quest，请改用更精确的任务名或 TID。"])

    quest_row = matches[0]
    payload, notes = _build_payload(index, quest_row)
    return QuestQueryResult(
        query=q,
        domain="quest",
        status="ok",
        quest=QuestSummary(tid=int(quest_row["TID"]), name=_quest_name(quest_row) or quest_row["TID"]),
        candidates=[],
        payload=payload,
        notes=notes,
    )


def _match_quests(index: QuestQueryIndex, query: str) -> list[dict[str, str]]:
    if query.isdigit():
        row = index.quest_by_tid.get(query)
        return [row] if row else []
    return index.quests_by_name.get(query, [])


def _build_payload(index: QuestQueryIndex, quest_row: dict[str, str]) -> tuple[QuestQueryPayload, list[str]]:
    notes: list[str] = []
    quest_tid = int(quest_row["TID"])
    give_items = _resolve_give_items(index, quest_row)
    missions = _resolve_mission(index, quest_row)
    rewards = _resolve_rewards(index, quest_row)
    quest_drops, drop_note = _resolve_quest_drops(index, quest_row)
    if drop_note:
        notes.append(drop_note)

    payload = QuestQueryPayload(
        tid=quest_tid,
        name=_quest_name(quest_row) or str(quest_tid),
        prev_quest=_resolve_quest_link(index, quest_row, "PrevQuest"),
        next_quest=_resolve_quest_link(index, quest_row, "NextQuest"),
        give_items=give_items,
        missions=missions,
        rewards=rewards,
        quest_drops=quest_drops,
        related_items=_collect_related_items(give_items, rewards, quest_drops),
        related_npcs=_collect_related_npcs(quest_drops),
    )
    return payload, notes


def _resolve_quest_link(index: QuestQueryIndex, quest_row: dict[str, str], field: str) -> QuestLink:
    raw = quest_row.get(field, "").strip()
    if not _is_valid_link_id(raw):
        return QuestLink(tid=0, name=None, status=MISSING)
    linked = index.quest_by_tid.get(raw)
    if not linked:
        return QuestLink(tid=int(raw), name=None, status=MISSING)
    return QuestLink(tid=int(raw), name=_quest_name(linked), status=CONFIRMED)


def _resolve_give_items(index: QuestQueryIndex, quest_row: dict[str, str]) -> list[QuestGiveItem]:
    results: list[QuestGiveItem] = []
    for slot, count_field in (("GiveItem1", "GiveItemCnt1"), ("GiveItem2", "GiveItemCnt2")):
        raw = quest_row.get(slot, "").strip()
        if not _is_valid_link_id(raw):
            continue
        item_row = index.items_by_tid.get(raw)
        results.append(
            QuestGiveItem(
                slot=slot,
                item_tid=int(raw),
                item_name=item_row.get("LocalName", "").strip() or None if item_row else None,
                count=_to_int(quest_row.get(count_field, "0")),
                status=CONFIRMED if item_row else MISSING,
            )
        )
    return results


def _resolve_mission(index: QuestQueryIndex, quest_row: dict[str, str]) -> list[QuestMissionRecord]:
    mission_tid = quest_row.get("MissionTID", "").strip()
    if not _is_valid_link_id(mission_tid):
        return []
    mission_row = index.mission_by_tid.get(mission_tid)
    if not mission_row:
        return [QuestMissionRecord(mission_tid=int(mission_tid), fields={}, status=MISSING)]
    return [QuestMissionRecord(mission_tid=int(mission_tid), fields=mission_row, status=CONFIRMED)]


def _resolve_rewards(index: QuestQueryIndex, quest_row: dict[str, str]) -> list[QuestRewardRecord]:
    reward_tid = quest_row.get("RewardTID", "").strip()
    if not _is_valid_link_id(reward_tid):
        return []

    reward_rows = index.rewards_by_tid.get(reward_tid, [])
    if not reward_rows:
        return [QuestRewardRecord(reward_tid=int(reward_tid), type="", value=0, count=0, is_select=False, resolved_item_tid=None, resolved_item_name=None, status=MISSING, note=None)]

    records: list[QuestRewardRecord] = []
    for row in reward_rows:
        reward_type = row.get("Type", "").strip()
        value = _to_int(row.get("Value", "0"))
        item_row = index.items_by_tid.get(str(value)) if reward_type == "1" and value > 0 else None
        if reward_type == "1" and item_row:
            status = CONFIRMED
            resolved_item_tid = value
            resolved_item_name = item_row.get("LocalName", "").strip() or None
            note = None
        else:
            status = PENDING if reward_type else MISSING
            resolved_item_tid = None
            resolved_item_name = None
            note = "奖励值语义受 Type 影响，当前仅保留原始条目。" if reward_type else None
        records.append(
            QuestRewardRecord(
                reward_tid=_to_int(row.get("TID", reward_tid)),
                type=reward_type,
                value=value,
                count=_to_int(row.get("Count", "0")),
                is_select=row.get("IsSelect", "0").strip() == "1",
                resolved_item_tid=resolved_item_tid,
                resolved_item_name=resolved_item_name,
                status=status,
                note=note,
            )
        )
    return records


def _resolve_quest_drops(index: QuestQueryIndex, quest_row: dict[str, str]) -> tuple[list[QuestDropRecord], str | None]:
    quest_tid = quest_row.get("TID", "").strip()
    drop_rows = index.drops_by_quest_tid.get(quest_tid, [])
    note = None

    drop_tid = quest_row.get("DropTID", "").strip()
    if _is_valid_link_id(drop_tid) and drop_rows:
        if all(row.get("TID", "").strip() != drop_tid for row in drop_rows):
            note = "QuestTable.DropTID 未作为主事实来源；当前仅按 QuestDropTable.QuestTID 返回 quest-specific drop。"

    records: list[QuestDropRecord] = []
    for row in drop_rows:
        npc_tid = row.get("NpcTID", "").strip()
        item_tid = row.get("ItemTID", "").strip()
        npc_row = index.npcs_by_tid.get(npc_tid)
        item_row = index.items_by_tid.get(item_tid)
        status = CONFIRMED if npc_row and item_row else PENDING
        note_text = None if status == CONFIRMED else "QuestDrop 记录存在，但 NPC 或 Item 解释仍待确认。"
        records.append(
            QuestDropRecord(
                quest_tid=_to_int(row.get("QuestTID", "0")),
                npc_tid=_to_int(npc_tid),
                npc_name=npc_row.get("LocalName", "").strip() or None if npc_row else None,
                item_tid=_to_int(item_tid),
                item_name=item_row.get("LocalName", "").strip() or None if item_row else None,
                drop_rate=_to_int(row.get("DropRate", "0")),
                drop_stack=_to_int(row.get("DropStack", "0")),
                drop_all=row.get("DropAll", "0").strip() == "1",
                status=status,
                note=note_text,
            )
        )
    return records, note


def _collect_related_items(
    give_items: list[QuestGiveItem],
    rewards: list[QuestRewardRecord],
    quest_drops: list[QuestDropRecord],
) -> list[QuestSummary]:
    items: dict[int, QuestSummary] = {}
    for give_item in give_items:
        if give_item.item_name:
            items[give_item.item_tid] = QuestSummary(tid=give_item.item_tid, name=give_item.item_name)
    for reward in rewards:
        if reward.resolved_item_tid and reward.resolved_item_name:
            items[reward.resolved_item_tid] = QuestSummary(tid=reward.resolved_item_tid, name=reward.resolved_item_name)
    for drop in quest_drops:
        if drop.item_name:
            items[drop.item_tid] = QuestSummary(tid=drop.item_tid, name=drop.item_name)
    return list(items.values())


def _collect_related_npcs(quest_drops: list[QuestDropRecord]) -> list[QuestSummary]:
    npcs: dict[int, QuestSummary] = {}
    for drop in quest_drops:
        if drop.npc_name:
            npcs[drop.npc_tid] = QuestSummary(tid=drop.npc_tid, name=drop.npc_name)
    return list(npcs.values())


def _group_by(rows: list[dict[str, str]], field: str) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        value = row.get(field, "").strip()
        if value:
            grouped.setdefault(value, []).append(row)
    return grouped


def _quest_name(row: dict[str, str]) -> str:
    return row.get("LocalTitle", "").strip()


def _to_summary(row: dict[str, str]) -> QuestSummary:
    return QuestSummary(tid=_to_int(row.get("TID", "0")), name=_quest_name(row) or row.get("TID", ""))


def _is_valid_link_id(value: str) -> bool:
    return bool(value.strip() and value.strip() != "0")


def _to_int(value: str) -> int:
    try:
        return int(value.strip())
    except (AttributeError, ValueError):
        return 0
