import streamlit as st
import folium
import streamlit as st
import json

import streamlit as st

st.title("Geolocalización del Usuario en Streamlit")

# Función para obtener la geolocalización del usuario en JavaScript
javascript_code = """
<script>
function getUserLocation() {
    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(function(position) {
            var latitude = position.coords.latitude;
            var longitude = position.coords.longitude;

            // Muestra los datos de latitud y longitud en Streamlit
            document.getElementById("latitude").innerHTML = "Latitud: " + latitude.toFixed(6);
            document.getElementById("longitude").innerHTML = "Longitud: " + longitude.toFixed(6);
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
    # Llama a la función JavaScript para obtener la geolocalización
    st.markdown("<div id='latitude'></div>", unsafe_allow_html=True)
    st.markdown("<div id='longitude'></div>", unsafe_allow_html=True)
    st.write("Esperando la geolocalización...")


