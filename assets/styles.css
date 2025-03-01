import streamlit as st

# Credenciales fijas
CREDENTIALS = {"admin": "admin"}

def login():
    """Muestra la interfaz de inicio de sesión."""
    st.title("Iniciar Sesión")
    username = st.text_input("Usuario", value="", max_chars=20)
    password = st.text_input("Contraseña", value="", type="password")

    if st.button("Ingresar"):
        if username in CREDENTIALS and CREDENTIALS[username] == password:
            st.session_state["logged_in"] = True
            st.rerun()
        else:
            st.error("Usuario o contraseña incorrectos")

def logout():
    """Cierra la sesión del usuario."""
    st.session_state["logged_in"] = False
    st.rerun()

def check_authentication():
    """Verifica si el usuario está autenticado."""
    return st.session_state.get("logged_in", False)
