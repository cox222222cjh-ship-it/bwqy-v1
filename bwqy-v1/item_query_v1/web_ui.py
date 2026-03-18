from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Callable
from urllib.parse import parse_qs
from wsgiref.simple_server import make_server

from .query_service import ItemQueryIndex, build_item_query_index, query_item
from .result_view_model import (
    CandidateResultModel,
    FieldDisplayItem,
    ItemResultPageModel,
    ResultViewModel,
    SectionModel,
    build_result_view_model,
)


@dataclass
class QueryPageState:
    query: str = ""
    result: ResultViewModel | None = None
    no_result: bool = False
    error: str | None = None


@dataclass
class AppState:
    index: ItemQueryIndex | None
    startup_error: str | None


def init_app_state(
    index_builder: Callable[[], ItemQueryIndex] = build_item_query_index,
) -> AppState:
    try:
        return AppState(index=index_builder(), startup_error=None)
    except Exception as exc:  # noqa: BLE001
        return AppState(index=None, startup_error=f"索引加载失败: {exc}")


def query_to_page_state(index: ItemQueryIndex, query: str) -> QueryPageState:
    q = query.strip()
    if not q:
        return QueryPageState(query="")

    raw = query_item(index, q)
    if not raw.matched_items and not raw.candidates:
        return QueryPageState(query=q, no_result=True)

    return QueryPageState(query=q, result=build_result_view_model(raw))


def build_html(state: QueryPageState) -> str:
    return f"""<!doctype html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"utf-8\" />
  <title>item-query-v1</title>
  <style>
    body {{ font-family: sans-serif; margin: 2rem auto; max-width: 1000px; line-height: 1.5; }}
    .row {{ display: flex; gap: 0.5rem; }}
    input[type='text'] {{ width: 420px; padding: 0.4rem; }}
    button {{ padding: 0.4rem 0.8rem; }}
    .panel {{ border: 1px solid #ddd; padding: 0.8rem; margin-top: 1rem; border-radius: 6px; }}
    .state {{ font-weight: bold; }}
    .error {{ color: #b00020; }}
    .warn {{ color: #a06700; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 0.5rem; }}
    th, td {{ border: 1px solid #ddd; padding: 0.35rem; text-align: left; vertical-align: top; }}
    .badge {{ padding: 0.1rem 0.4rem; border: 1px solid #888; border-radius: 10px; font-size: 0.8rem; }}
  </style>
</head>
<body>
  <h1>item-query-v1（Task 5 最小本地只读界面）</h1>
  <form method=\"post\" class=\"panel\">
    <label for=\"q\">输入物品名称或物品 ID：</label>
    <div class=\"row\">
      <input id=\"q\" name=\"q\" type=\"text\" value=\"{escape(state.query)}\" />
      <button type=\"submit\">查询</button>
    </div>
  </form>
  {_render_output(state)}
</body>
</html>"""


def _render_output(state: QueryPageState) -> str:
    if state.error:
        return f'<section class="panel error"><div class="state">错误</div><div>{escape(state.error)}</div></section>'

    if state.no_result:
        return '<section class="panel"><div class="state">无结果</div><div>未命中任何物品。</div></section>'

    if state.result is None:
        return '<section class="panel"><div class="state">等待查询</div></section>'

    if isinstance(state.result, CandidateResultModel):
        return _render_candidates(state.result)

    return _render_item_detail(state.result)


def _render_candidates(model: CandidateResultModel) -> str:
    rows = "".join(_render_candidate_row(candidate) for candidate in model.candidates)
    return (
        '<section class="panel">'
        '<div class="state">候选结果</div>'
        "<div>命中多个候选，请按 TID/名称再发起精确查询。</div>"
        "<table><thead><tr><th>物品ID</th><th>物品名称</th><th>英文键</th><th>是否装备（推断）</th><th>来源追踪</th><th>状态</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></section>"
    )


