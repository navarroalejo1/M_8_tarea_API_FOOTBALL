import streamlit as st
from pages.dashboard import show as dashboard_show
from pages.players import show as players_show


def navigate():
    """Muestra el menú lateral y permite cambiar de página."""
    st.sidebar.title("Menú de Navegación")
    option = st.sidebar.radio("Selecciona una página", ["Dashboard", "Jugadores"])
    
    if option == "Dashboard":
        dashboard_show()
    elif option == "Jugadores":
        players_show()