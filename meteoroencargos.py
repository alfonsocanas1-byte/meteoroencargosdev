import streamlit as st

st.set_page_config(page_title="Meteoro Test ⚡")
st.title("⚡ Sistema Meteoro - Fase de Prueba")

st.write("Si estás viendo esto, la conexión con GitHub y Streamlit es EXITOSA.")

# Simulación de registros para probar la interfaz
st.subheader("📋 Registros de Prueba")
st.success("✅ Compra de servomotores (Simulado)")
st.info("✅ Plan Misión España (Simulado)")

if st.button("Pulsar para confirmar vida"):
    st.balloons()
    st.write("¡El sistema está vivo!")