def _render_candidate_row(candidate: ItemResultPageModel) -> str:
    tid = _field(candidate.basic_information, "TID")
    local_name = _field(candidate.basic_information, "LocalName")
    eng_name = _field(candidate.basic_information, "EngName")
    equipment = _field(candidate.classification, "is_equipment")
    pending = _has_pending_confirmation(candidate)
    pending_label = (
        '<span class="badge warn">pending_confirmation（待确认）</span>'
        if pending
        else "-"
    )
    equipment_value = escape(equipment.value if equipment else "")
    trace_items = [
        field for field in [tid, local_name, eng_name, equipment] if field is not None
    ]
    trace_value = "<br/>".join(
        f"{escape(field.label)}: {escape(field.source_table)}.{escape(field.source_field)} [{_format_status(field.status)}]"
        for field in trace_items
    )
    return (
        "<tr>"
        f"<td>{escape(tid.value if tid else '')}</td>"
        f"<td>{escape(local_name.value if local_name else '')}</td>"
        f"<td>{escape(eng_name.value if eng_name else '')}</td>"
        f"<td>{equipment_value}</td>"
        f"<td>{trace_value}</td>"
        f"<td>{pending_label}</td>"
        "</tr>"
    )


def _render_item_detail(model: ItemResultPageModel) -> str:
    pending_note = (
        '<div class="warn">包含 pending_confirmation 字段，请谨慎使用。</div>'
        if _has_pending_confirmation(model)
        else ""
    )
    return "".join(
        [
            pending_note,
            _render_section(model.basic_information, "基础信息"),
            _render_section(model.classification, "分类"),
            _render_section(model.source_information, "来源信息"),
            _render_section(model.trust_status, "可信状态"),
            _render_equipment_chain(model),
        ]
    )


def _render_section(section: SectionModel, title: str) -> str:
    rows = "".join(_render_field_row(field) for field in section.fields)
    return (
        '<section class="panel">'
        f"<h2>{escape(title)}</h2>"
        "<table><thead><tr><th>字段</th><th>值</th><th>可信状态</th><th>来源</th><th>备注</th></tr></thead>"
        f"<tbody>{rows}</tbody></table></section>"
    )


def _render_equipment_chain(model: ItemResultPageModel) -> str:
    header = f"装备链路（state={escape(model.equipment_chain.state)}）"
    return _render_section(model.equipment_chain.section, header)


def _render_field_row(field: FieldDisplayItem) -> str:
    status_cell = _format_status(field.status)
    if field.status == "pending_confirmation":
        status_cell = f'{status_cell} <span class="badge">待确认</span>'
    note = escape(field.note or "")
    source = f"{escape(field.source_table)}.{escape(field.source_field)}"
    return (
        "<tr>"
        f"<td>{escape(field.label)}</td>"
        f"<td>{escape(field.value)}</td>"
        f"<td>{status_cell}</td>"
        f"<td>{source}</td>"
        f"<td>{note}</td>"
        "</tr>"
    )


def _field(section: SectionModel, key: str) -> FieldDisplayItem | None:
    return next((field for field in section.fields if field.key == key), None)


def _has_pending_confirmation(model: ItemResultPageModel) -> bool:
    sections = [
        model.basic_information,
        model.classification,
        model.source_information,
        model.trust_status,
        model.equipment_chain.section,
    ]
    return any(
        field.status == "pending_confirmation"
        for section in sections
        for field in section.fields
    )


def make_wsgi_app(app_state: AppState):
    def app(environ, start_response):
        if app_state.startup_error:
            page_state = QueryPageState(error=app_state.startup_error)
        else:
            try:
                method = environ.get("REQUEST_METHOD", "GET").upper()
                if method == "POST":
                    length = int(environ.get("CONTENT_LENGTH") or 0)
                    body = environ["wsgi.input"].read(length).decode("utf-8")
                    form = parse_qs(body)
                    query = form.get("q", [""])[0]
                    assert app_state.index is not None
                    page_state = query_to_page_state(app_state.index, query)
                else:
                    page_state = QueryPageState()
            except Exception as exc:  # noqa: BLE001
                page_state = QueryPageState(error=f"查询失败: {exc}")

        html = build_html(page_state).encode("utf-8")
        start_response(
            "200 OK",
            [
                ("Content-Type", "text/html; charset=utf-8"),
                ("Content-Length", str(len(html))),
            ],
        )
        return [html]

    return app


def run_server(host: str = "127.0.0.1", port: int = 8000) -> None:
    app_state = init_app_state()
    with make_server(host, port, make_wsgi_app(app_state)) as server:
        print(f"item-query-v1 web UI running at http://{host}:{port}")
        server.serve_forever()


_STATUS_LABELS = {
    "direct": "直接读取",
    "derived": "推断",
    "pending_confirmation": "待确认",
}


def _format_status(status: str) -> str:
    localized = _STATUS_LABELS.get(status)
    if localized is None:
        return escape(status)
    return f"{escape(status)}（{escape(localized)}）"


if __name__ == "__main__":
    run_server()
