import streamlit as st

from calculations import (
    optical_frequency,
    resonant_cross_section,
    detuned_cross_section,
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


def render_rpr_section():
    st.header("R_pr：Probing rate")

    st.write(
        "這一頁計算 probe light 對原子造成的 probing rate。"
    )

    st.subheader("1. Input parameters")

    col1, col2 = st.columns(2)

    with col1:
        wavelength_value, wavelength_unit = number_with_unit(
            "Probe wavelength λ",
            "RPR_wavelength_value",
            "RPR_wavelength_unit",
            ["nm", "μm", "m"]
        )

        intensity_value, intensity_unit = number_with_unit(
            "Probe intensity I",
            "RPR_intensity_value",
            "RPR_intensity_unit",
            ["mW/cm²", "W/m²"]
        )

        detuning_value, detuning_unit = number_with_unit(
            "Detuning Δ",
            "RPR_detuning_value",
            "RPR_detuning_unit",
            ["GHz", "MHz", "Hz"]
        )

    with col2:
        gamma_nat_value, gamma_nat_unit = number_with_unit(
            "Natural linewidth Γ_nat",
            "RPR_gamma_nat_value",
            "RPR_gamma_nat_unit",
            ["MHz", "GHz", "Hz"]
        )

        delta_nu_total_value, delta_nu_total_unit = number_with_unit(
            "Total linewidth Δν_total",
            "RPR_delta_nu_total_value",
            "RPR_delta_nu_total_unit",
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

    detuning_hz = frequency_to_hz(
        detuning_value,
        detuning_unit
    )

    text_card([
        f"λ = {wavelength_value:g} {wavelength_unit} = {wavelength_m:.4g} m",
        f"I = {intensity_value:g} {intensity_unit} = {intensity_w_m2:.4g} W/m²",
        f"Γ_nat = {gamma_nat_value:g} {gamma_nat_unit} = {gamma_nat_hz:.4g} Hz",
        f"Δν_total = {delta_nu_total_value:g} {delta_nu_total_unit} = {delta_nu_total_hz:.4g} Hz",
        f"Δ = {detuning_value:g} {detuning_unit} = {detuning_hz:.4g} Hz",
    ])

    st.divider()

    st.subheader("3. Calculation process")

    frequency = optical_frequency(wavelength_m)

    sigma_0 = resonant_cross_section(
        wavelength_m,
        gamma_nat_hz,
        delta_nu_total_hz
    )

    sigma_delta = detuned_cross_section(
        sigma_0,
        delta_nu_total_hz,
        detuning_hz
    )

    R_pr_resonant = probing_rate(
        sigma_0,
        intensity_w_m2,
        frequency
    )

    R_pr = probing_rate(
        sigma_delta,
        intensity_w_m2,
        frequency
    )

    tau_pr_ms = 1000 / R_pr

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

    sigma_delta_formula = (
        rf"$\displaystyle "
        rf"\sigma(\Delta)"
        rf"=\sigma_0"
        rf"\frac{{(\Delta\nu_{{total}}/2)^2}}{{\Delta^2}}"
        rf"={sigma_0:.4g}"
        rf"\frac{{({delta_nu_total_hz:.4g}/2)^2}}{{({detuning_hz:.4g})^2}}"
        rf"={sigma_delta:.4g}\ \mathrm{{m^2}}"
        rf"$"
    )

    Rpr_formula = (
        rf"$\displaystyle "
        rf"R_{{pr}}"
        rf"=\frac{{\sigma(\Delta)I}}{{h\nu}}"
        rf"=\frac{{{sigma_delta:.4g}\times {intensity_w_m2:.4g}}}"
        rf"{{6.6261\times10^{{-34}}\times {frequency:.4g}}}"
        rf"={R_pr:.4g}\ \mathrm{{s^{{-1}}}}"
        rf"$"
    )

    Rpr0_formula = (
        rf"$\displaystyle "
        rf"R_{{pr}}(\Delta=0)"
        rf"=\frac{{\sigma_0 I}}{{h\nu}}"
        rf"={R_pr_resonant:.4g}\ \mathrm{{s^{{-1}}}}"
        rf"$"
    )

    with st.container(border=True):
        st.markdown(frequency_formula)
        st.markdown(sigma0_formula)
        st.markdown(Rpr0_formula)
        st.markdown(sigma_delta_formula)
        st.markdown(Rpr_formula)

    st.divider()

    st.subheader("4. Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        result_card(
            "R_pr",
            f"{R_pr:.4g} s⁻¹",
            "Probing rate at selected detuning"
        )

    with result_col2:
        result_card(
            "τ_pr",
            f"{tau_pr_ms:.4g} ms",
            "Probing time constant"
        )

    st.session_state["R_pr"] = R_pr