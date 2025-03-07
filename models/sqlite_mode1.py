import sqlite3
import pandas as pd

DB_PATH = "data/database.db"

def get_all_players():
    """Obtiene todos los jugadores desde la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM jugadores"
    df = pd.read_sql(query, conn)
    conn.close()
    return df
