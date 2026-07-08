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
    st.subheader("Analítica prescriptiva")
    st.caption(
        "Score = total de casos + casos con arma de fuego × 0,7 + "
        "casos en noche/madrugada × 0,4."
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

    st.markdown("#### Recomendaciones automáticas")
    for fila in ranking.head(3).itertuples():
        st.markdown(
            f"- Priorizar **{fila.canton} ({fila.provincia})**: {fila.total_casos} casos, "
            f"{fila.casos_arma_fuego} con arma de fuego y {fila.casos_noche_madrugada} "
            "en noche o madrugada."
        )
    criticos = datos[datos["franja_horaria"].isin(["Noche", "Madrugada"])]
    if not criticos.empty and not criticos["zona"].dropna().empty:
        zona = criticos["zona"].value_counts().index[0]
        st.markdown(f"- Reforzar recursos preventivos en **{zona}** durante horarios críticos.")
    fuego = datos[_arma_fuego(datos["arma"]) | _arma_fuego(datos["tipo_arma"])]
    if not fuego.empty and not fuego["lugar"].dropna().empty:
        lugar = fuego["lugar"].value_counts().index[0]
        st.markdown(f"- Focalizar controles de armas de fuego en entornos de **{lugar}**.")
    st.caption(
        "Estas recomendaciones apoyan la priorización estratégica; deben validarse "
        "con autoridades, contexto territorial y protocolos institucionales."
    )
