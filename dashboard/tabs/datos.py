"""Exploración de datos y control de calidad."""

import pandas as pd
import streamlit as st


def renderizar_datos(datos: pd.DataFrame, calidad: dict) -> None:
    st.markdown(
        """<div class="section-head"><div><div class="section-kicker">Dataset</div>
        <div class="section-title">Explorador de registros analizados</div>
        <div class="section-question">Consulta, verifica y descarga el subconjunto que
        sustenta los indicadores activos.</div></div><span class="section-tag">TRAZABILIDAD</span></div>""",
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Registros", f"{len(datos):,}")
    c2.metric("Variables", len(datos.columns))
    c3.metric("Fechas válidas", f"{calidad.get('fechas_validas', 0):,}")
    c4.metric("Coordenadas válidas", f"{calidad.get('coordenadas_validas', 0):,}")
    st.markdown(
        f"""<div class="section-note"><b>Fuente:</b> {calidad.get('fuente', '')}<br>
        <b>Hoja:</b> {calidad.get('hoja_utilizada', '')}<br>
        <b>Tratamiento:</b> {calidad.get('tratamiento', '')}</div>""",
        unsafe_allow_html=True,
    )
    consulta = st.text_input("Buscar en los registros", placeholder="Provincia, cantón, arma...")
    vista = datos
    if consulta:
        mascara = datos.astype("string").apply(
            lambda columna: columna.str.contains(consulta, case=False, na=False)
        ).any(axis=1)
        vista = datos[mascara]
    columnas_clave = [
        "fecha_infraccion", "hora_infraccion", "provincia", "canton", "zona",
        "franja_horaria", "arma", "tipo_arma", "sexo", "edad", "grupo_edad",
        "lugar", "presunta_motivacion", "latitud", "longitud",
    ]
    columnas_clave = [c for c in columnas_clave if c in vista.columns]
    mostrar_todas = st.toggle("Mostrar todas las variables", value=False)
    tabla = vista if mostrar_todas else vista[columnas_clave]
    st.caption(f"Mostrando {len(tabla):,} registros y {len(tabla.columns)} variables.")
    st.dataframe(tabla, width="stretch", hide_index=True, height=480)
    st.download_button(
        "Descargar vista filtrada (CSV)",
        tabla.to_csv(index=False).encode("utf-8-sig"),
        "safeanalytics_datos_filtrados.csv",
        "text/csv",
    )
    with st.expander("Nulos por columna"):
        nulos = pd.DataFrame(
            calidad.get("nulos_por_columna", {}).items(), columns=["columna", "valores_nulos"]
        ).sort_values("valores_nulos", ascending=False)
        st.dataframe(nulos, width="stretch", hide_index=True)
