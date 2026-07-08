"""Registro del template global de SafeAnalytics EC."""

import plotly.graph_objects as go
import plotly.io as pio

from dashboard.theme.colores import SECUENCIA_COLORES, TINTA


def registrar_tema_plotly() -> None:
    """Registra y activa el template institucional de Plotly."""
    pio.templates["safeanalytics"] = go.layout.Template(
        layout=go.Layout(
            font=dict(family="Inter, 'Segoe UI', sans-serif", size=13, color=TINTA),
            title=dict(font=dict(size=15, color=TINTA), x=0, xanchor="left"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            colorway=SECUENCIA_COLORES,
            xaxis=dict(gridcolor="#E3E9F2", zerolinecolor="#E3E9F2", linecolor="#CBD5E1"),
            yaxis=dict(gridcolor="#E3E9F2", zerolinecolor="#E3E9F2", linecolor="#CBD5E1"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
                        font=dict(size=11)),
            margin=dict(l=10, r=10, t=60, b=10),
            hoverlabel=dict(font_family="Inter, 'Segoe UI', sans-serif"),
        )
    )
    pio.templates.default = "safeanalytics"
