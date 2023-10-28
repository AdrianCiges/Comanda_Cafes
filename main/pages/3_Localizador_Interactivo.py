import streamlit as st
import leafmap.foliumap as leafmap

def get_user_location():
    m = leafmap.Map()
    
    # Añadimos la función de geolocalización
    locate_control = leafmap.LocateControl(auto_start=True, fly_to=True)
    m.add_control(locate_control)

    # Aquí puedes añadir código adicional para mostrar el mapa en Streamlit si lo deseas
    # Por ejemplo: m.to_streamlit()

    # Devuelve las coordenadas del usuario
    return locate_control.last_location

if st.button("Get my location"):
    location = get_user_location()
    if location:
        st.write(f"Your coordinates are: {location}")
    else:
        st.write("Unable to get your location.")
