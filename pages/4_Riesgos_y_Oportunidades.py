import streamlit as st

st.title("⚠️ Riesgos y Oportunidades")

with st.expander("Editar riesgos y oportunidades (Markdown)"):
    default_md = """
**Riesgos técnicos**  
- **Costo inicial SSD** alto → *Mitigación:* arquitectura híbrida.  
- **Ciclos de escritura SSD** → *Mitigación:* wear leveling y monitoreo S.M.A.R.T.  
- **Dependencia de conectividad en Nube** → *Mitigación:* enlaces redundantes y caché local.  
- **Seguridad en Nube** → *Mitigación:* cifrado E2E, MFA, cumplimiento (GDPR, etc.).

**Oportunidades**  
- **Escalabilidad en Nube** (crece bajo demanda).  
- **Rendimiento SSD** (baja latencia).  
- **Reducción OPEX** frente a capex en picos.  
- **Continuidad de negocio** (DR/HA multi-región).
"""
    md = st.text_area("Contenido", value=default_md, height=260, key="riesgos_md")
st.markdown(st.session_state.get("riesgos_md", md))

st.info("Usa esta sección para documentar supuestos, controles compensatorios y requisitos regulatorios.")
