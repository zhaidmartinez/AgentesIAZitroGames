-- Crear base de datos generic_lake en AWS Athena
CREATE DATABASE IF NOT EXISTS generic_lake;

-- Usar la base de datos
USE generic_lake;

-- Eliminar tabla si existe (para recrear con nueva estructura)
DROP TABLE IF EXISTS zitro_games_data;

-- Crear tabla zitro_games_data particionada
CREATE EXTERNAL TABLE IF NOT EXISTS zitro_games_data (
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
    'projection.month.digits' = '2',
    'storage.location.template' = 's3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/year=${year}/month=${month}/'
);

-- Reparar particiones (si es necesario)
MSCK REPAIR TABLE zitro_games_data;

-- Consulta de ejemplo
SELECT 
    estado,
    COUNT(*) as total_registros,
    SUM(coin_in) as total_coin_in,
    AVG(coin_in/maquinas_dia) as coin_in_pud
FROM zitro_games_data 
WHERE year = 2023 AND month = 1
GROUP BY estado
ORDER BY total_coin_in DESC;