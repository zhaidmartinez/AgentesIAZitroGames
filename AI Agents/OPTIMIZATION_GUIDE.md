# Guía de Optimización de Agentes Zitro Games

## 🎯 Objetivo: Reducir tiempo de respuesta de 60-90s a 15-30s

---

## 1. OPTIMIZACIONES DE ATHENA (Impacto: 70%)

### A. Sugerir particiones inteligentemente
```yaml
# En Zitro-Games-Analyst.yml
optimization_hints:
  - "Sugerir filtros year/month cuando sea beneficioso"
  - "Detectar consultas lentas y recomendar particiones"
  - "Informar al usuario sobre optimizaciones disponibles"
```

### B. Implementar caché de consultas frecuentes
```yaml
# Agregar en variables
cache_enabled: true
cache_ttl_minutes: 15
common_queries_cache: ["kpis_diarios", "ranking_casinos", "rtp_promedio"]
```

### C. Consultas pre-agregadas
```sql
-- Crear vista materializada en Athena
CREATE VIEW zitro_games_monthly_kpis AS
SELECT 
  year, month, casino, estado,
  SUM(coin_in) / SUM(maquinas_dia) as coin_in_pud,
  SUM(coin_in - coin_out) / SUM(maquinas_dia) as win_pud,
  SUM(coin_out) / SUM(coin_in) * 100 as rtp
FROM zitro_games_data
GROUP BY year, month, casino, estado;
```

---

## 2. OPTIMIZACIONES DE FLUJOS (Impacto: 20%)

### A. Reducir pasos en flujos
```yaml
# ANTES (8 pasos)
steps: [
  "Consultar diccionario",
  "Identificar filtros",
  "Validar SQL",
  "Consultar Athena",
  "Calcular KPIs",
  "Colaborar Visualization",
  "Presentar insights",
  "Proponer alternativas"
]

# DESPUÉS (4 pasos)
steps: [
  "Validar y consultar (paralelo)",
  "Calcular KPIs",
  "Generar respuesta",
  "Sugerir visualización (opcional)"
]
```

### B. Caché de diccionario de datos
```yaml
# En Zitro-Games-Analyst.yml
variables:
  cache_knowledge_base: true
  cache_duration_minutes: 60
  validate_on_first_query_only: true
```

---

## 3. PARALELIZACIÓN (Impacto: 15%)

### A. Consultas independientes en paralelo
```yaml
# En Zitro-Games-Host.yml
sequential_routing: false  # Para consultas simples
parallel_execution_rules:
  - when: "single_casino_single_month"
    parallel: true
  - when: "multiple_casinos_comparison"
    parallel: true
  - when: "complex_aggregations"
    parallel: false  # Mantener secuencial
```

### B. Pre-cargar datos comunes
```yaml
preload_on_session_start:
  - "lista_casinos"
  - "lista_juegos"
  - "rangos_fecha_disponibles"
```

---

## 4. OPTIMIZACIONES DE RESPUESTA (Impacto: 10%)

### A. Respuestas más concisas
```yaml
# En todos los agentes
max_words: 150  # Reducido de 200-300
response_structure: [
  "KPIs clave (solo números)",
  "Insight principal (1 frase)",
  "Acción sugerida (1 frase)"
]
```

### B. Streaming de respuestas
```yaml
streaming_enabled: true
stream_partial_results: true
show_progress_indicators: true
```

---

## 5. OPTIMIZACIONES DE INFRAESTRUCTURA

### A. Athena Query Result Location
```
s3://xami-power-ups-tmp-data-athena/query-results/
```
- Habilitar caché de resultados de Athena (24 horas)

### B. Índices en S3
```bash
# Crear índices Parquet
aws s3api put-object-tagging \
  --bucket xami-power-ups-tmp-data-athena \
  --key zitro-games/zitro_games_data/ \
  --tagging 'TagSet=[{Key=indexed,Value=true}]'
```

### C. Compresión Parquet
```python
# En scripts de generación
df.to_parquet(
    out_file, 
    compression='snappy',  # Más rápido que gzip
    index=False
)
```

---

## 6. MÉTRICAS DE ÉXITO

### Antes de optimización:
- Consulta simple: 60s
- Consulta con visualización: 90s
- Análisis completo: 120s

### Después de optimización (objetivo):
- Consulta simple: 15s (75% mejora)
- Consulta con visualización: 30s (67% mejora)
- Análisis completo: 45s (62% mejora)

---

## 7. IMPLEMENTACIÓN POR FASES

### Fase 1 (Impacto inmediato - 1 día):
- ✅ Reducir max_words a 150
- ✅ Caché de diccionario de datos
- ✅ Simplificar flujos (8 → 4 pasos)
- ✅ Sugerir particiones inteligentemente

### Fase 2 (Impacto medio - 3 días):
- ⏳ Implementar caché de consultas
- ⏳ Crear vistas pre-agregadas
- ⏳ Reducir pasos en flujos

### Fase 3 (Impacto alto - 1 semana):
- ⏳ Paralelización selectiva
- ⏳ Streaming de respuestas
- ⏳ Índices en S3

---

## 8. MONITOREO

```yaml
# Agregar en monitoring
performance_targets:
  p50_response_time: "< 20s"
  p95_response_time: "< 45s"
  p99_response_time: "< 60s"
  cache_hit_rate: "> 40%"
  athena_query_time: "< 10s"
```
