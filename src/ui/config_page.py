"""Konfigurazio fasearen UI."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from src.i18n import eu
from src.physics import calc_lambda, calc_reynolds_array
from src.plots import build_blade_planform_figure, build_reynolds_figure, build_tsr_figure
from src.state import fasea_aldatu, go_to_hasiera, reset_iteration_state, update_geometry_from_params
from src.ui.theme import academic_note, section_divider


def _handle_nominal_change() -> None:
    st.session_state.aero_cache = {}


def render_config_page() -> None:
    academic_note(eu.PHASES["KONFIG"]["description"])

    st.markdown(f"### {eu.CONFIG['nominal_title']}")
    st.markdown(f"*{eu.CONFIG['nominal_help']}*")

    col_nom, col_geom, col_sec = st.columns(3)

    with col_nom:
        rpm_berria = st.number_input(
            eu.CONFIG["rpm"],
            min_value=1.0,
            value=float(st.session_state.rpm),
            step=1.0,
        )
        v_rated_berria = st.number_input(
            eu.CONFIG["wind_speed"],
            min_value=0.1,
            value=float(st.session_state.v_rated),
            step=0.1,
        )

        if rpm_berria != st.session_state.rpm or v_rated_berria != st.session_state.v_rated:
            st.session_state.rpm = rpm_berria
            st.session_state.v_rated = v_rated_berria
            _handle_nominal_change()
            st.rerun()

    with col_geom:
        st.markdown(f"**{eu.CONFIG['geometry_title']}**")
        erradio_min_berria = st.number_input(
            eu.CONFIG["hub_radius"],
            min_value=0.01,
            value=float(st.session_state.erradio_min),
            step=0.01,
        )
        erradio_max_berria = st.number_input(
            eu.CONFIG["max_radius"],
            min_value=0.05,
            value=float(st.session_state.erradio_max),
            step=0.01,
        )
        korda_base_berria = st.number_input(
            eu.CONFIG["base_chord"],
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
            _handle_nominal_change()
            st.rerun()

    with col_sec:
        st.markdown(f"**{eu.CONFIG['sections_title']}**")
        sekzio_berriak = st.number_input(
            eu.CONFIG["station_count"],
            min_value=2,
            max_value=30,
            value=int(st.session_state.puntu_kopurua),
            step=1,
        )
        if sekzio_berriak != st.session_state.puntu_kopurua:
            st.session_state.puntu_kopurua = sekzio_berriak
            update_geometry_from_params()
            _handle_nominal_change()
            st.rerun()

    with st.expander(eu.CONFIG["aero_expander"]):
        alpha_min = st.number_input(
            eu.CONFIG["alpha_min"],
            value=float(st.session_state.alpha_min),
            step=1.0,
        )
        alpha_max = st.number_input(
            eu.CONFIG["alpha_max"],
            value=float(st.session_state.alpha_max),
            step=1.0,
        )
        alpha_steps = st.slider(
            eu.CONFIG["alpha_steps"],
            min_value=30,
            max_value=120,
            value=int(st.session_state.alpha_steps),
            step=10,
            help=eu.CONFIG["alpha_steps_help"],
        )
        if (
            alpha_min != st.session_state.alpha_min
            or alpha_max != st.session_state.alpha_max
            or alpha_steps != st.session_state.alpha_steps
        ):
            st.session_state.alpha_min = alpha_min
            st.session_state.alpha_max = alpha_max
            st.session_state.alpha_steps = alpha_steps
            _handle_nominal_change()
            st.rerun()

    section_divider()

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
    m1.metric(
        eu.CONFIG["metrics_blade_length"],
        f"{st.session_state.erradio_max - st.session_state.erradio_min:.2f} m",
    )
    m2.metric(eu.CONFIG["metrics_tsr_mean"], f"{float(np.mean(lambda_array)):.2f}")
    m3.metric(eu.CONFIG["metrics_re_min"], f"{float(np.min(reynolds_array)):.2e}")
    m4.metric(eu.CONFIG["metrics_re_max"], f"{float(np.max(reynolds_array)):.2e}")

    tab_plan, tab_re, tab_tsr = st.tabs(
        [eu.CONFIG["tab_planform"], eu.CONFIG["tab_reynolds"], eu.CONFIG["tab_tsr"]]
    )

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

    st.markdown(f"### {eu.CONFIG['chords_title']}")
    df_kordak = pd.DataFrame(
        {
            eu.CONFIG["col_station"]: estazioak,
            eu.CONFIG["col_radius"]: np.round(st.session_state.erradioak, 3),
            eu.CONFIG["col_chord"]: np.round(st.session_state.kordak, 3),
            eu.CONFIG["col_reynolds"]: [f"{re:.2e}" for re in reynolds_array],
            "TSR": np.round(lambda_array, 2),
        }
    )

    df_editatua = st.data_editor(
        df_kordak,
        num_rows="fixed",
        hide_index=True,
        use_container_width=True,
        disabled=[
            eu.CONFIG["col_station"],
            eu.CONFIG["col_radius"],
            eu.CONFIG["col_reynolds"],
            "TSR",
        ],
        key="config_chord_editor",
    )
    st.session_state.kordak = df_editatua[eu.CONFIG["col_chord"]].values

    section_divider()
    col_back, col_btn, col_spacer = st.columns([1, 2, 1])
    with col_back:
        if st.button(eu.CONFIG["back_to_landing"], use_container_width=True):
            go_to_hasiera()
    with col_btn:
        if st.button(eu.CONFIG["start_analysis"], use_container_width=True):
            reset_iteration_state()
            fasea_aldatu("1_URRATSA")
