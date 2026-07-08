"""Carga centralizada de datos para SafeAnalytics EC."""

import pandas as pd
import streamlit as st

from dashboard.data.rutas import RUTA_PROCESSED, RUTA_REPORTES


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    return pd.read_csv(
        RUTA_PROCESSED / "homicidios_procesados.csv",
        parse_dates=["fecha_infraccion"],
        low_memory=False,
    )


@st.cache_data
def cargar_ranking() -> pd.DataFrame:
    return pd.read_csv(RUTA_REPORTES / "ranking_riesgo_cantones.csv")
