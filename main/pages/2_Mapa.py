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
from bokeh.io import show
from bokeh.plotting import gmap
from bokeh.models import GMapOptions
from bokeh.models import ColumnDataSource
from bokeh.palettes import Set3
from bokeh.palettes import Category20
from bokeh.palettes import RdBu3
from bokeh.resources import CDN
from bokeh.embed import file_html
import math

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

# -------------------------------------------------------------------------------FUNCIONA-------------------------------------

loc_button = Button(label="Mi ubicación")
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
        st.write(f"Tu ubicación es: {result.get('GET_LOCATION')}")
        ubi = result.get("GET_LOCATION")

# --------------------------------------------------------------------------------------------------------------------
        latitude = 40
        longitude = -3
        data = pd.DataFrame({'LAT': [latitude], 'LON': [longitude]})
        st.map(data, zoom=10)




        # #bokeh_width, bokeh_height = ubi["lat"], ubi["lon"]
        
        # import streamlit as st
        # from bokeh.plotting import figure
        # from bokeh.tile_providers import get_provider, Vendors
        
        # # Coordinates
        # latitude = 40
        # longitude = -3
        
        # # Convert latitude and longitude to Web Mercator format
        # def lonlat_to_mercator(lon, lat):
        #     lat_rad = lat * (3.141592653589793 / 180.0)
        #     merc_x = lon * 20037508.34 / 180.0
        #     merc_y = (180.0 / 3.141592653589793) * \
        #              (6378137.0 * 3.141592653589793 * \
        #               0.25 * \
        #               (math.log(1.0 + math.sin(lat_rad)) -
        #                math.log(1.0 - math.sin(lat_rad))))
        #     return merc_x, merc_y
        
        # # Create Bokeh figure
        # tile_provider = get_provider(Vendors.CARTODBPOSITRON)
        # p = figure(x_range=(-2000000, 6000000), y_range=(-1000000, 7000000),
        #            x_axis_type="mercator", y_axis_type="mercator", width=800, height=600)
        # p.add_tile(tile_provider)
        
        # # Convert coordinates to Web Mercator
        # merc_x, merc_y = lonlat_to_mercator(ubi['lat'], ubi['lon'])
        
        # # Plot coordinates on the map
        # p.circle(x=[merc_x], y=[merc_y], size=10, color="red")
        
        # # Streamlit
        # st.bokeh_chart(p, use_container_width=True)
