import streamlit as st
import pandas as pd
from collections import Counter
from PIL import Image
import base64
import io
import datetime
from datetime import datetime, time, timedelta
import re
import streamlit.components.v1 as components
import time as timee
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

st.set_page_config(layout="wide", page_title="Ruta del Café", page_icon="./img/cafe5.png")

# Cambiar el tema de la página principal
st.markdown(
    """
    <style>
    .stApp {
        background-color: #e9ecef;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Texto principal
texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL CAFÉ</u></h1>'

# Estilos CSS para el logo y el contenedor
estilos_css = f"""
    <style>
    .logo-container {{
        display: flex;
        align-items: center;
        justify-content: center;
    }}

    .logo-img {{
        height: 40px;
        width: auto;
        margin-left: 20px;
    }}
    </style>
    """

# --------------------------------------------------------------------------------------------------------------------

# loc_button = Button(label="Mi ubicación")
loc_button = st.button('Mi ubicación')
loc_button.js_on_event("button_click", CustomJS(code="""
    navigator.geolocation.getCurrentPosition(
        (loc) => {
            document.dispatchEvent(new CustomEvent("GET_LOCATION", {detail: {lat: loc.coords.latitude, lon: loc.coords.longitude}}))
        }
    )
    """))
result = streamlit_bokeh_events(
    loc_button,
    events="GET_LOCATION",
    key="get_location",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_LOCATION" in result:
        st.write(result.get("GET_LOCATION"))

# --------------------------------------------------------------------------------------------------------------------

# # Sample list of countries and cities
# countries = ["Spain", "USA", "Germany"]
# cities = {
#     "Spain": ["Madrid", "Barcelona"],
#     "USA": ["New York", "San Francisco"],
#     "Germany": ["Berlin", "Munich"]
# }


# # Sample coffee shop data (replace with actual data)
# coffee_shops = {
#     "Madrid": pd.DataFrame({
#         'lat': [40.4286, 40.4168],
#         'lon': [-3.7037, -3.7024]
#     }),
#     "Barcelona": pd.DataFrame({
#         'lat': [41.3879, 41.3962],
#         'lon': [2.1699, 2.1603]
#     }),
#     "New York": pd.DataFrame({
#         'lat': [40.7128, 40.7189],
#         'lon': [-74.0060, -74.0112]
#     }),
#     "San Francisco": pd.DataFrame({
#         'lat': [37.7749, 37.7824],
#         'lon': [-122.4194, -122.4090]
#     })
# }

# # Dropdown to select country
# selected_country = st.selectbox("Select a country:", countries)

# # Dropdown to select city based on country
# if selected_country:
#     selected_city = st.selectbox("Select a city:", cities[selected_country])

# # Display coffee shops on map
# if selected_city:
#     st.map(coffee_shops[selected_city])


# --------------------------------------------------------------------------------------------------------------------

# JavaScript code to get location
st.markdown("""
    <script>
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition((position) => {
                    const pos = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    fetch('/get_location', {
                        method: 'POST',
                        body: JSON.stringify(pos),
                        headers: {
                            'Content-Type': 'application/json'
                        }
                    })
                });
            }
        }
    </script>
""", unsafe_allow_html=True)

# Streamlit button
if st.button('Mi ubicación'):
    st.write('Button clicked. Check server for POST request.')
