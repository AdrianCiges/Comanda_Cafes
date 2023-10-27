import streamlit as st
import folium
from streamlit_folium import folium_static
from folium.plugins import Draw

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])

# Opciones de mapas base
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Tipo de mapa:", options, index)

m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)

# Añadimos la herramienta de dibujo al mapa
draw = Draw(draw_options={'polyline': False, 'rectangle': False, 'polygon': False, 'circle': False, 'circlemarker': False})
draw.add_to(m)

# Mostrar el mapa en Streamlit
folium_static(m)

# Captura las coordenadas dibujadas en el mapa
drawn_shapes = st.session_state.get('drawn_shapes', None)
if drawn_shapes:
    if "geometry" in drawn_shapes[-1]:
        coords = drawn_shapes[-1]["geometry"]["coordinates"]
        st.write(f"Latitud: {coords[1]}, Longitud: {coords[0]}")
