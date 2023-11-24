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
from streamlit_js_eval import streamlit_js_eval, copy_to_clipboard, create_share_link, get_geolocation
import json
import googlemaps

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

# Ruta de la imagen del logo
LOGO_IMAGE = "./img/mapa.png"

# Texto principal
texto_principal = '<h1 style="text-align:center"><span style="font-size: 40px;">☕</span> <u>LA RUTA DEL CAFÉ</u></h1>'
    
# Leer la imagen del logo y codificarla en base64
with open(LOGO_IMAGE, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode()

# Mostrar el texto principal y el logo
st.markdown(estilos_css, unsafe_allow_html=True)
st.markdown(
    f'<div class="logo-container">{texto_principal}<img src="data:image/png;base64,{encoded_image}" class="logo-img"></div>',
    unsafe_allow_html=True
)

tab1, tab2 = st.tabs(["Open Street Map", "Google Maps API"])
    
# ------------------------------------------------------------------------------------CONFIG⬆️-------------------------------------
# ---------------------------------------------------------------------------------FUNCIONES⬇️-------------------------------------

# def extract_cafeterias_in_madrid():
#     api = overpy.Overpass()

#     # Definimos una consulta para extraer las cafeterías en Madrid
#     query = f"""
#     area["name"="{city}"];
#     node["amenity"="cafe"](area);
#     out;
#     """

#     result = api.query(query)

#     cafes = []

#     for node in result.nodes:
#         cafe_info = {
#             "Name": node.tags.get("name", "No especificado"),
#             "Tlf": node.tags.get("phone", "-"),
#             "Web": node.tags.get("website", "-"),
#             "Facebook": node.tags.get("contact:facebook", "-"),
#             "Calle": node.tags.get("addr:street", "-"),
#             "Numero": node.tags.get("addr:housenumber", ""),
#             "Horario": node.tags.get("opening_hours", "No especificado"),
#             "Terraza": node.tags.get("outdoor_seating", "No especificado").capitalize(),
#             "Latitude": float(node.lat),
#             "Longitude": float(node.lon)
#         }
#         cafes.append(cafe_info)

#     return cafes


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

def buscar_cafeterias(latitud, longitud, key, radio=10000):
    # Configurar la clave de API

    gmaps = googlemaps.Client(key=key)

    # Realizar la búsqueda
    resultados = gmaps.places_nearby(location=(latitud, longitud), radius=radio, type='cafe')

    # Extraer la información deseada
    cafeterias = []
    for lugar in resultados['results']:
        # Detalles básicos
        place_id = lugar.get('place_id', None)
        nombre = lugar.get('name', None)
        latitud = lugar.get('geometry', {}).get('location', None).get('lat')
        longitud = lugar.get('geometry', {}).get('location', None).get('lng')
        rating = lugar.get('rating', None)
        opiniones = lugar.get('user_ratings_total', None)

        # Obtener detalles del lugar
        detalles = gmaps.place(place_id=place_id)
        abierto_ahora = detalles.get('result', {}).get('current_opening_hours', {}).get('open_now', None)
        wheelchair_accessible_entrance = detalles.get('result', {}).get('wheelchair_accessible_entrance', None) 
        price_level = detalles.get('result', {}).get('price_level', None)
        reservable = detalles.get('result', {}).get('reservable', None)
        
        # Más detalles
        serves_breakfast = detalles.get('result', {}).get('serves_breakfast', None)
        serves_brunch = detalles.get('result', {}).get('serves_brunch', None)
        serves_lunch = detalles.get('result', {}).get('serves_lunch', None)
        serves_dinner = detalles.get('result', {}).get('serves_dinner', None)
        serves_vegetarian_food = detalles.get('result', {}).get('serves_vegetarian_food', None)
        serves_beer = detalles.get('result', {}).get('serves_beer', None)
        serves_wine = detalles.get('result', {}).get('serves_wine', None)
        takeout = detalles.get('result', {}).get('takeout', None)
        url = detalles.get('result', {}).get('url')

        cafeterias.append([nombre, abierto_ahora, latitud, longitud, rating, 
                           opiniones, wheelchair_accessible_entrance, reservable, price_level,
                           serves_breakfast, serves_brunch, serves_lunch, serves_dinner,
                           serves_vegetarian_food, serves_beer, serves_wine, takeout, url])

        # Convertir a DataFrame
        df_cafeterias = pd.DataFrame(cafeterias, columns=['nombre', 'abierto_ahora', 'latitud', 'longitud', 'rating', 
                                                          'opiniones', 'wheelchair_accessible_entrance', 'reservable','price_level',
                                                          'serves_breakfast', 'serves_brunch', 'serves_lunch', 'serves_dinner',
                                                          'serves_vegetarian_food', 'serves_beer', 'serves_wine', 'takeout', 'url'])

        return df_cafeterias

    # ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
    # --------------------------------------------------------------------------------------UBI ⬇️-------------------------------------

with tab1:
    
    num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")
    
    from_pc = st.sidebar.checkbox('Vista para ordenador')
    
    
    if num_cafeterias != 1:
        st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -50px;'>Tus {num_cafeterias} cafeterías más cercanas</h2>", unsafe_allow_html=True)
    else:
        st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -50px;'>Tu cafetería más cercana</h2>", unsafe_allow_html=True)
    
    
    loc = get_geolocation()
    
    if st.checkbox('📍 Usar mi ubicación'):
        location = [loc]
        latitud = location[0]['coords']['latitude']
        longitud = location[0]['coords']['longitude']
    try:
        latitud = round(float(latitud), 4)
        longitud = round(float(longitud), 4)
    except:
        latitud = 40.4336
        longitud = -3.7043
    
    
    # # MAPEAR
    # with st.expander('**📍ENCONTRAR MI UBICACIÓN**', expanded=expander_expanded):   
    
    #     m = leafmap.Map(locate_control=True, latlon_control=True, draw_export=False, minimap_control=True)
    #     m.to_streamlit(height=600, width=685)
    
    df = get_data()
    
    if latitud == 40.4336 and longitud == -3.7043:
        st.warning('Estás utilizando la ubicación predeterminada en Glorieta de Quevedo. Para usar tu ubicación, marca la casilla de "📍 Usar mi ubicación"')
    
    latitude = latitud
    longitude = longitud
    
    
    
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
    
    if from_pc:
        folium_static(m, width=1025)
    else:
        folium_static(m, width=380)

with tab2:
    
    loc1 = get_geolocation()
    
    if st.checkbox('📍 Usar mi ubicación   '):
        location = [loc1]
        latitud = location[0]['coords']['latitude']
        longitud = location[0]['coords']['longitude']
    try:
        latitud = round(float(latitud), 4)
        longitud = round(float(longitud), 4)
    except:
        latitud = 40.4336
        longitud = -3.7043

        # latitud_usuario = st.number_input("Ingrese la latitud:", min_value=-90.0000, max_value=90.0000, value=40.4336)
        # longitud_usuario = st.number_input("Ingrese la longitud:", min_value=-180.0000, max_value=180.0000, value=-3.7043)
        # key = st.text_input("Ingrese API key de Google Maps ")

        # if key:
        #     df_resultante = buscar_cafeterias(latitud_usuario, longitud_usuario, key)
        #     st.table(df_resultante)
        # else:
        #     if latitud == 40.4336 and longitud == -3.7043:
        #         st.warning('Estás utilizando la ubicación predeterminada en Glorieta de Quevedo. Para usar tu ubicación, marca la casilla de "📍 Usar mi ubicación"')
