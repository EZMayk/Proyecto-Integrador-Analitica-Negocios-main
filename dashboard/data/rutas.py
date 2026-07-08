"""Rutas relativas del proyecto SafeAnalytics EC."""

from pathlib import Path

RUTA_PROYECTO = Path(__file__).resolve().parents[2]
RUTA_RAW = RUTA_PROYECTO / "data" / "raw"
RUTA_PROCESSED = RUTA_PROYECTO / "data" / "processed"
RUTA_REPORTES = RUTA_PROYECTO / "reports"
