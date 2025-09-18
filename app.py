import streamlit as st
from io import StringIO

st.set_page_config(page_title="Análisis de Almacenamiento", layout="wide")

st.title("🔎 Análisis Técnico – Soluciones de Almacenamiento")
st.write("Informe interactivo para comparar HDD, SSD, Cintas y Nube, con simulaciones y recomendaciones.")

st.subheader("1) Descripción del escenario")
with st.expander("✍️ Editar resumen (Markdown)"):
    default_md = """
**Proyecto:** Solución de Almacenamiento de Datos  
**Cliente:** (completar)  
**Dolores actuales:** lentitud de acceso, límites de escalabilidad, costes crecientes, requisitos de seguridad.  
**Objetivo:** mejorar rendimiento, fiabilidad y crecimiento con coste óptimo.
"""
    scenario_md = st.text_area("Descripción", value=default_md, height=200, key="scenario_md")
st.markdown(st.session_state.get("scenario_md", default_md))

st.subheader("2) Criterios de evaluación")
st.markdown(
    "- **Velocidad** (lectura/escritura)  \n"
    "- **Capacidad total**  \n"
    "- **Costo/GB**  \n"
    "- **Fiabilidad (MTBF)**  \n"
    "- **Consumo energético** (W)  \n"
    "- **Seguridad** (cifrado, controles)  \n"
    "- **Escalabilidad**"
)

st.subheader("8) Conclusiones técnicas")
conclusiones = st.text_area(
    "Conclusión y recomendación",
    value="Recomendamos una solución **híbrida**: SSD para cargas críticas y **Nube** para respaldo/archivos fríos y DR, equilibrando rendimiento y coste total.",
    height=140,
    key="conclusiones_md"
)
st.markdown(conclusiones)

# Export simple (Markdown/HTML) vía download button
colA, colB = st.columns(2)
with colA:
    st.download_button(
        label="⬇️ Descargar resumen (Markdown)",
        data=StringIO(f"# Descripción del escenario\n\n{st.session_state.get('scenario_md','')}\n\n# Conclusiones\n\n{conclusiones}\n"),
        file_name="resumen_conclusiones.md",
        mime="text/markdown"
    )

with colB:
    html_content = f"""
    <html><head><meta charset='utf-8'><title>Resumen</title></head>
    <body>
      <h1>Descripción del escenario</h1>
      <div>{st.session_state.get('scenario_md','').replace('\\n','<br>')}</div>
      <h1>Conclusiones</h1>
      <div>{conclusiones.replace('\\n','<br>')}</div>
    </body></html>"""
    st.download_button(
        label="⬇️ Descargar resumen (HTML)",
        data=html_content,
        file_name="resumen_conclusiones.html",
        mime="text/html"
    )

st.info("Usa la navegación lateral para acceder a **Comparativa**, **Simulaciones**, **Arquitectura** y **Riesgos & Oportunidades**.")
