"""Layout nagusia: header, sidebar eta estazio-banner."""

from __future__ import annotations

import streamlit as st

from src.i18n import eu
from src.physics import calc_station_metrics
from src.state import go_to_hasiera, reset_to_konfig
from src.ui.theme import academic_warning, header_rule, section_divider


ANALYSIS_PHASES = {"1_URRATSA", "2_URRATSA", "3_URRATSA"}


def render_header() -> None:
    if st.session_state.fase == "HASIERA":
        st.title(eu.APP_TITLE)
        st.markdown(f"*{eu.APP_CAPTION}*")
        header_rule()
        return

    phase = eu.PHASES.get(st.session_state.fase, {})
    st.title(f"{eu.APP_TITLE}")
    st.markdown(
        f"**{st.session_state.iterazioa}. iterazioa** — {phase.get('title', '')}"
    )
    st.markdown(f"*{eu.APP_CAPTION}*")
    header_rule()


def render_sidebar() -> None:
    fase = st.session_state.fase

    if fase in {"HASIERA", "KONFIG"}:
        return

    with st.sidebar:
        if fase in ANALYSIS_PHASES:
            st.markdown(f"### {eu.SIDEBAR['title_analysis']}")
            st.markdown(f"**{eu.SIDEBAR['nominal_title']}**")
            st.metric(eu.SIDEBAR["rpm"], f"{st.session_state.rpm:.0f}")
            st.metric(eu.SIDEBAR["wind_speed"], f"{st.session_state.v_rated:.1f}")

            section_divider()
            st.metric(eu.SIDEBAR["iteration"], st.session_state.iterazioa)
            st.metric(
                eu.SIDEBAR["station"],
                f"{st.session_state.uneko_estazioa + 1} / {st.session_state.puntu_kopurua}",
            )

            section_divider()
            st.markdown(f"**{eu.SIDEBAR['selected_profiles']}**")
            if st.session_state.amaierako_nacak:
                for i, naca in enumerate(st.session_state.amaierako_nacak, start=1):
                    st.markdown(f"{i}. NACA {naca}")
            else:
                st.markdown(f"*{eu.SIDEBAR['no_profiles_yet']}*")

            section_divider()
            if not st.session_state.confirm_reset_config:
                if st.button(eu.SIDEBAR["back_to_config"], use_container_width=True):
                    st.session_state.confirm_reset_config = True
                    st.rerun()
            else:
                academic_warning(eu.SIDEBAR["back_to_config_warning"])
                col_yes, col_no = st.columns(2)
                if col_yes.button(eu.SIDEBAR["confirm_reset"], use_container_width=True):
                    reset_to_konfig()
                if col_no.button(eu.SIDEBAR["cancel"], use_container_width=True):
                    st.session_state.confirm_reset_config = False
                    st.rerun()

        elif fase == "LABURPENA":
            st.markdown(f"### {eu.SIDEBAR['title_summary']}")
            st.metric(eu.SIDEBAR["iteration"], st.session_state.iterazioa)
            st.metric(eu.SIDEBAR["station"], st.session_state.puntu_kopurua)
            st.metric(eu.SIDEBAR["rpm"], f"{st.session_state.rpm:.0f}")
            st.metric(eu.SIDEBAR["wind_speed"], f"{st.session_state.v_rated:.1f}")
            section_divider()
            if st.button(eu.SIDEBAR["back_to_home"], use_container_width=True):
                go_to_hasiera()


def render_station_banner() -> None:
    if st.session_state.fase not in ANALYSIS_PHASES:
        return

    idx = st.session_state.uneko_estazioa
    r_unekoa = st.session_state.erradioak[idx]
    c_unekoa = st.session_state.kordak[idx]
    metrics = calc_station_metrics(
        r_unekoa, c_unekoa, st.session_state.rpm, st.session_state.v_rated
    )

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric(
        eu.METRICS["station"],
        f"{idx + 1} / {st.session_state.puntu_kopurua}",
    )
    col2.metric(eu.METRICS["radius"], f"{r_unekoa:.3f} m")
    col3.metric(eu.METRICS["chord"], f"{c_unekoa:.3f} m")
    col4.metric(eu.METRICS["reynolds"], f"{metrics['reynolds']:.2e}")
    col5.metric(eu.METRICS["tsr"], f"{metrics['lambda']:.2f}")

    section_divider()
