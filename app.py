import streamlit as st

from state import init_state
from sections.summary_section import render_summary
from sections.rd_section import render_rd_section
from sections.rsd_section import render_rsd_section
from sections.rse_section import render_rse_section
from sections.rpr_section import render_rpr_section
from sections.rp_section import render_rp_section

st.set_page_config(
    page_title="OPM Parameter Calculator",
    page_icon="🧲",
    layout="wide"
)

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 3rem;
        padding-left: 2rem;
        padding-right: 2rem;
        max-width: 100%;
    }

    section[data-testid="stSidebar"] {
        width: 320px !important;
    }

    section[data-testid="stSidebar"] > div {
        width: 320px !important;
    }

    div[data-testid="stTabs"] [role="tablist"] {
        display: flex;
        width: 100%;
    }

    div[data-testid="stTabs"] [role="tab"] {
        flex: 1 1 0;
        justify-content: center;
        text-align: center;
    }

    div[data-testid="stTabs"] [role="tab"] p {
        width: 100%;
        text-align: center;
        font-size: 1rem;
        font-weight: 600;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 14px !important;
        background-color: rgba(255, 255, 255, 0.035) !important;
        padding: 1.1rem 1.4rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 1.4rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

init_state()

st.title("OPM Parameter Calculator 4.0")

st.markdown(
    """
這是一個用於計算 OPM 參數的網站工具。  

Version history (ノ°∀°)ノ⌒･*:.｡. .｡. 

**OPM Parameter Calculator 1.0**：建立 R_D diffusion collision rate 的完整計算流程。  
**OPM Parameter Calculator 1.5**：優化版面。  
**OPM Parameter Calculator 2.0**：加入 R_sd 的計算。  
**OPM Parameter Calculator 2.5**：同步共同參數。  
**OPM Parameter Calculator 3.0**：修正科學記號顯示&加入R_se的計算。  
**OPM Parameter Calculator 4.0**：加入R_PR, R_p的計算。  




"""
)

col_img, col_text = st.columns([1, 6])
st.image("我的虛擬人像/9998191e-b637-4f3d-a01b-3c45fca4f405.png", width=110)
with col_text:
    st.markdown("""
    Welcome to OPM Calculator! I'm Web Producer - Ting-An, Li  
    If you have any problem, please let me know ~~ Ann930226ann@gmail.com
    """)

tab_rd, tab_rsd, tab_rse, tab_rpr, tab_rp = st.tabs(
    ["R_D", "R_sd", "R_se", "R_pr", "R_p"]
)

with tab_rd:
    render_rd_section()

with tab_rsd:
    render_rsd_section()

with tab_rse:
    render_rse_section()
    
with tab_rpr:
    render_rpr_section()

with tab_rp:
    render_rp_section()

render_summary()
