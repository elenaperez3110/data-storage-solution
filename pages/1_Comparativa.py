import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.title("📊 Comparativa de Tecnologías")

st.sidebar.header("Datos")
uploaded = st.sidebar.file_uploader("Subir CSV de comparativa", type=["csv"], key="uploader_comp")
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/comparativa_ejemplo.csv")

# Normalización numérica básica
for col in ["VelocidadLecturaMBs","VelocidadEscrituraMBs","CapacidadTB","CostoPorGBUSD","MTBFHoras","ConsumoW"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

st.subheader("Tabla editable")
edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
df = edited.copy()

st.markdown("**Métricas derivadas**")

# Supuestos de TCO
with st.expander("Ajustes de coste (supuestos)"):
    col1, col2, col3 = st.columns(3)
    with col1:
        mantenimiento_pct = st.slider("Mantenimiento on-prem (% anual)", 0, 30, 10, 1, help="Aplicado a HDD/SSD/Cintas")
    with col2:
        crecimiento_datos_pct = st.slider("Crecimiento anual datos (%)", 0, 150, 50, 5)
    with col3:
        descuento_pct = st.slider("Tasa de descuento (% anual)", 0, 30, 8, 1)

def npv(cashflows, r):
    return sum(cf/((1+r)**t) for t, cf in enumerate(cashflows))

# Calcular coste anual y TCO 3/5 años
if {"CapacidadTB","CostoPorGBUSD","Tecnologia"}.issubset(df.columns):
    df["CostoAnualUSD_aprox"] = (df["CapacidadTB"] * 1024 * df["CostoPorGBUSD"]).round(2)

    tcos = []
    for _, row in df.iterrows():
        cap_tb = float(row.get("CapacidadTB", 0.0) or 0.0)
        cpgb = float(row.get("CostoPorGBUSD", 0.0) or 0.0)
        tech = str(row.get("Tecnologia", ""))

        growth = 1 + (crecimiento_datos_pct/100)
        years = [0,1,2,3,4,5]
        volume_gb = [cap_tb*1024*(growth**t) for t in years]

        if tech.lower() == "nube":
            # OPEX anual dependiente del volumen
            cashflows = [ - (volume_gb[t] * cpgb) for t in years ]
        else:
            # CAPEX inicial + mantenimiento anual
            capex = -(cap_tb*1024*cpgb)
            maint = - (abs(capex) * (mantenimiento_pct/100.0))
            cashflows = [capex] + [maint for _ in years[1:]]

        r = descuento_pct/100.0
        tco_3y = -npv(cashflows[:4], r)   # 0..3
        tco_5y = -npv(cashflows, r)       # 0..5
        tcos.append((tco_3y, tco_5y))

    df["TCO_3y_USD"] = np.array([t[0] for t in tcos]).round(2)
    df["TCO_5y_USD"] = np.array([t[1] for t in tcos]).round(2)

st.dataframe(df, use_container_width=True)

st.markdown("**Barras: Velocidad de Lectura y Escritura**")
col1, col2 = st.columns(2)
with col1:
    if {"Tecnologia","VelocidadLecturaMBs"}.issubset(df.columns):
        fig_read = px.bar(df, x="Tecnologia", y="VelocidadLecturaMBs", title="Lectura (MB/s)")
        st.plotly_chart(fig_read, use_container_width=True)
with col2:
    if {"Tecnologia","VelocidadEscrituraMBs"}.issubset(df.columns):
        fig_write = px.bar(df, x="Tecnologia", y="VelocidadEscrituraMBs", title="Escritura (MB/s)")
        st.plotly_chart(fig_write, use_container_width=True)

# Radar
st.markdown("**Radar: Fiabilidad, Escalabilidad, Seguridad**")
scale_map = {"Baja":1, "Media":3, "Alta":4, "Muy alta":5, "Muy Alta":5}
radar_cols = ["Fiabilidad","Escalabilidad","Seguridad"]
if set(radar_cols).issubset(df.columns):
    radar_df = df[["Tecnologia"]+radar_cols].copy()
    for c in radar_cols:
        radar_df[c] = radar_df[c].map(scale_map).fillna(3)
    categories = radar_cols
    fig = go.Figure()
    for _, row in radar_df.iterrows():
        fig.add_trace(go.Scatterpolar(r=row[categories].values, theta=categories, fill='toself', name=row["Tecnologia"]))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0,5])), showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# Costos
st.markdown("**Costos: Costo/GB y OPEX estimado**")
if {"Tecnologia","CostoPorGBUSD","CapacidadTB"}.issubset(df.columns):
    df_cost = df.copy()
    df_cost["OPEX_estimado_USD"] = (df_cost["CapacidadTB"]*1024*df_cost["CostoPorGBUSD"]).round(2)
    fig_cost = px.bar(df_cost, x="Tecnologia", y=["CostoPorGBUSD","OPEX_estimado_USD"], barmode="group", title="Costos")
    st.plotly_chart(fig_cost, use_container_width=True)

st.caption("💡 Exporta la tabla desde el menú de tres puntos del componente de datos.")
