import streamlit as st
import leafmap.foliumap as leafmap

# Título de la aplicación
st.title("Geolocalización del Usuario con Leafmap en Streamlit")

# Crear un mapa interactivo con Leafmap
m = leafmap.Map(zoom_control=False, draw_export=False, locate_control=True)

# Mostrar el mapa en la aplicación
st.write(m)

# Función para obtener la geolocalización del usuario
def get_user_location():
    user_location = m.get_location()
    if user_location:
        latitude = user_location["lat"]
        longitude = user_location["lng"]
        st.write(f"Latitud: {latitude:.6f}")
        st.write(f"Longitud: {longitude:.6f}")
    else:
        st.warning("La geolocalización no está habilitada o no se pudo obtener.")

# Botón para obtener la geolocalización del usuario
if st.button("Obtener Geolocalización"):
    get_user_location()
