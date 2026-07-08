"""Identidad visual ejecutiva de SafeAnalytics EC."""

import streamlit as st


def inyectar_css() -> None:
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@600;700;800&display=swap');
:root{--navy:#0B1F33;--blue:#176B87;--cyan:#2FA8A0;--green:#2F855A;--amber:#D97706;
--red:#C2414D;--ink:#172033;--muted:#66758A;--line:#DCE4ED;--surface:#FFFFFF;--bg:#F3F6FA}
html,body,[class*="css"],[data-testid="stAppViewContainer"] *{font-family:'DM Sans','Segoe UI',sans-serif}
/* Streamlit representa varios controles con ligaduras de Material Symbols.
   La regla tipográfica global no debe convertir sus nombres en texto visible. */
[data-testid="stIconMaterial"],
span[class*="material-symbols"],
span[class*="material-icons"],
button span[data-testid="stIconMaterial"]{
  font-family:'Material Symbols Rounded','Material Symbols Outlined','Material Icons'!important;
  font-weight:normal!important;
  font-style:normal!important;
  letter-spacing:normal!important;
  text-transform:none!important;
  white-space:nowrap!important;
  word-wrap:normal!important;
  direction:ltr!important;
  -webkit-font-feature-settings:'liga'!important;
  -webkit-font-smoothing:antialiased!important;
  font-feature-settings:'liga'!important;
}
[data-testid="stAppViewContainer"]{background:var(--bg);color:var(--ink)}
[data-testid="stMainBlockContainer"]{max-width:1480px;padding:1.7rem 2.1rem 1.3rem}
[data-testid="stHeader"]{background:transparent}
footer,[data-testid="stToolbar"]{visibility:hidden}
[data-testid="stExpandSidebarButton"]{visibility:visible}
h1,h2,h3,h4{font-family:'Manrope',sans-serif!important;color:var(--ink)!important;letter-spacing:-.025em}

/* panel de filtros */
[data-testid="stSidebar"]{background:var(--navy);border-right:1px solid #173853}
[data-testid="stSidebar"] *{color:#E7F0F8!important}
.brand{padding:4px 1px 18px;border-bottom:1px solid rgba(255,255,255,.12);margin-bottom:18px}
.brand-mark{display:inline-grid;place-items:center;width:39px;height:39px;border-radius:10px;background:#2FA8A0;
color:white;font:800 19px Manrope;margin-right:10px}.brand-name{font:800 1rem Manrope;vertical-align:middle}
.brand-sub{display:block;margin:7px 0 0 52px;color:#91A9BE!important;font-size:.67rem;letter-spacing:.12em;text-transform:uppercase}
.filter-intro{color:#AFC1D1!important;font-size:.78rem;line-height:1.5;margin:-5px 0 13px}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#112D45!important;border:1px solid #294B64!important;border-radius:9px}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"]{background:#176B87!important;border-radius:6px}
[data-baseweb="popover"] [role="option"]{color:#172033!important}
[data-testid="stSidebar"] .stButton button{width:100%;background:transparent;border:1px solid #527087;border-radius:9px;color:#DDEAF4!important}
.source-note{margin-top:15px;padding:12px 13px;border-radius:10px;background:#102A40;border:1px solid #24455E;
font-size:.7rem;line-height:1.55;color:#9EB4C7!important}.source-note b{color:#60CEC4!important}

/* cabecera */
.command-header{background:var(--navy);border-radius:18px;padding:25px 28px;color:white;margin-bottom:15px;
display:flex;justify-content:space-between;gap:24px;align-items:center;box-shadow:0 12px 30px rgba(11,31,51,.16)}
.command-header .overline{color:#64D3C9;font-size:.68rem;font-weight:700;letter-spacing:.15em;text-transform:uppercase}
.command-header h1{color:white!important;font-size:2rem;margin:5px 0 4px}.command-header p{color:#B8C9D8;margin:0;font-size:.86rem;max-width:760px}
.dataset-badge{flex:0 0 auto;padding:10px 13px;border:1px solid #34566E;border-radius:10px;color:#C7D8E5;font-size:.7rem;text-align:right}
.dataset-badge b{display:block;color:white;font-size:.82rem;margin-bottom:2px}

/* KPIs */
.kpi{background:white;border:1px solid var(--line);border-radius:13px;padding:16px 17px;min-height:145px;
box-shadow:0 5px 15px rgba(23,32,51,.045);position:relative;overflow:hidden}
.kpi:before{content:'';position:absolute;left:0;top:0;bottom:0;width:4px;background:var(--blue)}
.kpi.alerta:before{background:var(--amber)}.kpi.critico:before{background:var(--red)}
.kpi .etiqueta{color:var(--muted);font-size:.67rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;min-height:31px}
.kpi .valor{font:800 1.38rem Manrope;color:var(--ink);line-height:1.16;overflow-wrap:anywhere}
.kpi .unidad{font-size:.76rem;color:var(--muted)}.kpi .pilar{display:inline-block;margin-top:9px;padding:3px 7px;
border-radius:5px;background:#E8F4F5;color:#176B87;font-size:.59rem;font-weight:700;letter-spacing:.08em}
.kpi .micro{color:#78869A;font-size:.66rem;line-height:1.3;margin-top:8px}

/* navegación */
.stTabs [data-baseweb="tab-list"]{gap:5px;margin:20px 0 8px;padding:5px;background:white;border:1px solid var(--line);border-radius:12px}
.stTabs [data-baseweb="tab"]{height:40px;padding:0 16px;border-radius:8px;color:#617086;font-size:.77rem;font-weight:700}
.stTabs [aria-selected="true"]{background:var(--navy)!important;color:white!important}
.stTabs [data-baseweb="tab-highlight"],.stTabs [data-baseweb="tab-border"]{display:none}
.section-head{display:flex;justify-content:space-between;gap:20px;align-items:end;margin:12px 0 15px}
.section-kicker{color:var(--blue);font-size:.65rem;font-weight:800;letter-spacing:.14em;text-transform:uppercase}
.section-title{font:800 1.45rem Manrope;color:var(--ink);margin:3px 0}.section-question{color:var(--muted);font-size:.82rem}
.section-tag{background:#E8F2F5;color:#176B87;border-radius:999px;padding:6px 11px;font-size:.66rem;font-weight:700}

[data-testid="stVerticalBlockBorderWrapper"]:has(.js-plotly-plot),div[data-testid="stDataFrame"]{
background:white;border:1px solid var(--line);border-radius:13px;box-shadow:0 4px 14px rgba(23,32,51,.035);padding:5px}
[data-testid="stMetric"]{background:white;border:1px solid var(--line);border-radius:12px;padding:13px 15px}
.insight{background:#EDF6F6;border:1px solid #CBE7E5;border-left:4px solid var(--cyan);border-radius:10px;
padding:13px 15px;color:#294B59;font-size:.8rem;line-height:1.5;margin:4px 0 14px}
.insight.warning{background:#FFF7E8;border-color:#F2D8A8;border-left-color:var(--amber);color:#6E4D17}
.story-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:12px;margin:7px 0 15px}
.story-card{background:white;border:1px solid var(--line);border-radius:12px;padding:17px}
.story-card .label{color:var(--blue);font-size:.63rem;font-weight:800;letter-spacing:.11em;text-transform:uppercase}
.story-card h4{font-size:.94rem;margin:7px 0}.story-card p{color:var(--muted);font-size:.76rem;line-height:1.5;margin:0}
.analytics-row{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;margin:10px 0 15px}
.analytics-chip{background:#102A40;color:white;border-radius:10px;padding:12px}.analytics-chip b{display:block;color:#64D3C9;font-size:.68rem}
.analytics-chip span{font-size:.7rem;color:#C4D3DF}
.action-card{background:white;border:1px solid var(--line);border-radius:12px;padding:15px;margin-bottom:10px}
.action-card.high{border-left:5px solid var(--red)}.action-card.medium{border-left:5px solid var(--amber)}
.action-card .priority{font-size:.61rem;font-weight:800;letter-spacing:.1em;color:var(--red)}
.action-card.medium .priority{color:var(--amber)}.action-card h4{margin:5px 0;font-size:.91rem}
.action-card p{margin:0;color:var(--muted);font-size:.75rem;line-height:1.45}
.footer-line{border-top:1px solid var(--line);margin-top:25px;padding:16px 0 3px;display:flex;justify-content:space-between;color:#7B899B;font-size:.66rem}
@media(max-width:900px){[data-testid="stMainBlockContainer"]{padding:1rem}.command-header{display:block}.dataset-badge{margin-top:15px;text-align:left}
.story-grid,.analytics-row{grid-template-columns:1fr}.stTabs [data-baseweb="tab"]{padding:0 9px}}
</style>
""",
        unsafe_allow_html=True,
    )
