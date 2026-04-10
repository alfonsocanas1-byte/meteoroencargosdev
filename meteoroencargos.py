import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import json
import time
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Meteoro ⚡", layout="wide")

# ALERTA INICIAL DE CONTROL
status_info = st.info("⚡ Sistema Meteoro Activo - Verificando conexión...")

# 2. Conexión con Rastreador de Pasos
@st.cache_resource
def conectar_db():
    if not firebase_admin._apps:
        try:
            if "firebase" not in st.secrets:
                st.error("❌ ERROR: No se encontró la sección [firebase] en Secrets.")
                st.stop()

            # Procesando credenciales
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
            return firestore.client()
            
        except Exception as e:
            st.error(f"⚠️ ERROR CRÍTICO: {e}")
            st.stop()
    return firestore.client()

db = conectar_db()
status_info.empty() # Quita el aviso azul si conectó

# 3. Acceso de Seguridad
if "auth" not in st.session_state:
    st.session_state.auth = False

if not st.session_state.auth:
    st.title("⚡ Acceso Meteoro")
    password = st.text_input("Introduce la llave", type="password")
    if password == "5555":
        st.session_state.auth = True
        st.rerun()
    st.stop()

# 4. Panel de Control
st.title("⚡ Panel de Encargos - Misión España")

with st.expander("➕ Lanzar Nuevo Encargo", expanded=True):
    with st.form("f_nuevo", clear_on_submit=True):
        desc = st.text_area("Descripción del encargo:")
        if st.form_submit_button("Lanzar"):
            if desc and db:
                try:
                    db.collection("encargos").add({
                        "desc": desc,
                        "estado": "🔴 Recibido",
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                        "timestamp": datetime.now()
                    })
                    st.success("✅ ¡Encargo manifestado!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Fallo al escribir: {e}")

# 5. Visualización Directa de Firebase
st.subheader("📋 Lista de Encargos Registrados")

if db:
    try:
        docs = db.collection("encargos").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        lista = list(docs)
        
        if not lista:
            st.warning("⚠️ Conexión OK, pero la lista de encargos está vacía en Firebase.")
        else:
            for doc in lista:
                data = doc.to_dict()
                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    fecha = data.get('fecha', 'S/F')
                    descripcion = data.get('desc', 'Sin descripción')
                    est_actual = data.get('estado', "🔴 Recibido")
                    
                    col1.write(f"**{fecha}** - {descripcion}")
                    
                    opciones = ["🔴 Recibido", "🟡 En proceso", "🔵 Comprado", "🟢 Entregado"]
                    idx = opciones.index(est_actual) if est_actual in opciones else 0
                    
                    nuevo_est = col2.selectbox("Estado", opciones, index=idx, key=doc.id)
                    if nuevo_est != est_actual:
                        db.collection("encargos").document(doc.id).update({"estado": nuevo_est})
                        st.rerun()
    except Exception as e:
        st.error(f"❌ Error al consultar Firebase: {e}")