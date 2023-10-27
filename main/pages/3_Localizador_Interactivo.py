import streamlit as st
from streamlit.components.v1 import ComponentBase

class Geolocation(ComponentBase):
    def __init__(self):
        super().__init__()

geolocation = Geolocation()

st.title("Geolocalización del Usuario en Streamlit")

if st.button("Obtener Geolocalización"):
    geolocation._update_widget_state(data={})
    st.write("Esperando la geolocalización...")

# Código JavaScript para obtener la geolocalización
javascript_code = """
if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition(function(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        var locationData = { latitude, longitude };
        // Envía los datos de latitud y longitud al servidor de Streamlit
        Streamlit.setComponentValue(locationData);
    });
} else {
    alert("Tu navegador no admite geolocalización.");
}
"""

# Agrega el código JavaScript a la página
st.markdown(javascript_code, unsafe_allow_html=True)

# Escucha los datos de geolocalización obtenidos
location_data = geolocation._get_value()
if location_data:
    latitude = location_data.get("latitude", 0)
    longitude = location_data.get("longitude", 0)
    st.write(f"Latitud: {latitude:.6f}")
    st.write(f"Longitud: {longitude:.6f}")
