import streamlit as st


def render_summary():
    st.sidebar.header("Summary")

    R_D = st.session_state.get("R_D", None)
    R_sd = st.session_state.get("R_sd", None)
    R_se = st.session_state.get("R_se", None)
    R_pr = st.session_state.get("R_pr", None)
    R_p = st.session_state.get("R_p", None)

    if (
        R_D is None
        and R_sd is None
        and R_se is None
        and R_pr is None
        and R_p is None
    ):
        st.sidebar.info("尚未計算結果")
        return

    if R_D is not None:
        tau_D_ms = 1000 / R_D

        st.sidebar.markdown(
            f"""
            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-top: 1rem;
                margin-bottom: 1rem;
            ">
                <b>R_D</b> = {R_D:.3g} s⁻¹<br>
                <b>τ_D</b> = {tau_D_ms:.3g} ms
            </div>
            """,
            unsafe_allow_html=True
        )

    if R_sd is not None:
        tau_sd_ms = 1000 / R_sd

        st.sidebar.markdown(
            f"""
            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-top: 1rem;
                margin-bottom: 1rem;
            ">
                <b>R_sd</b> = {R_sd:.3g} s⁻¹<br>
                <b>τ_sd</b> = {tau_sd_ms:.3g} ms
            </div>
            """,
            unsafe_allow_html=True
        )

    if R_se is not None:
        tau_se_ms = 1000 / R_se

        st.sidebar.markdown(
            f"""
            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-top: 1rem;
                margin-bottom: 1rem;
            ">
                <b>R_se</b> = {R_se:.3g} s⁻¹<br>
                <b>τ_se</b> = {tau_se_ms:.3g} ms
            </div>
            """,
            unsafe_allow_html=True
        )

    if R_pr is not None:
        tau_pr_ms = 1000 / R_pr

        st.sidebar.markdown(
            f"""
            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-top: 1rem;
                margin-bottom: 1rem;
            ">
                <b>R_pr</b> = {R_pr:.3g} s⁻¹<br>
                <b>τ_pr</b> = {tau_pr_ms:.3g} ms
            </div>
            """,
            unsafe_allow_html=True
        )

    if R_p is not None:
        tau_p_ms = 1000 / R_p

        st.sidebar.markdown(
            f"""
            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-top: 1rem;
                margin-bottom: 1rem;
            ">
                <b>R_p</b> = {R_p:.3g} s⁻¹<br>
                <b>τ_p</b> = {tau_p_ms:.3g} ms
            </div>
            """,
            unsafe_allow_html=True
        )

    # =========================
    # Compare rates
    # =========================
    rates = {
        "R_D": R_D,
        "R_sd": R_sd,
        "R_se": R_se,
        "R_pr": R_pr,
        "R_p": R_p,
    }

    valid_rates = {
        name: value
        for name, value in rates.items()
        if value is not None and value > 0
    }

    if len(valid_rates) >= 2:
        sorted_rates = sorted(
            valid_rates.items(),
            key=lambda item: item[1],
            reverse=True
        )

        comparison_text = " > ".join(
            name for name, value in sorted_rates
        )

        st.sidebar.markdown(
            f"""
            <hr style="
                border: none;
                border-top: 1px solid rgba(255,255,255,0.2);
                margin-top: 1.2rem;
                margin-bottom: 1.2rem;
            ">

            <div style="
                font-size: 1.05rem;
                line-height: 1.7;
                margin-bottom: 1rem;
            ">
                <b>Comparison</b><br>
                {comparison_text}
            </div>
            """,
            unsafe_allow_html=True
        )