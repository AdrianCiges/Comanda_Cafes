import streamlit as st
import leafmap.foliumap as leafmap
import streamlit_option_menu as option_menu

markdown = """
Web App URL: <https://geotemplate.streamlit.app>
GitHub Repository: <https://github.com/giswqs/streamlit-multipage-template>
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://i.imgur.com/UbOXYAU.png"
st.sidebar.image(logo)

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

# Función para capturar las coordenadas cuando se hace clic en el mapa
def handle_map_click(event):
    if event["type"] == "click":
        coordinates.append((event["latlng"]["lat"], event["latlng"]["lng"]))

# Registra la función de manejo de clics en el mapa
m.on("click", handle_map_click)

# Botón para obtener la geolocalización del usuario
if st.button("Geolocalizar Usuario"):
    user_location = m.get_location()
    if user_location:
        coordinates.append((user_location["lat"], user_location["lng"]))

# Muestra las coordenadas capturadas debajo del mapa
if coordinates:
    st.write("Coordenadas Capturadas:")
    for lat, lon in coordinates:
        st.write(f"Latitud: {lat:.6f}, Longitud: {lon:.6f}")
