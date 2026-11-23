"""Design tokens, global CSS and Plotly styling for the dashboard."""
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st

PRIMARY, TEAL, AMBER = "#4F46E5", "#0D9488", "#F59E0B"
PRIMARY_SOFT, TEAL_SOFT, AMBER_SOFT = "#EEF2FF", "#CCFBF1", "#FEF3C7"
TEXT, MUTED, BORDER, BG = "#0F172A", "#5B6B82", "#E2E8F0", "#F8FAFC"
FONT = "Inter, system-ui, -apple-system, 'Segoe UI', sans-serif"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp {{ font-family: {FONT}; color: {TEXT}; }}
.stApp {{ background: {BG}; }}
header[data-testid="stHeader"] {{ background: transparent; height: 0; }}
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"] {{ visibility: hidden; height: 0; }}
.block-container {{ padding: 1.4rem 2.2rem 4rem; max-width: 1280px; }}

/* ---- sidebar / navigation ---- */
section[data-testid="stSidebar"] {{ background: #FFFFFF; border-right: 1px solid {BORDER}; }}
section[data-testid="stSidebar"] .block-container, section[data-testid="stSidebar"] > div {{ padding-top: 1.2rem; }}
.brand {{ display:flex; align-items:center; gap:10px; margin: 0 0 22px 4px; font-weight:700; font-size:16px; letter-spacing:-.01em; }}
.brand-mark {{ width:32px; height:32px; border-radius:9px; background:{PRIMARY}; display:flex; align-items:center; justify-content:center; }}
.brand small {{ font-weight:500; color:{MUTED}; font-size:16px; }}
section[data-testid="stSidebar"] [role="radiogroup"] {{ gap: 4px; }}
section[data-testid="stSidebar"] [role="radiogroup"] label {{
  padding: 11px 14px; border-radius: 10px; width: 100%; cursor: pointer;
  transition: background .15s, color .15s; }}
section[data-testid="stSidebar"] [role="radiogroup"] label:hover {{ background: #F1F5F9; }}
section[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child {{ display: none !important; }}
section[data-testid="stSidebar"] label[data-testid="stRadioOption"] > div > div:first-child {{ display: none !important; }}
section[data-testid="stSidebar"] label[data-baseweb="radio"] {{ margin: 0; }}
section[data-testid="stSidebar"] [role="radiogroup"] label p {{ font-size: 14px; font-weight: 500; color: #334155; margin: 0; }}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {{ background: {PRIMARY_SOFT}; }}
section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p {{ color: #4338CA; font-weight: 600; }}
.side-note {{ margin-top: 26px; padding: 14px 16px; border-radius: 12px; background: {BG}; border: 1px solid {BORDER};
  font-size: 12.5px; line-height: 1.55; color: #475569; }}
.side-note b {{ color: {TEXT}; display:block; margin-bottom:3px; }}

/* ---- page heading ---- */
.page-title {{ font-size: 28px; font-weight: 700; letter-spacing: -.02em; line-height: 1.2; margin: 4px 0 6px; }}
.page-sub {{ font-size: 15px; color: {MUTED}; margin: 0 0 22px; line-height: 1.5; }}
.topchip {{ display:inline-flex; align-items:center; gap:8px; padding:6px 12px; border:1px solid {BORDER}; border-radius:999px;
  font-size:13px; color:#475569; background:#FFFFFF; margin-bottom: 10px; }}
.topchip i {{ width:7px; height:7px; border-radius:50%; background:{TEAL}; display:inline-block; }}

/* ---- cards: bordered containers ---- */
div[data-testid="stVerticalBlockBorderWrapper"] {{
  background: #FFFFFF; border: 1px solid {BORDER} !important; border-radius: 16px !important;
  box-shadow: 0 1px 2px rgba(15,23,42,.04); padding: 6px 8px; transition: box-shadow .2s, border-color .2s; }}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {{ box-shadow: 0 4px 16px rgba(15,23,42,.07); border-color: #CBD5E1 !important; }}
.card-title {{ font-size: 16px; font-weight: 600; margin: 0; }}
.card-sub {{ font-size: 13px; color: {MUTED}; margin: 4px 0 4px; }}

/* ---- KPI cards ---- */
.kpi {{ background:#FFFFFF; border:1px solid {BORDER}; border-radius:16px; padding:20px 22px; box-shadow:0 1px 2px rgba(15,23,42,.04);
  transition: box-shadow .2s, border-color .2s; height: 100%; }}
.kpi:hover {{ box-shadow:0 4px 16px rgba(15,23,42,.07); border-color:#CBD5E1; }}
.kpi-top {{ display:flex; align-items:center; justify-content:space-between; font-size:13px; font-weight:500; color:{MUTED}; }}
.kpi-ico {{ width:32px; height:32px; border-radius:9px; display:flex; align-items:center; justify-content:center; }}
.kpi-val {{ font-size:32px; font-weight:700; letter-spacing:-.02em; line-height:1.1; margin:12px 0 8px; font-variant-numeric:tabular-nums; }}
.kpi-note {{ font-size:13px; color:{MUTED}; }}

/* ---- pills / chips ---- */
.pill {{ display:inline-block; padding:6px 12px; border-radius:999px; font-size:13px; font-weight:600; margin-right:8px; }}
.pill.p {{ background:{PRIMARY_SOFT}; color:#4338CA; }}
.pill.n {{ background:#F1F5F9; color:#334155; font-weight:500; }}

/* ---- model compare cards ---- */
.mcard {{ background:#FFFFFF; border:1px solid {BORDER}; border-radius:16px; padding:24px; box-shadow:0 1px 2px rgba(15,23,42,.04); height:100%; }}
.mcard:hover {{ box-shadow:0 4px 16px rgba(15,23,42,.07); }}
.mhead {{ display:flex; align-items:center; justify-content:space-between; font-size:15px; font-weight:700; }}
.mdot {{ display:inline-block; width:12px; height:12px; border-radius:4px; margin-right:9px; }}
.badge {{ padding:5px 11px; border-radius:999px; font-size:12px; font-weight:700; }}
.mbig {{ font-size:38px; font-weight:800; letter-spacing:-.03em; margin:4px 0 10px; font-variant-numeric:tabular-nums; }}
.mlabel {{ font-size:13px; color:{MUTED}; font-weight:500; }}
.track {{ height:8px; border-radius:6px; background:#F1F5F9; overflow:hidden; }}
.track > div {{ height:100%; border-radius:6px; }}
.msub {{ display:grid; grid-template-columns:1fr 1fr; gap:16px; padding-top:16px; margin-top:18px; border-top:1px solid #F1F5F9; }}
.msub b {{ display:block; font-size:20px; margin-top:3px; font-variant-numeric:tabular-nums; }}
.insight {{ display:flex; gap:14px; align-items:flex-start; background:#FFFFFF; border:1px solid {BORDER}; border-radius:16px;
  padding:18px 22px; font-size:14.5px; line-height:1.6; color:#334155; margin: 4px 0; }}
.insight .ico {{ width:34px; height:34px; flex:0 0 34px; border-radius:10px; background:{PRIMARY_SOFT}; color:{PRIMARY}; display:flex; align-items:center; justify-content:center; }}

/* ---- estimator result panel (sticky) ---- */
div[data-testid="stColumn"]:has(.sticky-marker) {{ position: sticky; top: 1rem; align-self: flex-start; }}
.result {{ background:#FFFFFF; border:1px solid {BORDER}; border-radius:20px; padding:28px; box-shadow:0 8px 30px rgba(15,23,42,.07); }}
.res-top {{ display:flex; justify-content:space-between; align-items:center; }}
.res-eyebrow {{ font-size:13px; font-weight:600; color:{MUTED}; text-transform:uppercase; letter-spacing:.05em; }}
.res-price {{ font-size:46px; font-weight:800; letter-spacing:-.035em; line-height:1.05; margin:18px 0 8px; font-variant-numeric:tabular-nums; }}
.res-range {{ font-size:15px; color:#475569; font-weight:500; }}
.res-range b {{ color:{TEXT}; }}
.rbar {{ position:relative; height:44px; margin-top:22px; }}
.rbar .base {{ position:absolute; left:0; right:0; top:19px; height:8px; border-radius:6px; background:#F1F5F9; }}
.rbar .span {{ position:absolute; top:19px; height:8px; border-radius:6px; background:{PRIMARY}; }}
.rbar .mid {{ position:absolute; top:11px; width:4px; height:24px; border-radius:2px; background:{TEXT}; transform:translateX(-50%); }}
.rbar .mkt {{ position:absolute; top:16px; width:14px; height:14px; border-radius:50%; background:{AMBER}; border:3px solid #fff; box-shadow:0 0 0 1px #D97706; transform:translateX(-50%); }}
.legend {{ display:flex; flex-wrap:wrap; gap:16px; font-size:12.5px; color:#475569; margin-top:2px; }}
.legend span {{ display:inline-flex; align-items:center; gap:7px; }}
.res-h {{ font-size:13px; font-weight:700; margin:24px 0 12px; padding-top:20px; border-top:1px solid #F1F5F9; }}
.take {{ display:flex; gap:12px; align-items:flex-start; font-size:14px; line-height:1.55; color:#334155; margin-bottom:12px; }}
.take i {{ width:22px; height:22px; flex:0 0 22px; border-radius:50%; display:flex; align-items:center; justify-content:center; margin-top:1px; font-style:normal; font-weight:800; font-size:12px; }}
.mini {{ display:grid; grid-template-columns:repeat(2,1fr); gap:10px; margin-top:4px; }}
.mini div {{ border:1px solid {BORDER}; border-radius:12px; padding:10px 14px; font-size:12.5px; color:{MUTED}; }}
.mini b {{ display:block; color:{TEXT}; font-size:16px; margin-top:2px; font-variant-numeric:tabular-nums; }}
.result p.fine, .fine {{ font-size:12px !important; color:{MUTED}; line-height:1.5; margin:16px 0 0 !important; }}
.lbl {{ font-size:12.5px; font-weight:600; color:#475569; margin:0 0 6px; }}

/* ---- widgets ---- */
div[data-baseweb="select"] > div, div[data-testid="stNumberInput"] input, div[data-baseweb="input"] > div {{
  border-radius: 10px !important; border-color: #CBD5E1 !important; min-height: 44px; transition: border-color .15s, box-shadow .15s; }}
div[data-baseweb="select"] > div:hover {{ border-color: #94A3B8 !important; }}
label[data-testid="stWidgetLabel"] p {{ font-size: 12.5px !important; font-weight: 600 !important; color: #475569 !important; }}
button[kind="primary"], div[data-testid="stButton"] button[kind="primary"] {{
  background: {PRIMARY}; border: none; border-radius: 12px; height: 52px; font-size: 15.5px; font-weight: 700; color:#fff;
  transition: background .15s, box-shadow .15s, transform .1s; }}
button[kind="primary"]:hover {{ background:#4338CA; box-shadow:0 4px 12px rgba(79,70,229,.3); color:#fff; }}
button[kind="primary"]:active {{ transform: translateY(1px); }}
button[kind="secondary"] {{ border-radius: 12px; border: 1px solid #CBD5E1; background:#fff; font-weight:600; color:#334155; height: 52px; transition: background .15s, border-color .15s; }}
button[kind="secondary"]:hover {{ background:#F1F5F9; border-color:#CBD5E1; color:#0F172A; }}
div[data-testid="stSegmentedControl"] {{ background: #E2E8F0; border-radius: 12px; padding: 4px; }}
div[data-testid="stExpander"] details {{ border: 1px solid {BORDER}; border-radius: 16px; background:#fff; }}
div[data-testid="stExpander"] summary p {{ font-weight: 600; font-size: 16px; }}
div[data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}
div[data-testid="stSlider"] [role="slider"] {{ background: {PRIMARY}; }}
@media (max-width: 1180px) {{
  div[data-testid="stHorizontalBlock"] {{ flex-wrap: wrap; row-gap: 1rem; }}
  div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {{ flex: 1 1 calc(50% - 1rem); min-width: 230px; }}
  div[data-testid="stColumn"]:has(.sticky-marker) {{ position: static; flex-basis: 100% !important; }}
}}
@media (max-width: 900px) {{ .block-container {{ padding: 1rem 1rem 3rem; }} div[data-testid="stColumn"]:has(.sticky-marker) {{ position: static; }} .res-price {{ font-size: 38px; }} }}
</style>
"""

def inject():
    st.markdown(CSS, unsafe_allow_html=True)

def icon(path, size=17, color="currentColor", sw=1.9):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{path}"/></svg>')

def fm(lakhs, short=False):
    """Format a price given in units of LKR 100,000 as LKR millions."""
    m = float(lakhs) / 10
    if short:
        return f"{m:.0f}M" if m >= 10 else f"{m:.1f}M"
    return f"LKR {m:.1f}M" if m >= 10 else f"LKR {m:.2f}M"

def fl(lakhs):
    x = float(lakhs) * 1e5
    return f"LKR {x/1e6:.2f}M" if x >= 1e6 else f"LKR {round(x/1e3)}k"

def style(fig, height=300, legend=False):
    """Minimal chart look: no vertical grid, faint horizontal guides, Inter, tidy hover."""
    fig.update_layout(
        height=height, margin=dict(l=4, r=36, t=8, b=4), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family=FONT, size=12, color=MUTED), showlegend=legend, bargap=0.25,
        hoverlabel=dict(bgcolor=TEXT, font=dict(family=FONT, size=12.5, color="#FFFFFF"), bordercolor=TEXT),
        legend=dict(orientation="h", y=1.1, x=0))
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor=BORDER, ticks="", title=None)
    fig.update_yaxes(showgrid=True, gridcolor="#F1F5F9", zeroline=False, showline=False, ticks="", title=None)
    return fig
