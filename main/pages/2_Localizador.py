import streamlit as st
import pandas as pd
import overpy
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
import math
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import urllib.parse
import geocoder
import os
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide", page_title="Ruta del Café", page_icon="./img/cafe5.png")

# Inyectar CSS personalizado para centrar todo el contenido de la página
st.markdown("""
    <style>
        .reportview-container {
            flex-direction: column;
            display: flex;
            align-items: center;
            justify-content: center !important;
        }
        .reportview-container .main {
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 65%;
        }
    </style>
    """, unsafe_allow_html=True)



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

# ------------------------------------------------------------------------------------CONFIG⬆️-------------------------------------
# ---------------------------------------------------------------------------------FUNCIONES⬇️-------------------------------------

def extract_cafeterias_in_madrid():
    api = overpy.Overpass()

    # Definimos una consulta para extraer las cafeterías en Madrid
    query = f"""
    area["name"="{city}"];
    node["amenity"="cafe"](area);
    out;
    """

    result = api.query(query)

    cafes = []

    for node in result.nodes:
        cafe_info = {
            "Name": node.tags.get("name", "No especificado"),
            "Tlf": node.tags.get("phone", "-"),
            "Web": node.tags.get("website", "-"),
            "Facebook": node.tags.get("contact:facebook", "-"),
            "Calle": node.tags.get("addr:street", "-"),
            "Numero": node.tags.get("addr:housenumber", ""),
            "Horario": node.tags.get("opening_hours", "No especificado"),
            "Terraza": node.tags.get("outdoor_seating", "No especificado").capitalize(),
            "Latitude": float(node.lat),
            "Longitude": float(node.lon)
        }
        cafes.append(cafe_info)

    return cafes

def get_city_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="city_finder")
    
    # Obtener la dirección completa a partir de las coordenadas
    location = geolocator.reverse((latitude, longitude), exactly_one=True) # Susceptible de timeout error!! Arreglar
    
    # Extraer la ciudad de la dirección
    if location:
        address = location.address
        address_parts = address.split(", ")
        city = address_parts[-4]  # La ciudad generalmente se encuentra en la tercera posición desde el final
        return city
    else:
        return "No se pudo encontrar la ciudad"

def convert_coordinates(input_string):
    # Dividir las coordenadas en latitud y longitud
    lat, lon = map(float, input_string.split(', '))

    # Convertir la latitud a grados, minutos y segundos
    lat_deg = int(lat)
    lat_min = int((lat - lat_deg) * 60)
    lat_sec = (lat - lat_deg - lat_min / 60) * 3600

    # Convertir la longitud a grados, minutos y segundos
    lon_deg = int(lon)
    lon_min = int((lon - lon_deg) * 60)
    lon_sec = (lon - lon_deg - lon_min / 60) * 3600

    # Construir la cadena de salida en el formato deseado
    if "-" in str(lat) and "-" in str(lon):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"S+{lon_deg}°{lon_min}'{lon_sec:.1f}\"W"
    elif "-" in str(lat):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"S+{lon_deg}°{lon_min}'{lon_sec:.1f}\"E"
    elif "-" in str(lon):
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"N+{lon_deg}°{lon_min}'{lon_sec:.1f}\"W"
    else:
        output_string = f"{lat_deg}°{lat_min}'{lat_sec:.1f}\"N+{lon_deg}°{lon_min}'{lon_sec:.1f}\"E"

    return output_string.replace("-","")

