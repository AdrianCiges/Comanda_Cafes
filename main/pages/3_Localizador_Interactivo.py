import streamlit as st
import folium
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
