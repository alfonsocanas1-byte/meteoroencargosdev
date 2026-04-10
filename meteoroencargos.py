import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os

# 1. Configuración de la App
st.set_page_config(page_title="Meteoro ⚡", layout="wide")

# 2. Conexión Directa al JSON del Repositorio
@st.cache_resource
def conectar_firebase():
    if not firebase_admin._apps:
        # Usamos el nombre exacto de tu archivo
        ruta_json = "jsonencargosencargosmeteoro.json"
        
        # Verificación de existencia para evitar que la app se caiga
        if not os.path.exists(ruta_json):
            st.error(f"❌ Error Crítico: No se encuentra '{ruta_json}' en el repositorio.")
            st.info("Asegúrate de que el archivo esté en la raíz de la rama 'desarrollo'.")
            st.stop()
            
        try:
            cred = credentials.Certificate(ruta_json)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"⚠️ Fallo en la llave de Firebase: {e}")
            st.stop()
            
    return firestore.client()

db = conectar_firebase()

# 3. Interfaz del Panel
st.title("⚡ Panel de Encargos - Misión España")

# Mostrar registros existentes (Prueba de lectura)
st.subheader("📋 Encargos Registrados")
if db:
    try:
        # Intentamos traer los datos de la colección 'encargos'
        docs = db.collection("encargos").stream()
        lista = list(docs)
        
        if not lista:
            st.warning("Conexión exitosa, pero no hay datos en la colección 'encargos'.")
        else:
            for doc in lista:
                data = doc.to_dict()
                with st.container(border=True):
                    st.write(f"📦 **{data.get('desc', 'Sin descripción')}**")
                    if 'fecha' in data:
                        st.caption(f"Fecha: {data['fecha']}")
    except Exception as e:
        st.error(f"Error al leer de Firebase: {e}")

# Formulario de entrada
with st.form("nuevo_encargo", clear_on_submit=True):
    nuevo = st.text_input("Escribe un nuevo encargo:")
    if st.form_submit_button("Lanzar"):
        if nuevo:
            db.collection("encargos").add({
                "desc": nuevo,
                "estado": "🔴 Recibido"
            })
            st.success("¡Encargo manifestado!")
            st.rerun()