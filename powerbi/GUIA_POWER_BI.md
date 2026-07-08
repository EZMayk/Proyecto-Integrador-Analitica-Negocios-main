# Guía de Power BI — SafeAnalytics EC

Power BI es una salida opcional y utiliza la misma tabla generada por el ETL:
`data/processed/homicidios_procesados.csv`.

## Importación

1. Abrir Power BI Desktop.
2. Seleccionar **Obtener datos → Texto/CSV**.
3. Importar `homicidios_procesados.csv` con codificación UTF-8.
4. Confirmar los tipos: fecha para `fecha_infraccion`, decimal para `hora`,
   `latitud` y `longitud`, entero para `edad`, `mes`, `dia` y `total`.

## Medidas DAX

```DAX
Total Homicidios = SUM ( homicidios_procesados[total] )

Casos Arma de Fuego =
CALCULATE (
    [Total Homicidios],
    CONTAINSSTRING ( homicidios_procesados[arma], "FUEGO" )
        || CONTAINSSTRING ( homicidios_procesados[tipo_arma], "FUEGO" )
)

Porcentaje Arma de Fuego =
DIVIDE ( [Casos Arma de Fuego], [Total Homicidios], 0 )
```

## Páginas recomendadas

1. **Resumen ejecutivo:** KPIs, tendencia mensual y distribución provincial.
2. **Diagnóstico territorial:** cantones, franjas horarias, armas y mapa.
3. **Priorización:** importar `reports/ranking_riesgo_cantones.csv` y mostrar
   el score, sus componentes y los cantones prioritarios.

Usar segmentadores para provincia, cantón, arma, sexo, mes y franja horaria.
La proyección debe presentarse como referencial y académica.
