import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Meteoro ⚡", layout="wide")

# 2. Conexión usando la LLAVE REAL
@st.cache_resource
def conectar_firebase():
    if not firebase_admin._apps:
        # IMPORTANTE: Usamos llave.json que es el archivo con credenciales
        ruta_json = "llave.json"
        
        if not os.path.exists(ruta_json):
            st.error(f"❌ Error: No se encuentra '{ruta_json}' en el repositorio.")
            st.stop()
            
        try:
            cred = credentials.Certificate(ruta_json)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"⚠️ Fallo de autenticación con Google: {e}")
            st.stop()
            
    return firestore.client()

db = conectar_firebase()

# 3. Interfaz del Panel - Misión España
st.title("⚡ Panel de Encargos - Misión España")

with st.form("nuevo_encargo", clear_on_submit=True):
    nuevo = st.text_input("¿Qué encargo vamos a manifestar hoy?")
    if st.form_submit_button("Lanzar Encargo"):
        if nuevo and db:
            db.collection("encargos").add({
                "desc": nuevo,
                "estado": "🔴 Recibido",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "timestamp": datetime.now()
            })
            st.success("✅ ¡Encargo manifestado en el Sistema!")
            st.rerun()

# 4. Visualización de la Base de Datos
st.subheader("📋 Encargos Registrados")
if db:
    try:
        # Traemos los datos ordenados por tiempo
        docs = db.collection("encargos").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        registros = list(docs)
        
        if not registros:
            st.info("Aún no hay encargos reales. El sistema está listo para el primero.")
        else:
            for doc in registros:
                data = doc.to_dict()
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    col1.write(f"📦 **{data.get('desc')}**")
                    col1.caption(f"Registro: {data.get('fecha', 'S/F')}")
                    col2.warning(data.get('estado', '🔴 Recibido'))
    except Exception as e:
        st.error(f"Error al leer Firebase: {e}")