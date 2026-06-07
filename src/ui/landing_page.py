"""Hasiera-orria: prozesuaren azalpena."""

from __future__ import annotations

import streamlit as st

from src.i18n import eu
from src.state import fasea_aldatu


def render_landing_page() -> None:
    st.header(eu.LANDING["title"])
    st.markdown(eu.LANDING["intro"])

    st.subheader(eu.LANDING["steps_title"])
    cols = st.columns(len(eu.LANDING["steps"]))
    for col, step in zip(cols, eu.LANDING["steps"]):
        with col:
            with st.container(border=True):
                st.markdown(f"**{step['title']}**")
                st.caption(step["body"])

    col_naca, col_re = st.columns(2)
    with col_naca:
        with st.container(border=True):
            st.markdown(f"**{eu.LANDING['naca_title']}**")
            st.markdown(eu.LANDING["naca_body"])
    with col_re:
        with st.container(border=True):
            st.markdown(f"**{eu.LANDING['reynolds_title']}**")
            st.markdown(eu.LANDING["reynolds_body"])

    with st.expander(eu.LANDING["details_title"]):
        st.markdown(eu.LANDING["details_body"])

    st.divider()
    _, col_btn, _ = st.columns([1, 2, 1])
    with col_btn:
        if st.button(eu.LANDING["cta"], type="primary", use_container_width=True):
            fasea_aldatu("KONFIG")
