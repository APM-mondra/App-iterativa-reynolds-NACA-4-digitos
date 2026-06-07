"""UI faseentzat: 1_URRATSA, 2_URRATSA, 3_URRATSA."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from src.aero import get_or_compute_phase_results, get_phase_cache_key
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
from src.state import estazioa_atzera, fasea_aldatu


def _render_ranking_table(results: list[dict]) -> None:
    if not results:
        st.warning("Ez da profil baliodunik aurkitu.")
        return

    df = pd.DataFrame(
        [
            {
                "NACA": item["naca"],
                "Cl/Cd max": round(item["max_cl_cd"], 2),
                "Alpha opt (°)": round(item["alpha_opt"], 2),
                "Cl @ opt": round(item["cl_at_opt"], 3),
                "Cd @ opt": round(item["cd_at_opt"], 4),
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
    st.markdown("**Egin klik profil batean edo hautatu zerrendatik:**")

    cols = st.columns(zutabe_kop)
    aukeratua = None
    for i, aukera in enumerate(validos):
        if cols[i % zutabe_kop].button(
            f"NACA {aukera}",
            key=f"{key_prefix}_btn_{aukera}",
            use_container_width=True,
        ):
            aukeratua = aukera

    selectbox_choice = st.selectbox(
        "Profila hautatu",
        options=["--"] + validos,
        format_func=lambda x: f"NACA {x}" if x != "--" else "Hautatu...",
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
    st.subheader(title)

    idx = st.session_state.uneko_estazioa
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
    if preview_naca not in validos and validos:
        preview_naca = validos[0]
        st.session_state.selected_preview_naca = preview_naca

    col_main, col_side = st.columns([3, 1])

    with col_main:
        tab_eff, tab_cl, tab_cd, tab_polar, tab_rank = st.tabs(
            ["Cl/Cd", "Cl", "Cd", "Polarra", "Ranking"]
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
        if validos:
            preview_choice = st.selectbox(
                "Aurrebista",
                options=validos,
                index=validos.index(preview_naca) if preview_naca in validos else 0,
                format_func=lambda x: f"NACA {x}",
                key=f"{key_prefix}_preview",
            )
            st.session_state.selected_preview_naca = preview_choice
            st.plotly_chart(
                build_airfoil_geometry_figure(preview_choice),
                use_container_width=True,
                key=f"{key_prefix}_geom",
            )

    with st.container(border=True):
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
        title="1. urratsa: kurbaduraren aukeraketa (lehen digitua)",
        naca_list=nacas_fase1(),
        key_prefix="p1",
        back_label="Aurreko estaziora atzera",
        back_callback=estazioa_atzera,
        on_select=on_select,
    )


def render_step2_page() -> None:
    if st.session_state.m_hautatua == "0":
        st.warning("Profil simetrikoa detektatu da (kurbadura = 0). Kurbaduraren posizioa saltatzen.")
        st.session_state.p_hautatua = "0"

        col_atzera, col_huts, col_aurrera = st.columns([1, 4, 1])
        if col_atzera.button("Aurrekoa", use_container_width=True):
            fasea_aldatu("1_URRATSA")
        if col_aurrera.button("Lodierara joan", type="primary", use_container_width=True):
            fasea_aldatu("3_URRATSA")
        return

    def on_select(aukera: str) -> None:
        st.session_state.p_hautatua = aukera[1]
        fasea_aldatu("3_URRATSA")

    _render_step_results(
        fase="2_URRATSA",
        title=f"2. urratsa: kurbaduraren posizioa (M={st.session_state.m_hautatua})",
        naca_list=nacas_fase2(st.session_state.m_hautatua),
        key_prefix="p2",
        back_label="Kurbadurara atzera (1. urratsa)",
        back_callback=lambda: fasea_aldatu("1_URRATSA"),
        on_select=on_select,
    )


def render_step3_page() -> None:
    def on_select(aukera: str) -> None:
        st.session_state.amaierako_nacak.append(aukera)
        if st.session_state.uneko_estazioa < st.session_state.puntu_kopurua - 1:
            st.session_state.uneko_estazioa += 1
            st.session_state.selected_preview_naca = None
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("LABURPENA")

    def back_callback() -> None:
        if st.session_state.m_hautatua == "0":
            fasea_aldatu("1_URRATSA")
        else:
            fasea_aldatu("2_URRATSA")

    _render_step_results(
        fase="3_URRATSA",
        title=f"3. urratsa: lodiera (NACA {st.session_state.m_hautatua}{st.session_state.p_hautatua}XX)",
        naca_list=nacas_fase3(st.session_state.m_hautatua, st.session_state.p_hautatua),
        key_prefix="p3",
        back_label="Posiziora atzera (2. urratsa)",
        back_callback=back_callback,
        on_select=on_select,
        zutabe_kop=6,
    )
