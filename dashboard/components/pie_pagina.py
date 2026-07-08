"""Pie institucional."""

import streamlit as st
from dashboard.theme import TINTA_SUAVE


def renderizar_pie() -> None:
    st.markdown(
        f"""<div style="text-align:center;color:{TINTA_SUAVE};font-size:.75rem;padding:18px 0">
        SafeAnalytics EC · Proyecto Integrador de Analítica de Negocios ·
        Fuente: dataset de homicidios intencionales MDI, enero–mayo 2026
        </div>""",
        unsafe_allow_html=True,
    )
