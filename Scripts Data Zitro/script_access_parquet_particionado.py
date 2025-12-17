import os
import pyodbc
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Carpeta donde tienes los archivos .accdb
ACCESS_FOLDER = r"C:\Users\zhaid\Downloads\PoC\DATA IA Access"

# Tabla que quieres exportar desde cada archivo Access
TABLE_NAME = "DATOS"   # <-- cámbiala por tu tabla

# Tipo de salida: csv o parquet
OUTPUT_FORMAT = "parquet"  # también puede ser "parquet"

# Carpeta de salida
OUTPUT_FOLDER = r"C:\Users\zhaid\Downloads\PoC\DATA IA Parquet"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mapeo de nombres de columnas (múltiples variaciones)
COLUMN_MAPPING = {
    # Casino
    "Casino": "casino",
    "CASINO": "casino",
    "casino": "casino",
    
    # Ciudad
    "Ciudad": "ciudad",
    "CIUDAD": "ciudad",
    "ciudad": "ciudad",
    
    # Estado
    "Estado": "estado",
    "ESTADO": "estado",
    "estado": "estado",
    
    # Fecha
    "Fecha": "fecha",
    "FECHA": "fecha",
    "fecha": "fecha",
    "Date": "fecha",
    
    # Juego
    "Juego": "juego",
    "JUEGO": "juego",
    "juego": "juego",
    "Game": "juego",
    
    # KAM
    "KAM": "kam",
    "kam": "kam",
    "Kam": "kam",
    
    # Licencia
    "Licencia": "licencia",
    "LICENCIA": "licencia",
    "licencia": "licencia",
    "License": "licencia",
    
    # Mueble
    "Mueble": "mueble",
    "MUEBLE": "mueble",
    "mueble": "mueble",
    
    # Operador
    "Operador": "operador",
    "OPERADOR": "operador",
    "operador": "operador",
    "Operator": "operador",
    
    # Región Comercial
    "Region Comercial": "region_comercial",
    "REGION COMERCIAL": "region_comercial",
    "region comercial": "region_comercial",
    "Región Comercial": "region_comercial",
    "Commercial Region": "region_comercial",
    
    # Tipo de Máquina
    "Tipo de Maquina ": "tipo_maquina",
    "Tipo de Maquina": "tipo_maquina",
    "TIPO DE MAQUINA": "tipo_maquina",
    "tipo de maquina": "tipo_maquina",
    "Tipo de Máquina": "tipo_maquina",
    "Machine Type": "tipo_maquina",
    
    # Tipo de Operación (variaciones exactas encontradas)
    "Tipo de operacion": "tipo_operacion",
    "Tipo de Operacion": "tipo_operacion", 
    "Tipo de Operación": "tipo_operacion",
    "TIPO DE OPERACION": "tipo_operacion",
    "tipo de operación": "tipo_operacion",
    "Operation Type": "tipo_operacion",
    
    # Coin In (múltiples variaciones)
    "_COIN IN (AGR)": "coin_in",
    "COIN IN (AGR)": "coin_in",
    "_COIN IN": "coin_in",
    "COIN IN": "coin_in",
    "coin in": "coin_in",
    "Coin In": "coin_in",
    "_Coin In (AGR)": "coin_in",
    
    # Coin Out (múltiples variaciones)
    "_COIN OUT (AGR)": "coin_out",
    "COIN OUT (AGR)": "coin_out",
    "_COIN OUT": "coin_out",
    "COIN OUT": "coin_out",
    "coin out": "coin_out",
    "Coin Out": "coin_out",
    "_Coin Out (AGR)": "coin_out",
    
    # Máquinas Día (variaciones exactas encontradas)
    "_Nº MACH DAY (AGR)": "maquinas_dia",
    "Maquinas Dia (AGR)": "maquinas_dia",
    "Nº MACH DAY (AGR)": "maquinas_dia",
    "_N MACH DAY (AGR)": "maquinas_dia",
    "N MACH DAY (AGR)": "maquinas_dia",
    "_MACH DAY": "maquinas_dia",
    "MACH DAY": "maquinas_dia",
    "Machine Day": "maquinas_dia",
    "Machines Day": "maquinas_dia",
    
    # Partidas (múltiples variaciones)
    "Partidas (SUMA)": "partidas",
    "PARTIDAS (SUMA)": "partidas",
    "Partidas": "partidas",
    "PARTIDAS": "partidas",
    "partidas": "partidas",
    "Games": "partidas",
    "GAMES": "partidas",
    "Games (SUM)": "partidas"
}

