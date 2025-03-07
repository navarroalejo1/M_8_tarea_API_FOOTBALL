"""
Módulo para cargar datos desde SQLite.
"""

import pandas as pd
import sqlite3

DB_PATH = "data/database.db"

def load_data():
    """Carga los datos de la base de datos SQLite."""
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM jugadores", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"❌ Error cargando datos: {e}")
        return pd.DataFrame()
