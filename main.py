"""
⚡ Dual AI Assistant Suite — Premium Streamlit Application
A side-by-side AI playground with glassmorphic dark UI, telemetry, and evaluation dashboard.
"""

import streamlit as st
import os
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ─── Page Configuration ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="⚡ Dual AI Assistant Suite",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://aistudio.google.com/",
        "About": "Dual AI Assistant Suite — Premium AI Playground with Telemetry & Evaluation"
    }
)

# ─── Premium CSS Styling ──────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts Import ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0a12;
    --bg-secondary: #111120;
    --bg-card: rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --border-subtle: rgba(255,255,255,0.08);
    --border-glow: rgba(99,102,241,0.4);
    --accent-purple: #818cf8;
    --accent-blue: #38bdf8;
    --accent-green: #34d399;
    --accent-amber: #fbbf24;
    --accent-red: #f87171;
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #475569;
    --gradient-purple: linear-gradient(135deg, #6366f1 0%, #818cf8 100%);
    --gradient-blue: linear-gradient(135deg, #0ea5e9 0%, #38bdf8 100%);
    --gradient-hero: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #06b6d4 100%);
    --shadow-glow: 0 0 40px rgba(99,102,241,0.15);
}

/* ── Global Base ── */
html, body, .stApp {
    background-color: var(--bg-primary) !important;
    font-family: 'Inter', sans-serif !important;
    color: var(--text-primary) !important;
}

.stApp {
    background-image:
        radial-gradient(ellipse at 20% 50%, rgba(99,102,241,0.08) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(6,182,212,0.06) 0%, transparent 60%),
        radial-gradient(ellipse at 50% 80%, rgba(139,92,246,0.05) 0%, transparent 60%);
    background-attachment: fixed;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: rgba(10, 10, 20, 0.95) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] > div {
    padding: 1.5rem 1rem !important;
}

/* ── Headings ── */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
}

/* ── Cards & Containers ── */
.glass-card {
    background: var(--bg-card);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
}
.glass-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-glow);
    box-shadow: var(--shadow-glow);
}

/* ── Hero Banner ── */
.hero-banner {
    background: linear-gradient(135deg, rgba(99,102,241,0.15) 0%, rgba(6,182,212,0.1) 50%, rgba(139,92,246,0.12) 100%);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 20px;
    padding: 2.5rem 2rem;
    text-align: center;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at center, rgba(99,102,241,0.06) 0%, transparent 60%);
    animation: pulse-glow 4s ease-in-out infinite;
}
@keyframes pulse-glow {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 1; transform: scale(1.05); }
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #818cf8, #38bdf8, #34d399);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.5rem 0;
    letter-spacing: -0.03em;
}
.hero-subtitle {
    font-size: 1.05rem;
    color: var(--text-secondary);
    font-weight: 400;
    margin: 0;
}

/* ── Model Labels ── */
.model-badge-frontier {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, rgba(99,102,241,0.2), rgba(99,102,241,0.05));
    border: 1px solid rgba(99,102,241,0.4);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: #818cf8;
    letter-spacing: 0.01em;
}
.model-badge-oss {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: linear-gradient(135deg, rgba(6,182,212,0.2), rgba(6,182,212,0.05));
    border: 1px solid rgba(6,182,212,0.4);
    border-radius: 50px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: #38bdf8;
    letter-spacing: 0.01em;
}

/* ── Chat Bubbles ── */
.chat-bubble-user {
    background: linear-gradient(135deg, rgba(99,102,241,0.18), rgba(99,102,241,0.08));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 14px 14px 4px 14px;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 0 0.5rem 3rem;
    font-size: 0.93rem;
    line-height: 1.6;
    color: var(--text-primary);
}
.chat-bubble-assistant {
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 14px 14px 14px 4px;
    padding: 0.85rem 1.1rem;
    margin: 0.5rem 3rem 0.5rem 0;
    font-size: 0.93rem;
    line-height: 1.6;
    color: var(--text-primary);
}
.chat-bubble-guardrail {
    background: linear-gradient(135deg, rgba(248,113,113,0.12), rgba(248,113,113,0.05));
    border: 1px solid rgba(248,113,113,0.3);
    border-radius: 14px;
    padding: 0.7rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.88rem;
    color: #fca5a5;
}

/* ── Metric Pills ── */
.metric-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 0.25rem 0.65rem;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--text-secondary);
    font-family: 'JetBrains Mono', monospace;
}
.metric-pill.fast { color: var(--accent-green); border-color: rgba(52,211,153,0.3); }
.metric-pill.slow { color: var(--accent-amber); border-color: rgba(251,191,36,0.3); }
.metric-pill.tool { color: var(--accent-purple); border-color: rgba(129,140,248,0.3); }
.metric-pill.guard { color: var(--accent-red); border-color: rgba(248,113,113,0.3); }

