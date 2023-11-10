import requests
import streamlit as st

def get_location_from_api():
    if st.button('Obtener Ubicación'):
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        st.write(f"Ubicación aproximada: {data['loc']}")

get_location_from_api()
