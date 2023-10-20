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

import streamlit as st
import pandas as pd
import requests
from streamlit_folium import folium_static
import folium

# Sample Country and City lists (replace with actual data)
countries = ["USA", "Spain", "France"]
cities = {
    "USA": ["New York", "San Francisco"],
    "Spain": ["Madrid", "Barcelona"],
    "France": ["Paris", "Lyon"]
}

# Country dropdown
selected_country = st.selectbox("Select a country:", countries)

# City dropdown
if selected_country:
    selected_city = st.selectbox("Select a city:", cities[selected_country])

# Fetch and Display Coffee Shops (this is an example; replace with actual data fetching)
if selected_city:
    # You would typically fetch real data from Google Places API or OpenStreetMap API here
    # For demonstration, let's assume we fetched the following coffee shop coordinates for the selected city
    sample_data = pd.DataFrame({
        'lat': [40.4286, 40.4168],
        'lon': [-3.7037, -3.7024],
        'name': ['Coffee Shop 1', 'Coffee Shop 2']
    })

    # Create a folium map centered around the first coffee shop coordinates
    m = folium.Map(location=[sample_data.iloc[0]['lat'], sample_data.iloc[0]['lon']], zoom_start=15)

    # Add coffee shop markers to the map
    for idx, row in sample_data.iterrows():
        folium.Marker([row['lat'], row['lon']], popup=row['name']).add_to(m)

    # Render map
    folium_static(m)

