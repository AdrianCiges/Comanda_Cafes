import streamlit as st
import folium
from streamlit_folium import folium_static

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])

# Opciones de mapas base
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Tipo de mapa:", options, index)

m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)  # Puedes cambiar las coordenadas iniciales

click_coords = []

# Función para capturar el evento de clic y obtener las coordenadas
def add_marker(map, coord):
    folium.Marker(location=coord, popup=f"Coordenadas: {coord[0]}, {coord[1]}").add_to(map)
    click_coords.append(coord)

m.add_child(folium.ClickForMarker(popup=add_marker))

# Mostrar el mapa en Streamlit
folium_static(m)

if click_coords:
    st.write(f"Latitud: {click_coords[-1][0]}, Longitud: {click_coords[-1][1]}")
