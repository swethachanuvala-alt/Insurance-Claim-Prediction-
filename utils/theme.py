import plotly.graph_objects as go
import streamlit as st

BLUES = ["#0A1F44", "#1E3A8A", "#1D6FB8", "#3B9AE1", "#7CC4F5", "#BFE3FB"]
NAVY, ROYAL, OCEAN, SKY, ICE = "#0A1F44", "#1E3A8A", "#1D6FB8", "#3B9AE1", "#BFE3FB"

CSS = """
<style>
.stApp {background: linear-gradient(180deg, #F3F8FE 0%, #E6F1FC 100%);}
.block-container {padding-top: 2rem; max-width: 1200px;}
h1, h2, h3, h4 {color: #0A1F44; letter-spacing: -0.3px;}
[data-testid="stSidebar"] {background: linear-gradient(180deg, #0A1F44 0%, #1E3A8A 60%, #1D6FB8 100%);}
[data-testid="stSidebar"] span, [data-testid="stSidebar"] p, [data-testid="stSidebar"] a,
[data-testid="stSidebar"] li, [data-testid="stSidebar"] div {color: #EAF4FF;}
[data-testid="stSidebarNav"] a {border-radius: 10px;}
[data-testid="stSidebarNav"] a:hover {background: rgba(255,255,255,0.12);}
.hero {background: linear-gradient(120deg, #0A1F44 0%, #1E3A8A 55%, #3B9AE1 100%);
  color: #fff; padding: 2.2rem 2.4rem; border-radius: 20px; margin-bottom: 1.6rem;
  box-shadow: 0 12px 30px rgba(10,31,68,0.25);}
.hero h1 {color: #fff; margin: 0 0 .4rem 0; font-size: 2.3rem;}
.hero p {color: #D6EBFF; margin: 0; font-size: 1.05rem; max-width: 760px;}
.kpi {background: #fff; border-radius: 16px; padding: 1.1rem 1.2rem; border-left: 6px solid #3B9AE1;
  box-shadow: 0 6px 18px rgba(30,58,138,0.10);}
.kpi .label {color: #5B7BA6; font-size: .8rem; text-transform: uppercase; letter-spacing: .8px;}
.kpi .value {color: #0A1F44; font-size: 1.8rem; font-weight: 700; line-height: 1.2;}
.card {background: #fff; border-radius: 18px; padding: 1.4rem 1.5rem; margin-bottom: 1rem;
  box-shadow: 0 6px 18px rgba(30,58,138,0.10); border-top: 4px solid #7CC4F5;}
.card h4 {margin: 0 0 .4rem 0; color: #1E3A8A;}
.card p {color: #35527D; margin: 0;}
.result-yes {background: linear-gradient(135deg, #1E3A8A, #3B9AE1); color: #fff; border-radius: 18px;
  padding: 1.4rem 1.6rem; box-shadow: 0 10px 24px rgba(30,58,138,0.30);}
.result-no {background: linear-gradient(135deg, #0A1F44, #1D6FB8); color: #fff; border-radius: 18px;
  padding: 1.4rem 1.6rem; box-shadow: 0 10px 24px rgba(10,31,68,0.30);}
.result-yes h2, .result-no h2, .result-yes p, .result-no p {color: #fff; margin: 0;}
.pill {display: inline-block; background: #DDEBFA; color: #1E3A8A; padding: .25rem .8rem;
  border-radius: 999px; font-size: .8rem; margin: .15rem .2rem .15rem 0; font-weight: 600;}
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
  background: linear-gradient(90deg, #1E3A8A, #3B9AE1); color: #fff; border: 0; border-radius: 12px;
  padding: .6rem 1.4rem; font-weight: 600;}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stDownloadButton > button:hover {
  filter: brightness(1.1); color: #fff;}
.stTabs [data-baseweb="tab"] {font-weight: 600; color: #1E3A8A;}
.stTabs [aria-selected="true"] {color: #1D6FB8;}
footer, #MainMenu {visibility: hidden;}
</style>
"""


def setup_page(title, icon="🛡️"):
    st.set_page_config(page_title=f"{title} | ClaimSense", page_icon=icon, layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    st.sidebar.markdown(
        "<div style='padding:.6rem 0 0 0'><div style='font-size:1.4rem;font-weight:700'>🛡️ ClaimSense</div>"
        "<div style='font-size:.85rem;opacity:.85'>Insurance claim prediction</div></div>",
        unsafe_allow_html=True)


def hero(title, subtitle):
    st.markdown(f"<div class='hero'><h1>{title}</h1><p>{subtitle}</p></div>", unsafe_allow_html=True)


def kpi(col, label, value):
    col.markdown(f"<div class='kpi'><div class='label'>{label}</div><div class='value'>{value}</div></div>",
                 unsafe_allow_html=True)


def card(title, text):
    st.markdown(f"<div class='card'><h4>{title}</h4><p>{text}</p></div>", unsafe_allow_html=True)


def style_fig(fig, height=380):
    fig.update_layout(
        height=height, colorway=BLUES[1:5], paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(255,255,255,0.7)",
        font=dict(color=NAVY), margin=dict(l=20, r=20, t=50, b=20),
        title_font=dict(size=17, color=ROYAL))
    return fig
