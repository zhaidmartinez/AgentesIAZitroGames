import pandas as pd

df = pd.read_parquet("C:/Users/zhaid/Downloads/PoC/202301.parquet")
print(df.head())     # muestra las primeras filas
print(df.info())     # muestra columnas y tipos de dato