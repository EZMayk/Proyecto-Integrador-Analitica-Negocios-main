"""Cabecera institucional del dashboard."""

import streamlit as st


def renderizar_hero(total: int) -> None:
    st.markdown(
        f"""<div class="command-header"><div>
        <div class="overline">Centro de comando ejecutivo · Analítica de negocios</div>
        <h1>SafeAnalytics EC</h1>
        <p>Sistema Inteligente para el Monitoreo y Análisis Estratégico de
        Homicidios Intencionales en Ecuador.</p></div>
        <div class="dataset-badge"><b>{total:,} registros consolidados</b>
        Ecuador · enero—mayo 2026<br>Actualización mediante dataset</div></div>""",
        unsafe_allow_html=True,
    )
