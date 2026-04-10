import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

# 1. Configuración de la App
st.set_page_config(page_title="Meteoro ⚡", layout="wide")

# Mensaje de vida inmediato
st.success("🚀 Sistema Meteoro Activo - Conectando...")

# 2. Conexión Protegida
@st.cache_resource
def conectar_db():
    if not firebase_admin._apps:
        try:
            if "firebase" not in st.secrets:
                st.error("❌ No se encontraron los Secrets '[firebase]'")
                st.stop()
            
            cred_dict = dict(st.secrets["firebase"])
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"⚠️ Error de conexión: {e}")
            st.stop()
    return firestore.client()

db = conectar_db()

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
                st.success("✅ ¡Lanzado!")
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error al escribir: {e}")

# 5. Lista Real de Firebase
st.subheader("📋 Encargos Registrados")
if db:
    try:
        docs = db.collection("encargos").order_by("timestamp", direction=firestore.Query.DESCENDING).stream()
        for doc in docs:
            data = doc.to_dict()
            with st.container(border=True):
                st.write(f"**{data.get('fecha')}** - {data.get('desc')}")
                st.info(f"Estado: {data.get('estado')}")
    except Exception as e:
        st.error(f"Error al leer datos: {e}")