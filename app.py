# -*- coding: utf-8 -*-
"""
Multi-Agent 审核中心的前端网页。
这是一个更完整的 Streamlit 单页应用，包含首页概览、审核输入、结果面板和历史记录。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from app.workflows.audit_orchestration import run_audit

st.set_page_config(
    page_title="Multi-Agent 审核中心",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

CSS = """
<style>
.block-container { padding-top: 1rem; padding-bottom: 2rem; max-width: 1240px; }
.stApp {
  background:
    radial-gradient(circle at top left, rgba(14,165,233,.12), transparent 30%),
    radial-gradient(circle at top right, rgba(16,185,129,.10), transparent 24%),
    linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%);
}
.hero {
  border-radius: 28px;
  padding: 28px;
  color: white;
  background: linear-gradient(135deg, #0f172a 0%, #1e293b 52%, #0f766e 100%);
  box-shadow: 0 22px 60px rgba(15,23,42,.18);
}
.hero h1 { font-size: 2.2rem; margin: 0 0 .35rem 0; }
.hero p { margin: 0; color: rgba(255,255,255,.88); font-size: 1.02rem; }
.hero-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 18px; }
.hero-chip {
  background: rgba(255,255,255,.10);
  border: 1px solid rgba(255,255,255,.14);
  border-radius: 18px;
  padding: 14px 16px;
  backdrop-filter: blur(8px);
}
.hero-chip b { display: block; margin-bottom: 4px; }
.card {
  border-radius: 22px;
  padding: 18px;
  background: rgba(255,255,255,.82);
  border: 1px solid rgba(148,163,184,.24);
  box-shadow: 0 12px 30px rgba(15,23,42,.06);
}
.section-title { font-size: 1.02rem; font-weight: 700; color: #0f172a; margin-bottom: 10px; }
.small-muted { color: #64748b; font-size: .92rem; }
.kpi {
  border-radius: 20px;
  padding: 16px;
  background: white;
  border: 1px solid rgba(148,163,184,.22);
  box-shadow: 0 10px 24px rgba(15,23,42,.05);
}
.kpi-label { color: #64748b; font-size: .88rem; margin-bottom: 6px; }
.kpi-value { color: #0f172a; font-size: 1.4rem; font-weight: 800; }
.trace-item {
  border-left: 3px solid #0f766e;
  padding: 12px 14px;
  margin-bottom: 10px;
  border-radius: 14px;
  background: #f8fafc;
}
.trace-item b { display: block; margin-bottom: 4px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

if "audit_history" not in st.session_state:
    st.session_state.audit_history: list[dict[str, Any]] = []


def _trace_item(stage: str, detail: str) -> str:
    return f"<div class='trace-item'><b>{stage}</b><div class='small-muted'>{detail}</div></div>"


def run_audit_ui(text: str) -> dict[str, Any]:
    result = run_audit(text)
    trace_html = []
    for step in result.get("log", []):
        stage = str(step.get("stage") or "流程节点")
        detail = str(step.get("result") or step.get("assessment") or step.get("signals") or step)
        trace_html.append(_trace_item(stage, detail[:240]))
    return {"trace_html": "".join(trace_html), "data": result}


def render_header() -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>Multi-Agent 审核中心</h1>
          <p>面向内容审核、规则判定与多智能体协作分析的一体化前端页面</p>
          <div class="hero-grid">
            <div class="hero-chip"><b>多智能体链路</b><span>意图分析、执行、验证、裁决</span></div>
            <div class="hero-chip"><b>结构化结果</b><span>可视化展示每一步审核轨迹</span></div>
            <div class="hero-chip"><b>历史可追踪</b><span>保留最近 5 次审核记录</span></div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_overview(data: dict[str, Any]) -> None:
    c1, c2, c3, c4 = st.columns(4)
    metrics = [
        ("最终裁决", str(data.get("final_verdict", "-"))),
        ("置信度", f"{float(data.get('final_confidence', 0.0) or 0.0):.2f}"),
        ("阶段数", str(len(data.get("log") or []))),
        ("是否仲裁", "是" if data.get("judge_result") else "否"),
    ]
    for col, (label, value) in zip((c1, c2, c3, c4), metrics, strict=True):
        with col:
            st.markdown(
                f"<div class='kpi'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div></div>",
                unsafe_allow_html=True,
            )


def page_audit() -> None:
    render_header()

    st.write("")
    left, right = st.columns([1.4, 0.9], gap="large")
    with left:
        st.markdown("<div class='card'><div class='section-title'>待审核内容</div>", unsafe_allow_html=True)
        text = st.text_area(
            label="",
            height=260,
            placeholder="在这里输入待审核文本，例如：合同条款、公告、申诉材料、平台内容等。",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    with right:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>使用说明</div>", unsafe_allow_html=True)
        st.write("1. 输入待审核内容")
        st.write("2. 点击开始审核")
        st.write("3. 查看最终裁决、置信度与轨迹")
        st.markdown("<div class='small-muted'>适合演示、部署和内部审核流程展示。</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='section-title'>流程链路</div>", unsafe_allow_html=True)
        st.write("• 意图分析")
        st.write("• 工作单元拆分")
        st.write("• 规则/验证器检查")
        st.write("• 终审与仲裁")
        st.markdown("</div>", unsafe_allow_html=True)

    run_col, clear_col, sample_col = st.columns([1, 1, 2])
    with run_col:
        run_clicked = st.button("开始审核", type="primary", use_container_width=True)
    with clear_col:
        if st.button("清空结果", use_container_width=True):
            st.session_state.audit_history = []
            st.rerun()
    with sample_col:
        st.caption("提示：可以直接粘贴一段文本进行演示，也可以让我帮你接上真实业务数据源。")

    if run_clicked:
        if not text.strip():
            st.warning("请输入内容后再审核。")
        else:
            with st.spinner("审核进行中…"):
                result = run_audit_ui(text.strip())
                st.session_state.audit_history.append({"text": text.strip(), **result})

    if st.session_state.audit_history:
        latest = st.session_state.audit_history[-1]
        data = latest.get("data") or {}
        render_overview(data)

        tab1, tab2, tab3 = st.tabs(["流程轨迹", "结构化结果", "历史记录"])
        with tab1:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.markdown(latest.get("trace_html") or "_无轨迹_", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with tab2:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            st.json(data)
            st.markdown("</div>", unsafe_allow_html=True)
        with tab3:
            st.markdown("<div class='card'>", unsafe_allow_html=True)
            for idx, item in enumerate(reversed(st.session_state.audit_history[-5:]), 1):
                st.write(f"{idx}. {item.get('text', '')[:80]}")
                if isinstance(item.get("data"), dict):
                    st.caption(f"裁决: {item['data'].get('final_verdict', '-')} | 置信度: {item['data'].get('final_confidence', 0.0)}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("当前还没有审核记录，输入内容后点击“开始审核”即可生成前端页面结果。")


page_audit()
