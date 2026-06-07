"""Entry point garapenerako - Streamlit Cloud staging."""

import streamlit as st

from src.state import init_session_state
from src.ui.config_page import render_config_page
from src.ui.layout import render_header, render_sidebar, render_station_banner, render_stepper
from src.ui.step_pages import render_step1_page, render_step2_page, render_step3_page
from src.ui.summary_page import render_summary_page

st.set_page_config(
    page_title="Hegalaren Diseinu Iteratiboa",
    page_icon="🌬️",
    layout="wide",
)

init_session_state()
render_sidebar()

render_header()
render_stepper()
render_station_banner()

fase = st.session_state.fase

if fase == "KONFIG":
    render_config_page()
elif fase == "1_URRATSA":
    render_step1_page()
elif fase == "2_URRATSA":
    render_step2_page()
elif fase == "3_URRATSA":
    render_step3_page()
elif fase == "LABURPENA":
    render_summary_page()
