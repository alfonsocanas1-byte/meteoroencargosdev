import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import os
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Meteoro ⚡", layout="wide")

# 2. Conexión Estable
@st.cache_resource
def conectar_firebase():
    if not firebase_admin._apps:
        ruta_json = "llave.json"
        if not os.path.exists(ruta_json):
            st.error(f"❌ No se encuentra '{ruta_json}'")
            st.stop()
        try:
            cred = credentials.Certificate(ruta_json)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"⚠️ Error de llave: {e}")
            st.stop()
    return firestore.client()

db = conectar_firebase()

# 3. Interfaz - Misión España
st.title("⚡ Panel de Encargos - Misión España")

# Formulario (Escritura controlada)
with st.form("nuevo_encargo", clear_on_submit=True):
    nuevo = st.text_input("¿Qué encargo vamos a manifestar hoy?")
    lanzar = st.form_submit_button("Lanzar Encargo")
    
    if lanzar and nuevo and db:
        try:
            db.collection("encargos").add({
                "desc": nuevo,
                "estado": "🔴 Recibido",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "timestamp": datetime.now()
            })
            st.success("✅ ¡Encargo registrado!")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Error al escribir: {e}")

# 4. Lista de Firebase (Lectura)
st.subheader("📋 Encargos Registrados")
if db:
    try:
        # Traemos los documentos ordenados
        docs = db.collection("encargos").order_by("timestamp", direction=firestore.Query.DESCENDING).limit(10).get()
        
        if not docs:
            st.info("El sistema está listo. Aún no hay registros en esta colección.")
        else:
            for doc in docs:
                data = doc.to_dict()
                with st.container(border=True):
                    st.write(f"📦 **{data.get('desc')}**")
                    st.caption(f"Fecha: {data.get('fecha')} | Estado: {data.get('estado')}")
    except Exception as e:
        st.error(f"Error de lectura: {e}")