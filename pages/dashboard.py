import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from data_loader import load_data
from fpdf import FPDF
import requests
from PIL import Image
import io
import tempfile

# 🔹 Cargar los datos desde el archivo CSV con caché
@st.cache_data
def load_cached_data():
    """Carga los datos del CSV y almacena los resultados en caché para mayor eficiencia."""
    return load_data()

df = load_cached_data()

# 🔹 Función para filtrar datos con caché
@st.cache_data
def filtrar_datos(df, equipo, jugador, posicion, liga):
    """Filtra los datos del DataFrame y almacena los resultados en caché."""
    return df[
        (df["nombre_equipo"] == equipo) &
        (df["nombre"] == jugador) &
        (df["posicion"] == posicion) &
        (df["nombre_liga"] == liga)
    ]

# 🔹 Función para descargar y almacenar en caché la imagen del jugador
@st.cache_data
def descargar_imagen(url):
    """Descarga y almacena en caché la imagen del jugador para evitar múltiples descargas."""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(io.BytesIO(response.content))
    except Exception:
        return None

# 🔹 Función para generar y almacenar en caché los gráficos
@st.cache_data
def generar_grafico_tiros(filtered_df, temp_dir):
    """Genera y guarda el gráfico de tiros en caché para evitar recalculaciones."""
    fig, ax = plt.subplots()
    ax.bar(["Tiros Totales", "Tiros al Arco"], 
           [filtered_df["tiros_total"].values[0], filtered_df["tiros_al_arco"].values[0]], 
           color=['blue', 'green'])
    ax.set_ylabel("Cantidad de Tiros")
    tiros_img_path = os.path.join(temp_dir, "tiros_grafico.png")
    fig.savefig(tiros_img_path)
    return tiros_img_path

@st.cache_data
def generar_grafico_duelos(filtered_df, temp_dir):
    """Genera y guarda el gráfico de duelos en caché para evitar recalculaciones."""
    fig, ax = plt.subplots()
    ax.bar(["Duelos Totales", "Duelos Ganados"], 
           [filtered_df["duelos_total"].values[0], filtered_df["duelos_ganados"].values[0]], 
           color=['red', 'purple'])
    ax.set_ylabel("Cantidad de Duelos")
    duelos_img_path = os.path.join(temp_dir, "duelos_grafico.png")
    fig.savefig(duelos_img_path)
    return duelos_img_path

# 🔹 Función para generar el PDF
def export_to_pdf(filtered_df, tiros_img_path, duelos_img_path):
    """Genera un archivo PDF con la información del jugador y gráficos."""
    
    temp_dir = tempfile.gettempdir()
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # 🏆 Agregar el logo del torneo si está disponible
    logo_path = "assets/logo_betplay.png"
    try:
        pdf.image(logo_path, x=80, y=10, w=50)
    except:
        pdf.cell(200, 10, "No se pudo cargar el logo", ln=True)
    pdf.ln(30)

    # 📌 Datos del Jugador
    pdf.cell(200, 10, "Datos Personales", ln=True, align='L')
    pdf.ln(5)
    pdf.cell(200, 10, f"Nombre: {filtered_df['nombre'].values[0]} {filtered_df['apellido'].values[0]}", ln=True)
    pdf.cell(200, 10, f"Edad: {filtered_df['edad'].values[0]}", ln=True)
    pdf.cell(200, 10, f"Fecha de nacimiento: {filtered_df['fecha_nacimiento'].values[0]}", ln=True)
    pdf.cell(200, 10, f"Nacionalidad: {filtered_df['nacionalidad'].values[0]}", ln=True)
    pdf.cell(200, 10, f"Peso: {filtered_df['peso'].values[0]} kg", ln=True)
    pdf.cell(200, 10, f"Altura: {filtered_df['altura'].values[0]} m", ln=True)
    pdf.ln(10)

    # 📌 Información del Equipo
    pdf.cell(200, 10, "Información del Equipo", ln=True, align='L')
    pdf.ln(5)
    pdf.cell(200, 10, f"Equipo: {filtered_df['nombre_equipo'].values[0]}", ln=True)
    pdf.cell(200, 10, f"Liga: {filtered_df['nombre_liga'].values[0]}", ln=True)
    pdf.ln(10)

    # 📸 Foto del Jugador
    img = descargar_imagen(filtered_df["foto"].values[0])
    if img:
        img_path = os.path.join(temp_dir, "temp_foto.jpg")
        img.save(img_path)
        pdf.image(img_path, x=10, y=pdf.get_y(), w=50)

    pdf.ln(20)

    # 📊 Agregar gráficos al PDF
    pdf.add_page()
    pdf.image(tiros_img_path, x=10, y=pdf.get_y(), w=150)

    pdf.add_page()
    pdf.image(duelos_img_path, x=10, y=pdf.get_y(), w=150)

    # ✅ Guardar el archivo PDF
    filename = f"{filtered_df['nombre_equipo'].values[0]}_{filtered_df['nombre'].values[0]}.pdf".replace(" ", "_")
    filepath = os.path.join(temp_dir, filename)
    pdf.output(filepath)

    return filepath

# 🔹 Función principal para mostrar la página
def show():
    """Muestra los datos personales, gráficos y permite exportar a PDF."""
    st.image("assets/logo_betplay.png", width=200)
    st.title("Análisis Copa BetPlay 2023")

    equipo = st.sidebar.selectbox("Selecciona el equipo", df["nombre_equipo"].unique())
    jugadores_disponibles = df[df["nombre_equipo"] == equipo]["nombre"].unique()
    jugador = st.sidebar.selectbox("Selecciona el jugador", jugadores_disponibles)
    posicion = st.sidebar.selectbox("Selecciona la posición", df["posicion"].unique())
    liga = st.sidebar.selectbox("Selecciona la liga", df["nombre_liga"].unique())

    filtered_df = filtrar_datos(df, equipo, jugador, posicion, liga)

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

    temp_dir = tempfile.gettempdir()

    st.subheader("Comparación de Tiros")
    tiros_img_path = generar_grafico_tiros(filtered_df, temp_dir)
    st.image(tiros_img_path)

    st.subheader("Comparación de Duelos")
    duelos_img_path = generar_grafico_duelos(filtered_df, temp_dir)
    st.image(duelos_img_path)

    if st.button("Exportar a PDF"):
        pdf_filename = export_to_pdf(filtered_df, tiros_img_path, duelos_img_path)
        with open(pdf_filename, "rb") as f:
            st.download_button(label="Descargar PDF", data=f, file_name=os.path.basename(pdf_filename), mime="application/pdf")
