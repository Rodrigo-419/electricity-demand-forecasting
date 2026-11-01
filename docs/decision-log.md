# Registro de decisiones

## Fase 0: fuente de datos
- Fuente: EIA API v2, ruta electricity/rto/region-data, región ERCO (Texas), tipo D (demanda), frecuencia horaria.
- Datos descargados: año 2025, 8760 filas, sin duplicados, nulos ni horas faltantes (src/explore_demand.py).
- Zona horaria: `period` está en UTC (perfil horario y documentación de la EIA).
- Pendiente: confirmar con la documentación vigente de la API v2; saber si la hora es de inicio o de fin; términos de reutilización; límites de la API; historial más largo; retrasos de publicación; pronóstico del operador.

## Fase 1: definición del pronóstico (borrador)
- Tarea: al terminar el día D (último dato conocido: hora 23 UTC), predecir las 24 horas del día D+1.
- Métricas: MAE (MWh) y WAPE (%).
- Regla anti-fuga: ninguna variable puede usar datos posteriores al origen del pronóstico.

## Baselines 2025 (24 horas, misma hora)
- Naive diario (hace 24 h): MAE 2496 MWh, WAPE 4.47 %. Es el número a vencer.
- Naive semanal (hace 168 h): MAE 4754 MWh, WAPE 8.52 %.
- Naive mixto (semanal en lunes, sábado y domingo): MAE 3290 MWh, WAPE 5.89 %. Hipótesis descartada.

## Preguntas abiertas
- El semanal falla mucho en invierno (enero: 12 142 MWh de error medio). ¿Es el clima? No se puede comprobar sin temperatura.
- Un solo año y una sola región: repetir calidad de datos y baselines con más historial.