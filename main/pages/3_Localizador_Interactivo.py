import streamlit as st
import streamlit.components.v1 as components

def map_widget():
    st.title("Seleccione su Ubicación en el Mapa")
    components.iframe("https://www.openstreetmap.org", width=700, height=450)
    lat = st.number_input("Latitud", format="%f")
    lon = st.number_input("Longitud", format="%f")
    if st.button("Confirmar Ubicación"):
        st.write("Latitud:", lat, "Longitud:", lon)

if __name__ == "__main__":
    map_widget()
