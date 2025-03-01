import streamlit as st

# 🔹 Configuración de la página (Debe ser lo PRIMERO que se ejecute)
st.set_page_config(page_title="Dashboard de Jugadores", layout="wide")

from authentication import login, logout, check_authentication
from navigation import navigate

# 🔹 Verificar autenticación antes de cargar datos o mostrar cualquier otra cosa
if not check_authentication():
    login()
    st.stop()  # 🔹 Detiene la ejecución aquí hasta que el usuario inicie sesión

# 🔹 Si el usuario está autenticado, cargar datos y mostrar la navegación
navigate()
st.sidebar.button("Cerrar Sesión", on_click=logout)

# 🔹 Aplicar estilos personalizados con CSS
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("El archivo styles.css no se encontró en assets/")
