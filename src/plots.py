"""Figuras Plotly para la aplicacion."""

from __future__ import annotations

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from src.naca import get_airfoil_coordinates

COMMON_LAYOUT = dict(
    hovermode="x unified",
    template="plotly_white",
    legend=dict(
        title="Profilak",
        bgcolor="rgba(255,255,255,0.8)",
        bordercolor="#E5E7EB",
        borderwidth=1,
        orientation="v",
        yanchor="top",
        y=1,
        xanchor="left",
        x=1.02,
    ),
    margin=dict(l=40, r=150, t=60, b=40),
)

BEST_COLOR = "#E74C3C"
DEFAULT_COLORS = ["#1F618D", "#2E86AB", "#48A9A6", "#5C6BC0", "#7E57C2", "#AB47BC"]


def _base_layout(title: str, y_title: str) -> dict:
    return dict(
        title=dict(text=title, font=dict(size=18, color="#2C3E50")),
        xaxis_title="Eraso-angelua (Alpha) [deg]",
        yaxis_title=y_title,
        **COMMON_LAYOUT,
    )


def build_efficiency_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    if not results:
        return fig

    best_naca = results[0]["naca"]
    for i, item in enumerate(results):
        naca = item["naca"]
        is_best = naca == best_naca
        is_highlight = highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cl_cd"],
                mode="lines",
                name=f"NACA {naca}",
                line=dict(
                    width=4 if (is_best or is_highlight) else 2,
                    color=BEST_COLOR if is_best else DEFAULT_COLORS[i % len(DEFAULT_COLORS)],
                ),
            )
        )

    fig.update_layout(**_base_layout(f"{title} - Eraginkortasuna", "Eraginkortasuna (Cl/Cd)"))
    fig.add_hline(y=0, line_dash="dash", line_color="#7F8C8D", line_width=1.5)
    return fig


def build_cl_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    if not results:
        return fig

    best_naca = results[0]["naca"]
    for i, item in enumerate(results):
        naca = item["naca"]
        is_best = naca == best_naca
        is_highlight = highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cl"],
                mode="lines",
                name=f"NACA {naca}",
                line=dict(
                    width=4 if (is_best or is_highlight) else 2,
                    color=BEST_COLOR if is_best else DEFAULT_COLORS[i % len(DEFAULT_COLORS)],
                ),
            )
        )

    fig.update_layout(**_base_layout(f"{title} - Sustentazioa", "Sustentazioa (Cl)"))
    fig.add_hline(y=0, line_dash="dash", line_color="#7F8C8D", line_width=1.5)
    fig.add_hline(
        y=1.0,
        line_dash="dot",
        line_color=BEST_COLOR,
        line_width=2,
        annotation_text="Cl helburua ≈ 1.0",
    )
    return fig


def build_cd_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    if not results:
        return fig

    best_naca = results[0]["naca"]
    for i, item in enumerate(results):
        naca = item["naca"]
        is_best = naca == best_naca
        is_highlight = highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["alphas"],
                y=item["cd"],
                mode="lines",
                name=f"NACA {naca}",
                line=dict(
                    width=4 if (is_best or is_highlight) else 2,
                    color=BEST_COLOR if is_best else DEFAULT_COLORS[i % len(DEFAULT_COLORS)],
                ),
            )
        )

    fig.update_layout(**_base_layout(f"{title} - Erresistentzia", "Erresistentzia (Cd)"))
    return fig


def build_polar_figure(results: list[dict], title: str, highlight_naca: str | None = None) -> go.Figure:
    fig = go.Figure()
    if not results:
        return fig

    best_naca = results[0]["naca"]
    for i, item in enumerate(results):
        naca = item["naca"]
        is_best = naca == best_naca
        is_highlight = highlight_naca == naca
        fig.add_trace(
            go.Scatter(
                x=item["cd"],
                y=item["cl"],
                mode="lines",
                name=f"NACA {naca}",
                line=dict(
                    width=4 if (is_best or is_highlight) else 2,
                    color=BEST_COLOR if is_best else DEFAULT_COLORS[i % len(DEFAULT_COLORS)],
                ),
            )
        )

    fig.update_layout(
        title=dict(text=f"{title} - Polarra (Cl-Cd)", font=dict(size=18, color="#2C3E50")),
        xaxis_title="Cd",
        yaxis_title="Cl",
        **COMMON_LAYOUT,
    )
    return fig


