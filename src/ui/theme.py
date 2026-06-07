"""Sistema de diseno profesional — tokens, CSS global y helpers Plotly."""

from __future__ import annotations

import html

import streamlit as st

# --- Tipografia por rol ---
FONT_DISPLAY = "'Fraunces', Georgia, 'Times New Roman', serif"
FONT_SANS = "'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif"
FONT_MONO = "'IBM Plex Mono', 'SF Mono', Menlo, monospace"

# --- Paleta ---
COLOR_INK = "#1f2733"
COLOR_TEXT = COLOR_INK
COLOR_MUTED = "#5b6573"
COLOR_ACCENT = "#1c5d82"
COLOR_ACCENT_DARK = "#16475f"
COLOR_ACCENT_SOFT = "#e8f0f5"
COLOR_WARN = "#9a6a00"
COLOR_WARN_SOFT = "#fbf3e2"
COLOR_BORDER = "#e2e8f0"
COLOR_BORDER_STRONG = "#cbd5e0"
COLOR_BG = "#ffffff"
COLOR_SURFACE = "#f7f9fb"
COLOR_GRID = "#eef1f5"

# --- Plot ---
PLOT_COLORS = ["#1c5d82", "#5b6573", "#8aa0ad", "#9fb3bd", "#b9c5cd", "#cdd6dc"]
PLOT_HIGHLIGHT = COLOR_ACCENT
PLOT_LINE_WIDTH = 1.3
PLOT_HIGHLIGHT_WIDTH = 2.8
PLOT_FONT_SIZE = 12
PLOT_TITLE_SIZE = 15

ROMAN_NUMERALS = ["I", "II", "III", "IV", "V", "VI"]


