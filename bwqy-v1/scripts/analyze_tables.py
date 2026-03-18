from __future__ import annotations

import csv
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[2]
TABLES_DIR = ROOT / 'data' / 'tables'
REPORT_DIR = ROOT / 'bwqy-v1' / 'docs' / 'table-analysis'
ENCODINGS = ('utf-8-sig', 'utf-8', 'gb18030', 'latin1')
TYPE_TOKENS = {'int', 'string', 'float', 'bool', 'long', 'double'}
TYPE_VALUE_RE = re.compile(r'^(U|S|F)?\d+$|^CBwString(?::v)?$|^string$|^float$|^bool$|^DWORD$', re.IGNORECASE)
KEY_FIELD_RE = re.compile(r'(^TID$|.+TID$|.+ID$)', re.IGNORECASE)
ITEM_REF_RE = re.compile(
    r'^(ItemTID|ItemId|DropItem(?!Stack).*|BoxItem(?!Stack).*|CompleteItemTID|RewardItem(?!Stack).*|NeedItem(?!Count).*)$',
    re.IGNORECASE,
)
TOKEN_SPLIT_RE = re.compile(r'[|;/]')
NUMERIC_RE = re.compile(r'^\d+$')


@dataclass
class FieldStats:
    name: str
    non_empty: int
    total: int
    unique_non_empty: int
    duplicate_rows: int
    duplicate_values: int
    classification: str


@dataclass
class TableAnalysis:
    name: str
    path: Path
    header: list[str]
    start_row: int
    total_rows: int
    data_rows: list[dict[str, str]]
    key_fields: list[FieldStats]


def read_csv_rows(path: Path) -> list[list[str]]:
    last_error = None
    for encoding in ENCODINGS:
        try:
            with path.open('r', encoding=encoding, newline='') as f:
                return [row for row in csv.reader(f)]
        except UnicodeDecodeError as exc:
            last_error = exc
    raise RuntimeError(f'Failed to decode {path}: {last_error}')


def normalize_header(row: list[str]) -> list[str]:
    return [cell.strip() for cell in row]


def detect_data_start(rows: list[list[str]], header: list[str]) -> int:
    def is_type_row(row: list[str]) -> bool:
        cells = [cell.strip() for cell in row if cell.strip()]
        if not cells:
            return False
        type_like = sum(1 for cell in cells if cell.lower() in TYPE_TOKENS or TYPE_VALUE_RE.match(cell))
        return (type_like / len(cells)) >= 0.5

    if len(rows) >= 4 and is_type_row(rows[3]):
        return 5
    if len(rows) >= 3 and is_type_row(rows[2]):
        return 4
    if len(rows) >= 2 and is_type_row(rows[1]):
        return 3
    return 2


def classify_field(non_empty: int, total: int, unique_non_empty: int, duplicate_rows: int) -> str:
    if non_empty == 0:
        return '空字段（不能当主键）'
    if unique_non_empty == non_empty:
        return '表内唯一（可疑似主键）'
    unique_rate = unique_non_empty / non_empty
    if unique_rate >= 0.98 and duplicate_rows <= max(3, int(non_empty * 0.01)):
        return '高唯一但非严格唯一'
    return '明显重复（不能当主键）'


def field_stats(rows: list[dict[str, str]], field: str) -> FieldStats:
    values = [row.get(field, '').strip() for row in rows]
    non_empty_values = [value for value in values if value]
    counter = Counter(non_empty_values)
    duplicate_values = sum(1 for count in counter.values() if count > 1)
    duplicate_rows = sum(count - 1 for count in counter.values() if count > 1)
    unique_non_empty = len(counter)
    return FieldStats(
        name=field,
        non_empty=len(non_empty_values),
        total=len(rows),
        unique_non_empty=unique_non_empty,
        duplicate_rows=duplicate_rows,
        duplicate_values=duplicate_values,
        classification=classify_field(len(non_empty_values), len(rows), unique_non_empty, duplicate_rows),
    )


