"""
Módulo de autenticación de usuarios en Streamlit.
"""

import streamlit as st
import toml

CONFIG_PATH = ".streamlit/config.toml"

def load_config():
    """Carga la configuración desde el archivo TOML."""
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return toml.load(f)
    except Exception as e:
        st.error(f"❌ Error cargando config.toml: {e}")
        return {}

config = load_config()

def validar_usuario(usuario, contraseña):
    """Valida si el usuario y la contraseña son correctos."""
    usuarios_validos = config.get("authentication", {}).get("usuarios_validos", {})
    return usuarios_validos.get(usuario) == contraseña

def show_login():
    """Muestra el formulario de inicio de sesión."""
    st.title("🔐 Iniciar Sesión")
    usuario = st.text_input("Usuario:", key="usuario_input")
    contraseña = st.text_input("Contraseña:", type="password", key="contraseña_input")

    if st.button("Ingresar"):
        if validar_usuario(usuario, contraseña):
            st.session_state["logged_in"] = True
            st.session_state["usuario"] = usuario
            st.success(f"✅ Bienvenido {usuario}")
            st.rerun()  # 🔹 Corrección: Se usa `st.rerun()` en lugar de `st.experimental_rerun()`
        else:
            st.error("❌ Usuario o contraseña incorrectos")

def check_login():
    """Verifica si el usuario está autenticado antes de permitir el acceso."""
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        show_login()
        st.stop()

