from __future__ import annotations

import csv
from pathlib import Path

ALLOWED_TABLES = {
    "ItemTable": "ItemTable.csv",
    "ItemSetTable": "ItemSetTable.csv",
    "ItemSetAbilityTable": "ItemSetAbilityTable.csv",
}

CSV_ENCODINGS = ("utf-8-sig", "utf-8", "gb18030", "cp1252", "latin1")


def resolve_tables_dir(start: Path | None = None) -> Path:
    """从当前代码位置向上查找 data/tables，兼容当前仓库结构。"""

    base = (start or Path(__file__)).resolve()
    for parent in [base, *base.parents]:
        candidate = parent / "data" / "tables"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("无法在当前仓库中定位 data/tables 目录")


def load_csv_records(table_name: str, tables_dir: Path) -> list[dict[str, str]]:
    if table_name not in ALLOWED_TABLES:
        raise ValueError(f"不允许读取表: {table_name}")

    table_path = tables_dir / ALLOWED_TABLES[table_name]
    if not table_path.exists():
        raise FileNotFoundError(f"CSV 文件不存在: {table_path}")

    rows: list[list[str]] | None = None
    decode_errors: list[str] = []

    for encoding in CSV_ENCODINGS:
        try:
            with table_path.open("r", encoding=encoding, newline="") as handle:
                rows = list(csv.reader(handle))
            break
        except UnicodeDecodeError as exc:
            decode_errors.append(f"{encoding}: {exc}")

    if rows is None:
        raise UnicodeDecodeError(
            "csv-loader",
            b"",
            0,
            1,
            f"无法解析 CSV 编码: {table_path}; errors={decode_errors}",
        )

    if not rows:
        return []

    headers = rows[0]
    data_rows = rows[4:]  # 跳过第 2~4 行元信息，从第 5 行开始解析

    records: list[dict[str, str]] = []
    for row in data_rows:
        if not row or not any(cell.strip() for cell in row):
            continue

        # 某些行长度可能不足，统一右侧补空串，保证字段对齐且结果稳定
        padded = row + [""] * max(0, len(headers) - len(row))
        record = {header: padded[idx].strip() for idx, header in enumerate(headers)}
        records.append(record)

    return records


def load_allowed_tables(
    tables_dir: Path | None = None,
) -> dict[str, list[dict[str, str]]]:
    resolved = tables_dir or resolve_tables_dir()
    return {
        table_name: load_csv_records(table_name=table_name, tables_dir=resolved)
        for table_name in ALLOWED_TABLES
    }