def parse_table(path: Path) -> TableAnalysis:
    raw_rows = read_csv_rows(path)
    header = normalize_header(raw_rows[0])
    start_row = detect_data_start(raw_rows, header)
    data_rows: list[dict[str, str]] = []
    for row in raw_rows[start_row - 1 :]:
        padded = row + [''] * max(0, len(header) - len(row))
        mapped = {header[i]: padded[i].strip() for i in range(len(header)) if header[i]}
        if not any(mapped.values()):
            continue
        data_rows.append(mapped)
    key_fields = [field_stats(data_rows, field) for field in header if field and KEY_FIELD_RE.match(field)]
    return TableAnalysis(path.stem, path, header, start_row, len(raw_rows), data_rows, key_fields)


def fmt_pct(num: int, den: int) -> str:
    return '0.00%' if den == 0 else f'{(num / den) * 100:.2f}%'


def sanitize_value(value: str, limit: int = 60) -> str:
    value = value.replace('\n', ' ').strip()
    return value if len(value) <= limit else value[: limit - 3] + '...'


def extract_numeric_tokens(value: str) -> list[str]:
    value = value.strip()
    if not value:
        return []
    parts = [value] if NUMERIC_RE.fullmatch(value) else [part.strip() for part in TOKEN_SPLIT_RE.split(value)]
    return [part for part in parts if NUMERIC_RE.fullmatch(part)]


def write_table_key_candidates(analyses: list[TableAnalysis]) -> None:
    out = REPORT_DIR / 'table_key_candidates.md'
    lines = ['# 表级主键候选分析', '', '- 说明：只统计字段名命中 `TID`、`*ID`、`*TID` 的列。', '- 判定口径：`表内唯一`=非空值严格唯一；`高唯一但非严格唯一`=接近唯一但仍有少量重复；其余归为明显重复。', '']
    for table in analyses:
        lines += [f'## {table.name}', '', f'- 文件：`{table.path.relative_to(ROOT)}`', f'- Header 行：第 1 行', f'- 有效数据起始行：第 {table.start_row} 行', f'- 文件总行数：{table.total_rows}', f'- 解析后的业务数据行数：{len(table.data_rows)}', f'- 字段总数：{len(table.header)}', f'- 字段列表：{", ".join(table.header)}', '']
        if not table.key_fields:
            lines += ['- 未发现命中 `TID` / `*ID` / `*TID` 的字段。', '']
            continue
        lines += ['| 字段 | 非空率 | 非空值数 | 唯一值数 | 重复值种类 | 重复行数 | 判定 |', '| --- | --- | ---: | ---: | ---: | ---: | --- |']
        for stat in table.key_fields:
            lines.append(f'| `{stat.name}` | {fmt_pct(stat.non_empty, stat.total)} | {stat.non_empty} | {stat.unique_non_empty} | {stat.duplicate_values} | {stat.duplicate_rows} | {stat.classification} |')
        lines.append('')
    out.write_text('\n'.join(lines), encoding='utf-8')


def write_within_table_duplicates(analyses: list[TableAnalysis]) -> None:
    out = REPORT_DIR / 'tid_duplicates_within_table.md'
    lines = ['# 表内重复值分析（TID / *ID / *TID）', '', '- 说明：优先列出 exact `TID` 字段；若某表没有 `TID`，则列出重复最明显的 ID 类字段。', '']
    for table in analyses:
        rows = table.data_rows
        focus_fields = [stat for stat in table.key_fields if stat.name == 'TID'] or [stat for stat in table.key_fields if stat.duplicate_rows > 0]
        if not focus_fields:
            continue
        lines += [f'## {table.name}', '']
        for stat in focus_fields:
            values = [row.get(stat.name, '').strip() for row in rows if row.get(stat.name, '').strip()]
            counter = Counter(values)
            dup_items = [(value, count) for value, count in counter.items() if count > 1]
            dup_items.sort(key=lambda item: (-item[1], item[0]))
            lines.append(f'### `{stat.name}`')
            lines.append('')
            lines.append(f'- 判定：{stat.classification}')
            lines.append(f'- 非空值数：{stat.non_empty}')
            lines.append(f'- 唯一值数：{stat.unique_non_empty}')
            lines.append(f'- 重复值种类：{stat.duplicate_values}')
            lines.append(f'- 重复行数：{stat.duplicate_rows}')
            if dup_items:
                lines.append('- 重复样例（最多 20 个）：')
                lines.append('')
                lines.append('| 值 | 出现次数 |')
                lines.append('| --- | ---: |')
                for value, count in dup_items[:20]:
                    lines.append(f'| `{sanitize_value(value)}` | {count} |')
            else:
                lines.append('- 未发现重复值。')
            lines.append('')
    out.write_text('\n'.join(lines), encoding='utf-8')


