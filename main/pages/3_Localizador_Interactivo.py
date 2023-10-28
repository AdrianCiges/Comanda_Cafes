import streamlit as st
import leafmap.foliumap as leafmap

st.title("Interactive Map")

# Lista para almacenar las coordenadas capturadas
coordinates = []

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

    # Captura el evento 'click' y almacena las coordenadas
    def on_map_click(e):
        coordinates.append((e.latlng.lat, e.latlng.lng))
        st.write(f"Coordinates: {e.latlng.lat}, {e.latlng.lng}")

    m.on('click', on_map_click)
