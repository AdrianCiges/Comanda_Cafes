import streamlit as st
import folium

st.title("Interactive Map")

col1, col2 = st.columns([4, 1])
options = ["OpenStreetMap", "Stamen Terrain", "Stamen Toner", "Stamen Watercolor", "CartoDB positron", "CartoDB dark_matter"]
index = options.index("OpenStreetMap")

with col2:
    basemap = st.selectbox("Select a basemap:", options, index)

with col1:
    m = folium.Map(location=[40.4168, -3.7038], zoom_start=10, tiles=basemap)

# Supongamos que tienes un DataFrame llamado df con latitudes, longitudes y nombres de ubicaciones
# Por ejemplo:
import pandas as pd

df = pd.DataFrame({
    'latitude': [40.4168, 40.4070, 40.3999],
    'longitude': [-3.7038, -3.6950, -3.6860],
    'name': ['Location 1', 'Location 2', 'Location 3']
})

# Agregar marcadores para cada ubicación en el DataFrame
for idx, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']], popup=row['name']).add_to(m)

# Mostrar el mapa en Streamlit
st.folium_static(m)

import streamlit as st
import json

st.title("Geolocalización del Usuario en Streamlit")

# Función para obtener la geolocalización del usuario en JavaScript
javascript_code = """
<script>
function getUserLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            // Envía los datos de latitud y longitud al servidor de Streamlit
            const locationData = {latitude, longitude};
            Streamlit.setComponentValue(locationData);
        });
    } else {
        alert("Tu navegador no admite geolocalización.");
    }
}
</script>
"""

# Agrega el código JavaScript a la página
st.markdown(javascript_code, unsafe_allow_html=True)

# Botón para obtener la geolocalización del usuario
if st.button("Obtener Geolocalización"):
    # Obtiene los datos de geolocalización del usuario
    location_data = st._component_value
    if location_data:
        latitude = location_data["latitude"]
        longitude = location_data["longitude"]
        st.write(f"Latitud: {latitude:.6f}, Longitud: {longitude:.6f}")
    else:
        st.warning("La geolocalización no está habilitada o no se pudo obtener.")
