# Tasks: build-npc-drop-and-shop-query-v1

## Task 1: Freeze scope

- 仅覆盖 NPC <-> shop/drop <-> item
- 仅接入 `NpcTable`、`ItemDropTable`、`SaleTable`、`ItemTable`
- 不扩展 quest / world / map 逻辑

## Task 2: Build minimal read/index path

- NPC by TID / LocalName
- Item by TID / LocalName
- `SaleTID -> SaleTable rows`
- `ItemDropTID -> ItemDropTable row`
- item reverse lookup by iterating allowed business chain only

## Task 3: Define operator-facing result model

- NPC -> shop items
- NPC -> drop items
- Item -> NPC shop sources
- Item -> NPC drop sources
- visible source path and trust status

## Task 4: Add focused tests

- valid sale chain
- valid drop chain
- reverse sale lookup
- reverse drop lookup
- missing/zero/invalid relation IDs
- no false positives from TID collisions

## Task 5: Update docs

- short usage doc
- supported flow summary
- explicit deferrals
