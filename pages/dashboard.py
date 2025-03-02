def export_to_pdf(filtered_df):
    """Genera un archivo PDF con la información del jugador y lo guarda en una ubicación temporal."""
    
    # ✅ Crear un directorio temporal persistente
    temp_dir = tempfile.gettempdir()

    # ✅ Normalizar el nombre del archivo eliminando caracteres especiales
    pdf_filename = f"{filtered_df['nombre_equipo'].values[0]}_{filtered_df['nombre'].values[0]}".replace(" ", "_").replace(".", "").replace(",", "")
    
    # ✅ Asegurar que el nombre del archivo termine en .pdf
    pdf_filename = f"{pdf_filename}.pdf"

    # ✅ Definir la ruta final del archivo
    pdf_path = os.path.join(temp_dir, pdf_filename)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # ✅ Agregar logo
    logo_path = "assets/logo_betplay.png"
    try:
        pdf.image(logo_path, x=80, y=10, w=50)
    except Exception:
        pdf.cell(200, 10, "No se pudo cargar el logo", ln=True)
    
    pdf.ln(30)
    pdf.cell(200, 10, "Análisis Copa BetPlay 2023", ln=True, align='C')
    pdf.ln(10)

    # ✅ Datos del jugador
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

    # ✅ Descargar y agregar la foto del jugador
    try:
        response = requests.get(filtered_df["foto"].values[0])
        if response.status_code == 200:
            img = Image.open(requests.get(filtered_df["foto"].values[0], stream=True).raw)
            img_path = os.path.join(temp_dir, "foto_jugador.jpg")
            img.save(img_path)
            pdf.image(img_path, x=10, y=pdf.get_y(), w=50)
    except Exception:
        pdf.cell(200, 10, "No se pudo cargar la foto", ln=True)

    pdf.ln(20)

    # ✅ Guardar y agregar gráficos al PDF sin sobreponerlos
    pdf.add_page()
    pdf.cell(200, 10, "Comparación de Tiros Totales y Tiros al Arco", ln=True, align='C')
    pdf.ln(10)

    fig, ax = plt.subplots()
    ax.bar(["Tiros Totales", "Tiros al Arco"], 
           [filtered_df["tiros_total"].values[0], filtered_df["tiros_al_arco"].values[0]], color=["blue", "green"])
    ax.set_ylabel("Cantidad de Tiros")
    ax.grid(axis="y")
    
    tiros_img_path = os.path.join(temp_dir, "tiros_grafico.png")
    fig.savefig(tiros_img_path)
    pdf.image(tiros_img_path, x=10, y=pdf.get_y(), w=150)

    pdf.add_page()
    pdf.cell(200, 10, "Comparación de Duelos Totales y Duelos Ganados", ln=True, align='C')
    pdf.ln(10)

    fig, ax = plt.subplots()
    ax.bar(["Duelos Totales", "Duelos Ganados"], 
           [filtered_df["duelos_total"].values[0], filtered_df["duelos_ganados"].values[0]], color=["red", "yellow"])
    ax.set_ylabel("Cantidad de Duelos")
    ax.grid(axis="y")
    
    duelos_img_path = os.path.join(temp_dir, "duelos_grafico.png")
    fig.savefig(duelos_img_path)
    pdf.image(duelos_img_path, x=10, y=pdf.get_y(), w=150)

    # ✅ Guardar PDF
    pdf.output(pdf_path)

    # ✅ Verificar si el archivo realmente existe antes de devolverlo
    if os.path.exists(pdf_path):
        return pdf_path
    else:
        return None
