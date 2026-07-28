import streamlit as st

from calculations import diffusion_coefficient, diffusion_rate
from units import temperature_to_K, pressure_to_torr, length_to_cm
from state import sync_from_rd

def number_with_unit(label, value_key, unit_key, unit_options, on_change=None):
    st.write(label)

    col_value, col_unit = st.columns([2, 1])

    with col_value:
        value = st.number_input(
            label + " value",
            value=st.session_state[value_key],
            key=value_key,
            label_visibility="collapsed",
            on_change=on_change
        )

    with col_unit:
        unit = st.selectbox(
            label + " unit",
            unit_options,
            index=unit_options.index(st.session_state[unit_key]),
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


def render_rd_section():
    st.header("R_D：Diffusion collision rate")

    st.write(
        "計算 diffusion collision 對原子造成的 relaxation rate。"
    )

    st.subheader("1. Input parameters")

    col1, col2 = st.columns(2)

    with col1:
        T_value, T_unit = number_with_unit(
            "Temperature T",
            "T_value",
            "T_unit",
            ["K", "°C"],
            on_change=sync_from_rd
        )
        
        P_value, P_unit = number_with_unit(
            "Buffer gas pressure P",
            "P_buffer_value",
            "P_buffer_unit",
            ["torr", "Pa", "atm"],
            on_change=sync_from_rd
        )

    with col2:
        a_value, a_unit = number_with_unit(
            "Cell size a",
            "a_value",
            "a_unit",
            ["cm", "mm", "m"]
        )

        st.write("Cell geometry")

        geometry = st.selectbox(
            "Cell geometry",
            ["cube", "sphere"],
            index=["cube", "sphere"].index(st.session_state["geometry"]),
            key="geometry",
            label_visibility="collapsed"
        )

    with st.expander("Advanced reference parameters", expanded=False):
        D0 = st.number_input(
            "D0 (cm²/s)",
            value=0.33,
            key="RD_D0"
        )

        T0 = st.number_input(
            "T0 (K)",
            value=273.0,
            key="RD_T0"
        )

        P0 = st.number_input(
            "P0 (torr)",
            value=760.0,
            key="RD_P0"
        )

    st.divider()

    st.subheader("2. Unit conversion")

    T_K = temperature_to_K(T_value, T_unit)
    P_torr = pressure_to_torr(P_value, P_unit)
    a_cm = length_to_cm(a_value, a_unit)

    text_card([
        f"T = {T_value:g} {T_unit} = {T_K:.4g} K",
        f"P = {P_value:g} {P_unit} = {P_torr:.4g} torr",
        f"a = {a_value:g} {a_unit} = {a_cm:.4g} cm",
    ])

    st.divider()

    st.subheader("3. Calculation process")

    D = diffusion_coefficient(D0, P0, P_torr, T_K, T0)
    R_D = diffusion_rate(D, a_cm, geometry)
    tau_D_ms = 1000 / R_D

    D_formula = (
        rf"$\displaystyle "
        rf"D = D_0 \frac{{P_0}}{{P}}"
        rf"\left(\frac{{T}}{{T_0}}\right)^{{3/2}}"
        rf" = {D0:g}"
        rf"\times \frac{{{P0:g}}}{{{P_torr:.4g}}}"
        rf"\times \left(\frac{{{T_K:.4g}}}{{{T0:g}}}\right)^{{3/2}}"
        rf" = {D:.4g}\ \mathrm{{cm^2/s}}"
        rf"$"
    )

    if geometry == "cube":
        RD_formula = (
            rf"$\displaystyle "
            rf"R_D = 3D\left(\frac{{\pi}}{{a}}\right)^2"
            rf" = 3 \times {D:.4g}"
            rf"\times \left(\frac{{\pi}}{{{a_cm:.4g}}}\right)^2"
            rf" = {R_D:.4g}\ \mathrm{{s^{{-1}}}}"
            rf"$"
        )
    else:
        RD_formula = (
            rf"$\displaystyle "
            rf"R_D = D\left(\frac{{\pi}}{{a}}\right)^2"
            rf" = {D:.4g}"
            rf"\times \left(\frac{{\pi}}{{{a_cm:.4g}}}\right)^2"
            rf" = {R_D:.4g}\ \mathrm{{s^{{-1}}}}"
            rf"$"
        )

    with st.container(border=True):
        st.markdown(D_formula)
        st.markdown(RD_formula)

    st.divider()

    st.subheader("4. Result")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        result_card(
            "R_D",
            f"{R_D:.4g} s⁻¹",
            "Diffusion collision rate"
        )

    with result_col2:
        result_card(
            "τ_D",
            f"{tau_D_ms:.4g} ms",
            "Diffusion time constant"
        )

    st.session_state["R_D"] = R_D
