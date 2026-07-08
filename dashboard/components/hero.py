"""Encabezado ejecutivo de SafeAnalytics EC."""

import streamlit as st


def renderizar_hero(total: int) -> None:
    st.markdown(
        f"""
<div class="hero">
  <h1><span class="icono-material">shield</span> SafeAnalytics EC</h1>
  <p>Sistema Inteligente de Analítica de Negocios para el Monitoreo y Análisis
  Estratégico de Homicidios Intencionales en Ecuador</p>
  <div class="badges">
    <span class="badge">Ecuador · enero–mayo 2026</span>
    <span class="badge">{total:,} registros procesados</span>
    <span class="badge">Dataset histórico estático</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
