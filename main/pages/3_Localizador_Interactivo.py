import streamlit as st
from streamlit.components.v1 import ComponentBase

def get_geolocation():
    key = "c43c377d6b6b4b05b1750841e52a8473"
    response = requests.get("https://api.ipgeolocation.io/ipgeo?apiKey=" + key)
    return response.json()

if st.button('Mi ubicación'):
    get_geolocation()


