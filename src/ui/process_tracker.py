"""Prozesuaren jarraipen bisuala: makro-faseak eta mikro-urratsak."""

from __future__ import annotations

import streamlit as st

from src.i18n import eu


ANALYSIS_PHASES = {"1_URRATSA", "2_URRATSA", "3_URRATSA"}


def _macro_phase_index(fase: str) -> int:
    if fase == "HASIERA":
        return 0
    if fase == "KONFIG":
        return 1
    if fase in ANALYSIS_PHASES:
        return 2
    return 3


def render_macro_tracker(fase: str) -> None:
    current_idx = _macro_phase_index(fase)
    cols = st.columns(len(eu.MACRO_PHASES))

    for i, phase in enumerate(eu.MACRO_PHASES):
        label = phase["label"]
        with cols[i]:
            if i < current_idx:
                st.success(f"✓ {label}")
            elif i == current_idx:
                with st.container(border=True):
                    st.markdown(f"**▶ {label}**")
            else:
                st.caption(f"○ {label}")

    phase_info = eu.PHASES.get(fase)
    if phase_info and fase != "HASIERA":
        st.info(phase_info["description"])


def _render_station_dots(total: int, current: int, completed: int) -> None:
    dots = []
    for i in range(total):
        if i < completed:
            dots.append("🟢")
        elif i == current:
            dots.append("🔵")
        else:
            dots.append("⚪")
    st.markdown(f"**{eu.TRACKER['station_map_title']}:** {' '.join(dots)}")


def render_micro_tracker(fase: str) -> None:
    if fase not in ANALYSIS_PHASES:
        return

    total = st.session_state.puntu_kopurua
    current_station = st.session_state.uneko_estazioa
    completed_stations = current_station

    pct = int((completed_stations / total) * 100) if total else 0
    st.caption(eu.TRACKER["blade_progress"].format(pct=pct))
    st.progress(completed_stations / total if total else 0.0)
    st.caption(
        eu.TRACKER["station_label"].format(current=current_station + 1, total=total)
    )
    _render_station_dots(total, current_station, completed_stations)

    st.markdown(f"**{eu.TRACKER['substep_label']}**")
    sub_cols = st.columns(len(eu.MICRO_STEPS))
    for i, step in enumerate(eu.MICRO_STEPS):
        with sub_cols[i]:
            if step["id"] == fase:
                st.markdown(f"**▶ {step['label']}**")
            elif (fase == "2_URRATSA" and step["id"] == "1_URRATSA") or (
                fase == "3_URRATSA" and step["id"] in {"1_URRATSA", "2_URRATSA"}
            ):
                st.success(f"✓ {step['label']}")
            else:
                st.caption(f"○ {step['label']}")

    st.divider()


def render_process_tracker(fase: str) -> None:
    if fase == "HASIERA":
        return

    render_macro_tracker(fase)
    render_micro_tracker(fase)
