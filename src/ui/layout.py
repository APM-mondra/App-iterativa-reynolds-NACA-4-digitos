"""Layout nagusia: header, sidebar eta stepper."""

from __future__ import annotations

import streamlit as st

from src.physics import calc_reynolds, calc_station_metrics


PHASE_LABELS = {
    "KONFIG": "Konfig",
    "1_URRATSA": "M",
    "2_URRATSA": "P",
    "3_URRATSA": "T",
    "LABURPENA": "Laburpena",
}

STEP_ORDER = ["KONFIG", "1_URRATSA", "2_URRATSA", "3_URRATSA", "LABURPENA"]


def render_header() -> None:
    st.title(f"Hegalaren Diseinua - {st.session_state.iterazioa}. Iterazioa")
    st.caption("Diseinu iteratiboa NeuralFoil erabiliz | Bertsio garapena")


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Ezarpen orokorrak")

        rpm_berria = st.number_input(
            "RPM",
            min_value=1.0,
            value=float(st.session_state.rpm),
            step=1.0,
        )
        v_rated_berria = st.number_input(
            "Haize-abiadura (m/s)",
            min_value=0.1,
            value=float(st.session_state.v_rated),
            step=0.1,
        )

        params_changed = (
            rpm_berria != st.session_state.rpm
            or v_rated_berria != st.session_state.v_rated
        )
        if params_changed:
            st.session_state.rpm = rpm_berria
            st.session_state.v_rated = v_rated_berria
            st.session_state.aero_cache = {}
            st.rerun()

        st.divider()
        st.subheader("Alpha analisia")
        alpha_min = st.number_input(
            "Gutxienekoa (°)",
            value=float(st.session_state.alpha_min),
            step=1.0,
        )
        alpha_max = st.number_input(
            "Gehienezkoa (°)",
            value=float(st.session_state.alpha_max),
            step=1.0,
        )
        alpha_steps = st.slider(
            "Alpha urratsak",
            min_value=30,
            max_value=120,
            value=int(st.session_state.alpha_steps),
            step=10,
            help="Balio txikiagoek kalkulua azkarrago egiten dute.",
        )

        alpha_changed = (
            alpha_min != st.session_state.alpha_min
            or alpha_max != st.session_state.alpha_max
            or alpha_steps != st.session_state.alpha_steps
        )
        if alpha_changed:
            st.session_state.alpha_min = alpha_min
            st.session_state.alpha_max = alpha_max
            st.session_state.alpha_steps = alpha_steps
            st.session_state.aero_cache = {}
            st.rerun()

        st.divider()
        st.metric("Fasea", PHASE_LABELS.get(st.session_state.fase, st.session_state.fase))
        if st.session_state.fase not in ["KONFIG", "LABURPENA"]:
            st.metric(
                "Estazioa",
                f"{st.session_state.uneko_estazioa + 1} / {st.session_state.puntu_kopurua}",
            )

        if st.button("Konfiguraziora itzuli", use_container_width=True):
            st.session_state.fase = "KONFIG"
            st.rerun()


def render_stepper() -> None:
    if st.session_state.fase == "LABURPENA":
        current_idx = STEP_ORDER.index("LABURPENA")
    else:
        current_idx = STEP_ORDER.index(st.session_state.fase)

    cols = st.columns(len(STEP_ORDER))
    for i, phase in enumerate(STEP_ORDER):
        label = PHASE_LABELS[phase]
        if i < current_idx:
            cols[i].success(f"{i + 1}. {label}")
        elif i == current_idx:
            cols[i].info(f"{i + 1}. {label}")
        else:
            cols[i].caption(f"{i + 1}. {label}")


def render_station_banner() -> None:
    if st.session_state.fase in ["KONFIG", "LABURPENA"]:
        return

    idx = st.session_state.uneko_estazioa
    r_unekoa = st.session_state.erradioak[idx]
    c_unekoa = st.session_state.kordak[idx]
    metrics = calc_station_metrics(r_unekoa, c_unekoa, st.session_state.rpm, st.session_state.v_rated)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Estazioa", f"{idx + 1} / {st.session_state.puntu_kopurua}")
    col2.metric("Erradioa", f"{r_unekoa:.3f} m")
    col3.metric("Korda", f"{c_unekoa:.3f} m")
    col4.metric("Reynolds", f"{metrics['reynolds']:.2e}")
    col5.metric("TSR (lambda)", f"{metrics['lambda']:.2f}")

    st.progress(idx / st.session_state.puntu_kopurua)
    st.divider()
