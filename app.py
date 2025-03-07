"""
Aplicación Streamlit para la Liga BetPlay 2023.
Incluye autenticación, navegación y visualización de datos.
"""
import streamlit as st
from common.auth import check_login
from common.menu import show_menu

# Configuración de página
st.set_page_config(
    page_title="Estadísticas Liga BetPlay 2023",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Verificar autenticación
page = check_login()

# Mostrar menú de navegación
def main():
    show_menu(page)

if __name__ == "__main__":
    main()
