"""Figuras Plotly — estilo publicacion cientifica."""

from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.i18n import eu
from src.naca import get_airfoil_coordinates
from src.ui.theme import (
    COLOR_ACCENT,
    COLOR_BORDER,
    COLOR_MUTED,
    FONT_SANS,
    PLOT_COLORS,
    apply_scientific_axes,
    apply_scientific_legend,
    get_figure_title,
    get_plotly_layout_defaults,
    get_series_style,
)

ACCENT = COLOR_ACCENT
NEUTRAL = "#8aa0ad"


def _finalize_figure(fig: go.Figure, title: str, x_title: str, y_title: str, legend: bool = True) -> go.Figure:
    fig.update_layout(
        **get_plotly_layout_defaults(),
        title=get_figure_title(title),
        xaxis_title=x_title,
        yaxis_title=y_title,
    )
    apply_scientific_axes(fig)
    if legend:
        apply_scientific_legend(fig, eu.PLOTS["legend_profiles"])
    return fig


def build_efficiency_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    best_naca = results[0]["naca"] if results else None
    for i, item in enumerate(results):
        naca = item["naca"]
        is_highlight = naca == best_naca or highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cl_cd"],
                mode="lines",
                name=f"NACA {naca}",
                line=get_series_style(i, is_highlight),
            )
        )

    _finalize_figure(
        fig,
        f"{title} — {eu.PLOTS['efficiency_suffix']}",
        eu.PLOTS["axis_alpha"],
        eu.PLOTS["efficiency_y"],
    )
    fig.add_hline(y=0, line_dash="dash", line_color=COLOR_MUTED, line_width=0.8)
    return fig


def build_cl_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    best_naca = results[0]["naca"] if results else None
    for i, item in enumerate(results):
        naca = item["naca"]
        is_highlight = naca == best_naca or highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cl"],
                mode="lines",
                name=f"NACA {naca}",
                line=get_series_style(i, is_highlight),
            )
        )

    _finalize_figure(fig, f"{title} — {eu.PLOTS['cl_suffix']}", eu.PLOTS["axis_alpha"], eu.PLOTS["cl_y"])
    fig.add_hline(y=0, line_dash="dash", line_color=COLOR_MUTED, line_width=0.8)
    fig.add_hline(
        y=1.0,
        line_dash="dot",
        line_color=ACCENT,
        line_width=1,
        annotation_text=eu.PLOTS["cl_target"],
        annotation_font=dict(size=10, color=COLOR_MUTED),
    )
    return fig


def build_cd_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    best_naca = results[0]["naca"] if results else None
    for i, item in enumerate(results):
        naca = item["naca"]
        is_highlight = naca == best_naca or highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cd"],
                mode="lines",
                name=f"NACA {naca}",
                line=get_series_style(i, is_highlight),
            )
        )

    _finalize_figure(fig, f"{title} — {eu.PLOTS['cd_suffix']}", eu.PLOTS["axis_alpha"], eu.PLOTS["cd_y"])
    return fig


def build_polar_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    best_naca = results[0]["naca"] if results else None
    for i, item in enumerate(results):
        naca = item["naca"]
        is_highlight = naca == best_naca or highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["cd"],
                y=item["cl"],
                mode="lines",
                name=f"NACA {naca}",
                line=get_series_style(i, is_highlight),
            )
        )

    _finalize_figure(
        fig,
        f"{title} — {eu.PLOTS['polar_suffix']}",
        eu.PLOTS["polar_x"],
        eu.PLOTS["polar_y"],
    )
    return fig


def build_ranking_figure(results: list[dict]) -> go.Figure:
    fig = go.Figure()
    if not results:
        _finalize_figure(
            fig,
            eu.PLOTS["ranking_title"],
            eu.PLOTS["ranking_x"],
            eu.PLOTS["ranking_y"],
            legend=False,
        )
        return fig

    labels = [f"NACA {item['naca']}" for item in results]
    values = [item["max_cl_cd"] for item in results]
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            marker_color=[ACCENT if i == 0 else NEUTRAL for i in range(len(results))],
            marker_line=dict(color=COLOR_BORDER, width=0.5),
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["ranking_title"],
        eu.PLOTS["ranking_x"],
        eu.PLOTS["ranking_y"],
        legend=False,
    )
    return fig


