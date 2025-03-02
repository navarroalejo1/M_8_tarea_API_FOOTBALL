import streamlit as st

# 🔹 Configuración de la página (Debe ser la primera línea ejecutable)
st.set_page_config(page_title="Dashboard de Jugadores", layout="wide")

# 🔹 Importaciones después de la configuración
from authentication import login, logout, check_authentication
from navigation import navigate

# 🔹 Verificar autenticación antes de ejecutar cualquier otro código
if not check_authentication():
    login()
    st.stop()  # 🔹 Detiene la ejecución aquí hasta que el usuario inicie sesión

# 🔹 Aplicar estilos personalizados con CSS
css_path = "assets/styles.css"
try:
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error(f"No se encontró el archivo: {css_path}")

# 🔹 Mostrar la navegación y el menú lateral
navigate()

# 🔹 Botón para cerrar sesión
st.sidebar.button("Cerrar Sesión", on_click=logout)

