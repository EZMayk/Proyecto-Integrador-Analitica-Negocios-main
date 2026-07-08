"""Pie institucional."""

import streamlit as st


def renderizar_pie() -> None:
    st.markdown(
        """<div class="footer-line"><span>SAFEANALYTICS EC · ANALÍTICA DE NEGOCIOS</span>
        <span>SEGURIDAD CIUDADANA · ECUADOR 2026</span></div>""",
        unsafe_allow_html=True,
    )