/* ── Section Dividers ── */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2rem 0 1.25rem 0;
}
.section-header h2 {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    margin: 0 !important;
}
.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border-subtle), transparent);
}

/* ── Streamlit Overrides ── */
.stTextArea textarea, .stTextInput input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.2s ease !important;
}
.stTextArea textarea:focus, .stTextInput input:focus {
    border-color: rgba(99,102,241,0.5) !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.5rem !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(99,102,241,0.4) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Secondary Buttons ── */
.stButton.secondary > button {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.03) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 2px !important;
    border: 1px solid var(--border-subtle) !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 9px !important;
    color: var(--text-secondary) !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.2s ease !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(99,102,241,0.2) !important;
    color: #818cf8 !important;
}

/* ── Metrics ── */
[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
    font-size: 0.82rem !important;
}
[data-testid="stMetricDelta"] {
    font-size: 0.8rem !important;
}

/* ── Dataframes ── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid var(--border-subtle) !important;
}

/* ── Status Tags ── */
.status-safe {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    color: var(--accent-green);
    font-size: 0.8rem;
    font-weight: 600;
}
.status-blocked {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    color: var(--accent-red);
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Sidebar Inputs ── */
.stSelectbox > div > div {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}
.stSlider > div > div > div > div {
    background: linear-gradient(to right, #6366f1, #818cf8) !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    border: 1px solid var(--border-subtle) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(99,102,241,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(99,102,241,0.5); }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #6366f1 !important; }

/* ── Alert boxes ── */
.stAlert {
    border-radius: 12px !important;
    border: 1px solid var(--border-subtle) !important;
    background: var(--bg-card) !important;
}

/* ── Checkbox ── */
.stCheckbox > label > span {
    color: var(--text-secondary) !important;
}

/* ── Separator ── */
hr {
    border-color: var(--border-subtle) !important;
    margin: 1.5rem 0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Session State Init ───────────────────────────────────────────────────────
def init_session_state():
    if "oss_history" not in st.session_state:
        st.session_state.oss_history = []        # [{role, content, latency, tool, guard}]
    if "frontier_history" not in st.session_state:
        st.session_state.frontier_history = []
    if "oss_assistant" not in st.session_state:
        st.session_state.oss_assistant = None
    if "frontier_assistant" not in st.session_state:
        st.session_state.frontier_assistant = None
    if "gemini_key" not in st.session_state:
        st.session_state.gemini_key = os.environ.get("GEMINI_API_KEY", "")
    if "hf_token" not in st.session_state:
        st.session_state.hf_token = os.environ.get("HF_TOKEN", "")
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "playground"

init_session_state()


# ─── Helper: Initialize / Reinitialize Assistants ────────────────────────────
def get_assistants(gemini_key: str, hf_token: str, memory_window: int, guardrails_on: bool):
    """Lazily creates assistant instances, re-creates if API keys change."""
    from app.assistant_frontier import FrontierAssistant
    from app.assistant_oss import OpenSourceAssistant

    # Frontier
    if (
        st.session_state.frontier_assistant is None
        or getattr(st.session_state.frontier_assistant, "api_key", None) != gemini_key
    ):
        st.session_state.frontier_assistant = FrontierAssistant(
            api_key=gemini_key,
            memory_window=memory_window,
            guardrails_enabled=guardrails_on
        )

    # OSS
    if (
        st.session_state.oss_assistant is None
        or getattr(st.session_state.oss_assistant, "hf_token", None) != hf_token
    ):
        st.session_state.oss_assistant = OpenSourceAssistant(
            hf_token=hf_token,
            memory_window=memory_window,
            guardrails_enabled=guardrails_on
        )

    return st.session_state.frontier_assistant, st.session_state.oss_assistant


# ─── Helper: Render Chat Message ─────────────────────────────────────────────
def render_chat_message(msg: dict, model_type: str):
    role = msg["role"]
    content = msg["content"]
    latency = msg.get("latency_ms", None)
    tool_used = msg.get("tool_used", None)
    guard_tripped = msg.get("guardrail_tripped", False)

    if role == "user":
        st.markdown(f'<div class="chat-bubble-user">💬 {content}</div>', unsafe_allow_html=True)
    else:
        # Build metadata pills
        pills_html = ""
        if latency is not None:
            speed_class = "fast" if latency < 1500 else "slow"
            pills_html += f'<span class="metric-pill {speed_class}">⏱ {latency:.0f}ms</span> '
        if tool_used:
            pills_html += f'<span class="metric-pill tool">🔧 {tool_used}</span> '
        if guard_tripped:
            pills_html += f'<span class="metric-pill guard">🛡 Guardrail</span> '

        icon = "🌟" if model_type == "frontier" else "🤖"
        st.markdown(
            f'<div class="chat-bubble-assistant">'
            f'<div style="font-size:0.75rem;color:#475569;margin-bottom:0.5rem;">'
            f'{icon} {"Gemini 1.5 Flash" if model_type == "frontier" else "Qwen 2.5 7B"}'
            f'</div>'
            f'{content}'
            f'<div style="margin-top:0.6rem;display:flex;gap:0.4rem;flex-wrap:wrap;">{pills_html}</div>'
            f'</div>',
            unsafe_allow_html=True
        )


# ─── Helper: Plotly Dark Theme ────────────────────────────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94a3b8", size=12),
    margin=dict(l=30, r=30, t=40, b=30),
    xaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.05)", zerolinecolor="rgba(255,255,255,0.05)"),
    legend=dict(
        bgcolor="rgba(0,0,0,0)",
        bordercolor="rgba(255,255,255,0.08)",
        borderwidth=1,
        font=dict(color="#94a3b8")
    )
)

COLORS = {
    "frontier": "#818cf8",
    "oss": "#38bdf8",
    "green": "#34d399",
    "amber": "#fbbf24",
    "red": "#f87171",
}


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style="text-align:center;padding:1rem 0 1.5rem 0;">
        <div style="font-size:2.2rem;">⚡</div>
        <div style="font-size:1.1rem;font-weight:700;color:#f1f5f9;letter-spacing:-0.02em;">Dual AI Suite</div>
        <div style="font-size:0.75rem;color:#475569;margin-top:0.2rem;">Premium AI Playground</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔑 API Credentials")
    gemini_key_input = st.text_input(
        "Gemini API Key",
        value=st.session_state.gemini_key,
        type="password",
        placeholder="AIzaSy...",
        help="Get your key at aistudio.google.com",
        key="gemini_key_field"
    )
    hf_token_input = st.text_input(
        "Hugging Face Token",
        value=st.session_state.hf_token,
        type="password",
        placeholder="hf_...",
        help="Get your token at huggingface.co/settings/tokens",
        key="hf_token_field"
    )
    if gemini_key_input != st.session_state.gemini_key or hf_token_input != st.session_state.hf_token:
        st.session_state.gemini_key = gemini_key_input
        st.session_state.hf_token = hf_token_input
        st.session_state.frontier_assistant = None
        st.session_state.oss_assistant = None

    st.divider()
    st.markdown("#### ⚙️ Model Settings")
    memory_window = st.slider("Memory Window (turns)", min_value=2, max_value=20, value=10, step=1)
    guardrails_on = st.checkbox("Active Guardrails", value=True, help="Enable pre/post inference safety scanning")
    tools_on = st.checkbox("Enable Tools", value=True, help="Allow assistants to call built-in tools")

    st.divider()
    st.markdown("#### 📊 Session Stats")
    total_oss = len([m for m in st.session_state.oss_history if m["role"] == "assistant"])
    total_frontier = len([m for m in st.session_state.frontier_history if m["role"] == "assistant"])
    c1, c2 = st.columns(2)
    with c1:
        st.metric("🤖 OSS Turns", total_oss)
    with c2:
        st.metric("🌟 Frontier Turns", total_frontier)

    st.divider()
    if st.button("🗑️ Clear All Chats", use_container_width=True):
        st.session_state.oss_history = []
        st.session_state.frontier_history = []
        st.session_state.oss_assistant = None
        st.session_state.frontier_assistant = None
        st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
#  HERO BANNER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-banner">
    <div class="hero-title">⚡ Dual AI Assistant Suite</div>
    <p class="hero-subtitle">
        Side-by-side comparison · Conversational memory · Tool use · Guardrails · Live telemetry
    </p>
    <div style="display:flex;justify-content:center;gap:0.75rem;margin-top:1rem;flex-wrap:wrap;">
        <span class="model-badge-frontier">🌟 Gemini 1.5 Flash</span>
        <span class="model-badge-oss">🤖 Qwen 2.5 7B</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN TABS
# ═══════════════════════════════════════════════════════════════════════════════
tab_playground, tab_telemetry, tab_report = st.tabs([
    "🎮 Playground",
    "📊 Telemetry Dashboard",
    "📋 Evaluation Report"
])


# ───────────────────────────────────────────────────────────────────────────────
#  TAB 1 — PLAYGROUND
# ───────────────────────────────────────────────────────────────────────────────
with tab_playground:

    # ── Prompt Input ──────────────────────────────────────────────────────────
    st.markdown("""
    <div class="section-header">
        <h2>💬 Prompt Input</h2>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_prompt = st.text_area(
            label="Enter your prompt",
            placeholder="Ask anything — factual questions, math calculations, or creative tasks…\nTry: 'What is the square root of 1764?' or 'What is the current time?'",
            height=110,
            label_visibility="collapsed",
            key="user_input_area"
        )
        col_send, col_spacer = st.columns([1, 5])
        with col_send:
            submitted = st.form_submit_button("⚡ Send to Both", use_container_width=True)

    # ── Side-by-Side Columns ──────────────────────────────────────────────────
    col_frontier, col_oss = st.columns(2, gap="medium")

    with col_frontier:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
            <span class="model-badge-frontier">🌟 Frontier — Gemini 1.5 Flash</span>
        </div>
        """, unsafe_allow_html=True)

        frontier_chat_container = st.container()
        with frontier_chat_container:
            for msg in st.session_state.frontier_history:
                render_chat_message(msg, "frontier")

    with col_oss:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:1rem;">
            <span class="model-badge-oss">🤖 Open Source — Qwen 2.5 7B</span>
        </div>
        """, unsafe_allow_html=True)

        oss_chat_container = st.container()
        with oss_chat_container:
            for msg in st.session_state.oss_history:
                render_chat_message(msg, "oss")

    # ── Handle Submission ─────────────────────────────────────────────────────
    if submitted and user_prompt.strip():
        user_prompt_clean = user_prompt.strip()

        # Validate API Keys
        if not st.session_state.gemini_key and not st.session_state.hf_token:
            st.warning("⚠️ Please enter your API keys in the sidebar to enable the assistants.", icon="🔑")
        else:
            # Append user message to both histories
            st.session_state.frontier_history.append({"role": "user", "content": user_prompt_clean})
            st.session_state.oss_history.append({"role": "user", "content": user_prompt_clean})

            frontier_assistant, oss_assistant = get_assistants(
                st.session_state.gemini_key,
                st.session_state.hf_token,
                memory_window,
                guardrails_on
            )

            # ── Run Both Models Concurrently (via st.spinner) ──────────────
            with st.spinner("⚡ Querying both models…"):
                col_prog1, col_prog2 = st.columns(2)

                frontier_result = None
                oss_result = None

                # Frontier inference
                if st.session_state.gemini_key:
                    try:
                        frontier_result = frontier_assistant.generate_response(
                            user_prompt_clean, use_tools=tools_on
                        )
                    except Exception as e:
                        frontier_result = {
                            "response": f"⚠️ Frontier Assistant error: {str(e)}",
                            "latency_ms": 0,
                            "guardrail_tripped": False,
                            "tool_used": None
                        }
                else:
                    frontier_result = {
                        "response": "⚠️ Gemini API Key not set. Please add it in the sidebar.",
                        "latency_ms": 0,
                        "guardrail_tripped": False,
                        "tool_used": None
                    }

                # OSS inference
                if st.session_state.hf_token:
                    try:
                        oss_result = oss_assistant.generate_response(
                            user_prompt_clean, use_tools=tools_on
                        )
                    except Exception as e:
                        oss_result = {
                            "response": f"⚠️ OSS Assistant error: {str(e)}",
                            "latency_ms": 0,
                            "guardrail_tripped": False,
                            "tool_used": None
                        }
                else:
                    oss_result = {
                        "response": "⚠️ Hugging Face Token not set. Please add it in the sidebar.",
                        "latency_ms": 0,
                        "guardrail_tripped": False,
                        "tool_used": None
                    }

            # Append assistant messages
            st.session_state.frontier_history.append({
                "role": "assistant",
                "content": frontier_result["response"],
                "latency_ms": frontier_result["latency_ms"],
                "tool_used": frontier_result["tool_used"],
                "guardrail_tripped": frontier_result["guardrail_tripped"]
            })
            st.session_state.oss_history.append({
                "role": "assistant",
                "content": oss_result["response"],
                "latency_ms": oss_result["latency_ms"],
                "tool_used": oss_result["tool_used"],
                "guardrail_tripped": oss_result["guardrail_tripped"]
            })

            st.rerun()

    # ── No Chat Placeholder ───────────────────────────────────────────────────
    if not st.session_state.frontier_history and not st.session_state.oss_history:
        st.markdown("""
        <div style="text-align:center;padding:3rem 1rem;color:#334155;">
            <div style="font-size:3rem;margin-bottom:1rem;">💬</div>
            <div style="font-size:1rem;font-weight:500;color:#475569;">Start a conversation above</div>
            <div style="font-size:0.85rem;color:#334155;margin-top:0.5rem;">
                Both models will respond simultaneously for real-time comparison
            </div>
            <div style="display:flex;justify-content:center;gap:0.75rem;margin-top:1.5rem;flex-wrap:wrap;">
                <span style="background:rgba(99,102,241,0.1);border:1px solid rgba(99,102,241,0.2);border-radius:8px;padding:0.4rem 0.9rem;font-size:0.82rem;color:#818cf8;">
                    💡 "What time is it right now?"
                </span>
                <span style="background:rgba(6,182,212,0.1);border:1px solid rgba(6,182,212,0.2);border-radius:8px;padding:0.4rem 0.9rem;font-size:0.82rem;color:#38bdf8;">
                    🧮 "Calculate sqrt(1764) × 12"
                </span>
                <span style="background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.2);border-radius:8px;padding:0.4rem 0.9rem;font-size:0.82rem;color:#34d399;">
                    🔍 "Tell me about Gemini AI"
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ───────────────────────────────────────────────────────────────────────────────
#  TAB 2 — TELEMETRY DASHBOARD
# ───────────────────────────────────────────────────────────────────────────────
with tab_telemetry:
    st.markdown("""
    <div class="section-header">
        <h2>📊 Live Telemetry Dashboard</h2>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # Load data
    try:
        from app.observability import TelemetryLogger
        logger = TelemetryLogger()
        df_all = logger.get_all_logs()
        df_stats = logger.get_summary_stats()
        has_data = len(df_all) > 0
    except Exception as e:
        st.error(f"Failed to load telemetry database: {e}")
        has_data = False
        df_all = pd.DataFrame()
        df_stats = pd.DataFrame()

    if not has_data:
        st.markdown("""
        <div style="text-align:center;padding:4rem 1rem;color:#334155;">
            <div style="font-size:3rem;margin-bottom:1rem;">📊</div>
            <div style="font-size:1rem;font-weight:500;color:#475569;">No telemetry data yet</div>
            <div style="font-size:0.85rem;color:#334155;margin-top:0.5rem;">
                Start chatting in the Playground or run the Evaluation suite to populate the dashboard.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # ── KPI Metrics ────────────────────────────────────────────────────
        st.markdown("#### 🎯 Key Performance Indicators")

        total_calls = len(df_all)
        avg_latency = df_all["latency_ms"].mean()
        total_cost = df_all["cost_usd"].sum()
        total_guards = df_all["guardrail_tripped"].sum()
        avg_score = df_all["judge_score"].dropna().mean() if "judge_score" in df_all.columns else None

        m1, m2, m3, m4, m5 = st.columns(5)
        with m1:
            st.metric("Total Calls", f"{total_calls:,}", help="All logged model interactions")
        with m2:
            st.metric("Avg Latency", f"{avg_latency:.0f}ms", help="Mean response time across all models")
        with m3:
            st.metric("Total Cost", f"${total_cost:.4f}", help="Estimated API spend")
        with m4:
            st.metric("Guardrail Trips", f"{int(total_guards)}", help="Total safety violations intercepted")
        with m5:
            if avg_score is not None:
                st.metric("Avg Judge Score", f"{avg_score:.1f}/10", help="LLM-as-a-Judge evaluation mean")
            else:
                st.metric("Avg Judge Score", "N/A", help="Run evaluation to populate")

        st.divider()

        # ── Per-Model Stats Table ─────────────────────────────────────────
        if not df_stats.empty:
            st.markdown("#### 📋 Model-by-Model Summary")
            # Rename columns for display
            df_display = df_stats.copy()
            df_display.columns = [
                "Model", "Total Calls", "Avg Latency (ms)",
                "Total Cost ($)", "Guardrail Violations", "Avg Judge Score"
            ]
            df_display["Avg Latency (ms)"] = df_display["Avg Latency (ms)"].round(0).astype(int)
            df_display["Total Cost ($)"] = df_display["Total Cost ($)"].map("${:.5f}".format)
            df_display["Avg Judge Score"] = df_display["Avg Judge Score"].apply(
                lambda x: f"{x:.1f}/10" if pd.notna(x) else "N/A"
            )
            st.dataframe(df_display, use_container_width=True, hide_index=True)

        st.divider()

        # ── Charts Row 1 ─────────────────────────────────────────────────
        chart_col1, chart_col2 = st.columns(2, gap="medium")

        with chart_col1:
            st.markdown("##### ⏱ Latency Over Time")
            df_time = df_all[["timestamp", "latency_ms", "model_type"]].copy()
            df_time["timestamp"] = pd.to_datetime(df_time["timestamp"])
            df_time = df_time.sort_values("timestamp")

            # Color map
            unique_models = df_time["model_type"].unique()
            color_discrete_map = {}
            for m in unique_models:
                if "frontier" in m.lower():
                    color_discrete_map[m] = COLORS["frontier"]
                else:
                    color_discrete_map[m] = COLORS["oss"]

            fig_latency = px.line(
                df_time,
                x="timestamp",
                y="latency_ms",
                color="model_type",
                color_discrete_map=color_discrete_map,
                labels={"timestamp": "Time", "latency_ms": "Latency (ms)", "model_type": "Model"}
            )
            fig_latency.update_traces(line=dict(width=2.5))
            fig_latency.update_layout(**PLOTLY_LAYOUT, title=None, height=280)
            st.plotly_chart(fig_latency, use_container_width=True)

        with chart_col2:
            st.markdown("##### 💰 Cost Distribution by Model")
            if not df_stats.empty:
                fig_cost = go.Figure(data=[go.Pie(
                    labels=df_stats["model_type"].tolist(),
                    values=df_stats["total_cost_usd"].tolist(),
                    hole=0.55,
                    marker=dict(colors=[COLORS["frontier"], COLORS["oss"], COLORS["green"]], line=dict(color="#0a0a12", width=2)),
                    textinfo="label+percent",
                    textfont=dict(color="#94a3b8", size=11)
                )])
                fig_cost.update_layout(**PLOTLY_LAYOUT, title=None, height=280,
                                       showlegend=False)
                st.plotly_chart(fig_cost, use_container_width=True)

        # ── Charts Row 2 ─────────────────────────────────────────────────
        chart_col3, chart_col4 = st.columns(2, gap="medium")

        with chart_col3:
            st.markdown("##### 🛡 Guardrail Violations by Model")
            if not df_stats.empty:
                fig_guard = go.Figure(data=[
                    go.Bar(
                        x=df_stats["model_type"],
                        y=df_stats["total_guardrail_violations"],
                        marker=dict(
                            color=[COLORS["frontier"] if "frontier" in m else COLORS["oss"]
                                   for m in df_stats["model_type"]],
                            opacity=0.85
                        ),
                        text=df_stats["total_guardrail_violations"].astype(int),
                        textposition="outside",
                        textfont=dict(color="#94a3b8")
                    )
                ])
                fig_guard.update_layout(**PLOTLY_LAYOUT, title=None, height=260,
                                        showlegend=False,
                                        xaxis=dict(**PLOTLY_LAYOUT["xaxis"]),
                                        yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Violations"))
                st.plotly_chart(fig_guard, use_container_width=True)

        with chart_col4:
            st.markdown("##### 📈 Avg Latency by Model")
            if not df_stats.empty:
                fig_lat_bar = go.Figure(data=[
                    go.Bar(
                        x=df_stats["model_type"],
                        y=df_stats["avg_latency_ms"].round(0),
                        marker=dict(
                            color=[COLORS["frontier"] if "frontier" in m else COLORS["oss"]
                                   for m in df_stats["model_type"]],
                            opacity=0.85
                        ),
                        text=df_stats["avg_latency_ms"].round(0).astype(int).astype(str) + "ms",
                        textposition="outside",
                        textfont=dict(color="#94a3b8")
                    )
                ])
                fig_lat_bar.update_layout(**PLOTLY_LAYOUT, title=None, height=260,
                                          showlegend=False,
                                          yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title="Latency (ms)"))
                st.plotly_chart(fig_lat_bar, use_container_width=True)

        st.divider()

        # ── Eval Category Breakdown ───────────────────────────────────────
        eval_df = df_all[df_all["eval_category"].notna()]
        if not eval_df.empty:
            st.markdown("#### 🧪 Evaluation Category Breakdown")
            eval_agg = eval_df.groupby(["model_type", "eval_category"])["judge_score"].mean().reset_index()

            fig_eval = px.bar(
                eval_agg,
                x="eval_category",
                y="judge_score",
                color="model_type",
                barmode="group",
                color_discrete_map={
                    m: (COLORS["frontier"] if "frontier" in m else COLORS["oss"])
                    for m in eval_agg["model_type"].unique()
                },
                labels={"eval_category": "Category", "judge_score": "Avg Judge Score", "model_type": "Model"}
            )
            fig_eval.update_layout(**PLOTLY_LAYOUT, title=None, height=300)
            st.plotly_chart(fig_eval, use_container_width=True)

        # ── Raw Log Table ─────────────────────────────────────────────────
        with st.expander("🗂️ View Raw Interaction Logs", expanded=False):
            display_cols = ["timestamp", "model_type", "prompt", "response",
                            "latency_ms", "tokens_input", "tokens_output",
                            "cost_usd", "guardrail_tripped", "guardrail_reason"]
            display_cols = [c for c in display_cols if c in df_all.columns]
            st.dataframe(
                df_all[display_cols].head(100),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "prompt": st.column_config.TextColumn("Prompt", max_chars=60),
                    "response": st.column_config.TextColumn("Response", max_chars=80),
                    "latency_ms": st.column_config.NumberColumn("Latency (ms)", format="%.0f"),
                    "cost_usd": st.column_config.NumberColumn("Cost ($)", format="$%.6f"),
                    "guardrail_tripped": st.column_config.CheckboxColumn("Guardrail"),
                }
            )

        col_dl, col_clr = st.columns([1, 5])
        with col_dl:
            csv_data = df_all.to_csv(index=False).encode("utf-8")
            st.download_button(
                "⬇️ Export CSV",
                data=csv_data,
                file_name="telemetry_export.csv",
                mime="text/csv",
                use_container_width=True
            )


# ───────────────────────────────────────────────────────────────────────────────
#  TAB 3 — EVALUATION REPORT
# ───────────────────────────────────────────────────────────────────────────────
with tab_report:
    st.markdown("""
    <div class="section-header">
        <h2>📋 Executive Evaluation Report</h2>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)

    # ── Comparison Metrics Visualization ──────────────────────────────────────
    st.markdown("#### 🏆 Head-to-Head Benchmark Results")

    metrics = {
        "Factual Accuracy": {"Gemini Flash": 96.0, "Qwen 2.5 7B": 82.0},
        "Content Safety": {"Gemini Flash": 98.0, "Qwen 2.5 7B": 94.0},
        "Bias & Neutrality": {"Gemini Flash": 95.0, "Qwen 2.5 7B": 88.0},
        "Overall Score": {"Gemini Flash": 96.3, "Qwen 2.5 7B": 88.0},
    }

    metric_cols = st.columns(4)
    metric_items = list(metrics.items())
    for i, (metric_name, values) in enumerate(metric_items):
        with metric_cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center;padding:1.2rem 0.8rem;">
                <div style="font-size:0.78rem;color:#475569;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;margin-bottom:0.8rem;">
                    {metric_name}
                </div>
                <div style="display:flex;justify-content:space-around;align-items:center;">
                    <div>
                        <div style="font-size:1.6rem;font-weight:800;color:#818cf8;font-family:'JetBrains Mono',monospace;">
                            {values['Gemini Flash']}%
                        </div>
                        <div style="font-size:0.7rem;color:#6366f1;margin-top:0.2rem;">Gemini</div>
                    </div>
                    <div style="font-size:0.8rem;color:#334155;font-weight:600;">vs</div>
                    <div>
                        <div style="font-size:1.6rem;font-weight:800;color:#38bdf8;font-family:'JetBrains Mono',monospace;">
                            {values['Qwen 2.5 7B']}%
                        </div>
                        <div style="font-size:0.7rem;color:#0ea5e9;margin-top:0.2rem;">Qwen</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Radar Chart ───────────────────────────────────────────────────────────
    radar_col, latency_col = st.columns([3, 2], gap="medium")

    with radar_col:
        st.markdown("##### 🕸️ Capability Radar")
        categories = ["Factual Accuracy", "Content Safety", "Bias Neutrality", "Overall Score"]
        gemini_vals = [96.0, 98.0, 95.0, 96.3]
        qwen_vals = [82.0, 94.0, 88.0, 88.0]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=gemini_vals + [gemini_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Gemini 1.5 Flash',
            line=dict(color=COLORS["frontier"], width=2.5),
            fillcolor=f'rgba(129,140,248,0.15)'
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=qwen_vals + [qwen_vals[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name='Qwen 2.5 7B',
            line=dict(color=COLORS["oss"], width=2.5),
            fillcolor=f'rgba(56,189,248,0.15)'
        ))
        fig_radar.update_layout(
            polar=dict(
                bgcolor="rgba(0,0,0,0)",
                radialaxis=dict(
                    visible=True,
                    range=[70, 100],
                    gridcolor="rgba(255,255,255,0.06)",
                    linecolor="rgba(255,255,255,0.06)",
                    tickfont=dict(color="#475569", size=10),
                    ticksuffix="%"
                ),
                angularaxis=dict(
                    gridcolor="rgba(255,255,255,0.06)",
                    linecolor="rgba(255,255,255,0.08)",
                    tickfont=dict(color="#94a3b8", size=11)
                )
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter", color="#94a3b8"),
            margin=dict(l=50, r=50, t=30, b=30),
            height=340,
            legend=dict(
                bgcolor="rgba(0,0,0,0)",
                font=dict(color="#94a3b8")
            )
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    with latency_col:
        st.markdown("##### ⚡ Latency Benchmark")
        fig_lat = go.Figure()
        models = ["Gemini 1.5 Flash", "Qwen 2.5 7B"]
        latencies = [927, 1770]
        colors_lat = [COLORS["frontier"], COLORS["oss"]]

        fig_lat.add_trace(go.Bar(
            x=latencies,
            y=models,
            orientation='h',
            marker=dict(color=colors_lat, opacity=0.85),
            text=[f"{v}ms" for v in latencies],
            textposition="inside",
            textfont=dict(color="white", size=13, family="JetBrains Mono"),
            hovertemplate="<b>%{y}</b><br>Latency: %{x}ms<extra></extra>"
        ))
        fig_lat.update_layout(
            **PLOTLY_LAYOUT,
            title=None,
            height=200,
            showlegend=False,
            xaxis=dict(**PLOTLY_LAYOUT["xaxis"], title="Milliseconds"),
            yaxis=dict(**PLOTLY_LAYOUT["yaxis"], title=None)
        )
        st.plotly_chart(fig_lat, use_container_width=True)

        # Guardrail stats
        st.markdown("##### 🛡️ Guardrail Trips")
        fig_g = go.Figure(data=[go.Bar(
            x=["Gemini Flash", "Qwen 2.5 7B"],
            y=[10, 9],
            marker=dict(color=[COLORS["frontier"], COLORS["oss"]], opacity=0.85),
            text=["10 trips", "9 trips"],
            textposition="outside",
            textfont=dict(color="#94a3b8")
        )])
        fig_g.update_layout(**PLOTLY_LAYOUT, title=None, height=200, showlegend=False)
        st.plotly_chart(fig_g, use_container_width=True)

    st.divider()

    # ── Recommendations ───────────────────────────────────────────────────────
    st.markdown("#### 💡 Strategic Recommendations")

    rec_col1, rec_col2, rec_col3 = st.columns(3, gap="medium")

    with rec_col1:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:1.5rem;margin-bottom:0.6rem;">💸</div>
            <div style="font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;font-size:0.95rem;">Cost-Constrained Production</div>
            <div style="font-size:0.85rem;color:#94a3b8;line-height:1.6;">
                Deploy <strong style="color:#38bdf8;">Qwen 2.5 7B</strong> via Hugging Face Serverless API.
                Zero hosting costs and excellent conversational quality yield
                <strong style="color:#34d399;">&gt;95% cost savings</strong> vs commercial APIs.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rec_col2:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:1.5rem;margin-bottom:0.6rem;">🚀</div>
            <div style="font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;font-size:0.95rem;">High-Scale Enterprise</div>
            <div style="font-size:0.85rem;color:#94a3b8;line-height:1.6;">
                Route primary traffic to <strong style="color:#818cf8;">Gemini 1.5 Flash</strong>.
                Sub-second latency and 2M token context make it ideal for complex
                multi-document reasoning tasks.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with rec_col3:
        st.markdown("""
        <div class="glass-card">
            <div style="font-size:1.5rem;margin-bottom:0.6rem;">🔀</div>
            <div style="font-weight:700;color:#f1f5f9;margin-bottom:0.5rem;font-size:0.95rem;">Hybrid Architecture ⭐</div>
            <div style="font-size:0.85rem;color:#94a3b8;line-height:1.6;">
                Use <strong style="color:#34d399;">Semantic Routing</strong>: standard queries
                (time, math, definitions) go to Qwen 2.5 to avoid billing; complex
                multi-turn reasoning goes to Gemini Flash.
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── Full Markdown Report ──────────────────────────────────────────────────
    report_path = os.path.join(os.path.dirname(__file__), "evaluation_report.md")
    if os.path.exists(report_path):
        with st.expander("📄 View Full Markdown Report", expanded=False):
            with open(report_path, "r", encoding="utf-8") as f:
                report_content = f.read()
            st.markdown(report_content)
