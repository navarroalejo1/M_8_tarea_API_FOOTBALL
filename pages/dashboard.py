import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_data
from fpdf import FPDF
import requests
from PIL import Image
import io
import tempfile

# Cargar datos
df = load_data()

def export_to_pdf(filtered_df):
    with tempfile.TemporaryDirectory() as temp_dir:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        # Agregar logo
        logo_path = "assets/logo_betplay.png"
        try:
            pdf.image(logo_path, x=80, y=10, w=50)
        except Exception as e:
            pdf.cell(200, 10, "No se pudo cargar el logo", ln=True)
        pdf.ln(30)
        
        pdf.cell(200, 10, "Análisis Copa BetPlay 2023", ln=True, align='C')
        pdf.ln(10)
        
        pdf.cell(200, 10, "Datos Personales", ln=True, align='L')
        pdf.ln(5)
        pdf.cell(200, 10, f"Nombre: {filtered_df['nombre'].values[0]} {filtered_df['apellido'].values[0]}", ln=True)
        pdf.cell(200, 10, f"Edad: {filtered_df['edad'].values[0]}", ln=True)
        pdf.cell(200, 10, f"Fecha de nacimiento: {filtered_df['fecha_nacimiento'].values[0]}", ln=True)
        pdf.cell(200, 10, f"Nacionalidad: {filtered_df['nacionalidad'].values[0]}", ln=True)
        pdf.cell(200, 10, f"Peso: {filtered_df['peso'].values[0]} kg", ln=True)
        pdf.cell(200, 10, f"Altura: {filtered_df['altura'].values[0]} m", ln=True)
        pdf.ln(10)
        
        pdf.cell(200, 10, "Información del Equipo", ln=True, align='L')
        pdf.ln(5)
        pdf.cell(200, 10, f"Equipo: {filtered_df['nombre_equipo'].values[0]}", ln=True)
        pdf.cell(200, 10, f"Liga: {filtered_df['nombre_liga'].values[0]}", ln=True)
        pdf.ln(10)
        
        # Descarga y añade la foto del jugador
        try:
            response = requests.get(filtered_df["foto"].values[0])
            if response.status_code == 200:
                img = Image.open(io.BytesIO(response.content))
                img_path = f"{temp_dir}/temp_foto.jpg"
                img.save(img_path)
                pdf.image(img_path, x=10, y=pdf.get_y(), w=50)
        except Exception as e:
            pdf.cell(200, 10, "No se pudo cargar la foto", ln=True)
        
        pdf.ln(20)
        
        # Guardar y agregar gráficos al PDF sin sobreponerlos
        pdf.add_page()
        pdf.cell(200, 10, "Comparación de Tiros Totales y Tiros al Arco", ln=True, align='C')
        pdf.ln(10)
        
        fig, ax = plt.subplots()
        ax.plot(filtered_df.index, filtered_df["tiros_total"], label="Tiros Totales", marker="o")
        ax.plot(filtered_df.index, filtered_df["tiros_al_arco"], label="Tiros al Arco", marker="s")
        ax.set_xlabel("Índice del Jugador")
        ax.set_ylabel("Cantidad de Tiros")
        ax.legend()
        ax.grid(True)
        tiros_img_path = f"{temp_dir}/tiros_grafico.png"
        fig.savefig(tiros_img_path)
        pdf.image(tiros_img_path, x=10, y=pdf.get_y(), w=150)
        
        pdf.add_page()
        pdf.cell(200, 10, "Comparación de Duelos Totales y Duelos Ganados", ln=True, align='C')
        pdf.ln(10)
        
        fig, ax = plt.subplots()
        ax.plot(filtered_df.index, filtered_df["duelos_total"], label="Duelos Totales", marker="o")
        ax.plot(filtered_df.index, filtered_df["duelos_ganados"], label="Duelos Ganados", marker="s")
        ax.set_xlabel("Índice del Jugador")
        ax.set_ylabel("Cantidad de Duelos")
        ax.legend()
        ax.grid(True)
        duelos_img_path = f"{temp_dir}/duelos_grafico.png"
        fig.savefig(duelos_img_path)
        pdf.image(duelos_img_path, x=10, y=pdf.get_y(), w=150)
        
        filename = f"{temp_dir}/{filtered_df['nombre_equipo'].values[0]}_{filtered_df['nombre'].values[0]}.pdf".replace(" ", "_")
        pdf.output(filename)
        return filename

def show():
    st.image("assets/logo_betplay.png", width=200)
    st.title("Análisis Copa BetPlay 2023")
    
    equipo = st.sidebar.selectbox("Selecciona el equipo", df["nombre_equipo"].unique())
    jugadores_disponibles = df[df["nombre_equipo"] == equipo]["nombre"].unique()
    Jugadores = st.sidebar.selectbox("Selecciona el jugador", jugadores_disponibles)
    
    posicion = st.sidebar.selectbox("Selecciona la posición", df["posicion"].unique())
    liga = st.sidebar.selectbox("Selecciona la liga", df["nombre_liga"].unique())
    
    filtered_df = df[(df["nombre"] == Jugadores) & (df["posicion"] == posicion) & (df["nombre_liga"] == liga) & (df["nombre_equipo"] == equipo)]
    
    if filtered_df.empty:
        st.error("No se encontraron jugadores con los filtros seleccionados.")
        return
    
    st.subheader("Datos Personales")
    st.image(filtered_df["foto"].values[0], width=150)
    st.write(f"**Nombre:** {filtered_df['nombre'].values[0]} {filtered_df['apellido'].values[0]}")
    st.write(f"**Edad:** {filtered_df['edad'].values[0]}")
    st.write(f"**Fecha de nacimiento:** {filtered_df['fecha_nacimiento'].values[0]}")
    st.write(f"**Nacionalidad:** {filtered_df['nacionalidad'].values[0]}")
    st.write(f"**Peso:** {filtered_df['peso'].values[0]} kg")
    st.write(f"**Altura:** {filtered_df['altura'].values[0]} m")
    
    if st.button("Exportar a PDF"):
        pdf_filename = export_to_pdf(filtered_df)
        with open(pdf_filename, "rb") as f:
            st.download_button(
                label="Descargar PDF",
                data=f,
                file_name=pdf_filename,
                mime="application/pdf"
            )

