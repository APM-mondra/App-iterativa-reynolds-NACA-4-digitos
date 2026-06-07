"""Gestion del estado de sesion de Streamlit."""

from __future__ import annotations

import numpy as np
import streamlit as st


def init_session_state() -> None:
    defaults = {
        "fase": "HASIERA",
        "iterazioa": 1,
        "uneko_estazioa": 0,
        "puntu_kopurua": 8,
        "erradio_min": 0.05,
        "erradio_max": 0.80,
        "korda_base": 0.12,
        "rpm": 200.0,
        "v_rated": 4.0,
        "alpha_min": -5.0,
        "alpha_max": 20.0,
        "alpha_steps": 60,
        "m_hautatua": "0",
        "p_hautatua": "0",
        "amaierako_nacak": [],
        "aero_cache": {},
        "selected_preview_naca": None,
        "confirm_reset_config": False,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    sync_geometry_arrays()


def sync_geometry_arrays() -> None:
    """Mantener kordak/erradioak sincronizados con puntu_kopurua."""
    n = st.session_state.puntu_kopurua
    if (
        "kordak" not in st.session_state
        or len(st.session_state.kordak) != n
    ):
        st.session_state.kordak = np.full(n, st.session_state.korda_base)
    if (
        "erradioak" not in st.session_state
        or len(st.session_state.erradioak) != n
    ):
        st.session_state.erradioak = np.linspace(
            st.session_state.erradio_min,
            st.session_state.erradio_max,
            n,
        )


def get_safe_station_index() -> int:
    """Indice de estacion acotado al rango valido."""
    sync_geometry_arrays()
    max_idx = max(0, min(st.session_state.puntu_kopurua, len(st.session_state.erradioak)) - 1)
    return int(np.clip(st.session_state.uneko_estazioa, 0, max_idx))


def fasea_aldatu(fase_berria: str) -> None:
    st.session_state.fase = fase_berria
    st.session_state.confirm_reset_config = False
    st.rerun()


def go_to_hasiera() -> None:
    reset_iteration_state()
    st.session_state.fase = "HASIERA"
    st.session_state.confirm_reset_config = False
    st.rerun()


def estazioa_atzera() -> None:
    if st.session_state.uneko_estazioa > 0:
        st.session_state.uneko_estazioa -= 1
        if st.session_state.amaierako_nacak:
            st.session_state.amaierako_nacak.pop()
        st.session_state.selected_preview_naca = None
        st.session_state.m_hautatua = "0"
        st.session_state.p_hautatua = "0"
        fasea_aldatu("1_URRATSA")
    else:
        reset_iteration_state()
        fasea_aldatu("KONFIG")


def update_geometry_from_params() -> None:
    st.session_state.kordak = np.full(st.session_state.puntu_kopurua, st.session_state.korda_base)
    st.session_state.erradioak = np.linspace(
        st.session_state.erradio_min,
        st.session_state.erradio_max,
        st.session_state.puntu_kopurua,
    )


def reset_iteration_state() -> None:
    st.session_state.amaierako_nacak = []
    st.session_state.uneko_estazioa = 0
    st.session_state.aero_cache = {}
    st.session_state.selected_preview_naca = None
    st.session_state.m_hautatua = "0"
    st.session_state.p_hautatua = "0"


def reset_to_konfig() -> None:
    reset_iteration_state()
    fasea_aldatu("KONFIG")


def invalidate_aero_cache() -> None:
    st.session_state.aero_cache = {}