def write_across_table_collisions(analyses: list[TableAnalysis]) -> None:
    out = REPORT_DIR / 'tid_collisions_across_tables.md'
    index: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    strict_candidates = []
    for table in analyses:
        for stat in table.key_fields:
            if stat.classification != '表内唯一（可疑似主键）':
                continue
            strict_candidates.append((table.name, stat.name))
            for row in table.data_rows:
                value = row.get(stat.name, '').strip()
                if value:
                    index[value].append((table.name, stat.name, stat.classification))
    collisions = [(value, refs) for value, refs in index.items() if len(refs) > 1]
    collisions.sort(key=lambda item: (-len(item[1]), item[0]))
    lines = ['# 跨表同值碰撞分析', '', '- 说明：只对“表内唯一（可疑似主键）”字段建倒排索引，避免把明显重复字段当作跨表主键。', f'- 纳入倒排索引的字段数：{len(strict_candidates)}', '']
    lines.append('## 判读口径')
    lines.append('')
    lines.append('- **独立实体域的正常重号**：相同数值分别出现在不同主表的 `TID` / `ID` 字段，但字段语义彼此独立。')
    lines.append('- **可能的引用关系**：值相同且字段名/表名存在明显主从关系线索，例如 `SetTID` 对 `ItemSetTable.TID`。')
    lines.append('- **明显不可信的噪声**：来源字段本身并非严格主键，或值格式/上下文无法支撑稳定关联。')
    lines.append('')
    if collisions:
        lines.append('## 碰撞清单（最多 300 组）')
        lines.append('')
        for value, refs in collisions[:300]:
            ref_strings = [f'`{table}.{field}`' for table, field, _ in sorted(refs)]
            kind = '独立实体域的正常重号'
            if any(field != 'TID' for _, field, _ in refs):
                kind = '可能的引用关系'
            if len({table for table, _, _ in refs}) >= 4 and all(field == 'TID' for _, field, _ in refs):
                kind = '独立实体域的正常重号'
            lines.append(f'- 值 `{sanitize_value(value)}` 同时出现在 {", ".join(ref_strings)}；初步归类：**{kind}**。')
    else:
        lines.append('## 碰撞清单')
        lines.append('')
        lines.append('- 未发现跨表碰撞。')
    out.write_text('\n'.join(lines), encoding='utf-8')


def write_item_reference_candidates(analyses: list[TableAnalysis]) -> None:
    out = REPORT_DIR / 'item_reference_whitelist_candidates.md'
    item_table = next(table for table in analyses if table.name == 'ItemTable')
    item_tids = {row.get('TID', '').strip() for row in item_table.data_rows if row.get('TID', '').strip()}
    candidates = []
    for table in analyses:
        for field in table.header:
            if not field or not ITEM_REF_RE.match(field):
                continue
            token_total = 0
            token_hits = 0
            hit_examples: list[str] = []
            miss_examples: list[str] = []
            for row in table.data_rows:
                tokens = extract_numeric_tokens(row.get(field, ''))
                if not tokens:
                    continue
                token_total += len(tokens)
                for token in tokens:
                    if token in item_tids:
                        token_hits += 1
                        if len(hit_examples) < 5:
                            hit_examples.append(token)
                    elif len(miss_examples) < 5:
                        miss_examples.append(token)
            if token_total == 0:
                continue
            hit_rate = token_hits / token_total
            if token_hits == 0:
                strength = '仅语义命中，未命中 ItemTable.TID（不建议入白名单）'
            elif hit_rate >= 0.95:
                strength = '强引用候选（建议优先入白名单）'
            elif hit_rate >= 0.50:
                strength = '中等强度候选（需逐表复核）'
            else:
                strength = '弱候选（字段名像引用，但命中率不足）'
            candidates.append((table.name, field, token_total, token_hits, hit_rate, strength, hit_examples, miss_examples))
    candidates.sort(key=lambda item: (-item[4], -item[3], item[0], item[1]))
    lines = ['# ItemTable 强引用白名单候选', '', '- 说明：本报告只基于“字段名语义 + 值命中 `ItemTable.TID`”做候选识别，不把所有 `*.TID` 默认当作物品引用。', '']
    lines += ['| 表 | 字段 | 数值 token 数 | 命中 ItemTable.TID | 命中率 | 结论 | 命中样例 | 未命中样例 |', '| --- | --- | ---: | ---: | ---: | --- | --- | --- |']
    for table, field, token_total, token_hits, hit_rate, strength, hit_examples, miss_examples in candidates:
        lines.append(
            f'| `{table}` | `{field}` | {token_total} | {token_hits} | {hit_rate:.2%} | {strength} | '
            f'{", ".join(f"`{x}`" for x in hit_examples) or "-"} | '
            f'{", ".join(f"`{x}`" for x in miss_examples) or "-"} |'
        )
    out.write_text('\n'.join(lines), encoding='utf-8')


