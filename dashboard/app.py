"""Dashboard Ejecutivo SafeAnalytics EC.

Ejecutar desde la raíz: streamlit run dashboard/app.py
"""

from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

import pandas as pd
import streamlit as st

from dashboard.components import (
    renderizar_hero, renderizar_pie, silenciar_conn_reset_windows, tarjeta_kpi,
)
from dashboard.data import cargar_datos, cargar_reporte_calidad
from dashboard.tabs import (
    renderizar_datos, renderizar_descriptiva, renderizar_diagnostica,
    renderizar_portada, renderizar_predictiva, renderizar_prescriptiva,
)
from dashboard.theme import inyectar_css, registrar_tema_plotly

silenciar_conn_reset_windows()
st.set_page_config(
    page_title="SafeAnalytics EC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
registrar_tema_plotly()
inyectar_css()

datos = cargar_datos()
calidad = cargar_reporte_calidad()
renderizar_hero(int(datos["total"].sum()))


def opciones(columna: str) -> list[str]:
    return sorted(datos[columna].dropna().astype(str).unique().tolist())


with st.sidebar:
    st.markdown("### Filtros interactivos")
    provincia_sel = st.multiselect("Provincia", opciones("provincia"))
    base_cantones = datos[datos["provincia"].isin(provincia_sel)] if provincia_sel else datos
    cantones_disponibles = sorted(base_cantones["canton"].dropna().astype(str).unique())
    canton_sel = st.multiselect("Cantón", cantones_disponibles)
    arma_sel = st.multiselect("Arma", opciones("arma"))
    sexo_sel = st.multiselect("Sexo", opciones("sexo"))
    meses_sel = st.multiselect(
        "Mes", opciones("nombre_mes"),
        default=opciones("nombre_mes"),
    )
    franja_sel = st.multiselect(
        "Franja horaria", ["Madrugada", "Mañana", "Tarde", "Noche"],
        default=["Madrugada", "Mañana", "Tarde", "Noche"],
    )
    st.divider()
    st.caption(
        "Fuente histórica: homicidios intencionales registrados en Ecuador, "
        "enero–mayo de 2026. Actualización mediante dataset."
    )

filtro = pd.Series(True, index=datos.index)
for columna, seleccion in [
    ("provincia", provincia_sel), ("canton", canton_sel), ("arma", arma_sel),
    ("sexo", sexo_sel), ("nombre_mes", meses_sel), ("franja_horaria", franja_sel),
]:
    if seleccion:
        filtro &= datos[columna].isin(seleccion)
filtrados = datos[filtro].copy()

if filtrados.empty:
    st.warning("La combinación de filtros no contiene registros.")
    st.stop()


def principal(campo: str) -> str:
    serie = filtrados[campo].dropna().value_counts()
    return str(serie.index[0]) if not serie.empty else "Sin datos"


fuego = (
    filtrados["arma"].fillna("").str.contains("FUEGO", case=False, regex=False)
    | filtrados["tipo_arma"].fillna("").str.contains("FUEGO", case=False, regex=False)
)
porcentaje_fuego = fuego.mean() * 100
k1, k2, k3, k4, k5, k6 = st.columns(6)
tarjeta_kpi(k1, "Total de homicidios", f"{filtrados['total'].sum():,.0f}", "", "DESCRIPTIVA")
tarjeta_kpi(k2, "Provincia principal", principal("provincia").title(), "", "GEOGRAFÍA")
tarjeta_kpi(k3, "Cantón principal", principal("canton").title(), "", "GEOGRAFÍA")
tarjeta_kpi(k4, "Arma principal", principal("arma").title(), "", "DIAGNÓSTICA", "tierra")
tarjeta_kpi(k5, "Horario frecuente", principal("franja_horaria"), "", "TEMPORAL", "ambar")
tarjeta_kpi(k6, "Casos con arma de fuego", f"{porcentaje_fuego:.1f}", "%", "SEGURIDAD", "ambar")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
tab_portada, tab_desc, tab_diag, tab_pred, tab_presc, tab_datos = st.tabs([
    "Portada", "Descriptiva", "Diagnóstica", "Predictiva", "Prescriptiva", "Datos",
])
with tab_portada:
    renderizar_portada()
with tab_desc:
    renderizar_descriptiva(filtrados)
with tab_diag:
    renderizar_diagnostica(filtrados)
with tab_pred:
    renderizar_predictiva(filtrados)
with tab_presc:
    renderizar_prescriptiva(filtrados)
with tab_datos:
    renderizar_datos(filtrados, calidad)

st.markdown(
    f"""<div class="section-note"><b>Lectura ejecutiva:</b> La mayor concentración
    se observa en <b>{principal('provincia').title()}</b>, principalmente en
    <b>{principal('canton').title()}</b>. El arma más registrada es
    <b>{principal('arma').title()}</b> y la franja con mayor incidencia es
    <b>{principal('franja_horaria').lower()}</b>. Estos patrones orientan la
    priorización territorial y temporal de recursos.</div>""",
    unsafe_allow_html=True,
)
renderizar_pie()
