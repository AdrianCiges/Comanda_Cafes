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
    
# Lista de capitales de provincia de España con sus coordenadas
capitales_espana = [
                    {"ciudad": "Madrid", "latitud": 40.416775, "longitud": -3.703790},
                    {"ciudad": "Barcelona", "latitud": 41.385064, "longitud": 2.173403},
                    {"ciudad": "Valencia", "latitud": 39.469907, "longitud": -0.376288},
                    {"ciudad": "Sevilla", "latitud": 37.389092, "longitud": -5.984459},
                    {"ciudad": "Zaragoza", "latitud": 41.648822, "longitud": -0.889085},
                    {"ciudad": "Málaga", "latitud": 36.721302, "longitud": -4.421636},
                    {"ciudad": "Murcia", "latitud": 37.983810, "longitud": -1.129519},
                    {"ciudad": "Palma de Mallorca", "latitud": 39.569600, "longitud": 2.650160},
                    {"ciudad": "Las Palmas de Gran Canaria", "latitud": 28.124822, "longitud": -15.430006},
                    {"ciudad": "Santa Cruz de Tenerife", "latitud": 28.469581, "longitud": -16.254568},
                    {"ciudad": "Córdoba", "latitud": 37.888175, "longitud": -4.779383},
                    {"ciudad": "Valladolid", "latitud": 41.652251, "longitud": -4.724532},
                    {"ciudad": "Vitoria-Gasteiz", "latitud": 42.846718, "longitud": -2.672695},
                    {"ciudad": "Pamplona", "latitud": 42.817987, "longitud": -1.643252},
                    {"ciudad": "Logroño", "latitud": 42.462719, "longitud": -2.450592},
                    {"ciudad": "Oviedo", "latitud": 43.361914, "longitud": -5.849388},
                    {"ciudad": "Santander", "latitud": 43.462306, "longitud": -3.809980},
                    {"ciudad": "Toledo", "latitud": 39.861176, "longitud": -4.020876},
                    {"ciudad": "Granada", "latitud": 37.176164, "longitud": -3.597006},
                    {"ciudad": "Almería", "latitud": 36.838163, "longitud": -2.459722},
                    {"ciudad": "Huelva", "latitud": 37.261421, "longitud": -6.944722},
                    {"ciudad": "Cádiz", "latitud": 36.529722, "longitud": -6.292220},
                    {"ciudad": "Cáceres", "latitud": 39.476110, "longitud": -6.372778},
                    {"ciudad": "Badajoz", "latitud": 38.878450, "longitud": -6.970100},
                    {"ciudad": "Salamanca", "latitud": 40.966167, "longitud": -5.664722},
                    {"ciudad": "Burgos", "latitud": 42.340006, "longitud": -3.699944},
                    {"ciudad": "León", "latitud": 42.598694, "longitud": -5.567077},
                    {"ciudad": "Zamora", "latitud": 41.503471, "longitud": -5.743956},
                    {"ciudad": "Ávila", "latitud": 40.655014, "longitud": -4.700354},
                    {"ciudad": "Segovia", "latitud": 40.948654, "longitud": -4.118537},
                    {"ciudad": "Soria", "latitud": 41.762349, "longitud": -2.464682},
                    {"ciudad": "Teruel", "latitud": 40.343238, "longitud": -1.106177},
                    {"ciudad": "Ceuta", "latitud": 35.889681, "longitud": -5.321319},
                    {"ciudad": "Melilla", "latitud": 35.293981, "longitud": -2.938097}
                    ]
                    
# Función para obtener coordenadas
def obtener_coordenadas(ciudad):
    for capital in capitales_espana:
        if capital["ciudad"] == ciudad:
            return capital["latitud"], capital["longitud"]
    return None, None

@st.cache_data
def get_data():
    data_url = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cafeterias_espana.xlsx')
    df = pd.read_excel(data_url)
    df = df.drop('Unnamed: 0', axis=1)
    return df

# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# -------------------------------------------------------------------------------UBI A MANO ⬇️-------------------------------------

num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")
st.markdown(f"# Tus {num_cafeterias} cafeterías más cercanas", unsafe_allow_html=True)

copipaste = st.sidebar.checkbox('Pegar info del mapa "**📍ENCONTRAR MI UBICACAIÓN**"')

# Entrada de texto con valor predeterminado
coords = st.sidebar.text_input("Pega aquí las coordenadas tal como aparecen:", "Latitude: 40.4336 Longitude: -3.7043")

# Comprueba si el valor de coords ha cambiado
coords_changed = coords != "Latitude: 40.4336 Longitude: -3.7043"

# Si coords ha cambiado, comprime el desplegable; de lo contrario, mantenlo expandido
with st.expander('**📍ENCONTRAR MI UBICACAIÓN**', expanded=not coords_changed):   
        
    col1, col2 = st.columns([4, 1])
    options = list(leafmap.basemaps.keys())
    index = options.index("OpenTopoMap")
    
    with col2:
        basemap = st.selectbox("Select a basemap:", options, index)
    
    with col1:
        m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=False, minimap_control=True)
        m.add_basemap(basemap)
        m.to_streamlit(height=600, width=685)


# -------------------------------------------------------------------------------UBI A MANO ⬆️-------------------------------------
# ---------------------------------------------------------------------------------MAPEANDO ⬇️-------------------------------------


layout = st.sidebar.columns([1, 1])

#copipaste = st.sidebar.checkbox('Pegar info del mapa "**📍ENCONTRAR MI UBICACAIÓN**"')

if copipaste:
    # Inyectamos CSS personalizado para cambiar el color del texto predeterminado en text_input
    st.markdown("""
        <style>
            div.stTextInput > div > div > input {
                color: grey;
            }
        </style>
        """, unsafe_allow_html=True)
    
    # Entrada de texto con valor predeterminado
    coords = st.sidebar.text_input("Pega aquí las coordenadas tal como aparecen:", "Latitude: 40.4336 Longitude: -3.7043")

    try:
        latitud = round(float(coords.split(' ')[1]), 4)
        longitud = round(float(coords.split(' ')[3]), 4)
    except:
        latitud = 40.4336
        longitud = -3.7043
        st.sidebar.warning('Hay un error en tus coordenadas. Asegúrate que pegar el texto tal y como aparece en el mapa del desplegable.')

else:
    with layout[0]: 
        latitud = st.number_input(
            label="Latitud",
            min_value=-90.0000,  # Valor mínimo
            max_value=90.0000,   # Valor máximo
            value=40.4336,       # Valor predeterminado
            step=0.0100,         # Incremento
            format="%.4f"        # Formato de presentación
        )

    with layout[-1]: 
        longitud = st.number_input(
            label="Longitud:",
            min_value=-90.0000,  # Valor mínimo
            max_value=90.0000,   # Valor máximo
            value=-3.7043,       # Valor predeterminado
            step=0.0100,         # Incremento
            format="%.4f"        # Formato de presentación
        )

# st.sidebar.success('Puedes encontrar tus coordenadas en el desplegable "**📍ENCONTRAR MI UBICACAIÓN**"')



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
