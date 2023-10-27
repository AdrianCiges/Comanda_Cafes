import streamlit as st

# Título de la aplicación
st.title("Geolocalización del Usuario en Streamlit")

# Función para obtener la geolocalización del usuario
def get_user_location():
    if st.button("Obtener Geolocalización"):
        user_location = st.location()
        if user_location:
            latitude = user_location.latitude
            longitude = user_location.longitude
            st.write(f"Latitud: {latitude:.6f}")
            st.write(f"Longitud: {longitude:.6f}")
        else:
            st.warning("La geolocalización no está habilitada o no se pudo obtener.")

# Llama a la función para obtener la geolocalización
get_user_location()
