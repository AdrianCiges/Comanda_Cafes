import streamlit as st
import folium
from streamlit_folium import folium_static

st.title("Interactive Map")

# Lista para almacenar las coordenadas capturadas
coordinates = []

def display_coordinates(map, lat, lon):
    """Function to display coordinates and add marker when the map is clicked."""
    coordinates.append((lat, lon))
    folium.Marker([lat, lon], tooltip=f'Latitude: {lat}, Longitude: {lon}').add_to(map)

col1, col2 = st.columns([4, 1])
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Mapbox Bright", "Mapbox Control Room"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

m = folium.Map(location=[20,0], zoom_start=2, tiles=basemap)
m.add_child(folium.LatLngPopup())

with col1:
    folium_static(m)
