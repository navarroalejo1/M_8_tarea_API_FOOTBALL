import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from controllers.data_loader import load_data

df = load_data()

def show():
    """Muestra el análisis de jugadores con su información y estadísticas en Streamlit."""
    st.title("📊 ANÁLISIS DE JUGADORES - LIGA BETPLAY 2024")

    # 🔹 Filtros en el menú lateral
    st.sidebar.markdown("## 📌 Filtros")
    equipos = df["nombre_equipo"].dropna().unique()
    equipo = st.sidebar.selectbox("Selecciona el equipo", equipos)
    posiciones = df[df["nombre_equipo"] == equipo]["posicion"].dropna().unique()
    posicion = st.sidebar.selectbox("Selecciona la posición", posiciones)
    jugadores = df[(df["nombre_equipo"] == equipo) & (df["posicion"] == posicion)]["nombre"].dropna().unique()
    jugador = st.sidebar.selectbox("Selecciona el jugador", jugadores)
    ligas = df["nombre_liga"].dropna().unique()
    liga = st.sidebar.selectbox("Selecciona la liga", ligas)
    # Filtrar datos del jugador seleccionado
    filtered_df = df[df["nombre"] == jugador]

    if filtered_df.empty:
        st.warning("⚠ No hay datos disponibles después de aplicar los filtros.")
        return

    jugador_data = filtered_df.iloc[0].to_dict()

    # 🔹 Mostrar información del jugador
    st.subheader("📋 DATOS PERSONALES")
    st.image(jugador_data.get("foto", ""), width=150)
    st.write(f"**Nombre:** {jugador_data.get('nombre', 'No disponible')} {jugador_data.get('apellido', 'No disponible')}")
    st.write(f"**Edad:** {jugador_data.get('edad', 0)} años")
    st.write(f"**Fecha de nacimiento:** {jugador_data.get('fecha_nacimiento', 'No disponible')}")
    st.write(f"**Nacionalidad:** {jugador_data.get('nacionalidad', 'No disponible')}")
    st.write(f"**Peso:** {jugador_data.get('peso', 0)} kg")
    st.write(f"**Altura:** {jugador_data.get('altura', 0)} m")
    st.write(f"**Posición:** {jugador_data.get('posicion', 'No disponible')}")

    # 🔹 Mostrar estadísticas del jugador en gráficos
    st.subheader("📊 ESTADÍSTICAS INDIVIDUALES")
    stats = {
        "⚽ Goles": ["goles_pie_izq", "goles_pie_der", "goles_cabeza"],
        "💨 Pases": ["pases_completados", "pases_fallidos"],
        "🛑 Defensa": ["intercepciones", "despejes", "bloqueos"],
        "🔥 Faltas y Tarjetas": ["faltas_cometidas", "tarjetas_amarillas", "tarjetas_rojas"]
    }

    cols = st.columns(2)
    fig_paths = []
    for i, (titulo, columnas) in enumerate(stats.items()):
        with cols[i % 2]:
            st.subheader(titulo)
            if not any(col in filtered_df.columns for col in columnas):
                st.warning(f"⚠ No hay datos suficientes para {titulo}.")
                continue
            
            fig, ax = plt.subplots(figsize=(4, 3))
            valores = [jugador_data.get(col, 0) if jugador_data.get(col) is not None else 0 for col in columnas]
            ax.bar(range(len(columnas)), valores)
            ax.set_xticks(range(len(columnas)))
            ax.set_xticklabels(columnas, rotation=45)
            ax.set_ylabel("Cantidad")
            st.pyplot(fig)
            plt.close(fig)
            
            fig_path = f"temp_{titulo}.png".replace(" ", "_")
            fig.savefig(fig_path)
            fig_paths.append(fig_path)

    # 🔹 Botón para exportar datos a PDF
    if st.button("📄 Exportar a PDF"):
        exportar_pdf(jugador_data, fig_paths)

def exportar_pdf(jugador_data, fig_paths):
    """Exporta la información del jugador y sus gráficos a un archivo PDF."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)

    pdf.image("assets/logo_betplay.png", x=150, y=20, w=50)
    pdf.cell(200, 10, f"Reporte de {jugador_data.get('nombre', 'No disponible')}", ln=True, align='C')
    pdf.ln(10)

    # Datos personales
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "DATOS PERSONALES", ln=True, align='L')
    pdf.ln(5)
    pdf.set_font("Arial", size=11)
    pdf.cell(200, 10, f"Nombre: {jugador_data.get('nombre', 'No disponible')} {jugador_data.get('apellido', 'No disponible')}", ln=True)
    pdf.cell(200, 10, f"Edad: {jugador_data.get('edad', 0)} años", ln=True)
    pdf.cell(200, 10, f"Fecha de nacimiento: {jugador_data.get('fecha_nacimiento', 'No disponible')}", ln=True)
    pdf.cell(200, 10, f"Nacionalidad: {jugador_data.get('nacionalidad', 'No disponible')}", ln=True)
    pdf.cell(200, 10, f"Peso: {jugador_data.get('peso', 0)} kg", ln=True)
    pdf.cell(200, 10, f"Altura: {jugador_data.get('altura', 0)} m", ln=True)
    pdf.cell(200, 10, f"Posición: {jugador_data.get('posicion', 'No disponible')}", ln=True)
    pdf.ln(10)

    for fig_path in fig_paths:
        if os.path.exists(fig_path):
            pdf.image(fig_path, x=10, w=180)
            pdf.ln(10)

    pdf_filename = f"Reporte_{jugador_data.get('nombre', 'Jugador')}.pdf".replace(" ", "_")
    pdf.output(pdf_filename)
    st.success(f"Archivo exportado: {pdf_filename}")
    
    for fig_path in fig_paths:
        if os.path.exists(fig_path):
            os.remove(fig_path)
