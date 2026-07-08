"""Ranking de riesgo y recomendaciones."""

import pandas as pd
import plotly.express as px
import streamlit as st


def _arma_fuego(serie: pd.Series) -> pd.Series:
    return serie.fillna("").str.contains("FUEGO", case=False, regex=False)


def calcular_ranking(datos: pd.DataFrame) -> pd.DataFrame:
    base = datos.dropna(subset=["canton"]).copy()
    base["fuego"] = _arma_fuego(base["arma"]) | _arma_fuego(base["tipo_arma"])
    base["horario_critico"] = base["franja_horaria"].isin(["Noche", "Madrugada"])
    ranking = base.groupby(["provincia", "canton"], as_index=False).agg(
        total_casos=("total", "sum"),
        casos_arma_fuego=("fuego", "sum"),
        casos_noche_madrugada=("horario_critico", "sum"),
    )
    ranking["score_riesgo"] = (
        ranking["total_casos"] + ranking["casos_arma_fuego"] * .7
        + ranking["casos_noche_madrugada"] * .4
    ).round(1)
    return ranking.sort_values("score_riesgo", ascending=False)


def renderizar_prescriptiva(datos: pd.DataFrame) -> None:
    st.markdown(
        """<div class="section-head"><div><div class="section-kicker">Analítica prescriptiva</div>
        <div class="section-title">Panel de priorización y acciones sugeridas</div>
        <div class="section-question">Pregunta de negocio: ¿qué acciones deberían
        priorizarse con los recursos disponibles?</div></div>
        <span class="section-tag">SOPORTE A DECISIONES</span></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="insight"><b>Criterio de priorización.</b> Score = casos totales
        + casos con arma de fuego × 0,7 + casos en noche/madrugada × 0,4.
        El indicador ordena territorios; no reemplaza una evaluación operativa integral.</div>""",
        unsafe_allow_html=True,
    )
    ranking = calcular_ranking(datos)
    top = ranking.head(15).sort_values("score_riesgo")
    st.plotly_chart(px.bar(
        top, x="score_riesgo", y="canton", color="provincia", orientation="h",
        title="Ranking de cantones por score de riesgo",
        labels={"score_riesgo": "Score de riesgo", "canton": "", "provincia": "Provincia"},
        hover_data=["total_casos", "casos_arma_fuego", "casos_noche_madrugada"],
    ), width="stretch")
    st.dataframe(
        ranking.head(20), width="stretch", hide_index=True,
        column_config={"score_riesgo": st.column_config.ProgressColumn(
            "Score de riesgo", min_value=0, max_value=float(max(ranking["score_riesgo"].max(), 1))
        )},
    )

    st.markdown("### Recomendaciones ejecutivas")
    columnas = st.columns(3)
    for columna, fila in zip(columnas, ranking.head(3).itertuples()):
        columna.markdown(
            f"""<div class="action-card high"><div class="priority">PRIORIDAD ALTA</div>
            <h4>{fila.canton.title()} · {fila.provincia.title()}</h4>
            <p><b>Acción:</b> priorizar operativos y asignación territorial.<br>
            <b>Justificación:</b> score {fila.score_riesgo}, {fila.total_casos} casos,
            {fila.casos_arma_fuego} con arma de fuego y {fila.casos_noche_madrugada}
            en noche/madrugada.<br><b>Impacto esperado:</b> mayor focalización de recursos.</p></div>""",
            unsafe_allow_html=True,
        )
    criticos = datos[datos["franja_horaria"].isin(["Noche", "Madrugada"])]
    if not criticos.empty and not criticos["zona"].dropna().empty:
        zona = criticos["zona"].value_counts().index[0]
        z1, z2 = st.columns(2)
        z1.markdown(
            f"""<div class="action-card medium"><div class="priority">PRIORIDAD MEDIA · HORARIO</div>
            <h4>Reforzar despliegue en {zona.title()}</h4><p>Concentrar patrullaje y
            controles preventivos durante noche y madrugada, según el patrón filtrado.</p></div>""",
            unsafe_allow_html=True,
        )
    else:
        z1, z2 = st.columns(2)
    fuego = datos[_arma_fuego(datos["arma"]) | _arma_fuego(datos["tipo_arma"])]
    if not fuego.empty and not fuego["lugar"].dropna().empty:
        lugar = fuego["lugar"].value_counts().index[0]
        z2.markdown(
            f"""<div class="action-card medium"><div class="priority">PRIORIDAD MEDIA · ARMA</div>
            <h4>Focalizar controles en {lugar.title()}</h4><p>Dirigir acciones preventivas
            a lugares donde se concentra el uso registrado de arma de fuego.</p></div>""",
            unsafe_allow_html=True,
        )
    st.caption(
        "Estas recomendaciones apoyan la priorización estratégica; deben validarse "
        "con autoridades, contexto territorial y protocolos institucionales."
    )
