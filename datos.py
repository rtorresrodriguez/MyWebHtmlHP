import sqlite3
import pandas as pd

# Conectar a SQLite
conn = sqlite3.connect("test.db")

# Cargar datos en un DataFrame
df = pd.read_sql_query("SELECT * FROM usuarios", conn)

# Mostrar la tabla en formato bonito
print(df)

# Cerrar la conexión
conn.close()