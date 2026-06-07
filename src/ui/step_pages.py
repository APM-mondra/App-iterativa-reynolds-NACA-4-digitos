"""UI faseentzat: 1_URRATSA, 2_URRATSA, 3_URRATSA."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.aero import get_or_compute_phase_results, get_phase_cache_key
from src.i18n import eu
from src.naca import nacas_fase1, nacas_fase2, nacas_fase3
from src.physics import calc_reynolds
from src.plots import (
    build_airfoil_geometry_figure,
    build_cd_figure,
    build_cl_figure,
    build_efficiency_figure,
    build_polar_figure,
    build_ranking_figure,
)
from src.state import estazioa_atzera, fasea_aldatu, get_safe_station_index
from src.ui.theme import academic_warning, section_divider


def _render_ranking_table(results: list[dict]) -> None:
    if not results:
        academic_warning(eu.ERRORS["no_valid_profiles"])
        return

    df = pd.DataFrame(
        [
            {
                eu.STEPS["rank_naca"]: item["naca"],
                eu.STEPS["rank_cl_cd_max"]: round(item["max_cl_cd"], 2),
                eu.STEPS["rank_alpha_opt"]: round(item["alpha_opt"], 2),
                eu.STEPS["rank_cl_opt"]: round(item["cl_at_opt"], 3),
                eu.STEPS["rank_cd_opt"]: round(item["cd_at_opt"], 4),
            }
            for item in results
        ]
    )
    st.dataframe(df, hide_index=True, use_container_width=True)


def _render_profile_selector(
    validos: list[str],
    key_prefix: str,
    zutabe_kop: int = 4,
) -> str | None:
    if not validos:
        return None

    st.markdown(f"**{eu.STEPS['select_prompt']}**")

    cols = st.columns(zutabe_kop)
    aukeratua = None
    for i, aukera in enumerate(validos):
        if cols[i % zutabe_kop].button(
            f"NACA {aukera}",
            key=f"{key_prefix}_btn_{aukera}",
            use_container_width=True,
        ):
            aukeratua = aukera

    if aukeratua is None:
        selectbox_choice = st.selectbox(
            eu.STEPS["select_profile"],
            options=["--"] + validos,
            format_func=lambda x: f"NACA {x}" if x != "--" else eu.STEPS["select_placeholder"],
            key=f"{key_prefix}_select",
        )
        if selectbox_choice != "--":
            aukeratua = selectbox_choice

    return aukeratua


def _render_step_results(
    fase: str,
    title: str,
    naca_list: list[str],
    key_prefix: str,
    back_label: str,
    back_callback,
    on_select,
    zutabe_kop: int = 4,
) -> None:
    idx = get_safe_station_index()
    re = calc_reynolds(
        st.session_state.erradioak[idx],
        st.session_state.kordak[idx],
        st.session_state.rpm,
        st.session_state.v_rated,
    )

    cache_key = get_phase_cache_key(idx, fase, re)
    results = get_or_compute_phase_results(
        st.session_state.aero_cache,
        cache_key,
        naca_list,
        re,
        st.session_state.alpha_min,
        st.session_state.alpha_max,
        st.session_state.alpha_steps,
    )
    validos = [item["naca"] for item in results]

    preview_naca = st.session_state.selected_preview_naca
    if preview_naca not in validos:
        preview_naca = validos[0] if validos else None
        st.session_state.selected_preview_naca = preview_naca

    if not validos:
        academic_warning(eu.ERRORS["no_valid_profiles"])
        if st.button(back_label, use_container_width=False):
            back_callback()
        return

    col_main, col_side = st.columns([3, 1])

    with col_main:
        tab_eff, tab_cl, tab_cd, tab_polar, tab_rank = st.tabs(
            [
                eu.STEPS["tab_efficiency"],
                eu.STEPS["tab_cl"],
                eu.STEPS["tab_cd"],
                eu.STEPS["tab_polar"],
                eu.STEPS["tab_ranking"],
            ]
        )

        with tab_eff:
            st.plotly_chart(
                build_efficiency_figure(results, title, preview_naca),
                use_container_width=True,
                key=f"{key_prefix}_eff",
            )

        with tab_cl:
            st.plotly_chart(
                build_cl_figure(results, title, preview_naca),
                use_container_width=True,
                key=f"{key_prefix}_cl",
            )

        with tab_cd:
            st.plotly_chart(
                build_cd_figure(results, title, preview_naca),
                use_container_width=True,
                key=f"{key_prefix}_cd",
            )

        with tab_polar:
            st.plotly_chart(
                build_polar_figure(results, title, preview_naca),
                use_container_width=True,
                key=f"{key_prefix}_polar",
            )

        with tab_rank:
            st.plotly_chart(
                build_ranking_figure(results),
                use_container_width=True,
                key=f"{key_prefix}_rank",
            )
            _render_ranking_table(results)

    with col_side:
        if preview_naca:
            preview_choice = st.selectbox(
                eu.STEPS["preview"],
                options=validos,
                index=validos.index(preview_naca),
                format_func=lambda x: f"NACA {x}",
                key=f"{key_prefix}_preview",
            )
            st.session_state.selected_preview_naca = preview_choice
            st.plotly_chart(
                build_airfoil_geometry_figure(preview_choice),
                use_container_width=True,
                key=f"{key_prefix}_geom",
            )

    section_divider()
    aukera = _render_profile_selector(validos, key_prefix, zutabe_kop)

    if st.button(back_label, use_container_width=False):
        back_callback()

    if aukera:
        on_select(aukera)


def render_step1_page() -> None:
    def on_select(aukera: str) -> None:
        st.session_state.m_hautatua = aukera[0]
        fasea_aldatu("2_URRATSA")

    _render_step_results(
        fase="1_URRATSA",
        title=eu.PHASES["1_URRATSA"]["title"],
        naca_list=nacas_fase1(),
        key_prefix="p1",
        back_label=eu.STEPS["back_station"],
        back_callback=estazioa_atzera,
        on_select=on_select,
    )


def render_step2_page() -> None:
    if st.session_state.m_hautatua == "0":
        academic_warning(eu.STEPS["symmetric_warning"])
        st.session_state.p_hautatua = "0"

        col_atzera, col_huts, col_aurrera = st.columns([1, 4, 1])
        if col_atzera.button(eu.STEPS["btn_previous"], use_container_width=True):
            fasea_aldatu("1_URRATSA")
        if col_aurrera.button(eu.STEPS["btn_to_thickness"], use_container_width=True):
            fasea_aldatu("3_URRATSA")
        return

    def on_select(aukera: str) -> None:
        st.session_state.p_hautatua = aukera[1]
        fasea_aldatu("3_URRATSA")

    title = f"{eu.PHASES['2_URRATSA']['title']} (M={st.session_state.m_hautatua})"
    _render_step_results(
        fase="2_URRATSA",
        title=title,
        naca_list=nacas_fase2(st.session_state.m_hautatua),
        key_prefix="p2",
        back_label=eu.STEPS["back_step1"],
        back_callback=lambda: fasea_aldatu("1_URRATSA"),
        on_select=on_select,
    )


def render_step3_page() -> None:
    def on_select(aukera: str) -> None:
        st.session_state.amaierako_nacak.append(aukera)
        if st.session_state.uneko_estazioa < st.session_state.puntu_kopurua - 1:
            st.session_state.uneko_estazioa += 1
            st.session_state.selected_preview_naca = None
            st.session_state.m_hautatua = "0"
            st.session_state.p_hautatua = "0"
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("LABURPENA")

    def back_callback() -> None:
        if st.session_state.m_hautatua == "0":
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("2_URRATSA")

    title = (
        f"{eu.PHASES['3_URRATSA']['title']} "
        f"(NACA {st.session_state.m_hautatua}{st.session_state.p_hautatua}XX)"
    )
    _render_step_results(
        fase="3_URRATSA",
        title=title,
        naca_list=nacas_fase3(st.session_state.m_hautatua, st.session_state.p_hautatua),
        key_prefix="p3",
        back_label=eu.STEPS["back_step2"],
        back_callback=back_callback,
        on_select=on_select,
        zutabe_kop=6,
    )
