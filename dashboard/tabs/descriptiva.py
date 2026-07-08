"""Vista descriptiva."""

import pandas as pd
import plotly.express as px
import streamlit as st


def _conteo(datos: pd.DataFrame, campo: str, n: int | None = None) -> pd.DataFrame:
    salida = datos.dropna(subset=[campo]).groupby(campo, as_index=False)["total"].sum()
    salida = salida.sort_values("total", ascending=False)
    return salida.head(n) if n else salida


def renderizar_descriptiva(datos: pd.DataFrame) -> None:
    st.markdown(
        """<div class="section-head"><div><div class="section-kicker">Analítica descriptiva</div>
        <div class="section-title">Panorama de los hechos registrados</div>
        <div class="section-question">Pregunta de negocio: ¿qué ocurrió y cómo se distribuyen
        los casos?</div></div><span class="section-tag">EVIDENCIA HISTÓRICA</span></div>""",
        unsafe_allow_html=True,
    )
    izq, der = st.columns(2)
    provincia = _conteo(datos, "provincia")
    izq.plotly_chart(px.bar(
        provincia.sort_values("total"), x="total", y="provincia", orientation="h",
        title="Homicidios por provincia", labels={"total": "Casos", "provincia": ""},
    ), width="stretch")
    canton = _conteo(datos, "canton", 15)
    der.plotly_chart(px.bar(
        canton.sort_values("total"), x="total", y="canton", orientation="h",
        title="Top 15 cantones", labels={"total": "Casos", "canton": ""},
    ), width="stretch")
    top_prov = provincia.iloc[0]
    top_canton = canton.iloc[0]
    st.markdown(
        f"""<div class="insight"><b>Lectura territorial.</b> {top_prov['provincia']} lidera
        la distribución con {int(top_prov['total']):,} casos. A escala local,
        {top_canton['canton']} registra la mayor concentración del segmento analizado.</div>""",
        unsafe_allow_html=True,
    )

    mensual = (
        datos.groupby(["mes", "nombre_mes"], as_index=False)["total"].sum().sort_values("mes")
    )
    fig = px.line(
        mensual, x="nombre_mes", y="total", markers=True, title="Tendencia mensual",
        labels={"nombre_mes": "Mes", "total": "Casos"},
    )
    fig.update_traces(line_width=4)
    st.plotly_chart(fig, width="stretch")
    pico = mensual.loc[mensual["total"].idxmax()]
    st.markdown(
        f"""<div class="insight"><b>Lectura temporal.</b> {pico['nombre_mes']} presenta el
        máximo mensual con {int(pico['total']):,} casos. La línea permite evaluar cambios
        de magnitud entre los cinco periodos observados.</div>""",
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.plotly_chart(px.pie(
        _conteo(datos, "sexo"), names="sexo", values="total", hole=.45,
        title="Distribución por sexo",
    ), width="stretch")
    c2.plotly_chart(px.bar(
        _conteo(datos, "arma", 8), x="arma", y="total", title="Armas más registradas",
        labels={"arma": "", "total": "Casos"},
    ).update_xaxes(tickangle=-35), width="stretch")
    orden = ["Madrugada", "Mañana", "Tarde", "Noche"]
    c3.plotly_chart(px.bar(
        _conteo(datos, "franja_horaria"), x="franja_horaria", y="total",
        category_orders={"franja_horaria": orden}, title="Casos por franja horaria",
        labels={"franja_horaria": "", "total": "Casos"},
    ), width="stretch")

    lugares, tipos = st.columns(2)
    lugares.plotly_chart(px.bar(
        _conteo(datos, "lugar", 10).sort_values("total"), x="total", y="lugar",
        orientation="h", title="Lugares con más casos", labels={"total": "Casos", "lugar": ""},
    ), width="stretch")
    tipos.plotly_chart(px.bar(
        _conteo(datos, "tipo_arma", 10).sort_values("total"), x="total", y="tipo_arma",
        orientation="h", title="Casos por tipo de arma", labels={"total": "Casos", "tipo_arma": ""},
    ), width="stretch")

    coordenadas = datos.dropna(subset=["latitud", "longitud"]).copy()
    if not coordenadas.empty:
        puntos = (
            coordenadas.groupby(
                ["latitud", "longitud", "provincia", "canton"], as_index=False, dropna=False
            )["total"].sum()
        )
        fig_mapa = px.scatter_map(
            puntos, lat="latitud", lon="longitud", size="total", color="total",
            hover_name="canton", hover_data={"provincia": True, "total": True},
            color_continuous_scale="YlOrRd", zoom=5.2, height=560,
            title="Distribución geográfica de registros",
            labels={"total": "Casos"},
        )
        fig_mapa.update_layout(map_style="carto-positron")
        st.plotly_chart(fig_mapa, width="stretch")
