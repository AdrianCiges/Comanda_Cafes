import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import LocateControl

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])

# Opciones de mapas base
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Tipo de mapa:", options, index)

m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)  # Puedes cambiar las coordenadas iniciales

# Agregar controles al mapa
LocateControl().add_to(m)

# Función para capturar el evento de clic y obtener las coordenadas
click_coords = []

def click_event_handler(feature, **kwargs):
    coords = feature['geometry']['coordinates']
    click_coords.append(coords)

m.add_child(folium.ClickForMarker(popup="Coordenadas: {} {}".format(*click_coords)))
m.add_child(folium.GeoJson("", name="Clicked Points", onEachFeature=click_event_handler))

# Mostrar el mapa en Streamlit
folium_static(m)

if click_coords:
    st.write(f"Latitud: {click_coords[-1][1]}, Longitud: {click_coords[-1][0]}")
