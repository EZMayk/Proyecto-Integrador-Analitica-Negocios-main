"""Proyección académica de tendencia."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def renderizar_predictiva(datos: pd.DataFrame) -> None:
    st.subheader("Analítica predictiva")
    st.warning(
        "La proyección es referencial y académica. Se basa únicamente en una "
        "tendencia lineal de cinco meses y no representa un modelo criminológico profesional."
    )
    mensual = (
        datos.groupby(["mes", "nombre_mes"], as_index=False)["total"].sum().sort_values("mes")
    )
    if len(mensual) < 2:
        st.info("Los filtros seleccionados no dejan suficientes meses para proyectar.")
        return
    pendiente, intercepto = np.polyfit(mensual["mes"], mensual["total"], 1)
    mes_siguiente = int(mensual["mes"].max() + 1)
    proyeccion = max(round(pendiente * mes_siguiente + intercepto), 0)
    meses = mensual["mes"].tolist() + [mes_siguiente]
    tendencia = [max(pendiente * m + intercepto, 0) for m in meses]
    nombres = mensual["nombre_mes"].tolist() + ["Junio" if mes_siguiente == 6 else f"Mes {mes_siguiente}"]

    k1, k2, k3 = st.columns(3)
    k1.metric("Proyección siguiente periodo", f"{proyeccion:,} casos")
    k2.metric("Variación mensual estimada", f"{pendiente:+.1f} casos")
    cambio = (proyeccion / mensual["total"].iloc[-1] - 1) * 100 if mensual["total"].iloc[-1] else 0
    k3.metric("Cambio frente al último mes", f"{cambio:+.1f}%")

    fig = go.Figure()
    fig.add_scatter(
        x=mensual["nombre_mes"], y=mensual["total"], mode="lines+markers",
        name="Casos observados", line=dict(width=4),
    )
    fig.add_scatter(
        x=nombres, y=tendencia, mode="lines+markers", name="Tendencia lineal",
        line=dict(dash="dash", color="#F9A825"),
    )
    fig.add_scatter(
        x=[nombres[-1]], y=[proyeccion], mode="markers+text", name="Proyección",
        text=[f"{proyeccion:,}"], textposition="top center", marker=dict(size=14, color="#C62828"),
    )
    fig.update_layout(title="Tendencia enero–mayo de 2026 y escenario referencial", xaxis_title="", yaxis_title="Casos")
    st.plotly_chart(fig, width="stretch")
    direccion = "creciente" if pendiente > 0 else "decreciente" if pendiente < 0 else "estable"
    st.info(
        f"Si la tendencia {direccion} observada continuara sin cambios, el siguiente "
        f"periodo podría registrar aproximadamente {proyeccion:,} casos. Este escenario "
        "no incorpora intervenciones, estacionalidad ni factores externos."
    )