def build_ranking_figure(results: list[dict]) -> go.Figure:
    fig = go.Figure()
    if not results:
        return fig

    labels = [f"NACA {item['naca']}" for item in results]
    values = [item["max_cl_cd"] for item in results]
    fig.add_trace(
        go.Bar(
            x=labels,
            y=values,
            marker_color=[BEST_COLOR if i == 0 else "#1F618D" for i in range(len(results))],
        )
    )
    fig.update_layout(
        title="Ranking - Gehienezko Cl/Cd",
        xaxis_title="Profila",
        yaxis_title="Cl/Cd max",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


def build_airfoil_geometry_figure(naca: str) -> go.Figure:
    xs, ys = get_airfoil_coordinates(naca)
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=xs,
            y=ys,
            mode="lines",
            fill="toself",
            name=f"NACA {naca}",
            line=dict(color="#1F618D", width=2),
            fillcolor="rgba(31, 97, 141, 0.15)",
        )
    )
    fig.update_layout(
        title=f"NACA {naca} geometria",
        xaxis_title="x/c",
        yaxis_title="y/c",
        template="plotly_white",
        yaxis=dict(scaleanchor="x", scaleratio=1),
        margin=dict(l=40, r=20, t=60, b=40),
        showlegend=False,
    )
    return fig


def build_blade_planform_figure(erradioak, kordak) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=erradioak,
            y=kordak,
            mode="lines+markers",
            name="Korda",
            line=dict(color="#1F618D", width=3),
            marker=dict(size=8),
        )
    )
    fig.update_layout(
        title="Hegalaren planoa (erradioa vs korda)",
        xaxis_title="Erradioa [m]",
        yaxis_title="Korda [m]",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


def build_reynolds_figure(estazioak, reynolds_values) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=estazioak,
            y=reynolds_values,
            marker_color="#2E86AB",
            name="Reynolds",
        )
    )
    fig.update_layout(
        title="Reynolds lokala estazio bakoitzean",
        xaxis_title="Estazioa",
        yaxis_title="Reynolds",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


def build_tsr_figure(estazioak, lambda_values) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=lambda_values,
            mode="lines+markers",
            name="TSR (lambda)",
            line=dict(color="#48A9A6", width=3),
            marker=dict(size=8),
        )
    )
    fig.update_layout(
        title="TSR (lambda) estazio bakoitzean",
        xaxis_title="Estazioa",
        yaxis_title="Lambda",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
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
            marker=dict(size=14, color="#1F618D"),
        )
    )
    fig.update_layout(
        title="NACA banaketa estazioaren arabera",
        xaxis_title="Estazioa",
        yaxis_title="Profila",
        template="plotly_white",
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig


def build_summary_dual_axis_figure(estazioak, kordak, reynolds_values) -> go.Figure:
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=kordak,
            mode="lines+markers",
            name="Korda [m]",
            line=dict(color="#1F618D", width=3),
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=estazioak,
            y=reynolds_values,
            mode="lines+markers",
            name="Reynolds",
            line=dict(color="#E74C3C", width=3, dash="dash"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Korda eta Reynolds banaketa",
        template="plotly_white",
        margin=dict(l=40, r=40, t=60, b=40),
        legend=dict(orientation="h"),
    )
    fig.update_xaxes(title_text="Estazioa")
    fig.update_yaxes(title_text="Korda [m]", secondary_y=False)
    fig.update_yaxes(title_text="Reynolds", secondary_y=True)
    return fig


def build_overlaid_airfoils_figure(nacak: list[str]) -> go.Figure:
    fig = go.Figure()
    unique_nacak = list(dict.fromkeys(nacak))
    for i, naca in enumerate(unique_nacak):
        xs, ys = get_airfoil_coordinates(naca)
        fig.add_trace(
            go.Scatter(
                x=xs,
                y=ys,
                mode="lines",
                name=f"NACA {naca}",
                line=dict(color=DEFAULT_COLORS[i % len(DEFAULT_COLORS)], width=2),
            )
        )
    fig.update_layout(
        title="Profilak gainjarriak",
        xaxis_title="x/c",
        yaxis_title="y/c",
        template="plotly_white",
        yaxis=dict(scaleanchor="x", scaleratio=1),
        margin=dict(l=40, r=20, t=60, b=40),
    )
    return fig
