"""Sistema de diseno cientifico — tokens, CSS global y helpers Plotly."""

from __future__ import annotations

import streamlit as st

FONT_SERIF = "'STIX Two Text', 'Times New Roman', Times, serif"
COLOR_TEXT = "#1a1a1a"
COLOR_MUTED = "#666666"
COLOR_BORDER = "#333333"
COLOR_GRID = "#e8e8e8"
COLOR_BG = "#FFFFFF"
COLOR_BG_ALT = "#f7f7f7"

PLOT_COLORS = ["#1a1a1a", "#555555", "#888888", "#aaaaaa", "#bbbbbb", "#cccccc"]
PLOT_HIGHLIGHT = "#000000"
PLOT_LINE_WIDTH = 1.0
PLOT_HIGHLIGHT_WIDTH = 2.5
PLOT_FONT_SIZE = 12
PLOT_TITLE_SIZE = 13

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI"]


def inject_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=STIX+Two+Text:ital,wght@0,400;0,600;1,400&display=swap');

        html, body, [class*="css"], .stApp {{
            font-family: {FONT_SERIF};
            color: {COLOR_TEXT};
        }}

        h1, h2, h3, h4, h5, h6, p, label, span, div {{
            font-family: {FONT_SERIF} !important;
        }}

        .stApp {{
            background-color: {COLOR_BG};
        }}

        [data-testid="stSidebar"] {{
            background-color: {COLOR_BG_ALT};
            border-right: 1px solid {COLOR_BORDER};
        }}

        [data-testid="stSidebar"] * {{
            font-family: {FONT_SERIF} !important;
        }}

        .stButton > button {{
            border-radius: 0 !important;
            border: 1px solid {COLOR_BORDER} !important;
            background-color: {COLOR_BG} !important;
            color: {COLOR_TEXT} !important;
            font-family: {FONT_SERIF} !important;
            font-weight: 400 !important;
            box-shadow: none !important;
        }}

        .stButton > button:hover {{
            background-color: {COLOR_BG_ALT} !important;
            border-color: {COLOR_TEXT} !important;
            color: {COLOR_TEXT} !important;
        }}

        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {{
            background-color: {COLOR_TEXT} !important;
            color: {COLOR_BG} !important;
        }}

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {{
            background-color: #333333 !important;
            color: {COLOR_BG} !important;
        }}

        .stTextInput input, .stNumberInput input, .stSelectbox > div > div,
        .stMultiSelect > div > div, [data-baseweb="select"] {{
            border-radius: 0 !important;
            font-family: {FONT_SERIF} !important;
        }}

        [data-testid="stMetric"] {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-size: 0.85rem !important;
            color: {COLOR_MUTED} !important;
            font-variant: small-caps !important;
        }}

        [data-testid="stMetricValue"] {{
            font-size: 1.1rem !important;
            color: {COLOR_TEXT} !important;
            font-weight: 400 !important;
        }}

        .stTabs [data-baseweb="tab-list"] {{
            gap: 0;
            border-bottom: 1px solid {COLOR_BORDER};
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 0 !important;
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            font-family: {FONT_SERIF} !important;
            color: {COLOR_MUTED} !important;
            padding: 0.5rem 1rem !important;
        }}

        .stTabs [aria-selected="true"] {{
            border-bottom: 2px solid {COLOR_TEXT} !important;
            color: {COLOR_TEXT} !important;
            font-weight: 600 !important;
        }}

        .stProgress > div > div {{
            border-radius: 0 !important;
            background-color: {COLOR_GRID} !important;
        }}

        .stProgress > div > div > div {{
            border-radius: 0 !important;
            background-color: {COLOR_TEXT} !important;
        }}

        [data-testid="stExpander"] {{
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 0 !important;
        }}

        .stDataFrame, [data-testid="stDataFrame"] {{
            font-family: {FONT_SERIF} !important;
        }}

        .scientific-divider {{
            border: none;
            border-top: 1px solid {COLOR_BORDER};
            margin: 1.5rem 0;
        }}

        .scientific-header-rule {{
            border: none;
            border-top: 2px solid {COLOR_TEXT};
            margin: 0.5rem 0 1.5rem 0;
        }}

        .phase-active {{
            font-weight: 600;
            text-decoration: underline;
            color: {COLOR_TEXT};
        }}

        .phase-completed {{
            color: {COLOR_MUTED};
        }}

        .phase-pending {{
            color: #aaaaaa;
        }}

        .academic-note {{
            border-left: 2px solid {COLOR_BORDER};
            padding-left: 1rem;
            margin: 1rem 0;
            color: {COLOR_MUTED};
            font-style: italic;
        }}

        .academic-warning {{
            border-left: 2px solid {COLOR_TEXT};
            padding-left: 1rem;
            margin: 1rem 0;
            color: {COLOR_TEXT};
        }}

        .academic-result {{
            border-left: 2px solid {COLOR_BORDER};
            padding-left: 1rem;
            margin: 1rem 0;
            color: {COLOR_TEXT};
        }}

        .tracker-station-active {{
            color: {COLOR_TEXT};
            font-weight: 600;
        }}

        .tracker-station-done {{
            color: {COLOR_MUTED};
        }}

        .tracker-station-pending {{
            color: #bbbbbb;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_divider() -> None:
    st.markdown('<hr class="scientific-divider">', unsafe_allow_html=True)


def header_rule() -> None:
    st.markdown('<hr class="scientific-header-rule">', unsafe_allow_html=True)


def academic_note(text: str) -> None:
    st.markdown(f'<div class="academic-note">{text}</div>', unsafe_allow_html=True)


def academic_warning(text: str) -> None:
    st.markdown(f'<div class="academic-warning"><em>Oharra:</em> {text}</div>', unsafe_allow_html=True)


def academic_result(text: str) -> None:
    st.markdown(f'<div class="academic-result"><em>Emaitza:</em> {text}</div>', unsafe_allow_html=True)


def get_plotly_layout_defaults() -> dict:
    return dict(
        font=dict(family=FONT_SERIF, size=PLOT_FONT_SIZE, color=COLOR_TEXT),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        margin=dict(l=55, r=30, t=40, b=45),
        hovermode="x unified",
    )


def apply_scientific_axes(fig) -> None:
    axis_style = dict(
        showline=True,
        linewidth=1,
        linecolor=COLOR_BORDER,
        mirror=True,
        ticks="inside",
        tickfont=dict(family=FONT_SERIF, size=11, color=COLOR_TEXT),
        titlefont=dict(family=FONT_SERIF, size=PLOT_FONT_SIZE, color=COLOR_TEXT),
        showgrid=True,
        gridwidth=0.5,
        gridcolor=COLOR_GRID,
        zeroline=False,
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)


def apply_scientific_legend(fig, title: str | None = None) -> None:
    fig.update_layout(
        legend=dict(
            title=dict(text=title or "", font=dict(family=FONT_SERIF, size=11)),
            font=dict(family=FONT_SERIF, size=10),
            bgcolor=COLOR_BG,
            bordercolor=COLOR_BORDER,
            borderwidth=1,
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        )
    )


def get_series_style(index: int, is_highlight: bool) -> dict:
    if is_highlight:
        return dict(color=PLOT_HIGHLIGHT, width=PLOT_HIGHLIGHT_WIDTH)
    return dict(
        color=PLOT_COLORS[min(index + 1, len(PLOT_COLORS) - 1)],
        width=PLOT_LINE_WIDTH,
    )
