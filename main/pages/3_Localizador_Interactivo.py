import streamlit as st
import folium

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)

# Supongamos que tienes un DataFrame llamado df con latitudes, longitudes y nombres de ubicaciones
# Por ejemplo:
import pandas as pd

df = pd.DataFrame({
    'latitude': [40.4168, 40.4070, 40.3999],
    'longitude': [-3.7038, -3.6950, -3.6860],
    'name': ['Location 1', 'Location 2', 'Location 3']
})

# Agregar marcadores para cada ubicación en el DataFrame
for idx, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Mostrar el mapa en Streamlit
st.folium_static(m)
