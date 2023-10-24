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

# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# -------------------------------------------------------------------------------UBI USUARIO⬇️-------------------------------------

ubi_allow = st.checkbox("Encontrar cafeterías según mi ubicación")

if ubi_allow:
    
    loc_button = Button(label="Mi ubicación", width=150, height=50, button_type="success")
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
            ubi = result.get("GET_LOCATION")
            #st.write(f"Tu ubicación es: {ubi}")        
            latitude = ubi['lat']
            longitude = ubi['lon']
            try:
                city = get_city_from_coordinates(latitude, longitude) # Susceptible de timeout error!! Arreglar
            except:
                st.warning('No ha sido posible determinar tu ubicación. Por favor, selecciona tu ciudad en el siguiente desplegable.')

                direccion = st.text_input("Escribe la dirección:")

                if st.button("Obtener Coordenadas"):
                    if direccion:
                        # Crear un objeto geocoder de Nominatim
                        geolocator = Nominatim(user_agent="myGeocoder")
                
                        try:
                            # Obtener las coordenadas de la dirección ingresada
                            location = geolocator.geocode(direccion)
                            if location:
                                latitude = location.latitude
                                longitude = location.longitude
                                st.write(f"Las coordenadas de la dirección '{direccion}' son:")
                                st.write(f"Latitud: {latitude}")
                                st.write(f"Longitud: {longitude}")
                            else:
                                st.warning("No se encontraron coordenadas para la dirección ingresada.")
                        except Exception as e:
                            st.error(f"Ocurrió un error al obtener las coordenadas: {str(e)}")
                    else:
                        st.warning("Por favor, ingresa una dirección antes de hacer clic en 'Obtener Coordenadas'.")
                ciudades_espana = [
                                    "Madrid", "Barcelona", "Valencia", "Sevilla", "Zaragoza", "Bilbao", "Granada", "Murcia", 
                                    "Toledo", "Salamanca", "Santiago de Compostela", "Palma de Mallorca", "Tenerife", "Cádiz",
                                    "Pamplona", "Valladolid", "Málaga", "Oviedo", "Córdoba", "Girona"
                                  ]
                verificar_ciudad = st.checkbox("Mi ciudad no aparece en el desplegable")
                if verificar_ciudad:
                    city = st.text_input("Indica aquí tu ciudad")
                else:
                    city = st.selectbox("Selecciona una ciudad de España", ciudades_espana)
                
            #st.write(f"La ciudad en las coordenadas ({latitude}, {longitude}) es: {city}")

# -------------------------------------------------------------------------------UBI USUARIO⬆️-------------------------------------
# ----------------------------------------------------------------------------------MAPEANDO⬇️-------------------------------------


        # Probando con folium
        m = folium.Map(location=[latitude, longitude], zoom_start=15) #, zoom_start=20
        red_icon = folium.Icon(color='red')
        folium.Marker(
            [latitude, longitude], popup='<div style="white-space: nowrap;">Estás aquí</div>', tooltip="Estás aquí", icon=red_icon
        ).add_to(m)

        if __name__ == "__main__":
            cafes_in_madrid = extract_cafeterias_in_madrid()
            
            # Crear un DataFrame a partir de la lista de cafeterías
            df = pd.DataFrame(cafes_in_madrid)

            df['lat_dif'] = [abs(float(lt) - latitude) for i,lt in enumerate(df['Latitude'])]
            df['lon_dif'] = [abs(float(lg) - longitude) for i,lg in enumerate(df['Longitude'])]
            df['dif_sum'] = df['lat_dif'] + df['lon_dif']
            
            sorted_df = df.sort_values(by='dif_sum', ascending=True)[:10]
            sorted_df = sorted_df.reset_index(drop=True)
            #sorted_df.index = range(1, len(sorted_df) + 1)
            sorted_df['Metros'] = [haversine_distance(latitude, longitude, e, sorted_df['Longitude'][i]) for i,e in enumerate(sorted_df['Latitude'])]

            # sorted_df = sorted_df.reset_index(drop=True)
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

# -----------------------------------------------------------------------------------SIN UBI⬇️-------------------------------------

else:
    st.write('Building')



# -----------------------------------------------------------------------------------SIN UBI⬆️-------------------------------------
