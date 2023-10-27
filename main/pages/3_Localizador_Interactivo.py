import streamlit as st
import leafmap.foliumap as leafmap

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = list(leafmap.basemaps.keys())
index = options.index("OpenTopoMap")

with col2:
    basemap = st.selectbox("Tipo de mapa:", options, index)

with col1:
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=True, minimap_control=True)
    m.add_basemap(basemap)
    m.to_streamlit(height=700)

    # Función para capturar el evento de clic y obtener las coordenadas
    click_coords = m.get_click_latlon()
    if click_coords:
        lat, lon = click_coords
        st.write(f"Latitud: {lat}, Longitud: {lon}")
