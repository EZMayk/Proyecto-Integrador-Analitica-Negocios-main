"""Proyección académica de tendencia."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


def renderizar_predictiva(datos: pd.DataFrame) -> None:
    st.markdown(
        """<div class="section-head"><div><div class="section-kicker">Analítica predictiva</div>
        <div class="section-title">Escenario de continuidad de tendencia</div>
        <div class="section-question">Pregunta de negocio: ¿qué podría pasar si el patrón
        mensual continúa?</div></div><span class="section-tag">ESTIMACIÓN REFERENCIAL</span></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="insight warning"><b>Uso responsable.</b> La estimación aplica una
        tendencia lineal a los meses disponibles. Es un ejercicio académico y no representa
        un modelo criminológico profesional.</div>""",
        unsafe_allow_html=True,
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
    st.markdown(
        f"""<div class="story-grid"><div class="story-card"><div class="label">Escenario proyectado</div>
        <h4>{proyeccion:,} casos en el siguiente periodo</h4><p>Valor esperado si la relación
        lineal observada se mantiene sin cambios externos.</p></div>
        <div class="story-card"><div class="label">Cómo interpretarlo</div><h4>Señal de planificación,
        no pronóstico definitivo</h4><p>Sirve para anticipar capacidad y contrastar escenarios,
        no para afirmar que el resultado ocurrirá.</p></div></div>""",
        unsafe_allow_html=True,
    )

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
    st.markdown(
        f"""<div class="insight"><b>Lectura ejecutiva.</b> Si la tendencia {direccion}
        continuara sin cambios, el siguiente periodo podría registrar aproximadamente
        {proyeccion:,} casos. Este escenario
        no incorpora intervenciones, estacionalidad ni factores externos.</div>""",
        unsafe_allow_html=True,
    )
