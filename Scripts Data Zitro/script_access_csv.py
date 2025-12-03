import os
import pyodbc
import pandas as pd

# Carpeta donde tienes los archivos .accdb
ACCESS_FOLDER = r"C:\Users\zhaid\Downloads\PoC\DATA IA Access"

# Tabla que quieres exportar desde cada archivo Access
TABLE_NAME = "DATOS"   # <-- cámbiala por tu tabla

# Tipo de salida: csv o parquet
OUTPUT_FORMAT = "csv"  # también puede ser "parquet"

# Carpeta de salida
OUTPUT_FOLDER = r"C:\Users\zhaid\Downloads\PoC\DATA IA CSV"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Mapeo de nombres de columnas (opcional)
# Formato: {"nombre_original": "nombre_nuevo"}
COLUMN_MAPPING = {
    "Casino": "casino",
    "Ciudad": "ciudad",
    "Estado": "estado",
    "Fecha": "fecha",
    "Juego": "juego",
    "KAM": "kam",
    "Licencia": "licencia",
    "Mueble": "mueble",
    "Operador": "operador",
    "Region Comercial": "region_comercial",
    "Tipo de Maquina ": "tipo_maquina",
    "Tipo de Maquina": "tipo_maquina",
    "Tipo de operacion": "tipo_operacion",
    "_COIN IN (AGR)": "coin_in",
    "_COIN OUT (AGR)": "coin_out",
    "_Nº MACH DAY (AGR)": "maquinas_dia",
    "Partidas (SUMA)": "partidas"
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
    
    # Renombrar columnas si hay mapeo definido
    if COLUMN_MAPPING:
        df = df.rename(columns=COLUMN_MAPPING)
    
    # Convertir columna fecha a tipo date
    if 'fecha' in df.columns:
        df['fecha'] = pd.to_datetime(df['fecha']).dt.date

    # Nombre del archivo de salida
    out_file = os.path.join(
        OUTPUT_FOLDER,
        f"{month_tag}.{OUTPUT_FORMAT}"
    )

    # Guardar CSV
    if OUTPUT_FORMAT == "csv":
        df.to_csv(out_file, index=False, encoding="utf-8-sig")
        print(f"[OK] Archivo generado: {out_file}")

    # Guardar Parquet
    elif OUTPUT_FORMAT == "parquet":
        df.to_parquet(out_file, index=False)
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
