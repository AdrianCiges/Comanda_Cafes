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
# from bokeh.io import show
# from bokeh.plotting import gmap
# from bokeh.models import GMapOptions
# from bokeh.models import ColumnDataSource
# from bokeh.palettes import Set3
# from bokeh.palettes import Category20
# from bokeh.palettes import RdBu3
# from bokeh.resources import CDN
# from bokeh.embed import file_html
import math
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim

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

def extract_cafeterias_in_madrid():
    api = overpy.Overpass()

    # Definimos una consulta para extraer las cafeterías en Madrid
    query = """
    area["name"="Madrid"];
    node["amenity"="cafe"](area);
    out;
    """

    result = api.query(query)

    cafes = []

    for node in result.nodes:
        cafe_info = {
            "Name": node.tags.get("name", "DESCONOCIDO"),
            "Tlf": node.tags.get("phone", "-"),
            "Web": node.tags.get("website", "-"),
            "Facebook": node.tags.get("contact:facebook", "-"),
            "Calle": node.tags.get("addr:street", "-"),
            "Numero": node.tags.get("addr:housenumber", ""),
            "Horario": node.tags.get("opening_hours", "-"),
            "Terraza": node.tags.get("outdoor_seating", "DESCONOCIDO"),
            "Latitude": float(node.lat),
            "Longitude": float(node.lon)
        }
        cafes.append(cafe_info)

    return cafes

def get_city_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="city_finder")
    
    # Obtener la dirección completa a partir de las coordenadas
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    
    # Extraer la ciudad de la dirección
    if location:
        address = location.address
        address_parts = address.split(", ")
        city = address_parts[-4]  # La ciudad generalmente se encuentra en la tercera posición desde el final
        return city
    else:
        return "No se pudo encontrar la ciudad"
        
# -------------------------------------------------------------------------------FUNCIONA-------------------------------------

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
        st.write(f"Tu ubicación es: {ubi}")        
        latitude = ubi['lat']
        longitude = ubi['lon']
        city = get_city_from_coordinates(latitude, longitude)
        st.write(f"La ciudad en las coordenadas ({latitude}, {longitude}) es: {city}")

# --------------------------------------------------------------------------------------------------------------------
        
        
        # data = pd.DataFrame({'LAT': [latitude], 'LON': [longitude]})
        # st.map(data, zoom=100)
        

        # Probando con folium
        m = folium.Map(location=[latitude, longitude], zoom_start=20)
        red_icon = folium.Icon(color='red')
        folium.Marker(
            [latitude, longitude], popup="Estás aquí", tooltip="Estás aquí",icon=red_icon
        ).add_to(m)
        
        # call to render Folium map in Streamlit
        st_data = folium_static(m)


        if __name__ == "__main__":
            cafes_in_madrid = extract_cafeterias_in_madrid()
            
            # Crear un DataFrame a partir de la lista de cafeterías
            df = pd.DataFrame(cafes_in_madrid)
            lat_max = latitude+0.005
            lat_min = latitude-0.005
            lon_max = longitude+0.01
            lon_min = longitude-0.01
            filtered_df = df[(df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) & (df['Longitude'] >= lon_min) & (df['Longitude'] <= lon_max)]
    
            # st.table(df)

            # Crea un mapa de Folium centrado en una ubicación inicial
            # m = folium.Map(location=[df["Latitude"].mean(), df["Longitude"].mean()], zoom_start=30)
            
            # Agrega marcadores para cada par de latitud y longitud en el DataFrame
            for index, row in filtered_df.iterrows():
                folium.Marker(
                    location=[row["Latitude"], row["Longitude"]],
                    popup=f"{row['Name']}, Ubi: {row['Calle']} {row['Numero']}",
                ).add_to(m)
            
            # Muestra el mapa interactivo en Streamlit
            st.write("Mapa de ubicaciones:")
            st_data2 = folium_static(m)


# --------------------------------------------------------------------------------------------------------------------

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
