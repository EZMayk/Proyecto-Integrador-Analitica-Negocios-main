"""Analítica descriptiva, diagnóstica, predictiva y prescriptiva."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
DATOS = RAIZ / "data" / "processed" / "homicidios_procesados.csv"
REPORTES = RAIZ / "reports"


def conteo(datos: pd.DataFrame, campo: str, limite: int | None = None) -> pd.DataFrame:
    resultado = (
        datos.dropna(subset=[campo]).groupby(campo, as_index=False)["total"].sum()
        .rename(columns={"total": "casos"}).sort_values("casos", ascending=False)
    )
    return resultado.head(limite) if limite else resultado


def es_arma_fuego(serie: pd.Series) -> pd.Series:
    return serie.fillna("").str.contains("FUEGO", case=False, regex=False)


def ranking_riesgo(datos: pd.DataFrame) -> pd.DataFrame:
    base = datos.dropna(subset=["canton"]).copy()
    base["es_arma_fuego"] = es_arma_fuego(base["arma"]) | es_arma_fuego(base["tipo_arma"])
    base["es_horario_critico"] = base["franja_horaria"].isin(["Noche", "Madrugada"])
    ranking = base.groupby(["provincia", "canton"], as_index=False).agg(
        total_casos=("total", "sum"),
        casos_arma_fuego=("es_arma_fuego", "sum"),
        casos_noche_madrugada=("es_horario_critico", "sum"),
    )
    ranking["score_riesgo"] = (
        ranking["total_casos"]
        + ranking["casos_arma_fuego"] * 0.7
        + ranking["casos_noche_madrugada"] * 0.4
    ).round(1)
    ranking["nivel_riesgo"] = pd.qcut(
        ranking["score_riesgo"].rank(method="first"),
        q=[0, .5, .8, 1], labels=["Moderado", "Alto", "Crítico"],
    )
    return ranking.sort_values("score_riesgo", ascending=False).reset_index(drop=True)


def tendencia_y_proyeccion(datos: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    mensual = (
        datos.dropna(subset=["mes"]).groupby(["mes", "nombre_mes"], as_index=False)["total"].sum()
        .rename(columns={"total": "casos"}).sort_values("mes")
    )
    if len(mensual) < 2:
        return mensual, float(mensual["casos"].iloc[-1]) if len(mensual) else 0.0
    pendiente, intercepto = np.polyfit(mensual["mes"], mensual["casos"], 1)
    siguiente = max(float(pendiente * (mensual["mes"].max() + 1) + intercepto), 0)
    return mensual, round(siguiente, 0)


def recomendaciones(datos: pd.DataFrame, ranking: pd.DataFrame) -> list[str]:
    recs: list[str] = []
    for fila in ranking.head(3).itertuples():
        recs.append(
            f"Priorizar {fila.canton} ({fila.provincia}) en la distribución de recursos: "
            f"{fila.total_casos} casos y score {fila.score_riesgo}."
        )
    criticos = datos[datos["franja_horaria"].isin(["Noche", "Madrugada"])]
    if not criticos.empty:
        zona = criticos["zona"].dropna().value_counts()
        if not zona.empty:
            recs.append(f"Reforzar despliegue preventivo en {zona.index[0]} durante noche y madrugada.")
    fuego = datos[es_arma_fuego(datos["arma"]) | es_arma_fuego(datos["tipo_arma"])]
    lugar = fuego["lugar"].dropna().value_counts()
    if not lugar.empty:
        recs.append(
            f"Focalizar controles de armas de fuego alrededor de {lugar.index[0]}, "
            "donde se concentra su mayor frecuencia."
        )
    recs.append("Revisar la asignación semanal con datos actualizados y coordinación territorial.")
    return recs


def main() -> None:
    datos = pd.read_csv(DATOS, parse_dates=["fecha_infraccion"])
    ranking = ranking_riesgo(datos)
    mensual, proyeccion = tendencia_y_proyeccion(datos)
    REPORTES.mkdir(parents=True, exist_ok=True)
    ranking.to_csv(REPORTES / "ranking_riesgo_cantones.csv", index=False, encoding="utf-8-sig")
    mensual.to_csv(REPORTES / "tendencia_mensual.csv", index=False, encoding="utf-8-sig")
    resumen = {
        "total_homicidios": int(datos["total"].sum()),
        "periodo": "enero a mayo de 2026",
        "provincia_mayor_incidencia": conteo(datos, "provincia", 1).to_dict("records"),
        "canton_mayor_incidencia": conteo(datos, "canton", 1).to_dict("records"),
        "arma_mas_utilizada": conteo(datos, "arma", 1).to_dict("records"),
        "franja_mas_frecuente": conteo(datos, "franja_horaria", 1).to_dict("records"),
        "porcentaje_arma_fuego": round(float(
            (es_arma_fuego(datos["arma"]) | es_arma_fuego(datos["tipo_arma"])).mean() * 100
        ), 2),
        "proyeccion_siguiente_periodo": int(proyeccion),
        "advertencia_prediccion": (
            "Proyección referencial y académica basada en tendencia lineal; "
            "no constituye un modelo criminológico profesional."
        ),
        "recomendaciones": recomendaciones(datos, ranking),
    }
    (REPORTES / "resumen_analitico.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Analítica completada: {resumen['total_homicidios']:,} casos")


if __name__ == "__main__":
    main()
