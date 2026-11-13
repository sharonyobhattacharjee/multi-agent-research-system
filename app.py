"""
NEXUS // Multi-Agent Research Intelligence System

Run:
    python -m streamlit run app.py

Architecture:
    Search Agent -> Reader Agent -> Writer Agent -> Critic Agent
"""

import html
import inspect
import os
import re
import textwrap
import time
from datetime import datetime

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


# ============================================================
# 01. PAGE CONFIGURATION (must be the first Streamlit call)
# ============================================================

st.set_page_config(
    page_title="NEXUS | Research Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 02. HELPERS FOR STREAMLIT-VERSION COMPATIBILITY AND HTML
# ============================================================

def _stretch_kwargs() -> dict:
    """
    Newer Streamlit replaced `use_container_width=True` with
    `width="stretch"`. Pick whichever this install supports.
    """
    try:
        if "width" in inspect.signature(st.button).parameters:
            return {"width": "stretch"}
    except (TypeError, ValueError):
        pass
    return {"use_container_width": True}


STRETCH = _stretch_kwargs()


def compact_html(block: str) -> str:
    """
    Collapse an HTML snippet into ONE line.

    Streamlit renders st.markdown() through a Markdown parser. Blank lines
    end an HTML block, and any line indented 4+ spaces afterwards becomes a
    code block, which would show raw HTML on screen. A single line avoids it.
    """
    return " ".join(line.strip() for line in block.splitlines() if line.strip())


# ============================================================
# 03. DESIGN SYSTEM
# ============================================================

CSS = textwrap.dedent(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #080b10;
        --panel: #0d121a;
        --panel2: #111925;
        --border: rgba(125, 160, 190, 0.16);
        --cyan: #54e7f2;
        --green: #8af5b5;
        --muted: #8291a5;
        --text: #e7eef7;
        --red: #ff647c;
    }

    /* Apply Inter to text only. A wildcard like [class*="css"] also hits the
       Material icon font and turns expander arrows into raw words. */
    html, body, .stApp, .stApp p, .stApp label, .stApp button,
    .stApp input, .stApp textarea, .stApp h1, .stApp h2, .stApp h3,
    .stApp h4, .stApp h5, .stApp h6, .stApp li {
        font-family: 'Inter', sans-serif;
    }

    [data-testid="stIconMaterial"],
    .material-symbols-rounded,
    .material-icons {
        font-family: 'Material Symbols Rounded', 'Material Icons' !important;
    }

    .stApp {
        background:
            radial-gradient(circle at 85% 5%, rgba(40, 180, 200, 0.07), transparent 28%),
            radial-gradient(circle at 5% 40%, rgba(30, 100, 160, 0.06), transparent 30%),
            var(--bg);
        color: var(--text);
    }

    header[data-testid="stHeader"] { background: transparent; }
    #MainMenu, footer { visibility: hidden; }

    .block-container {
        max-width: 1450px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #090e15;
        border-right: 1px solid var(--border);
    }

    /* Brand */
    .brand { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
    .brand-symbol {
        width: 42px; height: 42px;
        border: 1px solid rgba(84, 231, 242, .5);
        background: rgba(84, 231, 242, .08);
        color: var(--cyan);
        display: flex; align-items: center; justify-content: center;
        font-size: 25px; border-radius: 12px;
        box-shadow: 0 0 22px rgba(84, 231, 242, .10);
    }
    .brand-name { font-size: 1.05rem; font-weight: 800; letter-spacing: 2px; color: var(--text); }
    .brand-sub {
        font-family: 'DM Mono', monospace;
        font-size: .62rem; letter-spacing: 2px; color: var(--muted); margin-top: 3px;
    }

    /* Top system bar */
    .system-bar {
        display: flex; align-items: center; justify-content: space-between;
        gap: 12px; padding: 10px 15px;
        border: 1px solid var(--border); border-radius: 10px;
        background: rgba(13, 18, 26, .85);
        margin-bottom: 25px; flex-wrap: wrap;
    }
    .system-label {
        font-family: 'DM Mono', monospace;
        font-size: .69rem; letter-spacing: 1.5px; color: var(--muted);
    }
    .system-online {
        color: var(--green);
        font-family: 'DM Mono', monospace;
        font-size: .68rem; letter-spacing: 1px;
    }
    .online-dot {
        display: inline-block; width: 7px; height: 7px; border-radius: 50%;
        background: var(--green); margin-right: 7px; box-shadow: 0 0 10px var(--green);
    }

    /* Hero */
    .hero {
        position: relative; overflow: hidden;
        border: 1px solid rgba(84, 231, 242, .2);
        border-radius: 18px; padding: 34px;
        background: linear-gradient(110deg, rgba(13, 27, 39, .98), rgba(10, 16, 26, .96));
        margin-bottom: 24px;
    }
    .hero::after {
        content: "◈"; position: absolute; right: 45px; top: -40px;
        font-size: 190px; color: rgba(84, 231, 242, .045); pointer-events: none;
    }
    .eyebrow {
        color: var(--cyan);
        font-family: 'DM Mono', monospace;
        font-size: .7rem; letter-spacing: 3px; margin-bottom: 14px;
    }
    .hero h1 {
        color: #f2f8ff;
        font-size: clamp(2rem, 4vw, 3.2rem);
        font-weight: 800; letter-spacing: -1.8px; line-height: 1.1; margin: 0;
    }
    .hero h1 span { color: var(--cyan); }
    .hero p {
        color: #9baec0; font-size: .95rem; max-width: 650px;
        line-height: 1.8; margin-top: 15px; margin-bottom: 0;
    }

    /* Section headers */
    .section-head { display: flex; align-items: center; gap: 10px; margin: 27px 0 14px 0; }
    .section-index {
        font-family: 'DM Mono', monospace;
        font-size: .7rem; color: var(--cyan); letter-spacing: 1px;
    }
    .section-title {
        font-size: .88rem; font-weight: 700; color: #e6eef7;
        letter-spacing: 1.3px; text-transform: uppercase;
    }
    .section-line { height: 1px; flex: 1; background: var(--border); }

    /* Agent cards */
    .agent-grid {
        display: grid; grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px; margin: 15px 0 25px 0;
    }
    .agent-card {
        background: linear-gradient(145deg, #111a25, #0c121b);
        border: 1px solid var(--border); border-radius: 13px;
        padding: 17px; min-height: 130px; transition: .2s ease;
    }
    .agent-card.running { border-color: var(--cyan); box-shadow: 0 0 22px rgba(84, 231, 242, .10); }
    .agent-card.done { border-color: rgba(138, 245, 181, .55); }
    .agent-card.error { border-color: var(--red); }
    .agent-icon { font-size: 1.3rem; margin-bottom: 13px; color: var(--text); }
    .agent-name { color: #eaf3fc; font-size: .87rem; font-weight: 700; letter-spacing: .5px; }
    .agent-desc { color: var(--muted); font-size: .72rem; margin-top: 5px; line-height: 1.5; }
    .agent-status {
        color: var(--muted);
        font-family: 'DM Mono', monospace;
        font-size: .62rem; letter-spacing: 1px; margin-top: 12px;
    }
    .agent-card.done .agent-status { color: var(--green); }
    .agent-card.running .agent-status { color: var(--cyan); }
    .agent-card.error .agent-status { color: var(--red); }

    /* Metrics */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, #111a25, #0c121b);
        border: 1px solid var(--border); padding: 17px; border-radius: 12px;
    }
    div[data-testid="stMetricLabel"] { color: var(--muted); font-size: .75rem; }
    div[data-testid="stMetricValue"] { color: var(--cyan); font-family: 'DM Mono', monospace; }

    /* Inputs */
    .stTextInput input {
        background: #0c131d !important;
        border: 1px solid rgba(84, 231, 242, .25) !important;
        border-radius: 10px !important;
        color: #edf7ff !important;
        min-height: 48px;
    }
    .stTextInput input:focus {
        border-color: var(--cyan) !important;
        box-shadow: 0 0 0 2px rgba(84, 231, 242, .10) !important;
    }
    .stTextInput label, .stSlider label { color: #b6c4d3 !important; }

    /* Buttons */
    .stButton > button, .stDownloadButton > button {
        border-radius: 9px; min-height: 40px;
        border: 1px solid var(--border);
        background: #111a25; color: #dceaf5;
        font-weight: 600; transition: .2s ease;
    }
    .stButton > button:hover, .stDownloadButton > button:hover {
        border-color: var(--cyan); color: var(--cyan); background: #12212c;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #087f91, #0d9caa);
        border: 1px solid #37d4e2; color: #ffffff;
        font-weight: 800; letter-spacing: .6px; min-height: 48px;
        box-shadow: 0 5px 22px rgba(40, 200, 220, .13);
    }
    .stButton > button[kind="primary"]:hover {
        background: #12a8b9; color: white;
        box-shadow: 0 5px 28px rgba(40, 200, 220, .25);
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; border-bottom: 1px solid var(--border); }
    .stTabs [data-baseweb="tab"] {
        background: transparent; color: #91a2b5;
        border-radius: 8px 8px 0 0; font-size: .82rem;
    }
    .stTabs [aria-selected="true"] {
        color: var(--cyan) !important;
        border-bottom: 2px solid var(--cyan) !important;
    }

    /* Panels */
    .terminal {
        background: #070c12;
        border: 1px solid rgba(84, 231, 242, .17);
        border-radius: 10px; padding: 16px;
        font-family: 'DM Mono', monospace;
        color: #a9c2d2; font-size: .78rem; line-height: 1.7;
    }
    .terminal .ok { color: var(--green); }
    .terminal .bad { color: var(--red); }

    .source-item {
        background: #101923; border: 1px solid var(--border);
        border-radius: 9px; padding: 13px; margin-bottom: 9px;
        overflow-wrap: anywhere;
    }
    .source-item a { color: var(--cyan); text-decoration: none; font-size: .82rem; }
    .source-item a:hover { text-decoration: underline; }

    hr { border-color: var(--border) !important; }
    [data-testid="stCaptionContainer"] { color: var(--muted); }

    /* Responsive */
    @media (max-width: 900px) {
        .agent-grid { grid-template-columns: repeat(2, 1fr); }
        .hero { padding: 25px; }
    }
    @media (max-width: 500px) {
        .hero h1 { font-size: 2rem; }
    }
    </style>
    """
).strip()

st.markdown(CSS, unsafe_allow_html=True)


# ============================================================
# 04. CONSTANTS
# ============================================================

AGENTS = [
    {
        "icon": "⌕",
        "name": "SEARCH ENGINE",
        "description": "Web discovery and source identification",
    },
    {
        "icon": "▤",
        "name": "INTELLIGENCE READER",
        "description": "Webpage extraction and content analysis",
    },
    {
        "icon": "✧",
        "name": "REPORT SYNTHESIS",
        "description": "Research synthesis and report generation",
    },
    {
        "icon": "◈",
        "name": "QUALITY CRITIC",
        "description": "Evaluation, verification and feedback",
    },
]

EXAMPLES = [
    "The future of autonomous AI agents",
    "Impact of generative AI on software engineering",
    "Latest advances in quantum computing",
    "Solid-state battery technology in 2026",
]

# Excludes markdown characters (* and `) so "**https://x.com**" is captured cleanly.
URL_PATTERN = re.compile(r"https?://[^\s\)\]\}>\"'<,*`]+")

AGENT_CONFIG = {"recursion_limit": 25}


# ============================================================
# 05. SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "current" not in st.session_state:
    st.session_state.current = None

if "topic_input" not in st.session_state:
    st.session_state.topic_input = ""


# ============================================================
# 06. UTILITY FUNCTIONS
# ============================================================

def to_text(content) -> str:
    """
    Convert LangChain message content into plain text.

    Gemini 2.5 can return `content` as a list of blocks (text, thinking,
    signatures...). Only the text blocks are kept.
    """
    if content is None:
        return ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        parts = [to_text(item) for item in content]
        return "\n".join(part for part in parts if part)

    if isinstance(content, dict):
        block_type = content.get("type")

        if block_type in (None, "text"):
            return to_text(content.get("text", content.get("content", "")))

        return ""  # thinking / tool_use / signature blocks are skipped

    if hasattr(content, "content"):
        return to_text(content.content)

    return str(content)


def last_message_text(result) -> str:
    """Final message text of a LangChain agent result."""
    messages = result.get("messages", []) if isinstance(result, dict) else []

    if not messages:
        return ""

    return to_text(messages[-1]).strip()


def tool_output_text(result) -> str:
    """Concatenate the raw output of every tool call made by an agent."""
    outputs = []

    messages = result.get("messages", []) if isinstance(result, dict) else []

    for message in messages:
        if getattr(message, "type", None) == "tool":
            text = to_text(getattr(message, "content", "")).strip()

            if text:
                outputs.append(text)

    return "\n\n".join(outputs)


def truncate_clean(text: str, limit: int) -> str:
    """Cut text at a limit without slicing a URL or line in half."""
    if len(text) <= limit:
        return text

    cut = text[:limit]
    boundary = cut.rfind("\n")

    if boundary > limit * 0.6:
        cut = cut[:boundary]

    return cut


def extract_urls(*texts) -> list:
    """Find unique URLs, preserving first-seen order."""
    seen = set()
    urls = []

    for text in texts:
        for url in URL_PATTERN.findall(text or ""):
            url = url.rstrip(".,;:!?)")

            if url and url not in seen:
                seen.add(url)
                urls.append(url)

    return urls


def render_section(index, title):
    st.markdown(
        compact_html(
            f"""
            <div class="section-head">
                <span class="section-index">{html.escape(index)}</span>
                <span class="section-title">{html.escape(title)}</span>
                <span class="section-line"></span>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def render_agent_cards(placeholder, statuses, timings):
    """Render the four agent execution cards."""
    labels = {
        "running": "PROCESSING",
        "done": "COMPLETED",
        "error": "FAILED",
    }

    cards = []

    for i, agent in enumerate(AGENTS):
        status = statuses[i]
        label = labels.get(status, "STANDBY")
        timing = f"{timings[i]:.1f}s" if timings[i] is not None else "--"

        cards.append(
            compact_html(
                f"""
                <div class="agent-card {status}">
                    <div class="agent-icon">{agent['icon']}</div>
                    <div class="agent-name">{agent['name']}</div>
                    <div class="agent-desc">{agent['description']}</div>
                    <div class="agent-status">{label} &nbsp;//&nbsp; {timing}</div>
                </div>
                """
            )
        )

    placeholder.markdown(
        '<div class="agent-grid">' + "".join(cards) + "</div>",
        unsafe_allow_html=True,
    )


def make_export(topic, state):
    """Create a Markdown export of the research."""
    sources = "\n".join(f"- {url}" for url in state.get("urls", []))

    return f"""# {topic}

**Generated:** {state.get("generated_at", "")}

---

{state.get("report", "")}

---

# Critic Evaluation

{state.get("feedback", "")}

---

# Sources

{sources}
"""


def key_status(name: str) -> str:
    ok = bool(os.getenv(name))
    css = "ok" if ok else "bad"
    text = "SET" if ok else "MISSING"
    return f'<span class="{css}">{text}</span>'


# ---------- callbacks ----------

def set_topic(topic):
    st.session_state.topic_input = topic


def load_history(index):
    if 0 <= index < len(st.session_state.history):
        st.session_state.current = st.session_state.history[index]


def clear_history():
    st.session_state.history = []
    st.session_state.current = None


# ============================================================
# 07. RESEARCH EXECUTION ENGINE
# ============================================================

def run_pipeline_with_ui(topic, search_chars, agent_placeholder, log_placeholder):
    # Imported lazily so missing API keys show up as a readable error in the
    # UI instead of crashing the whole page at startup.
    from agents import (
        build_search_agent,
        build_reader_agent,
        writer_chain,
        critic_chain,
    )

    statuses = ["pending"] * 4
    timings = [None] * 4
    state = {}

    def refresh():
        render_agent_cards(agent_placeholder, statuses, timings)

    def start_agent(index, message):
        statuses[index] = "running"
        refresh()
        log_placeholder.info(message)
        return time.time()

    def finish_agent(index, start_time):
        timings[index] = time.time() - start_time
        statuses[index] = "done"
        refresh()

    refresh()
    total_start = time.time()

    try:
        # ----------------------------------------------------
        # AGENT 01: SEARCH
        # ----------------------------------------------------
        t0 = start_agent(
            0,
            "SEARCH ENGINE // Discovering relevant information and sources...",
        )

        search_result = build_search_agent().invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Find recent, reliable and relevant information "
                            f"about this research topic: {topic}. "
                            "Use the web search tool. Return source titles, "
                            "URLs and useful findings."
                        ),
                    }
                ]
            },
            config=AGENT_CONFIG,
        )

        search_raw = tool_output_text(search_result)
        state["search_results"] = last_message_text(search_result) or search_raw

        if not state["search_results"]:
            raise RuntimeError("The search agent returned no output.")

        finish_agent(0, t0)

        # ----------------------------------------------------
        # AGENT 02: READER
        # ----------------------------------------------------
        t0 = start_agent(
            1,
            "INTELLIGENCE READER // Extracting relevant webpage content...",
        )

        # Prefer the raw tool output: it always contains the real URLs.
        reader_input = truncate_clean(search_raw or state["search_results"], search_chars)

        reader_result = build_reader_agent().invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            f"Research topic: {topic}\n\n"
                            "Review the search results below. Select the "
                            "most relevant URLs and scrape their content "
                            "using the webpage scraping tool. Prioritize "
                            "reliable and authoritative sources. Do not "
                            "invent webpage content.\n\n"
                            f"SEARCH RESULTS:\n{reader_input}"
                        ),
                    }
                ]
            },
            config=AGENT_CONFIG,
        )

        scrape_raw = tool_output_text(reader_result)
        state["scraped_content"] = (
            last_message_text(reader_result)
            or scrape_raw
            or "No webpage content could be extracted."
        )

        finish_agent(1, t0)

        # ----------------------------------------------------
        # AGENT 03: WRITER
        # ----------------------------------------------------
        t0 = start_agent(
            2,
            "REPORT SYNTHESIS // Generating structured research report...",
        )

        combined_research = (
            f"SEARCH RESULTS:\n{state['search_results']}\n\n"
            f"SCRAPED CONTENT:\n{state['scraped_content']}"
        )

        state["report"] = to_text(
            writer_chain.invoke({"topic": topic, "research": combined_research})
        ).strip()

        if not state["report"]:
            raise RuntimeError("The writer agent returned an empty report.")

        finish_agent(2, t0)

        # ----------------------------------------------------
        # AGENT 04: CRITIC
        # ----------------------------------------------------
        t0 = start_agent(
            3,
            "QUALITY CRITIC // Evaluating report quality...",
        )

        state["feedback"] = to_text(
            critic_chain.invoke({"report": state["report"]})
        ).strip()

        finish_agent(3, t0)

    except Exception:
        for i, status in enumerate(statuses):
            if status == "running":
                statuses[i] = "error"

        refresh()
        raise

    # --------------------------------------------------------
    # FINAL OUTPUT
    # --------------------------------------------------------
    state["search_raw"] = search_raw
    state["scrape_raw"] = scrape_raw

    state["urls"] = extract_urls(
        search_raw,
        scrape_raw,
        state["search_results"],
        state["scraped_content"],
        state["report"],
    )

    state["elapsed"] = time.time() - total_start
    state["step_times"] = timings
    state["generated_at"] = datetime.now().strftime("%d %b %Y | %H:%M")

    return state


