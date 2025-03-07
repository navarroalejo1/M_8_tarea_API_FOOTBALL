import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from controllers.data_loader import load_data

df = load_data()

def show():
    """Muestra el análisis de equipos con su logo, estadísticas y exportación de datos."""
    st.title("📊 ANÁLISIS DE EQUIPOS - LIGA BETPLAY 2024")

    # 🔹 Filtros en el menú lateral
    st.sidebar.markdown("## 📌 Filtros")
    equipos = df["nombre_equipo"].dropna().unique()
    equipo = st.sidebar.selectbox("Selecciona el equipo", equipos)

    # Filtrar datos del equipo seleccionado
    filtered_df = df[df["nombre_equipo"] == equipo]

    if filtered_df.empty:
        st.warning("⚠ No hay datos disponibles después de aplicar los filtros.")
        return

    equipo_data = filtered_df.iloc[0].to_dict()
    
    # 🔹 Mostrar logo y nombre del equipo en la parte superior derecha
    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("📌 INFORMACIÓN DEL EQUIPO")
        st.write(f"**NOMBRE DEL EQUIPO:** {equipo_data.get('nombre_equipo', 'NO DISPONIBLE').upper()}")
        st.write(f"**LIGA:** {equipo_data.get('nombre_liga', 'NO DISPONIBLE')}")
    
    with col2:
        logo_path = equipo_data.get("escudo", None)
        if logo_path and isinstance(logo_path, str):
            st.image(logo_path, width=120)

    # 🔹 Mostrar datos personales en una tabla antes de los gráficos
    st.subheader("📋 DATOS PERSONALES")
    columnas_requeridas = ["posicion", "nombre", "apellido", "edad", "fecha_nacimiento", "nacionalidad", "peso", "altura"]
    columnas_existentes = [col for col in columnas_requeridas if col in filtered_df.columns]

    if columnas_existentes:
        personal_info = filtered_df[columnas_existentes]
        st.dataframe(personal_info)
    else:
        st.warning("⚠ No hay suficientes datos personales disponibles para este equipo.")

    # 🔹 Estadísticas del equipo
    st.subheader("📊 ESTADÍSTICAS DEL EQUIPO")
    stats = {
        "⚽ GOLES DEL EQUIPO": ["goles_total"],
        "🛑 DEFENSAS": ["intercepciones", "despejes", "bloqueos"],
        "🔥 TARJETAS": ["tarjetas_amarillas", "tarjetas_rojas"],
        " FALTAS": ["faltas_cometidas", "faltas_recibidas"],
        "🏆 PENALES": ["penales_anotados", "penales_fallados"],
    }

    cols = st.columns(2)
    fig_paths = []
    for i, (titulo, columnas) in enumerate(stats.items()):
        columnas_existentes = [col for col in columnas if col in filtered_df.columns]
        if not columnas_existentes:
            st.warning(f"⚠ No hay datos suficientes para {titulo}.")
            continue

        with cols[i % 2]:
            st.subheader(titulo)
            fig, ax = plt.subplots(figsize=(4, 3))
            valores = [filtered_df[col].fillna(0).sum() for col in columnas_existentes]
            ax.bar(columnas_existentes, valores)
            ax.set_ylabel("Cantidad")
            ax.set_xticklabels(columnas_existentes, rotation=45)
            st.pyplot(fig)
            
            fig_path = f"temp_{titulo}.png".replace(" ", "_")
            fig.savefig(fig_path)
            fig_paths.append(fig_path)
    
    # 🔹 Exportación de datos y gráficos a PDF
    if st.button("📄 Exportar a PDF"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)

        pdf.image("assets/logo_betplay.png", x=130, y=10, w=50)
        pdf.cell(200, 10, "ANÁLISIS COPA BETPLAY 2024", ln=True, align='C')
        pdf.ln(20)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "DATOS DEL EQUIPO", ln=True, align='L')
        pdf.ln(5)
        pdf.set_font("Arial", size=11)

        for col in columnas_existentes:
            pdf.cell(200, 10, f"{col.upper()}: {filtered_df[col].values[0]}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "ESTADÍSTICAS DEL EQUIPO", ln=True, align='L')
        pdf.ln(5)

        for fig_path in fig_paths:
            if os.path.exists(fig_path):
                pdf.image(fig_path, x=10, w=180)
                pdf.ln(10)

        pdf_filename = f"{equipo_data.get('nombre_equipo', 'EQUIPO').replace(' ', '_')}_{equipo_data.get('nombre_liga', 'LIGA').replace(' ', '_')}.pdf"
        pdf.output(pdf_filename)
        st.success(f"Archivo exportado: {pdf_filename}")

        for fig_path in fig_paths:
            if os.path.exists(fig_path):
                os.remove(fig_path)
