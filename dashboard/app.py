"""Dashboard Ejecutivo SafeAnalytics EC.

Ejecutar: streamlit run dashboard/app.py
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
    page_title="SafeAnalytics EC | Centro Ejecutivo",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)
registrar_tema_plotly()
inyectar_css()

datos = cargar_datos()
calidad = cargar_reporte_calidad()


def opciones(columna: str) -> list[str]:
    return sorted(datos[columna].dropna().astype(str).unique().tolist())


def limpiar_filtros() -> None:
    for clave in ["f_provincia", "f_canton", "f_arma", "f_sexo", "f_mes", "f_franja"]:
        st.session_state[clave] = []


with st.sidebar:
    st.markdown(
        """<div class="brand"><span class="brand-mark">S</span>
        <span class="brand-name">SafeAnalytics EC</span>
        <span class="brand-sub">Panel de filtros</span></div>
        <div class="filter-intro">Ajusta los criterios para explorar los indicadores,
        patrones y recomendaciones del sistema.</div>""",
        unsafe_allow_html=True,
    )
    provincia_sel = st.multiselect("Provincia", opciones("provincia"), key="f_provincia")
    base_cantones = datos[datos["provincia"].isin(provincia_sel)] if provincia_sel else datos
    cantones_disponibles = sorted(base_cantones["canton"].dropna().astype(str).unique())
    canton_sel = st.multiselect("Cantón", cantones_disponibles, key="f_canton")
    arma_sel = st.multiselect("Arma", opciones("arma"), key="f_arma")
    sexo_sel = st.multiselect("Sexo", opciones("sexo"), key="f_sexo")
    meses_sel = st.multiselect("Mes", opciones("nombre_mes"), key="f_mes")
    franja_sel = st.multiselect(
        "Franja horaria", ["Madrugada", "Mañana", "Tarde", "Noche"], key="f_franja",
    )
    st.button("↺ Limpiar filtros", on_click=limpiar_filtros, width="stretch")
    st.markdown(
        """<div class="source-note"><b>FUENTE HISTÓRICA</b><br>
        Homicidios intencionales registrados en Ecuador entre enero y mayo de 2026.
        El sistema se actualiza mediante la carga y procesamiento del dataset.</div>""",
        unsafe_allow_html=True,
    )

filtro = pd.Series(True, index=datos.index)
for columna, seleccion in [
    ("provincia", provincia_sel), ("canton", canton_sel), ("arma", arma_sel),
    ("sexo", sexo_sel), ("nombre_mes", meses_sel), ("franja_horaria", franja_sel),
]:
    if seleccion:
        filtro &= datos[columna].isin(seleccion)
filtrados = datos[filtro].copy()

renderizar_hero(int(datos["total"].sum()))
if filtrados.empty:
    st.warning("La combinación seleccionada no contiene registros. Limpia o ajusta los filtros.")
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
tarjeta_kpi(k1, "Total de homicidios", f"{filtrados['total'].sum():,.0f}", "", "VOLUMEN",
            interpretacion="Magnitud del segmento analizado")
tarjeta_kpi(k2, "Provincia crítica", principal("provincia").title(), "", "TERRITORIO",
            interpretacion="Mayor concentración territorial")
tarjeta_kpi(k3, "Cantón crítico", principal("canton").title(), "", "FOCO LOCAL",
            interpretacion="Prioridad operativa cantonal")
tarjeta_kpi(k4, "Arma predominante", principal("arma").title(), "", "PATRÓN", "alerta",
            "Factor crítico de seguridad")
tarjeta_kpi(k5, "Horario crítico", principal("franja_horaria"), "", "TEMPORAL", "alerta",
            "Patrón temporal dominante")
tarjeta_kpi(k6, "Casos con arma de fuego", f"{porcentaje_fuego:.1f}", "%", "EXPOSICIÓN", "critico",
            "Indicador de riesgo operativo")

tab_portada, tab_desc, tab_diag, tab_pred, tab_presc, tab_datos = st.tabs([
    "⌂ Vista ejecutiva", "▥ Descriptiva", "⌁ Diagnóstico",
    "↗ Predicción", "◎ Recomendaciones", "≡ Dataset",
])
with tab_portada:
    renderizar_portada(filtrados)
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

renderizar_pie()
