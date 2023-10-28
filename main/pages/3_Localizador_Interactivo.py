import streamlit as st
import folium
from streamlit_folium import folium_static

st.title("Interactive Map")

# Lista para almacenar las coordenadas capturadas
coordinates = []

col1, col2 = st.columns([4, 1])
options = ["OpenStreetMap", "OpenTopoMap", "Stamen Terrain"]
index = options.index("OpenTopoMap")

with col2:
    basemap_choice = st.selectbox("Select a basemap:", options, index)

# Creamos un mapa usando folium
m = folium.Map(location=[20, 0], zoom_start=2)

# Añadimos el basemap elegido
if basemap_choice == "OpenTopoMap":
    folium.TileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', name="OpenTopoMap", attr="OpenTopoMap").add_to(m)
elif basemap_choice == "Stamen Terrain":
    folium.TileLayer('https://stamen-tiles-{s}.a.ssl.fastly.net/terrain/{z}/{x}/{y}.png', name="Stamen Terrain", attr="Stamen").add_to(m)

# Función para capturar las coordenadas en un popup al hacer clic
def add_marker(map, location):
    coordinates.append(location)
    folium.Marker(location, popup=f"Coordinates: {location[0]}, {location[1]}").add_to(map)

m.add_child(folium.ClickForMarker(popup=add_marker))

# Mostramos el mapa en streamlit
with col1:
    folium_static(m)

for coord in coordinates:
    st.write(f"Coordinates: {coord[0]}, {coord[1]}")
