import streamlit as st


DEFAULTS = {
    # =========================
    # R_D shared/global parameters
    # =========================
    "T_value": 373.0,
    "T_unit": "K",

    "P_buffer_value": 100.0,
    "P_buffer_unit": "torr",

    "a_value": 0.425,
    "a_unit": "cm",

    "geometry": "cube",

    # =========================
    # R_D result
    # =========================
    "R_D": None,

    # =========================
    # R_sd input parameters
    # =========================
    "RSD_T_value": 373.0,
    "RSD_T_unit": "K",

    "RSD_P_buffer_value": 100.0,
    "RSD_P_buffer_unit": "torr",

    "RSD_sigma_sd_value": 5.7e-23,
    "RSD_sigma_sd_unit": "cm²",

    "RSD_m_Rb_value": 87.0,
    "RSD_m_Rb_unit": "u",

    "RSD_m_bg_value": 28.0,
    "RSD_m_bg_unit": "u",

    # =========================
    # R_sd result
    # =========================
    "R_sd": None,
    
    # =========================
    # R_se input parameters
    # =========================
    "RSE_T_value": 373.0,
    "RSE_T_unit": "K",

    "RSE_P_Rb_value": 2.3e-4,
    "RSE_P_Rb_unit": "torr",

    "RSE_sigma_se_value": 1.9e-14,
    "RSE_sigma_se_unit": "cm²",

    "RSE_m_Rb_value": 87.0,
    "RSE_m_Rb_unit": "u",

    # =========================
    # R_se result
    # =========================
    "R_se": None,
    
    # =========================
    # R_pr input parameters
    # =========================
    "RPR_wavelength_value": 780.0,
    "RPR_wavelength_unit": "nm",

    "RPR_intensity_value": 1.0,
    "RPR_intensity_unit": "mW/cm²",

    "RPR_gamma_nat_value": 6.0,
    "RPR_gamma_nat_unit": "MHz",

    "RPR_delta_nu_total_value": 1.76,
    "RPR_delta_nu_total_unit": "GHz",

    "RPR_detuning_value": 100.0,
    "RPR_detuning_unit": "GHz",

    "R_pr": None,
    
    # =========================
    # R_p input parameters
    # =========================
    "RP_wavelength_value": 795.0,
    "RP_wavelength_unit": "nm",

    "RP_intensity_value": 1.0,
    "RP_intensity_unit": "mW/cm²",

    "RP_gamma_nat_value": 5.75,
    "RP_gamma_nat_unit": "MHz",

    "RP_delta_nu_total_value": 1.76,
    "RP_delta_nu_total_unit": "GHz",

    # =========================
    # R_p results
    # =========================
    "R_p": None,
}


def init_state():
    for key, value in DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = value


def sync_from_rd():
    # R_D → R_sd
    st.session_state["RSD_T_value"] = st.session_state["T_value"]
    st.session_state["RSD_T_unit"] = st.session_state["T_unit"]

    st.session_state["RSD_P_buffer_value"] = (
        st.session_state["P_buffer_value"]
    )
    st.session_state["RSD_P_buffer_unit"] = (
        st.session_state["P_buffer_unit"]
    )

    # R_D → R_se
    st.session_state["RSE_T_value"] = st.session_state["T_value"]
    st.session_state["RSE_T_unit"] = st.session_state["T_unit"]

def sync_from_rsd():
    # R_sd → R_D
    st.session_state["T_value"] = st.session_state["RSD_T_value"]
    st.session_state["T_unit"] = st.session_state["RSD_T_unit"]

    st.session_state["P_buffer_value"] = (
        st.session_state["RSD_P_buffer_value"]
    )
    st.session_state["P_buffer_unit"] = (
        st.session_state["RSD_P_buffer_unit"]
    )

    # R_sd → R_se
    st.session_state["RSE_T_value"] = st.session_state["RSD_T_value"]
    st.session_state["RSE_T_unit"] = st.session_state["RSD_T_unit"]
    
def sync_from_rse():
    # R_se → R_D
    st.session_state["T_value"] = st.session_state["RSE_T_value"]
    st.session_state["T_unit"] = st.session_state["RSE_T_unit"]

    # R_se → R_sd
    st.session_state["RSD_T_value"] = st.session_state["RSE_T_value"]
    st.session_state["RSD_T_unit"] = st.session_state["RSE_T_unit"]
    
    #注意這裡只同步溫度，不同步 RSE_P_Rb_value 因為 Rb vapor pressure 和 buffer gas pressure 是不同物理量。