def export_table_from_access(access_file, table_name, month_tag):
    # Conexión al archivo Access
    conn_str = (
        r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
        f"DBQ={access_file};"
    )

    conn = pyodbc.connect(conn_str)
    
    # Leer tabla completa
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, conn)
    
    # Mostrar columnas originales para diagnóstico
    print(f"[INFO] Columnas originales en {month_tag}: {list(df.columns)}")
    
    # Renombrar columnas si hay mapeo definido
    if COLUMN_MAPPING:
        original_columns = df.columns.tolist()
        df = df.rename(columns=COLUMN_MAPPING)
        
        # Mostrar mapeo aplicado
        mapped_columns = [col for col in original_columns if col in COLUMN_MAPPING]
        if mapped_columns:
            print(f"[INFO] Columnas mapeadas: {mapped_columns}")
        
        # Advertir sobre columnas no mapeadas
        unmapped_columns = [col for col in original_columns if col not in COLUMN_MAPPING]
        if unmapped_columns:
            print(f"[WARN] Columnas NO mapeadas en {month_tag}: {unmapped_columns}")
    
    # Convertir columna fecha y agregar year, month
    if 'fecha' in df.columns:
        fecha_dt = pd.to_datetime(df['fecha'])
        df['fecha'] = fecha_dt.dt.date
        df['year'] = fecha_dt.dt.year
        df['month'] = fecha_dt.dt.month
    
    # Limpiar maquinas_dia: null o 0 → 1
    if 'maquinas_dia' in df.columns:
        df['maquinas_dia'] = df['maquinas_dia'].fillna(1)
        df.loc[df['maquinas_dia'] == 0, 'maquinas_dia'] = 1

    # Crear estructura de carpetas year=YYYY/month=M/ (sin ceros)
    year = month_tag[:4]
    month = str(int(month_tag[4:6]))  # Convierte "01" a "1"
    partition_folder = os.path.join(OUTPUT_FOLDER, f"year={year}", f"month={month}")
    os.makedirs(partition_folder, exist_ok=True)
    
    # Nombre del archivo de salida
    out_file = os.path.join(partition_folder, f"{month_tag}.{OUTPUT_FORMAT}")

    # Guardar CSV
    if OUTPUT_FORMAT == "csv":
        df.to_csv(out_file, index=False, encoding="utf-8-sig")
        print(f"[OK] Archivo generado: {out_file}")

    # Guardar Parquet con esquema PyArrow dinámico
    elif OUTPUT_FORMAT == "parquet":
        # Definir tipos por columna
        column_types = {
            "casino": pa.string(),
            "ciudad": pa.string(),
            "estado": pa.string(),
            "fecha": pa.date32(),
            "year": pa.int32(),
            "month": pa.int32(),
            "juego": pa.string(),
            "kam": pa.string(),
            "licencia": pa.string(),
            "mueble": pa.string(),
            "operador": pa.string(),
            "region_comercial": pa.string(),
            "tipo_maquina": pa.string(),
            "tipo_operacion": pa.string(),
            "coin_in": pa.float64(),
            "coin_out": pa.float64(),
            "maquinas_dia": pa.int64(),
            "partidas": pa.int64(),
        }
        
        # Crear esquema solo con columnas disponibles
        schema_fields = [(col, column_types.get(col, pa.string())) for col in df.columns if col in column_types]
        schema = pa.schema(schema_fields)
        
        # Convertir a PyArrow Table
        table = pa.Table.from_pandas(df[list(dict(schema_fields).keys())], schema=schema)
        pq.write_table(table, out_file)
        print(f"[OK] Archivo generado: {out_file}")

    conn.close()


def main():
    # Iterar 202301 .. 202312
    for year in [2023]:
        for month in range(1, 13):
            tag = f"{year}{month:02d}"
            file_path = os.path.join(ACCESS_FOLDER, f"{tag}.mdb")

            if not os.path.exists(file_path):
                print(f"[WARN] No existe: {file_path}")
                continue

            print(f"Procesando {file_path} ...")
            export_table_from_access(file_path, TABLE_NAME, tag)

    print("\nProceso finalizado.")


if __name__ == "__main__":
    main()