def build_airfoil_geometry_figure(naca: str) -> go.Figure:
    coords = get_airfoil_coordinates(naca)
    fig = go.Figure()
    if coords is None:
        fig.update_layout(title=eu.ERRORS["geometry_unavailable"])
        return fig

    xs, ys = coords
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            fill="toself",
            name=f"NACA {naca}",
            line=dict(color=ACCENT, width=1.8),
            fillcolor="rgba(28, 93, 130, 0.08)",
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["geometry_title"].format(naca=naca),
        eu.PLOTS["geometry_x"],
        eu.PLOTS["geometry_y"],
        legend=False,
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig


def build_blade_planform_figure(erradioak, kordak) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=erradioak,
            y=kordak,
            mode="lines+markers",
            name=eu.PLOTS["planform_y"],
            line=dict(color=ACCENT, width=1.8),
            marker=dict(size=6, color=ACCENT, line=dict(width=0.5, color="#ffffff")),
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["planform_title"],
        eu.PLOTS["planform_x"],
        eu.PLOTS["planform_y"],
        legend=False,
    )
    return fig


def build_reynolds_figure(estazioak, reynolds_values) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=estazioak,
            y=reynolds_values,
            marker_color=ACCENT,
            marker_line=dict(color=COLOR_BORDER, width=0.5),
            name=eu.PLOTS["reynolds_y"],
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["reynolds_title"],
        eu.PLOTS["reynolds_x"],
        eu.PLOTS["reynolds_y"],
        legend=False,
    )
    return fig


def build_tsr_figure(estazioak, lambda_values) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=lambda_values,
            mode="lines+markers",
            name=eu.PLOTS["tsr_y"],
            line=dict(color=ACCENT, width=1.8),
            marker=dict(size=6, color=ACCENT, line=dict(width=0.5, color="#ffffff")),
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["tsr_title"],
        eu.PLOTS["tsr_x"],
        eu.PLOTS["tsr_y"],
        legend=False,
    )
    return fig


def build_spanwise_naca_figure(estazioak, nacak) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=[f"NACA {naca}" for naca in nacak],
            mode="markers+text",
            text=[f"NACA {naca}" for naca in nacak],
            textposition="middle right",
            textfont=dict(family=FONT_SANS, size=11),
            marker=dict(size=9, color=ACCENT, symbol="square", line=dict(width=0.5, color="#ffffff")),
        )
    )
    _finalize_figure(
        fig,
        eu.PLOTS["spanwise_title"],
        eu.PLOTS["spanwise_x"],
        eu.PLOTS["spanwise_y"],
        legend=False,
    )
    return fig


def build_summary_dual_axis_figure(estazioak, kordak, reynolds_values) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=kordak,
            mode="lines+markers",
            name=eu.PLOTS["dual_chord"],
            line=dict(color=ACCENT, width=1.8),
            marker=dict(size=6, color=ACCENT),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=reynolds_values,
            mode="lines+markers",
            name=eu.PLOTS["dual_reynolds"],
            line=dict(color=NEUTRAL, width=1.8, dash="dash"),
            marker=dict(size=6, color=NEUTRAL),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        **get_plotly_layout_defaults(),
        title=get_figure_title(eu.PLOTS["dual_title"]),
        legend=dict(
            orientation="h",
            font=dict(size=10),
            bgcolor="white",
            bordercolor=COLOR_BORDER,
            borderwidth=1,
        ),
    )
    apply_scientific_axes(fig)
    fig.update_xaxes(title_text=eu.PLOTS["reynolds_x"])
    fig.update_yaxes(title_text=eu.PLOTS["dual_chord"], secondary_y=False)
    fig.update_yaxes(title_text=eu.PLOTS["dual_reynolds"], secondary_y=True)
    return fig


def build_overlaid_airfoils_figure(nacak: list[str]) -> go.Figure:
    fig = go.Figure()
    unique_nacak = list(dict.fromkeys(nacak))
    for i, naca in enumerate(unique_nacak):
        coords = get_airfoil_coordinates(naca)
        if coords is None:
            continue
        xs, ys = coords
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                name=f"NACA {naca}",
                line=dict(color=PLOT_COLORS[min(i + 1, len(PLOT_COLORS) - 1)], width=1.2),
            )
        )
    _finalize_figure(
        fig,
        eu.PLOTS["overlay_title"],
        eu.PLOTS["geometry_x"],
        eu.PLOTS["geometry_y"],
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig
