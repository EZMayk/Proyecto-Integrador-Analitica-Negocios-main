"""Vista diagnóstica."""

import pandas as pd
import plotly.express as px
import streamlit as st


def _top(datos: pd.DataFrame, campo: str) -> tuple[str, int]:
    serie = datos[campo].dropna().value_counts()
    return (str(serie.index[0]), int(serie.iloc[0])) if not serie.empty else ("Sin datos", 0)


def renderizar_diagnostica(datos: pd.DataFrame) -> None:
    st.markdown(
        """<div class="section-head"><div><div class="section-kicker">Analítica diagnóstica</div>
        <div class="section-title">Concentraciones y factores asociados</div>
        <div class="section-question">Pregunta de negocio: ¿dónde y por qué se concentra
        el problema?</div></div><span class="section-tag">HALLAZGOS CLAVE</span></div>""",
        unsafe_allow_html=True,
    )
    provincia, _ = _top(datos, "provincia")
    canton, _ = _top(datos, "canton")
    arma, _ = _top(datos, "arma")
    franja, _ = _top(datos, "franja_horaria")
    lugar, _ = _top(datos, "lugar")
    grupo, _ = _top(datos, "grupo_edad")
    sexo, _ = _top(datos, "sexo")
    st.markdown(
        f"""<div class="insight"><b>Hallazgo principal.</b> La mayor concentración se observa en
        <b>{provincia}</b>, principalmente en <b>{canton}</b>. El perfil predominante
        corresponde a <b>{sexo}</b> del grupo <b>{grupo}</b>. La combinación más
        frecuente involucra <b>{arma}</b>, durante la <b>{franja.lower()}</b>, y el
        lugar más recurrente es <b>{lugar}</b>.</div>""",
        unsafe_allow_html=True,
    )
    h1, h2, h3 = st.columns(3)
    h1.metric("Perfil predominante", f"{sexo.title()} · {grupo}")
    h2.metric("Lugar recurrente", lugar.title())
    h3.metric("Combinación crítica", f"{arma.title()} · {franja}")

    c1, c2 = st.columns(2)
    motivaciones = (
        datos.dropna(subset=["presunta_motivacion"])
        .groupby("presunta_motivacion", as_index=False)["total"].sum()
        .nlargest(12, "total").sort_values("total")
    )
    c1.plotly_chart(px.bar(
        motivaciones, x="total", y="presunta_motivacion", orientation="h",
        title="Motivaciones más frecuentes",
        labels={"total": "Casos", "presunta_motivacion": ""},
    ), width="stretch")

    cruce = pd.crosstab(datos["franja_horaria"], datos["arma"])
    armas_top = datos["arma"].value_counts().head(7).index
    cruce = cruce.reindex(columns=armas_top, fill_value=0)
    c2.plotly_chart(px.imshow(
        cruce, text_auto=True, aspect="auto", color_continuous_scale="Blues",
        title="Relación entre arma y horario",
        labels={"x": "Arma", "y": "Franja horaria", "color": "Casos"},
    ), width="stretch")

    ubicacion = (
        datos.dropna(subset=["provincia", "franja_horaria", "arma"])
        .groupby(["provincia", "franja_horaria", "arma"], as_index=False)["total"].sum()
        .nlargest(40, "total")
    )
    st.plotly_chart(px.sunburst(
        ubicacion, path=["provincia", "franja_horaria", "arma"], values="total",
        title="Relación jerárquica entre ubicación, horario y arma",
    ), width="stretch")
