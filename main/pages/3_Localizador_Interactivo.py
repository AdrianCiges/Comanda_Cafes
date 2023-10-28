import streamlit as st
import leafmap.foliumap as leafmap
import folium

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
    
    # Add ClickForMarker functionality using folium
    marker = folium.ClickForMarker(popup="Coordinates: Lat: {}<br>Lon: {}")
    m.add_child(marker)
    
    m.to_streamlit(height=700)

    st.write(marker)
