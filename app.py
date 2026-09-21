"""
Streamlit UI for the Multi-Agent AI Research System.

Run with:
    streamlit run app.py

Expects `pipeline.py` (with `run_research_pipeline`) and `agents.py`
(with the agent/chain builders) alongside this file, plus a `.env`
with whatever API keys your agents/tools need.
"""

import io
import re
import json
import contextlib
import traceback
from datetime import datetime

import streamlit as st

from pipeline import run_research_pipeline


# ==========================================================================
# Page config
# ==========================================================================
st.set_page_config(
    page_title="Research Copilot",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==========================================================================
# Custom CSS
# ==========================================================================
st.markdown(
    """
    <style>
        /* ---------- General ---------- */
        .stApp {
            background: radial-gradient(1200px 600px at 10% -10%, rgba(124,58,237,0.10), transparent),
                        radial-gradient(1200px 600px at 110% 10%, rgba(56,189,248,0.10), transparent);
        }
        #MainMenu, footer {visibility: hidden;}
        /* Keep header visible — it holds the sidebar collapse/expand arrow.
           Just make it blend in instead of hiding it outright. */
        header[data-testid="stHeader"] {
            background: transparent;
            box-shadow: none;
        }
        .block-container {padding-top: 1.5rem; max-width: 1200px;}

        /* ---------- Hero ---------- */
        .hero {
            padding: 1.8rem 2rem;
            border-radius: 18px;
            background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 55%, #0ea5e9 100%);
            color: white;
            margin-bottom: 1.4rem;
            box-shadow: 0 10px 30px rgba(79,70,229,0.25);
        }
        .hero h1 {
            font-size: 2rem;
            margin: 0 0 0.35rem 0;
            font-weight: 800;
            letter-spacing: -0.02em;
        }
        .hero p {
            margin: 0;
            opacity: 0.92;
            font-size: 1.02rem;
        }
        .hero-badges { margin-top: 0.9rem; }
        .hero-badge {
            display: inline-block;
            background: rgba(255,255,255,0.16);
            border: 1px solid rgba(255,255,255,0.28);
            padding: 3px 12px;
            border-radius: 999px;
            font-size: 0.78rem;
            margin-right: 8px;
            backdrop-filter: blur(6px);
        }

        /* ---------- Cards ---------- */
        .card {
            background: var(--background-color, #ffffff);
            border: 1px solid rgba(120,120,140,0.15);
            border-radius: 16px;
            padding: 1.1rem 1.3rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.04);
            margin-bottom: 1rem;
        }

        /* ---------- Suggestion chips ---------- */
        div[data-testid="stButton"] > button {
            border-radius: 999px !important;
            border: 1px solid rgba(124,58,237,0.35) !important;
            background: rgba(124,58,237,0.06) !important;
            color: inherit !important;
            font-size: 0.82rem !important;
            padding: 0.25rem 0.9rem !important;
            transition: all 0.15s ease-in-out;
        }
        div[data-testid="stButton"] > button:hover {
            background: rgba(124,58,237,0.18) !important;
            border-color: rgba(124,58,237,0.6) !important;
            transform: translateY(-1px);
        }

        /* Primary run button override */
        div[data-testid="stButton"] > button[kind="primary"] {
            border-radius: 12px !important;
            background: linear-gradient(135deg, #7c3aed, #0ea5e9) !important;
            border: none !important;
            color: white !important;
            font-weight: 700 !important;
            font-size: 0.95rem !important;
            padding: 0.6rem 1rem !important;
            box-shadow: 0 6px 16px rgba(79,70,229,0.35);
        }
        div[data-testid="stButton"] > button[kind="primary"]:hover {
            transform: translateY(-1px);
            box-shadow: 0 8px 20px rgba(79,70,229,0.45);
        }

        /* ---------- Step tracker ---------- */
        .step-track { display: flex; gap: 10px; margin: 0.4rem 0 1rem 0; }
        .step-pill {
            flex: 1;
            text-align: center;
            padding: 0.55rem 0.4rem;
            border-radius: 12px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(120,120,140,0.18);
            background: rgba(120,120,140,0.06);
            color: rgba(120,120,140,0.9);
        }
        .step-pill.done {
            background: linear-gradient(135deg, rgba(16,185,129,0.16), rgba(16,185,129,0.08));
            border-color: rgba(16,185,129,0.45);
            color: #059669;
        }
        .step-pill.active {
            background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(14,165,233,0.14));
            border-color: rgba(124,58,237,0.5);
            color: #7c3aed;
        }

        /* ---------- Metric chips ---------- */
        .metric-row { display: flex; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.6rem;}
        .metric-chip {
            background: rgba(124,58,237,0.07);
            border: 1px solid rgba(124,58,237,0.2);
            border-radius: 12px;
            padding: 0.6rem 1rem;
            min-width: 120px;
        }
        .metric-chip .val { font-size: 1.25rem; font-weight: 800; color: #7c3aed; }
        .metric-chip .lbl { font-size: 0.75rem; opacity: 0.7; }

        .section-title {
            font-weight: 700;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            opacity: 0.6;
            margin: 0.2rem 0 0.6rem 0;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ==========================================================================
# Suggested topics
# ==========================================================================
SUGGESTED_TOPICS = {
    "🤖 Technology": [
        "Latest advances in humanoid robotics",
        "State of open-source large language models",
        "Quantum computing breakthroughs in 2026",
    ],
    "🧬 Science & Health": [
        "CRISPR gene editing recent clinical trials",
        "mRNA vaccine technology beyond COVID-19",
        "Impact of ultra-processed foods on health",
    ],
    "💰 Business & Economy": [
        "Global semiconductor supply chain shifts",
        "Rise of AI agents in enterprise software",
        "Renewable energy investment trends 2026",
    ],
    "🌍 World & Policy": [
        "AI regulation policies across major economies",
        "Global climate adaptation strategies",
        "Space exploration commercial partnerships",
    ],
}

# ==========================================================================
# Session state
# ==========================================================================
defaults = {
    "history": [],
    "current": None,
    "logs": "",
    "is_running": False,
    "topic_input": "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


def set_topic(topic: str):
    st.session_state["topic_input"] = topic


# ==========================================================================
# Sidebar
# ==========================================================================
with st.sidebar:
    st.markdown("### 🧠 Research Copilot")
    st.caption("Search → Scrape → Write → Critique")
    st.divider()

    st.markdown("**✍️ Your topic**")
    topic = st.text_area(
        "Research topic",
        key="topic_input",
        placeholder="e.g. Latest advances in solid-state batteries",
        height=90,
        label_visibility="collapsed",
    )

    st.markdown("**💡 Need inspiration?**")
    for category, topics in SUGGESTED_TOPICS.items():
        with st.expander(category, expanded=False):
            for t in topics:
                st.button(t, key=f"sugg_{t}", on_click=set_topic, args=(t,), use_container_width=True)

    st.divider()
    run_clicked = st.button(
        "🚀 Run pipeline",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.is_running or not st.session_state.topic_input.strip(),
    )
    show_logs = st.toggle("Show console logs", value=True)

    st.divider()
    st.markdown("**🕓 History**")
    if not st.session_state.history:
        st.caption("No runs yet.")
    else:
        for i, run in enumerate(reversed(st.session_state.history)):
            idx = len(st.session_state.history) - 1 - i
            label = f"{run['timestamp'][-8:]} · {run['topic'][:26]}"
            if st.button(label, key=f"hist_{idx}", use_container_width=True):
                st.session_state.current = run["state"]
                st.session_state.logs = run.get("logs", "")

        if st.button("🗑️ Clear history", use_container_width=True):
            st.session_state.history = []
            st.session_state.current = None
            st.session_state.logs = ""
            st.rerun()


# ==========================================================================
# Hero header
# ==========================================================================
st.markdown(
    """
    <div class="hero">
        <h1>🧠 Multi-Agent Research System</h1>
        <p>Four specialized agents work together to search, read, write, and critique — turning any topic into a sourced research brief.</p>
        <div class="hero-badges">
            <span class="hero-badge">🔍 Search Agent</span>
            <span class="hero-badge">📚 Scrape Agent</span>
            <span class="hero-badge">✍️ Writer Chain</span>
            <span class="hero-badge">🧐 Critic Chain</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================================
# Helpers
# ==========================================================================
def as_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if hasattr(value, "content"):
        return str(value.content)
    return str(value)


def run_with_captured_logs(research_topic: str):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        result_state = run_research_pipeline(research_topic)
    return result_state, buf.getvalue()


def render_step_track(step_labels, active_index):
    """active_index: -1 idle, 0..n-1 in progress, len(labels) = all done"""
    html = '<div class="step-track">'
    for i, label in enumerate(step_labels):
        if active_index > i:
            cls = "done"
            icon = "✅"
        elif active_index == i:
            cls = "active"
            icon = "⏳"
        else:
            cls = ""
            icon = "○"
        html += f'<div class="step-pill {cls}">{icon} {label}</div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def count_sources(text: str) -> int:
    return len(re.findall(r"https?://", text or ""))


def word_count(text: str) -> int:
    return len((text or "").split())


# ==========================================================================
# Run pipeline
# ==========================================================================
if run_clicked:
    st.session_state.is_running = True
    step_labels = ["Search", "Scrape", "Write", "Critique"]
    placeholder = st.empty()

    run_succeeded = False
    error_message = ""
    error_trace = ""

    with placeholder.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown("##### ⚙️ Pipeline running…")
        render_step_track(step_labels, active_index=0)
        with st.spinner("Agents are working — this can take a minute or two..."):
            try:
                state, logs = run_with_captured_logs(st.session_state.topic_input.strip())
                run_record = {
                    "topic": st.session_state.topic_input.strip(),
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "state": state,
                    "logs": logs,
                }
                st.session_state.history.append(run_record)
                st.session_state.current = state
                st.session_state.logs = logs
                run_succeeded = True
            except Exception as e:
                error_message = str(e)
                error_trace = traceback.format_exc()
            finally:
                st.session_state.is_running = False
        st.markdown("</div>", unsafe_allow_html=True)

    # The progress card above is only useful *while* running. Once the
    # run is done, remove it entirely so it doesn't sit around looking
    # like a duplicate/stale set of tabs above the real results below.
    placeholder.empty()

    if run_succeeded:
        st.toast("Pipeline complete! ✅", icon="✅")
    else:
        st.error(f"Something went wrong while running the pipeline: {error_message}")
        with st.expander("Full traceback"):
            st.code(error_trace)


# ==========================================================================
# Results
# ==========================================================================
state = st.session_state.current

if state is None:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 👋 Get started")
    st.write(
        "Type a topic in the sidebar (or tap one of the 💡 suggestions), "
        "then hit **🚀 Run pipeline**. Your report, sources, and critic feedback "
        "will show up right here."
    )
    st.markdown("</div>", unsafe_allow_html=True)
else:
    report_text = as_text(state.get("report"))
    feedback_text = as_text(state.get("feedback"))
    search_text = as_text(state.get("search_results"))
    scrape_text = as_text(state.get("scrape_content"))

    # ---- Metrics row ----
    st.markdown('<div class="metric-row">', unsafe_allow_html=True)
    metrics = [
        ("📝", word_count(report_text), "Report words"),
        ("🔗", count_sources(search_text), "Sources found"),
        ("📚", count_sources(scrape_text), "Pages scraped"),
        ("⏱️", f"{max(1, word_count(report_text)//200)} min", "Est. read time"),
    ]
    cols = st.columns(len(metrics))
    for col, (icon, val, lbl) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""<div class="metric-chip">
                        <div class="val">{icon} {val}</div>
                        <div class="lbl">{lbl}</div>
                    </div>""",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    tab_report, tab_critic, tab_search, tab_scrape, tab_logs = st.tabs(
        ["📄 Report", "🧐 Critic Feedback", "🔍 Search Results", "📚 Scraped Content", "🖥️ Logs"]
    )

    with tab_report:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        if report_text:
            st.markdown(report_text)
        else:
            st.warning("No report was generated.")
        st.markdown("</div>", unsafe_allow_html=True)

        if report_text:
            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "⬇️ Download report (.md)",
                    data=report_text,
                    file_name="research_report.md",
                    mime="text/markdown",
                    use_container_width=True,
                )
            with c2:
                full_json = json.dumps(
                    {k: as_text(v) for k, v in state.items()}, indent=2, ensure_ascii=False
                )
                st.download_button(
                    "⬇️ Download full run (.json)",
                    data=full_json,
                    file_name="research_run.json",
                    mime="application/json",
                    use_container_width=True,
                )

    with tab_critic:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(feedback_text if feedback_text else "_No critic feedback was generated._")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_search:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(search_text if search_text else "_No search results captured._")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_scrape:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(scrape_text if scrape_text else "_No scraped content captured._")
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_logs:
        if show_logs:
            st.code(st.session_state.logs or "No logs captured.", language="text")
        else:
            st.caption("Console logs are hidden. Toggle them on in the sidebar.")


# ==========================================================================
# Footer
# ==========================================================================
st.write("")
st.caption(
    "Pipeline: build_search_agent → build_scrape_agent → writer_chain → critic_chain "
    "(defined in agents.py, orchestrated in pipeline.py)."
)