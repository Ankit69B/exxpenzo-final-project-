import streamlit as st
import streamlit.components.v1 as components

def apply_global_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;600;700&display=swap');

:root {
    --bg:        #0a0d14;
    --bg2:       #0f1420;
    --surface:   #141926;
    --surface2:  #1c2333;
    --border:    rgba(255,255,255,0.06);
    --border2:   rgba(255,255,255,0.1);
    --mint:      #00f5c4;
    --amber:     #f5a623;
    --red:       #ff4d6d;
    --blue:      #4da6ff;
    --text:      #e8ecf4;
    --muted:     #6b7a99;
    --radius:    16px;
    --radius-sm: 10px;
}

html { scroll-behavior: smooth; }

/* ── Base App ── */
.stApp {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, header, footer, .stDeployButton,
[data-testid="stStatusWidget"] { visibility: hidden !important; display: none !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--mint); border-radius: 4px; }

/* ── Page fade-in ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(18px); }
    to   { opacity: 1; transform: translateY(0); }
}
[data-testid="stVerticalBlock"] > div {
    animation: fadeUp 0.45s cubic-bezier(0.22,1,0.36,1) both;
}

/* ── Cards ── */
.card {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 28px !important;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease !important;
    color: var(--text) !important;
}
.card:hover {
    transform: translateY(-5px) !important;
    box-shadow: 0 16px 40px rgba(0,245,196,0.08) !important;
    border-color: rgba(0,245,196,0.25) !important;
}

/* ── Stat cards ── */
.stat-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 28px;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--mint), transparent);
    opacity: 0;
    transition: opacity 0.25s ease;
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,245,196,0.1);
    border-color: rgba(0,245,196,0.2);
}
.stat-card:hover::before { opacity: 1; }
.stat-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
}
.stat-value {
    font-family: 'Space Mono', monospace;
    font-size: 32px;
    font-weight: 700;
    color: var(--text);
    line-height: 1;
}
.stat-accent { color: var(--mint); }

/* ── Streamlit form / expander overrides ── */
[data-testid="stForm"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 28px !important;
}
[data-testid="stExpander"] {
    background: var(--surface2) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
}

/* ── Inputs ── */
input, textarea,
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--bg2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
}
input:focus, div[data-baseweb="select"] > div:focus-within {
    border-color: var(--mint) !important;
    box-shadow: 0 0 0 3px rgba(0,245,196,0.12) !important;
}

/* ── Number input ── */
[data-testid="stNumberInput"] input {
    font-family: 'Space Mono', monospace !important;
}

