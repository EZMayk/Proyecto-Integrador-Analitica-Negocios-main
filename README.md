# SafeAnalytics EC

**Sistema Inteligente de Analítica de Negocios para el Monitoreo y Análisis
Estratégico de Homicidios Intencionales en Ecuador**

Proyecto académico que transforma registros históricos de homicidios
intencionales en indicadores y visualizaciones para apoyar decisiones
estratégicas en seguridad ciudadana.

## Problemática

Los registros operativos suelen permanecer dispersos en archivos y reportes
tabulares. Esto dificulta identificar patrones geográficos, temporales y
delictivos, así como priorizar operativos y recursos. SafeAnalytics EC consolida
la información en un dashboard ejecutivo con análisis dinámico.

## Objetivo

Diseñar y desarrollar un Dashboard Ejecutivo interactivo para visualizar y
analizar los principales indicadores relacionados con homicidios intencionales
registrados en Ecuador, mediante analítica descriptiva, diagnóstica, predictiva
y prescriptiva.

## Fuente y alcance

- Dataset: `data/raw/mdi_homicidiosintencionalse_pm_2026_enero_mayo.xlsx`
- Hoja analítica detectada automáticamente: `1. Homicidios Intencionales`
- Cobertura: Ecuador, enero a mayo de 2026
- Naturaleza: archivo histórico estático

## Tecnologías

- Python 3.11–3.13
- pandas y NumPy para ETL y analítica
- Streamlit para la interfaz
- Plotly para visualizaciones
- openpyxl para lectura de Excel
- python-docx para el informe ejecutivo

No se introdujo un stack nuevo: la transformación reutiliza la arquitectura y
las librerías del proyecto original.

## Estructura

| Ruta | Contenido |
|---|---|
| `data/raw/` | Dataset fuente |
| `data/processed/` | Tabla analítica y reporte de calidad |
| `src/etl/transform_load.py` | Carga, limpieza, normalización y transformación |
| `src/analytics/eda.py` | KPIs, tendencia, ranking y recomendaciones |
| `dashboard/` | Dashboard modular Streamlit/Plotly |
| `reports/` | Resumen, tendencia y ranking de riesgo |
| `src/informe/generar_informe.py` | Generador del informe ejecutivo |
| `informe/` | Informe DOCX generado |

## Ejecución

Desde la raíz del proyecto:

```powershell
.\.venv\Scripts\Activate.ps1
python src/etl/transform_load.py
python src/analytics/eda.py
python src/informe/generar_informe.py
streamlit run dashboard/app.py
```

El dashboard estará disponible en `http://localhost:8501`.

## Analítica aplicada

- **Descriptiva:** totales y distribuciones por provincia, cantón, mes, sexo,
  arma, horario y lugar.
- **Diagnóstica:** concentración territorial, horarios críticos, motivaciones,
  perfil predominante y relaciones entre ubicación, arma y horario.
- **Predictiva:** tendencia lineal simple para el periodo siguiente.
- **Prescriptiva:** ranking de riesgo por cantón y recomendaciones automáticas
  para priorización de recursos.

El score de riesgo es:

```text
total_casos + casos_arma_fuego × 0.7 + casos_noche_madrugada × 0.4
```

## Limitaciones

El dataset cubre solo cinco meses y no incluye denominadores poblacionales,
subregistro, estacionalidad anual ni resultados de intervenciones. La proyección
es referencial y académica; no constituye un modelo criminológico profesional.
El sistema se actualiza mediante el reemplazo y procesamiento periódico del dataset.
