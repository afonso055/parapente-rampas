import streamlit as st
import pandas as pd
import math
import pydeck as pdk

# Dados das rampas
rampas = [
    {"nome": "Rampinha - São Paulo", "lat": -23.5489, "lon": -46.6388},
    {"nome": "Rampão - Rio de Janeiro", "lat": -22.9068, "lon": -43.1729},
    {"nome": "Quixadá - CE", "lat": -4.9707, "lon": -39.0167},
    {"nome": "Governador Valadares - MG", "lat": -18.8545, "lon": -41.9555},
    {"nome": "Jaraguá - GO", "lat": -15.7556, "lon": -49.3344},
    {"nome": "Andrada - MG", "lat": -22.0726, "lon": -46.5701}
]

df = pd.DataFrame(rampas)

# Interface
st.title("🪂 Distância entre Rampas de Parapente no Brasil")

col1, col2 = st.columns(2)
with col1:
    origem = st.selectbox("Escolha a rampa de origem", df["nome"])
with col2:
    destino = st.selectbox("Escolha a rampa de destino", df["nome"])

coord1 = df[df["nome"] == origem][["lat", "lon"]].values[0]
coord2 = df[df["nome"] == destino][["lat", "lon"]].values[0]

# Cálculo da distância
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = map(math.radians, coord1)
    lat2, lon2 = map(math.radians, coord2)
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

dist = haversine(coord1, coord2)
st.success(f"📏 Distância entre as rampas: **{dist} km**")

# Mapa com pydeck
layer = [
    pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_color='[255, 0, 0, 160]',
        get_radius=50000,
    ),
    pdk.Layer(
        "LineLayer",
        data=pd.DataFrame([{"lat": coord1[0], "lon": coord1[1]}, {"lat": coord2[0], "lon": coord2[1]}]),
        get_source_position='[lon, lat]',
        get_target_position='[lon, lat]',
        get_color=[0, 0, 255],
        get_width=5,
    )
]

st.pydeck_chart(pdk.Deck(
    initial_view_state=pdk.ViewState(
        latitude=(coord1[0] + coord2[0]) / 2,
        longitude=(coord1[1] + coord2[1]) / 2,
        zoom=4,
        pitch=0,
    ),
    layers=layer
))
