# Configuración AWS Athena para Zitro Games

## Pasos para crear la base de datos y tabla en Athena:

### 1. **Subir archivos Parquet a S3**
```bash
# Subir los archivos particionados generados por script_access_parquet_particionado.py
aws s3 sync "C:\Users\zhaid\Downloads\PoC\DATA IA Parquet\" s3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/ --recursive
```

### 2. **Ejecutar SQL en AWS Athena Console**
- Abrir AWS Athena Console
- Ejecutar el contenido de `create_athena_table.sql`
- Bucket configurado: `s3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/`

### 3. **Estructura esperada en S3:**
```
s3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/
├── year=2023/
│   ├── month=01/
│   │   └── 202301.parquet
│   ├── month=02/
│   │   └── 202302.parquet
│   └── month=12/
│       └── 202312.parquet
```

### 4. **Consultas de ejemplo:**
```sql
-- KPIs básicos por estado
SELECT 
    estado,
    SUM(coin_in) / SUM(maquinas_dia) as coin_in_pud,
    SUM(coin_in - coin_out) / SUM(maquinas_dia) as win_pud,
    SUM(coin_out) / SUM(coin_in) * 100 as rtp
FROM generic_lake.zitro_games_data 
WHERE year = 2023 AND month = 1
GROUP BY estado;

-- Análisis por casino
SELECT 
    casino,
    COUNT(DISTINCT licencia) as n_mach,
    SUM(partidas) / SUM(maquinas_dia) as games_pud
FROM generic_lake.zitro_games_data 
WHERE year = 2023
GROUP BY casino
ORDER BY n_mach DESC;
```

### 5. **Configuración para Agentes IA:**
- Base de datos: `generic_lake`
- Tabla: `zitro_games_data`
- Particiones: `year`, `month`
- Ubicación: S3 con estructura Hive

### 6. **Ventajas del particionado:**
- Consultas más rápidas por año/mes
- Menor costo en Athena (solo escanea particiones necesarias)
- Compatible con herramientas de BI
- Escalable para años futuros