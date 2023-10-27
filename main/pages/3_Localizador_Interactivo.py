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
            var locationData = {latitude, longitude};
            Shiny.setInputValue('locationData', locationData);
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
    # Ejecuta la función JavaScript para obtener la geolocalización
    st.markdown('<button onclick="getUserLocation()">Obtener ubicación</button>', unsafe_allow_html=True)
    
    # Escucha los datos de geolocalización obtenidos
    location_data = st.json_input('locationData', value={})
    if location_data:
        latitude = location_data.get("latitude", 0)
        longitude = location_data.get("longitude", 0)
        st.write(f"Latitud: {latitude:.6f}")
        st.write(f"Longitud: {longitude:.6f}")
    else:
        st.warning("La geolocalización no está habilitada o no se pudo obtener.")