def inject_global_styles() -> None:
    st.markdown(
        f"""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

        .stApp {{
            font-family: {FONT_SANS};
            color: {COLOR_INK};
            background-color: {COLOR_BG};
        }}

        /* Cuerpo y UI en sans */
        .stMarkdown,
        .stMarkdown p,
        .stMarkdown li,
        .stMarkdown td,
        .stMarkdown th,
        [data-testid="stMarkdownContainer"],
        [data-testid="stWidgetLabel"] p,
        [data-testid="stCaptionContainer"],
        .stButton > button,
        .stTabs [data-baseweb="tab"],
        [data-baseweb="select"] > div,
        .stTextInput input,
        .stNumberInput input {{
            font-family: {FONT_SANS} !important;
        }}

        /* Titulos en serif de display */
        h1, h2, h3,
        [data-testid="stHeading"],
        .stMarkdown h1,
        .stMarkdown h2,
        .stMarkdown h3,
        .stMarkdown h4 {{
            font-family: {FONT_DISPLAY} !important;
            color: {COLOR_INK} !important;
            font-weight: 600 !important;
            letter-spacing: -0.01em;
        }}

        h1, [data-testid="stHeading"] h1 {{
            font-weight: 600 !important;
        }}

        /* Valores numericos en mono */
        [data-testid="stMetricValue"] {{
            font-family: {FONT_MONO} !important;
            font-size: 1.25rem !important;
            color: {COLOR_INK} !important;
            font-weight: 500 !important;
        }}

        /* Iconos: preservar fuente nativa */
        [data-testid="stExpanderToggleIcon"],
        [data-testid="collapsedControl"],
        [data-testid="stTooltipIcon"],
        [data-testid="baseButton-headerNoPadding"],
        .material-icons,
        [class*="material-icons"],
        svg {{
            font-family: inherit !important;
        }}

        summary [data-testid="stExpanderToggleIcon"] {{
            font-family: "Material Symbols Rounded", "Material Icons", sans-serif !important;
        }}

        /* Sidebar */
        [data-testid="stSidebar"] {{
            background-color: {COLOR_SURFACE};
            border-right: 1px solid {COLOR_BORDER};
        }}

        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
            font-family: {FONT_SANS} !important;
        }}

        /* Botones */
        .stButton > button {{
            border-radius: 6px !important;
            border: 1px solid {COLOR_BORDER_STRONG} !important;
            background-color: {COLOR_BG} !important;
            color: {COLOR_INK} !important;
            font-weight: 500 !important;
            box-shadow: 0 1px 2px rgba(31, 39, 51, 0.04) !important;
            transition: all 0.15s ease !important;
        }}

        .stButton > button:hover {{
            background-color: {COLOR_SURFACE} !important;
            border-color: {COLOR_ACCENT} !important;
            color: {COLOR_ACCENT} !important;
        }}

        .stButton > button[kind="primary"],
        .stButton > button[data-testid="baseButton-primary"] {{
            background-color: {COLOR_ACCENT} !important;
            border-color: {COLOR_ACCENT} !important;
            color: #ffffff !important;
            box-shadow: 0 1px 3px rgba(28, 93, 130, 0.25) !important;
        }}

        .stButton > button[kind="primary"]:hover,
        .stButton > button[data-testid="baseButton-primary"]:hover {{
            background-color: {COLOR_ACCENT_DARK} !important;
            border-color: {COLOR_ACCENT_DARK} !important;
            color: #ffffff !important;
        }}

        /* Inputs */
        .stTextInput input, .stNumberInput input {{
            border-radius: 6px !important;
        }}

        .stSelectbox > div > div,
        .stMultiSelect > div > div,
        [data-baseweb="select"] {{
            border-radius: 6px !important;
        }}

        [data-baseweb="select"] svg,
        [data-testid="stNumberInput"] button,
        [data-testid="stNumberInput"] svg {{
            font-family: inherit !important;
        }}

        /* Metricas */
        [data-testid="stMetric"] {{
            background: {COLOR_SURFACE} !important;
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 8px !important;
            padding: 0.75rem 1rem !important;
        }}

        [data-testid="stSidebar"] [data-testid="stMetric"] {{
            background: transparent !important;
            border: none !important;
            padding: 0.1rem 0 !important;
        }}

        [data-testid="stMetricLabel"] {{
            font-family: {FONT_SANS} !important;
            font-size: 0.72rem !important;
            color: {COLOR_MUTED} !important;
            text-transform: uppercase !important;
            letter-spacing: 0.06em !important;
            font-weight: 500 !important;
        }}

        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            gap: 0.25rem;
            border-bottom: 1px solid {COLOR_BORDER};
        }}

        .stTabs [data-baseweb="tab"] {{
            border-radius: 6px 6px 0 0 !important;
            background: transparent !important;
            border: none !important;
            border-bottom: 2px solid transparent !important;
            color: {COLOR_MUTED} !important;
            font-weight: 500 !important;
            padding: 0.5rem 1rem !important;
        }}

        .stTabs [aria-selected="true"] {{
            border-bottom: 2px solid {COLOR_ACCENT} !important;
            color: {COLOR_ACCENT} !important;
            font-weight: 600 !important;
        }}

        /* Progress */
        .stProgress > div > div {{
            border-radius: 6px !important;
            background-color: {COLOR_GRID} !important;
        }}

        .stProgress > div > div > div {{
            border-radius: 6px !important;
            background-color: {COLOR_ACCENT} !important;
        }}

        /* Expander */
        [data-testid="stExpander"] {{
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 8px !important;
        }}

        /* Dataframe */
        .stDataFrame, [data-testid="stDataFrame"] {{
            font-family: {FONT_SANS} !important;
            border-radius: 8px !important;
        }}

        /* Divisores y callouts */
        .scientific-divider {{
            border: none;
            border-top: 1px solid {COLOR_BORDER};
            margin: 1.75rem 0;
        }}

        .scientific-header-rule {{
            border: none;
            border-top: 2px solid {COLOR_ACCENT};
            width: 64px;
            margin: 0.35rem 0 1.5rem 0;
        }}

        .phase-active {{
            font-weight: 600;
            color: {COLOR_ACCENT};
        }}

        .phase-completed {{
            color: {COLOR_INK};
        }}

        .phase-pending {{
            color: #aab4bf;
        }}

        .academic-note,
        .academic-warning,
        .academic-result {{
            font-family: {FONT_SANS} !important;
            border-radius: 8px;
            padding: 0.85rem 1.1rem;
            margin: 1rem 0;
            line-height: 1.5;
        }}

        .academic-note {{
            background: {COLOR_SURFACE};
            border-left: 3px solid {COLOR_BORDER_STRONG};
            color: {COLOR_MUTED};
        }}

        .academic-warning {{
            background: {COLOR_WARN_SOFT};
            border-left: 3px solid {COLOR_WARN};
            color: #6b4a00;
        }}

        .academic-result {{
            background: {COLOR_ACCENT_SOFT};
            border-left: 3px solid {COLOR_ACCENT};
            color: {COLOR_ACCENT_DARK};
        }}

        .academic-note em,
        .academic-warning em,
        .academic-result em {{
            font-style: normal;
            font-weight: 600;
        }}

        .tracker-station-active {{
            color: {COLOR_ACCENT};
            font-weight: 600;
        }}

        .tracker-station-done {{
            color: {COLOR_INK};
        }}

        .tracker-station-pending {{
            color: #c2cbd4;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def section_divider() -> None:
    st.markdown('<hr class="scientific-divider">', unsafe_allow_html=True)


def header_rule() -> None:
    st.markdown('<hr class="scientific-header-rule">', unsafe_allow_html=True)


def _escape(text: str) -> str:
    return html.escape(text, quote=True)


def academic_note(text: str) -> None:
    st.markdown(f'<div class="academic-note">{_escape(text)}</div>', unsafe_allow_html=True)


def academic_warning(text: str) -> None:
    st.markdown(
        f'<div class="academic-warning"><em>Oharra:</em> {_escape(text)}</div>',
        unsafe_allow_html=True,
    )


def academic_result(text: str) -> None:
    st.markdown(
        f'<div class="academic-result"><em>Emaitza:</em> {_escape(text)}</div>',
        unsafe_allow_html=True,
    )


def get_plotly_layout_defaults() -> dict:
    return dict(
        font=dict(family=FONT_SANS, size=PLOT_FONT_SIZE, color=COLOR_INK),
        paper_bgcolor=COLOR_BG,
        plot_bgcolor=COLOR_BG,
        margin=dict(l=60, r=30, t=46, b=48),
        hovermode="x unified",
    )


def apply_scientific_axes(fig) -> None:
    axis_font = dict(family=FONT_SANS, size=11, color=COLOR_MUTED)
    title_font = dict(family=FONT_SANS, size=PLOT_FONT_SIZE, color=COLOR_INK)
    axis_style = dict(
        showline=True,
        linewidth=1,
        linecolor=COLOR_BORDER_STRONG,
        mirror=False,
        ticks="outside",
        ticklen=4,
        tickcolor=COLOR_BORDER_STRONG,
        tickfont=axis_font,
        title=dict(font=title_font),
        showgrid=True,
        gridwidth=1,
        gridcolor=COLOR_GRID,
        zeroline=False,
    )
    fig.update_xaxes(**axis_style)
    fig.update_yaxes(**axis_style)


def apply_scientific_legend(fig, title: str | None = None) -> None:
    fig.update_layout(
        legend=dict(
            title=dict(text=title or "", font=dict(family=FONT_SANS, size=11, color=COLOR_MUTED)),
            font=dict(family=FONT_SANS, size=10, color=COLOR_INK),
            bgcolor="rgba(255,255,255,0.85)",
            bordercolor=COLOR_BORDER,
            borderwidth=1,
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02,
        )
    )


def get_figure_title(text: str) -> dict:
    return dict(
        text=text,
        font=dict(family=FONT_DISPLAY, size=PLOT_TITLE_SIZE, color=COLOR_INK),
        x=0,
        xanchor="left",
    )


def get_series_style(index: int, is_highlight: bool) -> dict:
    if is_highlight:
        return dict(color=PLOT_HIGHLIGHT, width=PLOT_HIGHLIGHT_WIDTH)
    return dict(
        color=PLOT_COLORS[min(index + 1, len(PLOT_COLORS) - 1)],
        width=PLOT_LINE_WIDTH,
    )
