import streamlit as st
import pandas as pd
from data_loader import load_data
import matplotlib.pyplot as plt

# Cargar datos
df = load_data()

def show():
    st.image("assets/logo_betplay.png", width=200)
    st.title("Jugadores de la Copa BetPlay 2024")
    
    # Filtros en la barra lateral
    equipo = st.sidebar.selectbox("Selecciona el equipo", df["nombre_equipo"].unique())
    liga = st.sidebar.selectbox("Selecciona la liga", df["nombre_liga"].unique())
    
    # Filtrar datos
    jugadores_filtrados = df[(df["nombre_equipo"] == equipo) & (df["nombre_liga"] == liga)]
    
    # Verificar que hay datos después del filtrado
    if jugadores_filtrados.empty:
        st.error("No se encontraron jugadores con los filtros seleccionados.")
        return
    
    # Eliminar posibles columnas duplicadas antes de mostrar la tabla
    jugadores_filtrados = jugadores_filtrados.loc[:, ~jugadores_filtrados.columns.duplicated()]
    
    # Mostrar tabla de jugadores
    st.subheader("Lista de Jugadores")
    st.dataframe(jugadores_filtrados[["nombre", "posicion", "nombre_equipo", "nombre_liga", "partidos_titular", "minutos_jugados", "tarjetas_amarillas", "tarjetas_rojas"]])
    
    # Verificar si existen las columnas necesarias para gráficos
    required_columns = ["goles_total", "asistencias"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"Las siguientes columnas no están en los datos: {', '.join(missing_columns)}")
        return
    
    # Gráfico de barras de goles vs asistencias
    st.subheader("Comparación de Goles y Asistencias por Jugador")
    fig, ax = plt.subplots()
    jugadores_filtrados.plot(kind="bar", x="nombre", y=["goles_total", "asistencias"], ax=ax)
    ax.set_ylabel("Cantidad")
    ax.set_title("Goles y Asistencias por Jugador")
    st.pyplot(fig)