# ============================================================
# 08. SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown(
        compact_html(
            """
            <div class="brand">
                <div class="brand-symbol">◈</div>
                <div>
                    <div class="brand-name">NEXUS</div>
                    <div class="brand-sub">RESEARCH INTELLIGENCE</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.markdown("##### SYSTEM CONFIGURATION")

    search_chars = st.slider(
        "Reader context size",
        min_value=800,
        max_value=6000,
        value=4000,
        step=400,
        help="Maximum search-result characters passed to the Reader Agent.",
    )

    st.caption("Higher context may increase model token usage.")

    st.markdown("---")
    st.markdown("##### EXECUTION HISTORY")

    if not st.session_state.history:
        st.caption("No previous research sessions.")
    else:
        for index in range(len(st.session_state.history) - 1, -1, -1):
            item = st.session_state.history[index]
            label = item["topic"]

            if len(label) > 32:
                label = label[:29] + "..."

            st.button(
                f"◈  {label}",
                key=f"history_{index}",
                on_click=load_history,
                args=(index,),
                **STRETCH,
            )

        st.button(
            "CLEAR SESSION HISTORY",
            key="clear_history",
            on_click=clear_history,
            **STRETCH,
        )

    st.markdown("---")

    all_keys_ok = bool(os.getenv("GEMINI_API_KEY")) and bool(os.getenv("TAVILY_API_KEY"))
    status_line = (
        '<span class="ok">READY</span>'
        if all_keys_ok
        else '<span class="bad">API KEY MISSING</span>'
    )

    st.markdown(
        compact_html(
            f"""
            <div class="terminal">
                SYSTEM: NEXUS CORE<br>
                ARCHITECTURE: MULTI-AGENT<br>
                EXECUTION: SEQUENTIAL<br>
                SEARCH: TAVILY [{key_status("TAVILY_API_KEY")}]<br>
                INTELLIGENCE: GEMINI [{key_status("GEMINI_API_KEY")}]<br>
                STATUS: {status_line}
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("")
    st.caption("NEXUS // Research Intelligence System")


# ============================================================
# 09. MAIN HEADER
# ============================================================

st.markdown(
    compact_html(
        """
        <div class="system-bar">
            <div class="system-label">NEXUS / INTELLIGENCE DIVISION / CONTROL TERMINAL</div>
            <div class="system-online"><span class="online-dot"></span>SYSTEM READY</div>
        </div>
        <div class="hero">
            <div class="eyebrow">AUTONOMOUS RESEARCH FRAMEWORK // V1.0</div>
            <h1>Intelligence.<br><span>Engineered.</span></h1>
            <p>
                An autonomous multi-agent research system.
                Four specialised AI agents collaborate to discover
                information, extract knowledge, synthesize reports
                and critically evaluate research.
            </p>
        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ============================================================
# 10. AGENT ARCHITECTURE
# ============================================================

render_section("01 /", "Agent architecture")

architecture_placeholder = st.empty()
render_agent_cards(architecture_placeholder, ["pending"] * 4, [None] * 4)


# ============================================================
# 11. RESEARCH CONSOLE
# ============================================================

render_section("02 /", "Research command console")

st.markdown("##### DEFINE YOUR RESEARCH OBJECTIVE")

topic = st.text_input(
    "Research topic",
    key="topic_input",
    placeholder="Enter a research objective...",
    label_visibility="collapsed",
)

col_run, col_info = st.columns([1, 3])

with col_run:
    run_clicked = st.button(
        "INITIALIZE RESEARCH  →",
        type="primary",
        **STRETCH,
    )

with col_info:
    st.caption("Initiates the four-stage autonomous research workflow.")

st.markdown(
    '<div class="system-label">SUGGESTED RESEARCH OBJECTIVES</div>',
    unsafe_allow_html=True,
)

example_columns = st.columns(4)

for column, example in zip(example_columns, EXAMPLES):
    column.button(
        example,
        key=f"example_{example}",
        on_click=set_topic,
        args=(example,),
        **STRETCH,
    )


# ============================================================
# 12. EXECUTION
# ============================================================

if run_clicked:
    clean_topic = (topic or "").strip()

    if not clean_topic:
        st.warning("Enter a research objective before initializing.")
    else:
        render_section("03 /", "Live execution")

        agent_placeholder = st.empty()
        log_placeholder = st.empty()

        try:
            result = run_pipeline_with_ui(
                topic=clean_topic,
                search_chars=search_chars,
                agent_placeholder=agent_placeholder,
                log_placeholder=log_placeholder,
            )

            log_placeholder.success(
                f"MISSION COMPLETE // Research generated in {result['elapsed']:.1f} seconds."
            )

            session = {"topic": clean_topic, "state": result}
            st.session_state.history.append(session)
            st.session_state.current = session

        except Exception as error:
            log_placeholder.error(
                f"EXECUTION FAILED // {type(error).__name__}: {error}"
            )

            with st.expander("TECHNICAL DIAGNOSTICS"):
                st.exception(error)


# ============================================================
# 13. RESEARCH RESULTS
# ============================================================

current = st.session_state.current

if current:
    state = current["state"]

    st.markdown("---")
    render_section("04 /", "Intelligence output")

    st.markdown(f"### {current['topic']}")
    st.caption(f"GENERATED: {state['generated_at']}")

    # ---------------- metrics ----------------
    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric("EXECUTION TIME", f"{state['elapsed']:.1f}s")
    metric2.metric("REPORT WORDS", f"{len(state['report'].split()):,}")
    metric3.metric("SOURCES DETECTED", len(state["urls"]))
    metric4.metric("AGENTS COMPLETED", "04 / 04")

    st.markdown("")

    report_tab, critic_tab, sources_tab, raw_tab = st.tabs(
        [
            "◈  RESEARCH REPORT",
            "◎  CRITIC EVALUATION",
            "⌕  SOURCE DATABASE",
            "▤  RAW INTELLIGENCE",
        ]
    )

    # ---------------- report ----------------
    with report_tab:
        st.markdown(state["report"])

        safe_filename = (
            re.sub(r"[^a-zA-Z0-9]+", "_", current["topic"]).strip("_").lower()[:60]
        )

        st.download_button(
            label="DOWNLOAD RESEARCH REPORT  ↓",
            data=make_export(current["topic"], state),
            file_name=f"{safe_filename or 'research_report'}.md",
            mime="text/markdown",
            key="download_report",
            **STRETCH,
        )

    # ---------------- critic ----------------
    with critic_tab:
        st.markdown("#### QUALITY CONTROL / CRITIC AGENT")
        st.markdown(state["feedback"] or "_No critic feedback was returned._")

    # ---------------- sources ----------------
    with sources_tab:
        st.markdown("#### RESEARCH SOURCE DATABASE")

        if state["urls"]:
            st.caption(f"{len(state['urls'])} UNIQUE URLS DETECTED")

            for number, url in enumerate(state["urls"], start=1):
                safe_url = html.escape(url, quote=True)

                st.markdown(
                    compact_html(
                        f"""
                        <div class="source-item">
                            <span class="system-label">SOURCE {number:02d}</span><br>
                            <a href="{safe_url}" target="_blank" rel="noopener noreferrer">{safe_url}</a>
                        </div>
                        """
                    ),
                    unsafe_allow_html=True,
                )
        else:
            st.info("No URLs were detected in the agent output.")

    # ---------------- raw ----------------
    with raw_tab:
        st.markdown("#### INTERNAL RESEARCH DATA")

        raw_sections = [
            ("01 // SEARCH ENGINE OUTPUT", state["search_results"]),
            ("02 // SEARCH TOOL RAW RESULTS", state.get("search_raw", "")),
            ("03 // READER AGENT OUTPUT", state["scraped_content"]),
            ("04 // SCRAPER TOOL RAW CONTENT", state.get("scrape_raw", "")),
        ]

        for title, body in raw_sections:
            with st.expander(title, expanded=False):
                st.text(body if body else "(empty)")

        st.markdown("#### AGENT EXECUTION TELEMETRY")

        for index, agent in enumerate(AGENTS):
            duration = state["step_times"][index]

            if duration is not None:
                st.write(f"**{agent['name']}** — {duration:.2f} seconds")

    st.markdown("---")
    st.caption("NEXUS // END OF REPORT // AUTONOMOUS RESEARCH EXECUTION COMPLETE")

else:
    st.markdown(
        compact_html(
            """
            <div class="terminal">
                &gt; AWAITING RESEARCH OBJECTIVE...<br>
                &gt; AGENT NETWORK: STANDBY<br>
                &gt; DATA PIPELINE: IDLE<br>
                &gt; READY FOR INITIALIZATION_
            </div>
            """
        ),
        unsafe_allow_html=True,
    )