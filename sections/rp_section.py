import streamlit as st

from calculations import (
    optical_frequency,
    resonant_cross_section,
    probing_rate,
)

from units import (
    wavelength_to_m,
    frequency_to_hz,
    intensity_to_w_per_m2,
)


def number_with_unit(
    label,
    value_key,
    unit_key,
    unit_options,
    number_format="%.6g"
):
    st.write(label)

    col_value, col_unit = st.columns([2, 1])

    with col_value:
        value = st.number_input(
            label + " value",
            value=st.session_state[value_key],
            key=value_key,
            label_visibility="collapsed",
            format=number_format
        )

    with col_unit:
        unit = st.selectbox(
            label + " unit",
            unit_options,
            index=unit_options.index(st.session_state[unit_key]),
            key=unit_key,
            label_visibility="collapsed"
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


def render_rp_section():
    st.header("R_p：Pumping rate")

    st.write(
        "計算 pump light 對原子造成的 pumping rate。"
    )

    st.subheader("1. Input parameters")

    col1, col2 = st.columns(2)

    with col1:
        wavelength_value, wavelength_unit = number_with_unit(
            "Pump wavelength λ",
            "RP_wavelength_value",
            "RP_wavelength_unit",
            ["nm", "μm", "m"]
        )

        intensity_value, intensity_unit = number_with_unit(
            "Pump intensity I",
            "RP_intensity_value",
            "RP_intensity_unit",
            ["mW/cm²", "W/m²"]
        )

    with col2:
        gamma_nat_value, gamma_nat_unit = number_with_unit(
            "Natural linewidth Γ_nat",
            "RP_gamma_nat_value",
            "RP_gamma_nat_unit",
            ["MHz", "GHz", "Hz"]
        )

        delta_nu_total_value, delta_nu_total_unit = number_with_unit(
            "Total linewidth Δν_total",
            "RP_delta_nu_total_value",
            "RP_delta_nu_total_unit",
            ["GHz", "MHz", "Hz"]
        )

    st.divider()

    st.subheader("2. Unit conversion")

    wavelength_m = wavelength_to_m(
        wavelength_value,
        wavelength_unit
    )

    intensity_w_m2 = intensity_to_w_per_m2(
        intensity_value,
        intensity_unit
    )

    gamma_nat_hz = frequency_to_hz(
        gamma_nat_value,
        gamma_nat_unit
    )

    delta_nu_total_hz = frequency_to_hz(
        delta_nu_total_value,
        delta_nu_total_unit
    )

    text_card([
        f"λ = {wavelength_value:g} {wavelength_unit} = {wavelength_m:.4g} m",
        f"I = {intensity_value:g} {intensity_unit} = {intensity_w_m2:.4g} W/m²",
        f"Γ_nat = {gamma_nat_value:g} {gamma_nat_unit} = {gamma_nat_hz:.4g} Hz",
        f"Δν_total = {delta_nu_total_value:g} {delta_nu_total_unit} = {delta_nu_total_hz:.4g} Hz",
    ])

    st.divider()

    st.subheader("3. Calculation process")

    frequency = optical_frequency(wavelength_m)

    sigma_0 = resonant_cross_section(
        wavelength_m,
        gamma_nat_hz,
        delta_nu_total_hz
    )

    R_p = probing_rate(
        sigma_0,
        intensity_w_m2,
        frequency
    )

    tau_p_ms = 1000 / R_p

    frequency_formula = (
        rf"$\displaystyle "
        rf"\nu=\frac{{c}}{{\lambda}}"
        rf"=\frac{{2.9979\times10^8}}{{{wavelength_m:.4g}}}"
        rf"={frequency:.4g}\ \mathrm{{Hz}}"
        rf"$"
    )

    sigma0_formula = (
        rf"$\displaystyle "
        rf"\sigma_0"
        rf"=\frac{{\lambda^2}}{{2\pi}}"
        rf"\frac{{\Gamma_{{nat}}}}{{\Delta\nu_{{total}}}}"
        rf"=\frac{{({wavelength_m:.4g})^2}}{{2\pi}}"
        rf"\frac{{{gamma_nat_hz:.4g}}}{{{delta_nu_total_hz:.4g}}}"
        rf"={sigma_0:.4g}\ \mathrm{{m^2}}"
        rf"$"
    )

    Rp_formula = (
        rf"$\displaystyle "
        rf"R_p"
        rf"=\frac{{\sigma_0 I}}{{h\nu}}"
        rf"=\frac{{{sigma_0:.4g}\times {intensity_w_m2:.4g}}}"
        rf"{{6.6261\times10^{{-34}}\times {frequency:.4g}}}"
        rf"={R_p:.4g}\ \mathrm{{s^{{-1}}}}"
        rf"$"
    )

    with st.container(border=True):
        st.markdown(frequency_formula)
        st.markdown(sigma0_formula)
        st.markdown(Rp_formula)

    st.divider()

    st.subheader("4. Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        result_card(
            "R_p",
            f"{R_p:.4g} s⁻¹",
            "Pumping rate"
        )

    with result_col2:
        result_card(
            "τ_p",
            f"{tau_p_ms:.4g} ms",
            "Pumping time constant"
        )

    st.session_state["R_p"] = R_p
