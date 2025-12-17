-- PASO 2: Crear tabla CON particionamiento (usar después del diagnóstico)
USE generic_lake;

-- Eliminar tabla sin particiones
DROP TABLE IF EXISTS zitro_games_data;

-- Crear tabla CON particionamiento
CREATE EXTERNAL TABLE zitro_games_data (
    casino string,
    ciudad string,
    estado string,
    fecha date,
    juego string,
    kam string,
    licencia string,
    mueble string,
    operador string,
    region_comercial string,
    tipo_maquina string,
    tipo_operacion string,
    coin_in double,
    coin_out double,
    maquinas_dia bigint,
    partidas bigint
)
PARTITIONED BY (
    year int,
    month int
)
STORED AS PARQUET
LOCATION 's3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/'
TBLPROPERTIES (
    'projection.enabled' = 'true',
    'projection.year.type' = 'integer',
    'projection.year.range' = '2020,2030',
    'projection.month.type' = 'integer', 
    'projection.month.range' = '1,12',
    'projection.month.digits' = '1',
    'storage.location.template' = 's3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/year=${year}/month=${month}/'
);

-- Consulta optimizada CON particionamiento
SELECT 
    estado,
    COUNT(*) as total_registros,
    SUM(coin_in) as total_coin_in,
    AVG(coin_in/maquinas_dia) as coin_in_pud
FROM zitro_games_data 
WHERE year = 2023 AND month = 4  -- Solo lee carpeta month=4
GROUP BY estado
ORDER BY total_coin_in DESC;