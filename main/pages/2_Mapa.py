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

bokeh_width, bokeh_height = ubi["lat"], ubi["lon"]

def plotAll(data, zoom=15, map_type='roadmap'):
    gmap_options = GMapOptions(lat=data[0][1], lng=data[0][2], 
                               map_type=map_type, zoom=zoom)
    p = gmap(GOOGLE_API_KEY, gmap_options, title='AwanTunai - Risk Intelligence', 
             width=bokeh_width, height=bokeh_height)
    
    latArr = []
    longArr = []
    colorArr = []
    labelArr = []
    colidx = 0
    colpalette =
 Category20.get(20)
    print(‘palette length: ‘, len(Set3))
    
    for x in data:
        if(x[4] == ‘Stationary’):
          latArr.append(x[1])
          longArr.append(x[2])
          labelArr.append(x[3])
          if(colidx == len(colpalette)):
              colidx=0
          colorArr.append(colpalette[colidx])
          colidx+=1
    
    print(‘latArr: ‘, latArr)
    print(‘longArr: ‘, longArr)
    print(‘colorArr: ‘, colorArr)
    print(‘label: ‘, labelArr)
    
    source = ColumnDataSource(dict(
                x=longArr,
                y=latArr,
                color=colorArr,
                label=labelArr
            ))
    
    center = p.circle(x=’x’, y=’y’, size=10, alpha=0.9, color=’color’, legend_group=’label’, source=source)
    
    if RESIDENCE_LATLONG is not None:
        p.triangle([RESIDENCE_LATLONG[1]], [RESIDENCE_LATLONG[0]], size=10, alpha=0.9, color=’red’)
    if BUSINESS_LATLONG is not None:
        p.triangle([BUSINESS_LATLONG[1]], [BUSINESS_LATLONG[0]], size=10, alpha=0.9, color=’blue’)
    html = file_html(p, CDN, "User locations")
    return html

import streamlit.components.v1 as components
if len(data) > 0:
    components.html(plotAll(data, 15, 'satellite'), height = bokeh_height + 100, width = bokeh_width + 100)
else:
    st.write('no location data found')
