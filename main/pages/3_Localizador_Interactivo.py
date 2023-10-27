import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_basemap(basemap)

# Supongamos que tienes un DataFrame llamado df con latitudes y longitudes
# Por ejemplo:
df = pd.DataFrame({
    'latitude': [40.4168, 40.4070, 40.3999],
    'longitude': [-3.7038, -3.6950, -3.6860],
    'name': ['Location 1', 'Location 2', 'Location 3']
})

# Agregar marcadores para cada ubicación en el DataFrame
for idx, row in df.iterrows():
    leafmap.Marker(location=(row['latitude'], row['longitude']), popup=row['name']).add_to(m)

# Mostrar el mapa en Streamlit
m.to_streamlit(height=700)
