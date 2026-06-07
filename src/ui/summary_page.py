"""Laburpen fasearen UI."""

from __future__ import annotations

import numpy as np
import pandas as pd
import streamlit as st

from src.naca import sortu_naca_txt
from src.physics import calc_reynolds_array
from src.plots import (
    build_overlaid_airfoils_figure,
    build_spanwise_naca_figure,
    build_summary_dual_axis_figure,
)
from src.state import fasea_aldatu


def render_summary_page() -> None:
    st.success(f"{st.session_state.iterazioa}. iterazioa arrakastaz amaitu da!")

    reynolds_amaiera = calc_reynolds_array(
        st.session_state.erradioak,
        st.session_state.kordak,
        st.session_state.rpm,
        st.session_state.v_rated,
    )
    estazioak = list(range(1, st.session_state.puntu_kopurua + 1))

    df_emaitzak = pd.DataFrame(
        {
            "Estazioa": estazioak,
            "Erradioa [m]": np.round(st.session_state.erradioak, 3),
            "Erabilitako korda [m]": np.round(st.session_state.kordak, 3),
            "Reynolds": [f"{re:.2e}" for re in reynolds_amaiera],
            "Aukeratutako NACA": st.session_state.amaierako_nacak,
        }
    )

    tab_table, tab_span, tab_dual, tab_profiles = st.tabs(
        ["Taula", "NACA banaketa", "Korda + Reynolds", "Profilak"]
    )

    with tab_table:
        st.dataframe(df_emaitzak, hide_index=True, use_container_width=True)
        st.download_button(
            label="CSV deskargatu",
            data=df_emaitzak.to_csv(index=False).encode("utf-8"),
            file_name=f"iterazio_{st.session_state.iterazioa}_emaitzak.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with tab_span:
        st.plotly_chart(
            build_spanwise_naca_figure(estazioak, st.session_state.amaierako_nacak),
            use_container_width=True,
            key="summary_spanwise",
        )

    with tab_dual:
        st.plotly_chart(
            build_summary_dual_axis_figure(
                estazioak,
                st.session_state.kordak,
                reynolds_amaiera,
            ),
            use_container_width=True,
            key="summary_dual",
        )

    with tab_profiles:
        st.plotly_chart(
            build_overlaid_airfoils_figure(st.session_state.amaierako_nacak),
            use_container_width=True,
            key="summary_profiles",
        )

    st.header("Profilen koordenatuak deskargatu")
    naca_bakarrak = list(dict.fromkeys(st.session_state.amaierako_nacak))
    if naca_bakarrak:
        cols = st.columns(min(len(naca_bakarrak), 4))
        for i, naca in enumerate(naca_bakarrak):
            with cols[i % len(cols)]:
                st.download_button(
                    label=f"NACA {naca}.txt",
                    data=sortu_naca_txt(naca),
                    file_name=f"NACA_{naca}.txt",
                    mime="text/plain",
                    use_container_width=True,
                    key=f"download_{naca}",
                )

    st.divider()
    st.header("Hurrengo iterazioa prestatu")

    with st.container(border=True):
        df_berriak = st.data_editor(
            pd.DataFrame(
                {
                    "Estazioa": estazioak,
                    "Korda berria [m]": np.round(st.session_state.kordak, 3),
                }
            ),
            hide_index=True,
            use_container_width=True,
            key="summary_next_chords",
        )

    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button("Iterazio berria hasi", type="primary", use_container_width=True):
            st.session_state.kordak = df_berriak["Korda berria [m]"].values
            st.session_state.iterazioa += 1
            st.session_state.aero_cache = {}
            st.session_state.selected_preview_naca = None
            fasea_aldatu("KONFIG")
