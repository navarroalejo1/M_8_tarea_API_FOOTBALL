import streamlit as st
from authentication import login, logout, check_authentication
from navigation import navigate

# 🔹 Configuración de la página
st.set_page_config(page_title="Dashboard de Jugadores", layout="wide")

# 🔹

# 🔹 Verificar autenticación antes de ejecutar cualquier otro código
if not check_authentication():
    login()
    st.stop()  # 🔹 Detiene la ejecución aquí hasta que el usuario inicie sesión

# Si el usuario está autenticado, se muestra la navegación
navigate()
st.sidebar.button("Cerrar Sesión", on_click=logout)

# 🔹 Aplicar estilos personalizados con CSS
try:
    with open("assets/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
except FileNotFoundError:
    st.error("El archivo styles.css no se encontró en assets/")
