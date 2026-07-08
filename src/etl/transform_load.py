"""ETL principal de SafeAnalytics EC.

Lee el archivo oficial de homicidios intencionales, normaliza sus campos y
genera una tabla analítica lista para Streamlit, Plotly y Power BI.
"""

from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parents[2]
ARCHIVO_ORIGEN = RAIZ / "data" / "raw" / "mdi_homicidiosintencionalse_pm_2026_enero_mayo.xlsx"
CARPETA_PROCESADA = RAIZ / "data" / "processed"
ARCHIVO_SALIDA = CARPETA_PROCESADA / "homicidios_procesados.csv"
ARCHIVO_CALIDAD = CARPETA_PROCESADA / "reporte_calidad.json"

VALORES_SIN_DATO = {
    "", "SIN DATO", "SIN_DATO", "NO DETERMINADO", "NO DETERMINADA",
    "N/D", "ND", "NAN", "NONE", "NULL",
}

RENOMBRES = {
    "codigo_subcircuito": "codigo_subcircuito",
    "coordenada_y": "latitud",
    "coordenada_x": "longitud",
    "presun_motiva_observada": "motivacion_observada",
    "probable_causa_motivada": "probable_causa",
}

MESES_ES = {
    1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo",
    6: "Junio", 7: "Julio", 8: "Agosto", 9: "Septiembre",
    10: "Octubre", 11: "Noviembre", 12: "Diciembre",
}

CAMPOS_PRIORITARIOS = [
    "tipo_muerte", "provincia", "canton", "zona", "subzona", "distrito",
    "circuito", "codigo_subcircuito", "subcircuito", "fecha_infraccion",
    "anio", "mes", "nombre_mes", "dia", "hora_infraccion", "hora",
    "franja_horaria", "arma", "tipo_arma", "sexo", "genero", "edad",
    "grupo_edad", "etnia", "nacionalidad", "estado_civil", "lugar",
    "tipo_lugar", "area_hecho", "presunta_motivacion",
    "motivacion_observada", "probable_causa", "latitud", "longitud", "total",
]


def limpiar_nombre(valor: object) -> str:
    """Convierte un encabezado a snake_case ASCII."""
    texto = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode()
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", texto.lower())).strip("_")


def normalizar_texto(serie: pd.Series) -> pd.Series:
    """Normaliza espacios, mayúsculas y marcadores de ausencia."""
    salida = serie.astype("string").str.strip().str.replace(r"\s+", " ", regex=True).str.upper()
    return salida.mask(salida.isin(VALORES_SIN_DATO), pd.NA)


def detectar_hoja_principal(ruta: Path) -> str:
    """Elige la hoja con mayor cantidad de columnas útiles."""
    libro = pd.ExcelFile(ruta)
    candidatos: list[tuple[int, str]] = []
    for hoja in libro.sheet_names:
        muestra = pd.read_excel(ruta, sheet_name=hoja, nrows=5)
        columnas = {limpiar_nombre(c) for c in muestra.columns}
        puntaje = len(columnas & {"provincia", "canton", "fecha_infraccion", "arma", "edad"})
        candidatos.append((puntaje * 100 + len(columnas), hoja))
    return max(candidatos)[1]


def convertir_hora(valor: object) -> float:
    """Devuelve hora decimal para valores time, texto o seriales de Excel."""
    if pd.isna(valor):
        return np.nan
    if hasattr(valor, "hour"):
        return float(valor.hour) + float(valor.minute) / 60 + float(valor.second) / 3600
    if isinstance(valor, (int, float)):
        numero = float(valor)
        return (numero % 1) * 24 if numero <= 1 else numero % 24
    texto = str(valor).strip()
    partes = texto.split(":")
    try:
        return float(partes[0]) + float(partes[1]) / 60 + (float(partes[2]) / 3600 if len(partes) > 2 else 0)
    except (ValueError, IndexError):
        fecha = pd.to_datetime(texto, errors="coerce")
        return np.nan if pd.isna(fecha) else fecha.hour + fecha.minute / 60


def clasificar_franja(hora: float) -> object:
    if pd.isna(hora):
        return pd.NA
    if hora < 6:
        return "Madrugada"
    if hora < 12:
        return "Mañana"
    if hora < 18:
        return "Tarde"
    return "Noche"