/* ── Buttons ── */
[data-testid="stButton"] button {
    background: var(--surface2) !important;
    border: 1px solid var(--border2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    height: 44px !important;
    transition: all 0.22s ease !important;
    letter-spacing: 0.3px !important;
}
[data-testid="stButton"] button:hover {
    background: var(--mint) !important;
    color: var(--bg) !important;
    border-color: var(--mint) !important;
    box-shadow: 0 6px 20px rgba(0,245,196,0.25) !important;
    transform: translateY(-2px) !important;
}

/* ── Submit / primary button ── */
[data-testid="stFormSubmitButton"] button {
    background: linear-gradient(135deg, #00f5c4, #00c9a7) !important;
    color: var(--bg) !important;
    border: none !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    height: 48px !important;
    font-size: 15px !important;
    box-shadow: 0 4px 20px rgba(0,245,196,0.3) !important;
}
[data-testid="stFormSubmitButton"] button:hover {
    box-shadow: 0 8px 30px rgba(0,245,196,0.45) !important;
    transform: translateY(-2px) !important;
    color: var(--bg) !important;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 4px;
    background: var(--surface) !important;
    padding: 6px;
    border-radius: var(--radius-sm);
    border: 1px solid var(--border);
}
[data-testid="stTabs"] button[role="tab"] {
    background: transparent !important;
    border: none !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    background: var(--mint) !important;
    color: var(--bg) !important;
    font-weight: 700 !important;
}
[data-testid="stTabs"] button[role="tab"]:hover:not([aria-selected="true"]) {
    color: var(--text) !important;
    background: var(--surface2) !important;
}

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    overflow: hidden;
}

/* ── Metric ── */
[data-testid="stMetric"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 20px 24px !important;
}
[data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 12px !important; letter-spacing: 1px !important; text-transform: uppercase !important; }
[data-testid="stMetricValue"] { font-family: 'Space Mono', monospace !important; color: var(--text) !important; }
[data-testid="stMetricDelta"] svg { display: none; }

/* ── Alerts ── */
[data-testid="stAlert"] {
    border-radius: var(--radius-sm) !important;
    border: none !important;
    background: var(--surface2) !important;
}

/* ── HR divider ── */
hr { border-color: var(--border) !important; margin: 32px 0 !important; }

/* ── Section headers ── */
h2, h3 { color: var(--text) !important; font-family: 'DM Sans', sans-serif !important; }
h2 { font-weight: 700 !important; }
h3 { font-weight: 600 !important; }

/* ── Caption / small ── */
[data-testid="stCaptionContainer"] p { color: var(--muted) !important; font-size: 13px !important; }

/* ── Nav bar ── */
.nav-wrapper {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 6px;
    margin: 0 auto 8px;
}
.nav-label {
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: var(--muted);
    text-align: center;
    margin-bottom: 10px;
}
/* ── Interactive User Badge (Popover) ── */
[data-testid="stPopover"] { 
    width: 100%;
    /* Align with native buttons by removing container offset */
    margin-top: -3px !important; 
}
[data-testid="stPopover"] > div:first-child > button {
    background: var(--surface2) !important;
    border: 1px solid rgba(0,245,196,0.2) !important;
    height: 44px !important;
    padding: 0 12px 0 16px !important;
    border-radius: var(--radius-sm) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    width: 100% !important;
    transition: all 0.22s ease !important;
    color: var(--mint) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    letter-spacing: 0.3px !important;
}

[data-testid="stPopover"] > div:first-child > button:hover {
    border-color: var(--mint) !important;
    box-shadow: 0 4px 20px rgba(0,245,196,0.15) !important;
}
[data-testid="stPopoverBody"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    padding: 16px !important;
    box-shadow: 0 12px 40px rgba(0,0,0,0.5) !important;
}

/* Clear ghost margins from the markdown and vertical block containers */
div[data-testid="stMarkdownContainer"] > p:empty { display: none; }
div[data-testid="stVerticalBlock"] > div {
    margin-bottom: 0px !important;
    padding-bottom: 0px !important;
}


/* ── Page title ── */
.page-title {
    font-family: 'DM Sans', sans-serif;
    font-size: 36px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -1px;
    margin-bottom: 4px;
}
.page-sub {
    color: var(--muted);
    font-size: 14px;
    margin-bottom: 32px;
    font-weight: 400;
}
.mint { color: var(--mint); }

/* ── Section label ── */
.section-label {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Login card ── */
.login-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 48px 40px;
}
.login-logo {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 3px;
    color: var(--mint);
    text-align: center;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.login-headline {
    font-family: 'DM Sans', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: var(--text);
    text-align: center;
    margin-bottom: 6px;
    letter-spacing: -0.5px;
}
.login-sub {
    color: var(--muted);
    font-size: 14px;
    text-align: center;
    margin-bottom: 32px;
}

/* ── Manage entry warning ── */
.danger-box {
    background: rgba(255,77,109,0.08);
    border-left: 3px solid var(--red);
    border-radius: 8px;
    padding: 14px 16px;
    margin-bottom: 16px;
}
.danger-box p { color: #ff8fa3; margin: 0; font-size: 13px; line-height: 1.5; }
.danger-box h5 { color: var(--red); margin: 0 0 4px; font-size: 13px; font-weight: 700; }

/* ── Behavior card ── */
.behavior-card {
    border-radius: var(--radius);
    padding: 28px;
    border: 1px solid;
    transition: transform 0.25s ease;
}
.behavior-card:hover { transform: translateY(-4px); }

/* ── Materialization ── */
@keyframes materialize {
    from { 
        opacity: 0; 
        transform: scale(0.96) translateY(24px);
        filter: blur(12px);
        clip-path: inset(40% 0 40% 0);
    }
    to { 
        opacity: 1; 
        transform: scale(1) translateY(0);
        filter: blur(0);
        clip-path: inset(0 0 0 0);
    }
}

div[data-testid="stPlotlyChart"] {
    animation: materialize 1.2s cubic-bezier(0.23, 1, 0.32, 1) both;
}

/* Cascading Delays */
div[data-testid="stPlotlyChart"]:nth-of-type(1) { animation-delay: 0.1s; }
div[data-testid="stPlotlyChart"]:nth-of-type(2) { animation-delay: 0.3s; }
div[data-testid="stPlotlyChart"]:nth-of-type(3) { animation-delay: 0.5s; }
div[data-testid="stPlotlyChart"]:nth-of-type(4) { animation-delay: 0.7s; }
div[data-testid="stPlotlyChart"]:nth-of-type(5) { animation-delay: 0.9s; }

</style>
""", unsafe_allow_html=True)

def apply_custom_cursor(enable=False):
    if enable:
        components.html("""
        <script>
        const doc = window.parent.document;
        if (!doc.getElementById('xp-cursor')) {
            const ring = doc.createElement('div');
            ring.id = 'xp-cursor';
            Object.assign(ring.style, {
                position: 'fixed', width: '36px', height: '36px',
                border: '1.5px solid rgba(0,245,196,0.5)', borderRadius: '50%',
                pointerEvents: 'none', transform: 'translate(-50%,-50%)',
                transition: 'width .2s,height .2s,background .2s',
                zIndex: '999999', top: '0', left: '0'
            });
            const dot = doc.createElement('div');
            dot.id = 'xp-dot';
            Object.assign(dot.style, {
                position: 'fixed', width: '5px', height: '5px',
                background: '#00f5c4', borderRadius: '50%',
                pointerEvents: 'none', transform: 'translate(-50%,-50%)',
                zIndex: '1000000', top: '0', left: '0'
            });
            doc.body.appendChild(ring); doc.body.appendChild(dot);
            let mx=0,my=0,rx=0,ry=0;
            doc.addEventListener('mousemove',e=>{ mx=e.clientX; my=e.clientY; dot.style.left=mx+'px'; dot.style.top=my+'px'; });
            (function loop(){ rx+=(mx-rx)*.18; ry+=(my-ry)*.18; ring.style.left=rx+'px'; ring.style.top=ry+'px'; requestAnimationFrame(loop); })();
            doc.addEventListener('mousedown',()=>{ ring.style.width='22px'; ring.style.height='22px'; ring.style.background='rgba(0,245,196,0.15)'; });
            doc.addEventListener('mouseup',()=>{ ring.style.width='36px'; ring.style.height='36px'; ring.style.background='transparent'; });
        }
        </script>
        """, height=0, width=0)
