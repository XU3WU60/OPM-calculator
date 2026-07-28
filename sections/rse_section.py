import streamlit as st

from calculations import (
    gas_density,
    thermal_relative_velocity,
    spin_exchange_rate,
)

from units import (
    temperature_to_K,
    pressure_to_pa,
    area_to_m2,
    mass_to_kg,
)

from state import sync_from_rse


ATOMIC_MASS_UNIT = 1.66053906660e-27


def number_with_unit(
    label,
    value_key,
    unit_key,
    unit_options,
    on_change=None
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
            format="%.6g"
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


def render_rse_section():
    st.header("R_se：Spin-exchange collision rate")

    st.write(
        "這一頁計算 Rb 原子彼此碰撞所造成的 "
        "spin-exchange collision rate。"
    )

    st.subheader("1. Input parameters")

    col1, col2 = st.columns(2)

    with col1:
        T_value, T_unit = number_with_unit(
            "Temperature T",
            "RSE_T_value",
            "RSE_T_unit",
            ["K", "°C"],
            on_change=sync_from_rse
        )

        P_Rb_value, P_Rb_unit = number_with_unit(
            "Rb vapor pressure P_Rb",
            "RSE_P_Rb_value",
            "RSE_P_Rb_unit",
            ["torr", "Pa", "atm"]
        )

    with col2:
        sigma_se_value, sigma_se_unit = number_with_unit(
            "Spin-exchange cross section σ_se",
            "RSE_sigma_se_value",
            "RSE_sigma_se_unit",
            ["cm²", "m²"]
        )

    with st.expander(
        "Advanced atomic mass parameter",
        expanded=False
    ):
        m_Rb_value, m_Rb_unit = number_with_unit(
            "Rb mass m_Rb",
            "RSE_m_Rb_value",
            "RSE_m_Rb_unit",
            ["u", "kg"]
        )

    st.divider()

    st.subheader("2. Unit conversion")

    T_K = temperature_to_K(T_value, T_unit)
    P_Rb_Pa = pressure_to_pa(P_Rb_value, P_Rb_unit)

    sigma_se_m2 = area_to_m2(
        sigma_se_value,
        sigma_se_unit
    )

    m_Rb_kg = mass_to_kg(
        m_Rb_value,
        m_Rb_unit
    )

    text_card([
        (
            f"T = {T_value:g} {T_unit} "
            f"= {T_K:.4g} K"
        ),
        (
            f"P_Rb = {P_Rb_value:.4g} {P_Rb_unit} "
            f"= {P_Rb_Pa:.4g} Pa"
        ),
        (
            f"σ_se = {sigma_se_value:.4g} "
            f"{sigma_se_unit} "
            f"= {sigma_se_m2:.4g} m²"
        ),
        (
            f"m_Rb = {m_Rb_value:g} {m_Rb_unit} "
            f"= {m_Rb_kg:.4g} kg"
        ),
    ])

    st.divider()

    st.subheader("3. Calculation process")

    n_Rb = gas_density(P_Rb_Pa, T_K)
    n_Rb_cm3 = n_Rb / 1e6

    mu_Rb = m_Rb_kg / 2
    mu_Rb_u = mu_Rb / ATOMIC_MASS_UNIT

    v_rel = thermal_relative_velocity(
        T_K,
        mu_Rb
    )

    R_se = spin_exchange_rate(
        n_Rb,
        sigma_se_m2,
        v_rel
    )

    tau_se_ms = 1000 / R_se

    density_formula = (
        rf"$\displaystyle "
        rf"n_{{Rb}}"
        rf"=\frac{{P_{{Rb}}}}{{k_B T}}"
        rf"=\frac{{{P_Rb_Pa:.4g}}}"
        rf"{{1.380649\times10^{{-23}}"
        rf"\times {T_K:.4g}}}"
        rf"={n_Rb_cm3:.4g}"
        rf"\ \mathrm{{cm^{{-3}}}}"
        rf"$"
    )

    mu_formula = (
        rf"$\displaystyle "
        rf"\mu_{{Rb}}"
        rf"=\frac{{m_{{Rb}}m_{{Rb}}}}"
        rf"{{m_{{Rb}}+m_{{Rb}}}}"
        rf"=\frac{{m_{{Rb}}}}{{2}}"
        rf"=\frac{{{m_Rb_value:g}}}{{2}}"
        rf"={mu_Rb_u:.4g}\ u"
        rf"$"
    )

    velocity_formula = (
        rf"$\displaystyle "
        rf"v_{{rel}}"
        rf"=\sqrt{{\frac{{8k_B T}}"
        rf"{{\pi\mu_{{Rb}}}}}}"
        rf"=\sqrt{{"
        rf"\frac{{8\times1.380649\times10^{{-23}}"
        rf"\times {T_K:.4g}}}"
        rf"{{\pi\times {mu_Rb:.4g}}}"
        rf"}}"
        rf"={v_rel:.4g}\ \mathrm{{m/s}}"
        rf"$"
    )

    rate_formula = (
        rf"$\displaystyle "
        rf"R_{{se}}"
        rf"=n_{{Rb}}\sigma_{{se}}v_{{rel}}"
        rf"={n_Rb:.4g}"
        rf"\times {sigma_se_m2:.4g}"
        rf"\times {v_rel:.4g}"
        rf"={R_se:.4g}\ \mathrm{{s^{{-1}}}}"
        rf"$"
    )

    with st.container(border=True):
        st.markdown(density_formula)
        st.markdown(mu_formula)
        st.markdown(velocity_formula)
        st.markdown(rate_formula)

    st.divider()

    st.subheader("4. Result")

    result_col1, result_col2 = st.columns(2)
        
    with result_col1:
        result_card(
            "R_se",
            f"{R_se:.4g} s⁻¹",
            "Spin-exchange collision rate"
        )

    with result_col2:
        result_card(
            "τ_se",
            f"{tau_se_ms:.4g} ms",
            "Spin-exchange time constant"
        )

    st.session_state["R_se"] = R_se