"""Vista ejecutiva de presentación."""

import pandas as pd
import streamlit as st


def renderizar_portada(datos: pd.DataFrame) -> None:
    provincias = datos["provincia"].nunique()
    cantones = datos["canton"].nunique()
    st.markdown(
        """<div class="section-head"><div>
        <div class="section-kicker">Vista ejecutiva</div>
        <div class="section-title">Inteligencia para decisiones en seguridad ciudadana</div>
        <div class="section-question">¿Cómo convierte SafeAnalytics EC los registros
        históricos en información estratégica?</div></div>
        <span class="section-tag">ANALÍTICA DE NEGOCIOS</span></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="story-grid">
        <div class="story-card"><div class="label">Problemática</div>
        <h4>Datos dispersos, decisiones más lentas</h4>
        <p>Los reportes tabulares dificultan detectar territorios, horarios y factores
        delictivos prioritarios. El sistema consolida la información y reduce esa brecha.</p></div>
        <div class="story-card"><div class="label">Objetivo</div>
        <h4>Transformar registros en señales ejecutivas</h4>
        <p>Visualizar indicadores y patrones mediante analítica descriptiva, diagnóstica,
        predictiva y prescriptiva para apoyar decisiones estratégicas.</p></div>
        <div class="story-card"><div class="label">Alcance del segmento</div>
        <h4>{len(datos):,} registros · {provincias} provincias · {cantones} cantones</h4>
        <p>Homicidios intencionales registrados en Ecuador entre enero y mayo de 2026,
        ajustados por los filtros activos.</p></div>
        <div class="story-card"><div class="label">Uso esperado</div>
        <h4>Priorización territorial y operativa</h4>
        <p>Orienta la lectura de tendencias, la focalización de recursos y la formulación
        de recomendaciones sustentadas en datos.</p></div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="analytics-row">
        <div class="analytics-chip"><b>DESCRIPTIVA</b><span>¿Qué ocurrió?</span></div>
        <div class="analytics-chip"><b>DIAGNÓSTICA</b><span>¿Dónde y por qué?</span></div>
        <div class="analytics-chip"><b>PREDICTIVA</b><span>¿Qué podría ocurrir?</span></div>
        <div class="analytics-chip"><b>PRESCRIPTIVA</b><span>¿Qué acciones priorizar?</span></div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        """<div class="insight warning"><b>Alcance metodológico.</b> El análisis utiliza
        un dataset histórico estático. La proyección es referencial y académica; no
        constituye un modelo criminológico profesional ni sustituye el criterio institucional.</div>""",
        unsafe_allow_html=True,
    )
