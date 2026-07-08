"""Acceso cacheado a datos y artefactos analíticos."""

from dashboard.data.cargar_datos import cargar_datos, cargar_ranking
from dashboard.data.cargar_reporte_calidad import cargar_reporte_calidad
from dashboard.data.rutas import RUTA_PROCESSED, RUTA_PROYECTO, RUTA_RAW, RUTA_REPORTES

__all__ = [
    "RUTA_PROCESSED", "RUTA_PROYECTO", "RUTA_RAW", "RUTA_REPORTES",
    "cargar_datos", "cargar_ranking", "cargar_reporte_calidad",
]
