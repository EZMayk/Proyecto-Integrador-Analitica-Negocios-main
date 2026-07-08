"""Tarjeta de indicador ejecutivo."""

from html import escape


def tarjeta_kpi(
    columna, etiqueta: str, valor: str, unidad: str, pilar: str,
    clase: str = "", interpretacion: str = "",
) -> None:
    columna.markdown(
        f"""<div class="kpi {escape(clase)}">
        <div class="etiqueta">{escape(etiqueta)}</div>
        <div class="valor">{escape(str(valor))} <span class="unidad">{escape(unidad)}</span></div>
        <span class="pilar">{escape(pilar)}</span>
        <div class="micro">{escape(interpretacion)}</div></div>""",
        unsafe_allow_html=True,
    )
