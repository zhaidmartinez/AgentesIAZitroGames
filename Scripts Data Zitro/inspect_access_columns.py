import os
import pyodbc
import pandas as pd

# Carpeta donde tienes los archivos .accdb
ACCESS_FOLDER = r"C:\Users\zhaid\Downloads\PoC\DATA IA Access"
TABLE_NAME = "DATOS"

def inspect_access_columns(access_file, month_tag):
    """Inspecciona las columnas de un archivo Access sin procesar datos"""
    try:
        # Conexión al archivo Access
        conn_str = (
            r"Driver={Microsoft Access Driver (*.mdb, *.accdb)};"
            f"DBQ={access_file};"
        )
        
        conn = pyodbc.connect(conn_str)
        
        # Leer solo la primera fila para obtener columnas
        query = f"SELECT TOP 1 * FROM {TABLE_NAME}"
        df = pd.read_sql(query, conn)
        
        print(f"\n=== {month_tag} ===")
        print(f"Archivo: {access_file}")
        print(f"Columnas ({len(df.columns)}):")
        for i, col in enumerate(df.columns, 1):
            print(f"  {i:2d}. '{col}'")
        
        conn.close()
        return list(df.columns)
        
    except Exception as e:
        print(f"[ERROR] {month_tag}: {e}")
        return []

def main():
    """Inspecciona todas las bases de datos Access"""
    all_columns = {}
    
    print("🔍 INSPECCIONANDO COLUMNAS EN ARCHIVOS ACCESS")
    print("=" * 50)
    
    # Iterar todos los archivos de 2023
    for year in [2023]:
        for month in range(1, 13):
            tag = f"{year}{month:02d}"
            file_path = os.path.join(ACCESS_FOLDER, f"{tag}.mdb")
            
            if not os.path.exists(file_path):
                print(f"[SKIP] No existe: {tag}.mdb")
                continue
            
            columns = inspect_access_columns(file_path, tag)
            if columns:
                all_columns[tag] = columns
    
    # Análisis de diferencias
    print("\n" + "=" * 50)
    print("📊 ANÁLISIS DE DIFERENCIAS")
    print("=" * 50)
    
    if all_columns:
        # Obtener todas las columnas únicas
        unique_columns = set()
        for cols in all_columns.values():
            unique_columns.update(cols)
        
        print(f"\n🔢 TOTAL COLUMNAS ÚNICAS ENCONTRADAS: {len(unique_columns)}")
        print("\nTodas las variaciones de nombres:")
        for i, col in enumerate(sorted(unique_columns), 1):
            print(f"  {i:2d}. '{col}'")
        
        # Detectar inconsistencias
        print(f"\n⚠️  INCONSISTENCIAS POR MES:")
        base_columns = list(all_columns.values())[0]  # Primer mes como referencia
        
        for month_tag, columns in all_columns.items():
            if columns != base_columns:
                print(f"\n{month_tag} - DIFERENTE:")
                # Columnas que faltan
                missing = set(base_columns) - set(columns)
                if missing:
                    print(f"  ❌ Faltan: {missing}")
                
                # Columnas extra
                extra = set(columns) - set(base_columns)
                if extra:
                    print(f"  ➕ Extra: {extra}")
            else:
                print(f"{month_tag} - ✅ Igual al primer mes")

if __name__ == "__main__":
    main()