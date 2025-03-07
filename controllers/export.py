import pandas as pd
from fpdf import FPDF
import os
import tempfile
import matplotlib.pyplot as plt

class ExportarDatos:
    def exportar_csv(self, df):
        """Exporta los datos a CSV."""
        temp_dir = tempfile.gettempdir()
        filename = os.path.join(temp_dir, "jugador_export.csv")
        df.to_csv(filename, index=False)
        return filename

    def exportar_pdf(self, df, filename, jugador_data, fig_paths, logo_path):
        """Exporta los datos personales, la foto y los gráficos a PDF."""
        temp_dir = tempfile.gettempdir()
        pdf_filename = os.path.join(temp_dir, filename)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)

        # Agregar logo si existe
        if os.path.exists(logo_path):
            pdf.image(logo_path, x=80, y=10, w=50)
        pdf.cell(200, 10, "Análisis Copa BetPlay 2024", ln=True, align='C')
        pdf.ln(20)

        # Datos personales
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "DATOS PERSONALES", ln=True, align='L')
        pdf.ln(5)

        # Foto del jugador si está disponible
        foto_path = jugador_data.get("foto", None)
        if foto_path and os.path.exists(foto_path):
            pdf.image(foto_path, x=10, y=pdf.get_y(), w=30)
        pdf.set_font("Arial", size=11)
        pdf.cell(200, 10, f"Nombre: {jugador_data.get('nombre', 'No disponible')} {jugador_data.get('apellido', 'No disponible')}", ln=True)
        pdf.cell(200, 10, f"Equipo: {jugador_data.get('nombre_equipo', 'No disponible')}", ln=True)
        pdf.cell(200, 10, f"Posición: {jugador_data.get('posicion', 'No disponible')}", ln=True)
        pdf.cell(200, 10, f"Edad: {jugador_data.get('edad', 0)} años", ln=True)
        pdf.cell(200, 10, f"Fecha de nacimiento: {jugador_data.get('fecha_nacimiento', 'No disponible')}", ln=True)
        pdf.cell(200, 10, f"Nacionalidad: {jugador_data.get('nacionalidad', 'No disponible')}", ln=True)
        pdf.cell(200, 10, f"Peso: {jugador_data.get('peso', 0)} kg", ln=True)
        pdf.cell(200, 10, f"Altura: {jugador_data.get('altura', 0)} m", ln=True)
        pdf.ln(10)

        # Agregar estadísticas al PDF
        pdf.set_font("Arial", "B", 12)
        pdf.cell(200, 10, "ESTADÍSTICAS INDIVIDUALES", ln=True, align='L')
        pdf.ln(5)

        # Verificar que las gráficas existen antes de agregarlas
        if not fig_paths:
            pdf.cell(200, 10, "⚠ No hay gráficos disponibles para este jugador", ln=True)
        else:
            for fig_path in fig_paths:
                if os.path.exists(fig_path):
                    pdf.image(fig_path, x=10, w=180)
                    pdf.ln(10)

        pdf.output(pdf_filename)
        
        # Eliminar imágenes temporales después de exportar el PDF
        for fig_path in fig_paths:
            if os.path.exists(fig_path):
                os.remove(fig_path)

        return pdf_filename
