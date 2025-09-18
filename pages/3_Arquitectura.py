import streamlit as st
from pathlib import Path

st.title("🗺️ Arquitectura propuesta")

st.markdown("""
Incluye aquí el **diagrama** exportado desde diagrams.net o Lucidchart.
Debe mostrar: componentes, flujo de datos, redundancias y backups.
""")

img = st.file_uploader("Subir diagrama (PNG/JPG)", type=["png","jpg","jpeg"])
if img:
    st.image(img, caption="Diagrama de la infraestructura propuesta", use_container_width=True)
else:
    placeholder = Path("assets/diagrama_infraestructura.png")
    if placeholder.exists():
        st.image(str(placeholder), caption="Placeholder de diagrama", use_container_width=True)
    else:
        st.info("Puedes colocar un placeholder en /assets/diagrama_infraestructura.png")
