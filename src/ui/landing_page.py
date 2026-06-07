"""Hasiera-orria: prozesuaren azalpena — estilo artikulu."""

from __future__ import annotations

import streamlit as st

from src.i18n import eu
from src.state import fasea_aldatu
from src.ui.theme import section_divider


def render_landing_page() -> None:
    st.markdown(f"## 1. Sarrera")
    st.markdown(eu.LANDING["intro"])

    section_divider()
    st.markdown(f"## 2. {eu.LANDING['steps_title']}")

    steps_table = "| Urratsa | Azalpena |\n| --- | --- |\n"
    for step in eu.LANDING["steps"]:
        steps_table += f"| {step['title']} | {step['body']} |\n"
    st.markdown(steps_table)

    section_divider()
    col_naca, col_re = st.columns(2)
    with col_naca:
        st.markdown(f"### {eu.LANDING['naca_title']}")
        st.markdown(eu.LANDING["naca_body"])
    with col_re:
        st.markdown(f"### {eu.LANDING['reynolds_title']}")
        st.markdown(eu.LANDING["reynolds_body"])

    with st.expander(eu.LANDING["details_title"]):
        st.markdown(eu.LANDING["details_body"])

    section_divider()
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button(eu.LANDING["cta"], use_container_width=True):
            fasea_aldatu("KONFIG")
