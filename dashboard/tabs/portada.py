"""Portada ejecutiva del sistema."""

import streamlit as st


def renderizar_portada() -> None:
    st.subheader("Portada ejecutiva")
    st.markdown(
        """
### SafeAnalytics EC

**Sistema Inteligente de Analítica de Negocios para el Monitoreo y Análisis
Estratégico de Homicidios Intencionales en Ecuador.**

#### Problemática

Las instituciones encargadas de la seguridad ciudadana generan grandes volúmenes
de información sobre homicidios intencionales. Cuando estos datos permanecen
dispersos en bases y reportes tabulares, se dificulta identificar oportunamente
patrones delictivos y orientar operativos, recursos policiales y políticas de
prevención.

El análisis manual limita la detección de provincias, cantones y zonas con mayor
incidencia, horarios críticos, armas utilizadas y perfiles predominantes. Este
dashboard consolida la información en una plataforma visual e interactiva para
facilitar el análisis dinámico y la toma de decisiones basada en datos.

#### Objetivo

Diseñar y desarrollar un Dashboard Ejecutivo interactivo para visualizar y
analizar los principales indicadores de homicidios intencionales registrados en
Ecuador, mediante analítica descriptiva, diagnóstica, predictiva y prescriptiva,
con el propósito de identificar patrones geográficos, temporales y delictivos que
apoyen decisiones estratégicas en seguridad ciudadana.

#### Alcance

- Registros de Ecuador entre enero y mayo de 2026.
- Análisis geográfico, temporal, delictivo y demográfico.
- Proyección académica de tendencia y priorización territorial.
- Actualización mediante la sustitución y procesamiento del dataset fuente.
"""
    )
    st.warning(
        "El análisis se basa en un archivo histórico estático. No corresponde a "
        "una fuente de actualización continua ni sustituye análisis criminológicos u operativos oficiales."
    )