def make_clickable(val):
    # target _blank to open new window
    return '<a target="_blank" href="{}">{}</a>'.format(val,val)

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance in meters between two points
    on the Earth's surface identified by latitude and longitude.
    :param lat1: Latitude of the first point (in degrees)
    :param lon1: Longitude of the first point (in degrees)
    :param lat2: Latitude of the second point (in degrees)
    :param lon2: Longitude of the second point (in degrees)
    :return: Distance in meters
    """
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    radius_earth = 6371000  # Earth's radius in meters
    distance = radius_earth * c

    return int(distance)

@st.cache_data
def get_data():
    data_url = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cafeterias_espana.xlsx')
    df = pd.read_excel(data_url)
    df = df.drop('Unnamed: 0', axis=1)
    return df

# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# -------------------------------------------------------------------------------UBI A MANO ⬇️-------------------------------------

# Inicializar las variables en st.session_state si no existen
if "coords_changed" not in st.session_state:
    st.session_state.coords_changed = False

num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")
st.markdown(f"# Tus {num_cafeterias} cafeterías más cercanas", unsafe_allow_html=True)

# Inyectamos CSS personalizado para cambiar el color del texto predeterminado en text_input
st.markdown("""
    <style>
        div.stTextInput > div > div > input {
            color: grey;
        }
    </style>
    """, unsafe_allow_html=True)

coords = st.sidebar.text_input("Pega aquí las coordenadas tal como aparecen:", "Latitude: 40.4336 Longitude: -3.7043")
st.session_state.coords_changed = coords != "Latitude: 40.4336 Longitude: -3.7043"

try:
    latitud = round(float(coords.split(' ')[1]), 4)
    longitud = round(float(coords.split(' ')[3]), 4)
except:
    latitud = 40.4336
    longitud = -3.7043
    st.sidebar.warning('Hay un error en tus coordenadas. Asegúrate que pegar el texto tal y como aparece en el mapa del desplegable.')

# Determinar si el st.expander debe estar comprimido
expander_expanded = not st.session_state.coords_changed

# MAPEAR
with st.expander('**📍ENCONTRAR MI UBICACIÓN**', expanded=expander_expanded):       
    m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=False, minimap_control=True)
    m.to_streamlit(height=600, width=685)



df = get_data()

if latitud == 40.4336 and longitud == -3.7043:
    st.warning('Estás utilizando la ubicación predeterminada en Glorieta de Quevedo. Para cambiarla usa el menú lateral.')


latitude = latitud
longitude = longitud

# MAPEANDO CON UBI A MANO
m = folium.Map(location=[latitude, longitude], zoom_start=15)
red_icon = folium.Icon(color='red')
folium.Marker(
    [latitude, longitude], popup='<div style="white-space: nowrap;">Tu ubicación</div>', tooltip="Tu ubicación", icon=red_icon
).add_to(m)

df['lat_dif'] = [abs(float(lt) - latitude) for i,lt in enumerate(df['Latitude'])]
df['lon_dif'] = [abs(float(lg) - longitude) for i,lg in enumerate(df['Longitude'])]
df['dif_sum'] = df['lat_dif'] + df['lon_dif']

sorted_df = df.sort_values(by='dif_sum', ascending=True)[:num_cafeterias]
sorted_df = sorted_df.reset_index(drop=True)
sorted_df['Metros'] = [haversine_distance(latitude, longitude, e, sorted_df['Longitude'][i]) for i,e in enumerate(sorted_df['Latitude'])]

coords = []
for i,e in enumerate(sorted_df['Latitude']):
    coords.append(str(e) + ", " +str(sorted_df['Longitude'][i]))
sorted_df['coords'] = coords
sorted_df['Cómo llegar'] = ['https://www.google.com/maps/search/'+convert_coordinates(e) for e in sorted_df['coords']]

for index, row in sorted_df.iterrows():
    # Crea el popup con el enlace clickeable que se abrirá en una nueva ventana
    
    link = sorted_df["Cómo llegar"][index].replace('"', '%22')
    popup_content = f'<div style="white-space: nowrap;">A {row["Metros"]} metros: <strong><a href="{link}" target="_blank" style="text-decoration: underline; cursor: pointer;">{row["Name"]}</a></strong></div>'

    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=popup_content,
    ).add_to(m)

folium_static(m)
