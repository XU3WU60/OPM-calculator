import streamlit as st

from calculations import (
    gas_density,
    reduced_mass,
    thermal_relative_velocity,
    spin_destruction_rate,
)

from units import (
    temperature_to_K,
    pressure_to_pa,
    area_to_m2,
    mass_to_kg,
)

from state import sync_from_rsd


def number_with_unit(
    label,
    value_key,
    unit_key,
    unit_options,
    on_change=None,
    number_format="%.2f"
):
    st.write(label)

    col_value, col_unit = st.columns([2, 1])

    with col_value:
        value = st.number_input(
            label + " value",
            value=st.session_state[value_key],
            key=value_key,
            label_visibility="collapsed",
            on_change=on_change,
            format=number_format
        )

    with col_unit:
        unit = st.selectbox(
            label + " unit",
            unit_options,
            index=unit_options.index(
                st.session_state[unit_key]
            ),
            key=unit_key,
            label_visibility="collapsed",
            on_change=on_change
        )

    return value, unit


def text_card(lines):
    html_lines = "".join(
        f"""
        <div style="
            font-size: 1rem;
            margin-bottom: 0.85rem;
            color: rgba(255,255,255,0.88);
        ">
            {line}
        </div>
        """
        for line in lines
    )

    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 14px;
            padding: 1.1rem 1.4rem 0.4rem 1.4rem;
            background-color: rgba(255,255,255,0.035);
            margin-top: 0.5rem;
            margin-bottom: 1.4rem;
        ">
            {html_lines}
        </div>
        """,
        unsafe_allow_html=True
    )


def result_card(title, value, subtitle):
    st.markdown(
        f"""
        <div style="
            border: 1px solid rgba(255,255,255,0.15);
            border-radius: 14px;
            padding: 1.2rem 1.4rem;
            background-color: rgba(255,255,255,0.035);
            margin-top: 0.5rem;
            margin-bottom: 0.5rem;
        ">
            <div style="
                font-size: 1.0rem;
                font-weight: 600;
                color: rgba(255,255,255,0.72);
                margin-bottom: 0.5rem;
            ">
                {title}
            </div>
            <div style="
                font-size: 2.2rem;
                font-weight: 750;
                line-height: 1.15;
                margin-bottom: 0.45rem;
                color: rgba(255,255,255,0.96);
            ">
                {value}
            </div>
            <div style="
                font-size: 0.9rem;
                color: rgba(255,255,255,0.55);
            ">
                {subtitle}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_rsd_section():
    st.header("R_sd：Spin-destruction collision rate")

    st.write(
        "這一頁計算 Rb 原子與 buffer gas，例如 N₂，或 wall collision 造成的 spin-destruction rate。"
    )

    st.subheader("1. Input parameters")

    col1, col2 = st.columns(2)

    with col1:
        T_value, T_unit = number_with_unit(
            "Temperature T",
            "RSD_T_value",
            "RSD_T_unit",
            ["K", "°C"],
            on_change=sync_from_rsd
        )

        P_value, P_unit = number_with_unit(
            "Buffer gas pressure P",
            "RSD_P_buffer_value",
            "RSD_P_buffer_unit",
            ["torr", "Pa", "atm"],
            on_change=sync_from_rsd
        )

    with col2:
        sigma_sd_value, sigma_sd_unit = number_with_unit(
        "Spin-destruction cross section σ_sd",
        "RSD_sigma_sd_value",
        "RSD_sigma_sd_unit",
        ["cm²", "m²"],
        number_format="%.3e"
    )

    with st.expander("Advanced mass parameters", expanded=False):
        col_m1, col_m2 = st.columns(2)

        with col_m1:
            m_Rb_value, m_Rb_unit = number_with_unit(
                "Rb mass m_Rb",
                "RSD_m_Rb_value",
                "RSD_m_Rb_unit",
                ["u", "kg"]
            )

        with col_m2:
            m_bg_value, m_bg_unit = number_with_unit(
                "Buffer gas mass m_bg",
                "RSD_m_bg_value",
                "RSD_m_bg_unit",
                ["u", "kg"]
            )

    st.divider()

    st.subheader("2. Unit conversion")

    T_K = temperature_to_K(T_value, T_unit)
    P_Pa = pressure_to_pa(P_value, P_unit)
    sigma_sd_m2 = area_to_m2(sigma_sd_value, sigma_sd_unit)
    m_Rb_kg = mass_to_kg(m_Rb_value, m_Rb_unit)
    m_bg_kg = mass_to_kg(m_bg_value, m_bg_unit)

    text_card([
        f"T = {T_value:g} {T_unit} = {T_K:.4g} K",
        f"P = {P_value:g} {P_unit} = {P_Pa:.4g} Pa",
        f"σ_sd = {sigma_sd_value:.4g} {sigma_sd_unit} = {sigma_sd_m2:.4g} m²",
        f"m_Rb = {m_Rb_value:g} {m_Rb_unit} = {m_Rb_kg:.4g} kg",
        f"m_bg = {m_bg_value:g} {m_bg_unit} = {m_bg_kg:.4g} kg",
    ])

    st.divider()

    st.subheader("3. Calculation process")

    n_bg = gas_density(P_Pa, T_K)
    n_bg_cm3 = n_bg / 1e6

    mu = reduced_mass(m_Rb_kg, m_bg_kg)
    mu_u = mu / 1.66053906660e-27

    v = thermal_relative_velocity(T_K, mu)
    R_sd = spin_destruction_rate(n_bg, sigma_sd_m2, v)
    tau_sd_ms = 1000 / R_sd

    n_formula = (
        rf"$\displaystyle "
        rf"n_{{bg}} = \frac{{P}}{{k_B T}}"
        rf" = \frac{{{P_Pa:.4g}}}{{1.380649\times10^{{-23}}\times {T_K:.4g}}}"
        rf" = {n_bg_cm3:.4g}\ \mathrm{{cm^{{-3}}}}"
        rf"$"
    )

    mu_formula = (
        rf"$\displaystyle "
        rf"\mu = \frac{{m_{{Rb}}m_{{bg}}}}{{m_{{Rb}}+m_{{bg}}}}"
        rf" = \frac{{{m_Rb_value:g}\times {m_bg_value:g}}}"
        rf"{{{m_Rb_value:g}+{m_bg_value:g}}}"
        rf" = {mu_u:.4g}\ u"
        rf"$"
    )

    v_formula = (
        rf"$\displaystyle "
        rf"v = \sqrt{{\frac{{8k_B T}}{{\pi\mu}}}}"
        rf" = \sqrt{{\frac{{8\times1.380649\times10^{{-23}}\times {T_K:.4g}}}"
        rf"{{\pi\times {mu:.4g}}}}}"
        rf" = {v:.4g}\ \mathrm{{m/s}}"
        rf"$"
    )

    Rsd_formula = (
        rf"$\displaystyle "
        rf"R_{{sd}} = n_{{bg}}\sigma_{{sd}}v"
        rf" = {n_bg:.4g}\times {sigma_sd_m2:.4g}\times {v:.4g}"
        rf" = {R_sd:.4g}\ \mathrm{{s^{{-1}}}}"
        rf"$"
    )

    with st.container(border=True):
        st.markdown(n_formula)
        st.markdown(mu_formula)
        st.markdown(v_formula)
        st.markdown(Rsd_formula)

    st.divider()

    st.subheader("4. Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        result_card(
            "R_sd",
            f"{R_sd:.4g} s⁻¹",
            "Spin-destruction collision rate"
        )

    with result_col2:
        result_card(
            "τ_sd",
            f"{tau_sd_ms:.4g} ms",
            "Spin-destruction time constant"
        )

    st.session_state["R_sd"] = R_sd