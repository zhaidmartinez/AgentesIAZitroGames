-- Crear base de datos generic_lake en AWS Athena
CREATE DATABASE IF NOT EXISTS generic_lake;

-- Usar la base de datos
USE generic_lake;

-- Eliminar tabla si existe (para recrear con nueva estructura)
DROP TABLE IF EXISTS zitro_games_data;

-- Crear tabla zitro_games_data SIN partition projection (ESTABLE)
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
LOCATION 's3://xami-power-ups-tmp-data-athena/zitro-games/zitro_games_data/';

-- Descubrir particiones manualmente
MSCK REPAIR TABLE zitro_games_data;

-- Verificar que la tabla se creó correctamente
DESCRIBE zitro_games_data;

-- Consultas de ejemplo (ahora más flexibles)

-- Consulta anual completa (ahora permitida)
SELECT 
    estado,
    COUNT(*) as total_registros,
    SUM(coin_in) as total_coin_in,
    AVG(coin_in/maquinas_dia) as coin_in_pud
FROM zitro_games_data 
WHERE year = 2023
GROUP BY estado
ORDER BY total_coin_in DESC;

-- Consulta con casino específico (ahora estable)
SELECT 
    month,
    tipo_maquina,
    ROUND(SUM(coin_in) / SUM(maquinas_dia), 2) AS coin_in_pud,
    ROUND(SUM(partidas) / SUM(maquinas_dia), 2) AS games_pud
FROM zitro_games_data
WHERE UPPER(casino) = 'CASINO KINGS' AND year = 2023
GROUP BY month, tipo_maquina
ORDER BY month, tipo_maquina;