def clasificar_edad(edad: float) -> object:
    if pd.isna(edad):
        return pd.NA
    if edad < 18:
        return "Menor de edad"
    if edad < 30:
        return "18 a 29"
    if edad < 45:
        return "30 a 44"
    if edad < 60:
        return "45 a 59"
    return "60 o más"


def transformar() -> tuple[pd.DataFrame, dict]:
    if not ARCHIVO_ORIGEN.exists():
        raise FileNotFoundError(f"No se encontró el dataset: {ARCHIVO_ORIGEN}")

    hoja = detectar_hoja_principal(ARCHIVO_ORIGEN)
    datos = pd.read_excel(ARCHIVO_ORIGEN, sheet_name=hoja)
    filas_iniciales = len(datos)
    datos.columns = [RENOMBRES.get(limpiar_nombre(c), limpiar_nombre(c)) for c in datos.columns]
    duplicados = int(datos.duplicated().sum())
    datos = datos.drop_duplicates().copy()

    columnas_texto = datos.select_dtypes(include=["object", "string"]).columns
    for columna in columnas_texto:
        if columna not in {"fecha_infraccion", "hora_infraccion", "coordenada_x", "coordenada_y"}:
            datos[columna] = normalizar_texto(datos[columna])

    datos["fecha_infraccion"] = pd.to_datetime(datos["fecha_infraccion"], errors="coerce", dayfirst=True)
    datos["anio"] = datos["fecha_infraccion"].dt.year.astype("Int64")
    datos["mes"] = datos["fecha_infraccion"].dt.month.astype("Int64")
    datos["nombre_mes"] = datos["mes"].map(MESES_ES)
    datos["dia"] = datos["fecha_infraccion"].dt.day.astype("Int64")

    datos["hora"] = datos["hora_infraccion"].map(convertir_hora).round(3)
    datos["hora_infraccion"] = datos["hora"].map(
        lambda h: pd.NA if pd.isna(h) else f"{int(h):02d}:{int((h % 1) * 60):02d}"
    )
    datos["franja_horaria"] = datos["hora"].map(clasificar_franja)

    datos["edad"] = pd.to_numeric(datos["edad"], errors="coerce").astype("Int64")
    datos.loc[~datos["edad"].between(0, 120), "edad"] = pd.NA
    datos["grupo_edad"] = datos["edad"].map(clasificar_edad)

    for columna in ["latitud", "longitud"]:
        datos[columna] = pd.to_numeric(
            datos[columna].astype("string").str.replace(",", ".", regex=False), errors="coerce"
        )
    coordenadas_validas = datos["latitud"].between(-5.5, 2.0) & datos["longitud"].between(-92, -75)
    datos.loc[~coordenadas_validas, ["latitud", "longitud"]] = np.nan
    datos["total"] = 1

    orden = [c for c in CAMPOS_PRIORITARIOS if c in datos.columns]
    adicionales = [c for c in datos.columns if c not in orden]
    datos = datos[orden + adicionales]

    calidad = {
        "proyecto": "SafeAnalytics EC",
        "fuente": str(ARCHIVO_ORIGEN.relative_to(RAIZ)),
        "hoja_utilizada": hoja,
        "filas_iniciales": filas_iniciales,
        "duplicados_eliminados": duplicados,
        "filas_finales": len(datos),
        "columnas_finales": len(datos.columns),
        "fechas_validas": int(datos["fecha_infraccion"].notna().sum()),
        "horas_validas": int(datos["hora"].notna().sum()),
        "edades_validas": int(datos["edad"].notna().sum()),
        "coordenadas_validas": int(datos[["latitud", "longitud"]].notna().all(axis=1).sum()),
        "nulos_por_columna": {c: int(v) for c, v in datos.isna().sum().items()},
        "tratamiento": "Marcadores SIN_DATO y NO DETERMINADO se convierten a valores nulos; no se imputan atributos de víctimas.",
    }
    return datos, calidad


def main() -> None:
    CARPETA_PROCESADA.mkdir(parents=True, exist_ok=True)
    datos, calidad = transformar()
    datos.to_csv(ARCHIVO_SALIDA, index=False, encoding="utf-8-sig", date_format="%Y-%m-%d")
    ARCHIVO_CALIDAD.write_text(json.dumps(calidad, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"SafeAnalytics EC — ETL completado: {len(datos):,} registros")
    print(f"Datos: {ARCHIVO_SALIDA.relative_to(RAIZ)}")
    print(f"Calidad: {ARCHIVO_CALIDAD.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
