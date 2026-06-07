"""Prozesuaren jarraipen bisuala — estilo tipografiko sobrio."""

from __future__ import annotations

import html

import streamlit as st

from src.i18n import eu
from src.ui.theme import ROMAN_NUMERALS, academic_note, section_divider


ANALYSIS_PHASES = {"1_URRATSA", "2_URRATSA", "3_URRATSA"}
MICRO_STEP_INDEX = {"1_URRATSA": 0, "2_URRATSA": 1, "3_URRATSA": 2}


def _macro_phase_index(fase: str) -> int:
    if fase == "HASIERA":
        return 0
    if fase == "KONFIG":
        return 1
    if fase in ANALYSIS_PHASES:
        return 2
    return 3


def _phase_html(label: str, roman: str, status: str) -> str:
    safe_label = html.escape(label)
    if status == "active":
        return f'<span class="phase-active">[{roman}] {safe_label}</span>'
    if status == "completed":
        return f'<span class="phase-completed">[{roman}] {safe_label}</span>'
    return f'<span class="phase-pending">[{roman}] {safe_label}</span>'


def render_macro_tracker(fase: str) -> None:
    current_idx = _macro_phase_index(fase)
    parts = []
    for i, phase in enumerate(eu.MACRO_PHASES):
        if i < current_idx:
            status = "completed"
        elif i == current_idx:
            status = "active"
        else:
            status = "pending"
        parts.append(_phase_html(phase["label"], ROMAN_NUMERALS[i], status))

    st.markdown(" &nbsp;&nbsp;|&nbsp;&nbsp; ".join(parts), unsafe_allow_html=True)

    phase_info = eu.PHASES.get(fase)
    if phase_info and fase != "HASIERA":
        academic_note(phase_info["description"])


def _station_marker(i: int, current: int, completed: int) -> str:
    if i < completed:
        return '<span class="tracker-station-done">●</span>'
    if i == current:
        return '<span class="tracker-station-active">◉</span>'
    return '<span class="tracker-station-pending">○</span>'


def render_micro_tracker(fase: str) -> None:
    if fase not in ANALYSIS_PHASES:
        return

    total = st.session_state.puntu_kopurua
    current_station = st.session_state.uneko_estazioa
    completed_stations = current_station
    micro_idx = MICRO_STEP_INDEX.get(fase, 0)
    micro_fraction = (micro_idx + 1) / 3.0
    overall_progress = (completed_stations + micro_fraction) / total if total else 0.0
    pct = int(min(overall_progress, 1.0) * 100)

    st.caption(eu.TRACKER["blade_progress"].format(pct=pct))
    st.progress(min(overall_progress, 1.0))
    st.caption(
        eu.TRACKER["station_label"].format(current=current_station + 1, total=total)
    )

    markers = " ".join(
        _station_marker(i, current_station, completed_stations) for i in range(total)
    )
    st.markdown(
        f"**{eu.TRACKER['station_map_title']}:** {markers}",
        unsafe_allow_html=True,
    )

    st.markdown(f"**{eu.TRACKER['substep_label']}**")
    sub_parts = []
    for i, step in enumerate(eu.MICRO_STEPS):
        safe_label = html.escape(step["label"])
        if step["id"] == fase:
            sub_parts.append(f'<span class="phase-active">{safe_label}</span>')
        elif (fase == "2_URRATSA" and step["id"] == "1_URRATSA") or (
            fase == "3_URRATSA" and step["id"] in {"1_URRATSA", "2_URRATSA"}
        ):
            sub_parts.append(f'<span class="phase-completed">{safe_label}</span>')
        else:
            sub_parts.append(f'<span class="phase-pending">{safe_label}</span>')

    st.markdown(" · ".join(sub_parts), unsafe_allow_html=True)
    section_divider()


def render_process_tracker(fase: str) -> None:
    if fase == "HASIERA":
        return

    render_macro_tracker(fase)
    render_micro_tracker(fase)
