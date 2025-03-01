import pandas as pd
import streamlit as st
import os

# Ruta del archivo CSV en la carpeta "data"
DATA_PATH = os.path.join("data", "estadisticas_jugadores_2023.csv")

@st.cache_data
def load_data():
    """Carga los datos desde un archivo CSV y normaliza los nombres de las columnas."""
    try:
        df = pd.read_csv(DATA_PATH)

        # Verificar si el archivo CSV tiene datos
        if df.empty:
            st.error("El archivo CSV está vacío o no se cargó correctamente.")
            return pd.DataFrame()

        # Normalizar nombres de columnas
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Mostrar las columnas disponibles en el DataFrame para depuración
        st.write("Columnas disponibles en el DataFrame:", df.columns.tolist())

        return df
    except FileNotFoundError:
        st.error(f"No se encontró el archivo: {DATA_PATH}")
        return pd.DataFrame()
