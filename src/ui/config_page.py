"""Konfigurazio fasearen UI."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from src.physics import calc_lambda, calc_reynolds_array
from src.plots import build_blade_planform_figure, build_reynolds_figure, build_tsr_figure
from src.state import fasea_aldatu, reset_iteration_state, update_geometry_from_params


def render_config_page() -> None:
    st.header("Iterazioaren konfigurazioa")

    col_param, col_sec = st.columns(2)

    with col_param:
        st.subheader("Parametro nagusiak")
        with st.container(border=True):
            erradio_min_berria = st.number_input(
                "Hasierako erradioa - Hub (m)",
                min_value=0.01,
                value=float(st.session_state.erradio_min),
                step=0.01,
            )
            erradio_max_berria = st.number_input(
                "Gehienezko erradioa (m)",
                min_value=0.05,
                value=float(st.session_state.erradio_max),
                step=0.01,
            )
            korda_base_berria = st.number_input(
                "Oinarrizko korda (m)",
                min_value=0.01,
                value=float(st.session_state.korda_base),
                step=0.01,
            )

            geom_changed = (
                erradio_min_berria != st.session_state.erradio_min
                or erradio_max_berria != st.session_state.erradio_max
                or korda_base_berria != st.session_state.korda_base
            )
            if geom_changed:
                st.session_state.erradio_min = erradio_min_berria
                st.session_state.erradio_max = erradio_max_berria
                st.session_state.korda_base = korda_base_berria
                update_geometry_from_params()
                st.session_state.aero_cache = {}
                st.rerun()

    with col_sec:
        st.subheader("Hegalaren sekzioak")
        with st.container(border=True):
            sekzio_berriak = st.number_input(
                "Estazio (puntu) kopurua",
                min_value=2,
                max_value=30,
                value=int(st.session_state.puntu_kopurua),
                step=1,
            )
            if sekzio_berriak != st.session_state.puntu_kopurua:
                st.session_state.puntu_kopurua = sekzio_berriak
                update_geometry_from_params()
                st.session_state.aero_cache = {}
                st.rerun()

    reynolds_array = calc_reynolds_array(
        st.session_state.erradioak,
        st.session_state.kordak,
        st.session_state.rpm,
        st.session_state.v_rated,
    )
    lambda_array = calc_lambda(
        st.session_state.erradioak,
        st.session_state.rpm,
        st.session_state.v_rated,
    )
    estazioak = list(range(1, st.session_state.puntu_kopurua + 1))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Pala luzera", f"{st.session_state.erradio_max - st.session_state.erradio_min:.2f} m")
    m2.metric("TSR medio", f"{float(np.mean(lambda_array)):.2f}")
    m3.metric("Reynolds min", f"{float(np.min(reynolds_array)):.2e}")
    m4.metric("Reynolds max", f"{float(np.max(reynolds_array)):.2e}")

    tab_plan, tab_re, tab_tsr = st.tabs(["Planoa", "Reynolds", "TSR"])

    with tab_plan:
        st.plotly_chart(
            build_blade_planform_figure(st.session_state.erradioak, st.session_state.kordak),
            use_container_width=True,
            key="config_planform",
        )

    with tab_re:
        st.plotly_chart(
            build_reynolds_figure(estazioak, reynolds_array),
            use_container_width=True,
            key="config_reynolds",
        )

    with tab_tsr:
        st.plotly_chart(
            build_tsr_figure(estazioak, lambda_array),
            use_container_width=True,
            key="config_tsr",
        )

    st.subheader("Uneko kordak eta Reynolds datuak")
    df_kordak = pd.DataFrame(
        {
            "Estazioa": estazioak,
            "Erradioa [m]": np.round(st.session_state.erradioak, 3),
            "Korda [m]": np.round(st.session_state.kordak, 3),
            "Reynolds": [f"{re:.2e}" for re in reynolds_array],
            "TSR": np.round(lambda_array, 2),
        }
    )

    df_editatua = st.data_editor(
        df_kordak,
        num_rows="fixed",
        hide_index=True,
        use_container_width=True,
        disabled=["Estazioa", "Erradioa [m]", "Reynolds", "TSR"],
        key="config_chord_editor",
    )
    st.session_state.kordak = df_editatua["Korda [m]"].values

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Estazioen analisia hasi", type="primary", use_container_width=True):
            reset_iteration_state()
            fasea_aldatu("1_URRATSA")