def write_summary(analyses: list[TableAnalysis]) -> None:
    out = REPORT_DIR / 'analysis_summary.md'
    independent_tables = [table.name for table in analyses if any(stat.name == 'TID' and stat.classification == '表内唯一（可疑似主键）' for stat in table.key_fields)]
    strong_item_fields = []
    avoid_auto_join = []
    item_table = next(table for table in analyses if table.name == 'ItemTable')
    item_tids = {row.get('TID', '').strip() for row in item_table.data_rows if row.get('TID', '').strip()}
    for table in analyses:
        for field in table.header:
            if not field:
                continue
            if ITEM_REF_RE.match(field):
                tokens = []
                for row in table.data_rows:
                    tokens.extend(extract_numeric_tokens(row.get(field, '')))
                if not tokens:
                    continue
                hit_rate = sum(1 for token in tokens if token in item_tids) / len(tokens)
                if hit_rate >= 0.95:
                    strong_item_fields.append(f'{table.name}.{field}')
                elif hit_rate < 0.5:
                    avoid_auto_join.append(f'{table.name}.{field}')
            elif field.endswith('TID') and field != 'TID':
                avoid_auto_join.append(f'{table.name}.{field}')

    strong_item_fields = sorted(set(strong_item_fields))
    avoid_auto_join = sorted(set(avoid_auto_join))
    lines = [
        '# 主键与引用分析结论摘要',
        '',
        f'- 可视为独立主表的表：共 {len(independent_tables)} 张，判断标准为 `TID` 在表内严格唯一。',
        f'- 独立主表示例：{", ".join(independent_tables[:30])}。',
        '- `ItemTable.TID` 应仅视为“物品域主键”，因为跨表同值碰撞在大量其他主表中同时存在，不能将数值相同直接解释成跨域同一实体。',
        f'- 建议进入“强证据引用白名单”的字段：{", ".join(strong_item_fields[:40])}。',
        f'- 不应自动参与关联推断的字段/表：{", ".join(avoid_auto_join[:40])}。',
        '',
        '## 使用建议',
        '',
        '- 先用 `table_key_candidates.md` 确认每张表的主键候选与唯一性。',
        '- 再用 `item_reference_whitelist_candidates.md` 建立只面向 Item 域的强引用白名单。',
        '- 对 `tid_collisions_across_tables.md` 中的跨表同值，默认按“独立域正常重号”处理，除非字段语义和命中关系同时成立。',
    ]
    out.write_text('\n'.join(lines), encoding='utf-8')


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    analyses = [parse_table(path) for path in sorted(TABLES_DIR.glob('*.csv'))]
    write_table_key_candidates(analyses)
    write_within_table_duplicates(analyses)
    write_across_table_collisions(analyses)
    write_item_reference_candidates(analyses)
    write_summary(analyses)
    print(f'Analyzed {len(analyses)} tables into {REPORT_DIR.relative_to(ROOT)}')


if __name__ == '__main__':
    main()
