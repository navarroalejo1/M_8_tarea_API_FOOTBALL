"""
Menú de navegación en Streamlit.
"""

import streamlit as st

def show_menu(page=None):
    """Muestra el menú de navegación en la barra lateral y selecciona la página actual."""

    st.sidebar.markdown("")
    
    opciones_menu = ["Jugadores", "Equipos"]
    
    # Evitar error de índice si page no está en opciones
    index_selected = opciones_menu.index(page) if page in opciones_menu else 0

    page_selected = st.sidebar.radio("Selecciona una página", opciones_menu, index=index_selected)

    if page_selected == "Jugadores":
        from pages import players
        players.show()
    elif page_selected == "Equipos":
        from pages import teams
        teams.show()

    st.sidebar.image("assets/logo_betplay.png", use_container_width=True)

    if st.sidebar.button("Cerrar sesión"):
        st.session_state["logged_in"] = False
        st.session_state.pop("usuario", None)
        st.rerun()

