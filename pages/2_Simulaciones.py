import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.title("🧪 Simulaciones de Rendimiento")

uploaded = st.sidebar.file_uploader("Subir CSV (opcional)", type=["csv"], key="uploader_sim")
if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/comparativa_ejemplo.csv")

for col in ["VelocidadLecturaMBs","VelocidadEscrituraMBs","CapacidadTB","CostoPorGBUSD","MTBFHoras","ConsumoW"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

st.subheader("Parámetros")
with st.expander("Configurar simulación"):
    vol_inicial_tb = st.number_input("Volumen inicial (TB)", 0.1, 100000.0, 10.0, 0.1)
    crecimiento = st.slider("Crecimiento anual (%)", 0, 300, 50, 5)
    anos = st.slider("Horizonte (años)", 1, 10, 2, 1)
    techs = st.multiselect("Tecnologías", df["Tecnologia"].tolist(), default=["HDD","SSD","Nube"])

    velocidades = {}
    for t in techs:
        base = df.loc[df["Tecnologia"]==t, "VelocidadLecturaMBs"]
        default_v = float(base.iloc[0]) if len(base) else 150.0
        velocidades[t] = st.number_input(f"Velocidad efectiva de {t} (MB/s)", 1.0, 1_000_000.0, default_v, 1.0)

anos_range = np.arange(0, anos+1)
vol_mb = (vol_inicial_tb * 1_000_000) * ((1 + (crecimiento/100)) ** anos_range)  # 1 TB ≈ 1,000,000 MB
sim_df = pd.DataFrame({"Año": anos_range, "Volumen_MB": vol_mb})

for t in techs:
    sim_df[f"{t}_tiempo_s"] = (vol_mb / max(velocidades[t], 1e-6))

st.markdown("**Resultados (segundos estimados por tecnología):**")
st.dataframe(sim_df, use_container_width=True)

fig = go.Figure()
for t in techs:
    fig.add_trace(go.Scatter(x=sim_df["Año"], y=sim_df[f"{t}_tiempo_s"], mode="lines+markers", name=t))
fig.update_layout(title="Tiempo de respuesta vs crecimiento de datos (↓ mejor)", xaxis_title="Año", yaxis_title="Tiempo (s)")
st.plotly_chart(fig, use_container_width=True)

st.success("Pro tip: simula el paso de HDD→SSD o HDD→Nube activando solo esas dos tecnologías y comparando curvas.")
