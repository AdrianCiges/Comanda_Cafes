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
import streamlit as st
import smtplib
from email.mime.text import MIMEText
import streamlit.components.v1 as components
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)

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

    
# ------------------------------------------------------------------------------------CONFIG⬆️-------------------------------------
# ---------------------------------------------------------------------------------FUNCIONES⬇️-------------------------------------

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
    data_url = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'cafeterias_horarios_ocupacion.xlsx')
    df = pd.read_excel(data_url)
    df = df.drop('Columna1', axis=1)
    return df

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("🔽 Añadir filtros")
    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        columnas_filtro = ['Nombre', 'Ciudad','Nivel de precios','Puntuación', 'Nº Comentarios', 'Horario hoy', 'Ocupación Ahora'
                             'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
                             'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
                          ]
        to_filter_columns = st.multiselect("Filtrar tabla por:", columnas_filtro, placeholder="Selecciona un campo")
        for column in to_filter_columns:
            left, right = st.columns((1, 20))
            left.write("↳")
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Valores de {column}",
                    df[column].unique(),
                    default=list(df[column].unique()),
                )
                df = df[df[column].isin(user_cat_input)]
            elif is_numeric_dtype(df[column]):
                _min = float(df[column].min())
                _max = float(df[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"{column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                df = df[df[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(df[column]):
                user_date_input = right.date_input(
                    f"Valores de {column}",
                    value=(
                        df[column].min(),
                        df[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    df = df.loc[df[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Buscar {column}",
                )
                if user_text_input:
                    df = df[df[column].astype(str).str.contains(user_text_input)]

    return df

# def buscar_cafeterias(latitud, longitud, key, radio=10000):
#     # Configurar la clave de API

#     gmaps = googlemaps.Client(key=key)

#     # Realizar la búsqueda
#     resultados = gmaps.places_nearby(location=(latitud, longitud), radius=radio, type='cafe')

#     # Extraer la información deseada
#     cafeterias = []
#     for lugar in resultados['results']:
#         # Detalles básicos
#         place_id = lugar.get('place_id', None)
#         nombre = lugar.get('name', None)
#         latitud = lugar.get('geometry', {}).get('location', None).get('lat')
#         longitud = lugar.get('geometry', {}).get('location', None).get('lng')
#         rating = lugar.get('rating', None)
#         opiniones = lugar.get('user_ratings_total', None)

#         # Obtener detalles del lugar
#         detalles = gmaps.place(place_id=place_id)
#         abierto_ahora = detalles.get('result', {}).get('current_opening_hours', {}).get('open_now', None)
#         wheelchair_accessible_entrance = detalles.get('result', {}).get('wheelchair_accessible_entrance', None) 
#         price_level = detalles.get('result', {}).get('price_level', None)
#         reservable = detalles.get('result', {}).get('reservable', None)
        
#         # Más detalles
#         serves_breakfast = detalles.get('result', {}).get('serves_breakfast', None)
#         serves_brunch = detalles.get('result', {}).get('serves_brunch', None)
#         serves_lunch = detalles.get('result', {}).get('serves_lunch', None)
#         serves_dinner = detalles.get('result', {}).get('serves_dinner', None)
#         serves_vegetarian_food = detalles.get('result', {}).get('serves_vegetarian_food', None)
#         serves_beer = detalles.get('result', {}).get('serves_beer', None)
#         serves_wine = detalles.get('result', {}).get('serves_wine', None)
#         takeout = detalles.get('result', {}).get('takeout', None)
#         url = detalles.get('result', {}).get('url')

#         cafeterias.append([nombre, abierto_ahora, latitud, longitud, rating, 
#                            opiniones, wheelchair_accessible_entrance, reservable, price_level,
#                            serves_breakfast, serves_brunch, serves_lunch, serves_dinner,
#                            serves_vegetarian_food, serves_beer, serves_wine, takeout, url])

#         # Convertir a DataFrame
#         df_cafeterias = pd.DataFrame(cafeterias, columns=['nombre', 'abierto_ahora', 'latitud', 'longitud', 'rating', 
#                                                           'opiniones', 'wheelchair_accessible_entrance', 'reservable','price_level',
#                                                           'serves_breakfast', 'serves_brunch', 'serves_lunch', 'serves_dinner',
#                                                           'serves_vegetarian_food', 'serves_beer', 'serves_wine', 'takeout', 'url'])

#         return df_cafeterias


# def convertir_a_decimal(hora_str):
#     # Normalizar la cadena para unificar los formatos de AM/PM y eliminar espacios no estándar
#     hora_str = re.sub(r'\s+', ' ', hora_str)  # Convierte todos los espacios a espacios estándar
#     hora_str = hora_str.replace('\xa0', ' ').upper()  # Reemplaza espacios no separables y normaliza a mayúsculas
#     hora_str = re.sub(r'([AP])\.?\s*M\.?', r'\1M', hora_str)  # Normaliza las marcas de AM/PM

#     # Extraer horas, minutos y periodo (AM/PM) utilizando una expresión regular
#     match = re.match(r'(\d+):?(\d*)\s*([AP]M)?', hora_str)
#     if match:
#         horas, minutos, periodo = match.groups()
#         horas = int(horas)
#         minutos = int(minutos) if minutos else 0
#         if periodo == 'PM' and horas < 12:
#             horas += 12
#         elif periodo == 'AM' and horas == 12:
#             horas = 0
        
#         # Convertir horas y minutos a formato decimal
#         hora_decimal = horas + minutos / 60
        
#         return round(hora_decimal, 2)
#     return None

# def procesar_horarios(horarios):
#     intervalos_finales = []
#     for horario in horarios:
#         # Inicializar una lista para este horario, que podría contener uno o dos intervalos
#         intervalos_de_este_horario = []
#         partes = horario.split(',')
#         for parte in partes:
#             # Usar expresión regular para dividir en 'inicio' y 'fin', manejando posibles errores
#             match = re.match(r'(.*?)(?:\s+to\s+)(.*)', parte.strip(), re.IGNORECASE)
#             if match:
#                 inicio, fin = match.groups()
#                 inicio_decimal = convertir_a_decimal(inicio)
#                 fin_decimal = convertir_a_decimal(fin)
#                 # Ajuste por cruce de medianoche si es necesario
#                 if fin_decimal < inicio_decimal:
#                     fin_decimal += 24
#                 intervalos_de_este_horario.append([inicio_decimal, fin_decimal])
#             else:
# #                 print(f"No se pudo procesar el intervalo: {parte}")
# #                 intervalos_de_este_horario.append('Desconocido')
#                 pass
#         # Añadir los intervalos procesados para este horario a la lista final
#         intervalos_finales.append(intervalos_de_este_horario)
#     return intervalos_finales

# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# ------------------------------------------------------------------------------------TABLA ⬇️-------------------------------------















# ------------------------------------------------------------------------------------TABLA ⬆️-------------------------------------
# --------------------------------------------------------------------------------------UBI ⬇️-------------------------------------

loc = get_geolocation()
    
num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")

from_pc = st.sidebar.checkbox('Vista para ordenador')


if num_cafeterias != 1:
    st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tus {num_cafeterias} cafeterías más cercanas</h2>", unsafe_allow_html=True)
else:
    st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tu cafetería más cercana</h2>", unsafe_allow_html=True)
    

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


# Cargamos el dataframe (necesitamos optimizar esto)
df = get_data()

# Obtener la fecha y hora actual
ahora = datetime.now()
hora_actual = datetime.now().hour + 1

# Obtener el nombre del día de la semana en inglés
dia_semana_ing = ahora.strftime("%A")

# Diccionario para traducir el día de la semana al español
dias_semana_es = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "`domingo"}

# Traducir el día de la semana al español
dia_semana_es = dias_semana_es.get(dia_semana_ing, "Desconocido")

# Renombramos las columnas
nuevos_nombres = ['Link', 'Nombre', 'Ciudad','Nivel de precios','Latitud','Longitud','Puntuación', 'Nº Comentarios', 'Cerrado permanentemene', 'Cerrado temporalmente', 'Horario','Porcentaje de Ocupación', 'LGBT+ friendly', 'Sirve aperitivos', 'Tiene terraza', 'Sirve Cerveza', 'Sirve desayunos/almuerzos', 'Puedes sentarte', 'Para llevar', 'Sirve postres', 'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'Sirve vino', 
                   'horario_raw_lunes', 'horario_lunes', 
                   'horario_raw_martes', 'horario_martes', 
                   'horario_raw_miércoles', 'horario_miércoles',
                   'horario_raw_jueves', 'horario_jueves', 
                   'horario_raw_viernes', 'horario_viernes', 
                   'horario_raw_sábado', 'horario_sábado',
                   'horario_raw_domingo', 'horario_domingo', 
                   'ocupacion_lunes', 'ocupacion_martes', 'ocupacion_miércoles', 'ocupacion_jueves', 'ocupacion_viernes', 'ocupacion_sábado', 'ocupacion_domingo']

df.columns = nuevos_nombres

columna_dia_hoy_raw = "horario_raw_"+dia_semana_es
columna_dia_hoy = "horario_"+dia_semana_es
columna_ocupacion_hoy = "ocupacion_"+dia_semana_es
columna_ocupacion_ahora = []

for o in df[columna_ocupacion_hoy]:
    try:
        # Decodificar el JSON una sola vez
        ocupacion = json.loads(o.replace("'", '"'))
        # Buscar la hora actual dentro de los objetos decodificados
        encontrado = False
        for h in ocupacion:
            if h['hour'] == hora_actual:
                columna_ocupacion_ahora.append(h['occupancyPercent'])
                encontrado = True
                break  # Salir del bucle una vez encontrada la hora actual
        if not encontrado:
            # Si no se encuentra la hora actual, agregar 'Desconocido' o un valor por defecto
            columna_ocupacion_ahora.append(0)
    except json.JSONDecodeError:
        # Manejar cadenas vacías, malformadas o valores None
        columna_ocupacion_ahora.append(0)

df['Ocupación Ahora'] = columna_ocupacion_ahora


# Reordenamos el dataframe
df = df[['Link', 'Nombre', 'Ciudad','Nivel de precios','Latitud','Longitud','Puntuación', 'Nº Comentarios', columna_dia_hoy_raw, columna_dia_hoy, 'Ocupación Ahora', # columna_ocupacion_hoy
         'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
         'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
         'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
        ]]


# Renombramos las columnas
nuevos_nombres = ['Link', 'Nombre', 'Ciudad','Nivel de precios','Latitud','Longitud','Puntuación', 'Nº Comentarios', 'Horario hoy', 'Horario hoy base_10', 'Ocupación Ahora',
                  'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
                  'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
                  'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
                 ]

df.columns = nuevos_nombres
#❗Intentamos generar una columna con el horario actual ----------------------------------------------------------------------------------------------------------







# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

df = filter_dataframe(df)
st.dataframe(df.drop(['Link','Latitud','Longitud', 'Cerrado permanentemene', 'Cerrado temporalmente', 'Horario hoy base_10'], axis=1))
# df = df.drop_duplicates()

if latitud == 40.4336 and longitud == -3.7043:
    st.warning('Estás utilizando la ubicación predeterminada en Glorieta de Quevedo. Para usar tu ubicación, marca la casilla de "📍 Usar mi ubicación"')

latitude = latitud
longitude = longitud

m = folium.Map(location=[latitude, longitude], zoom_start=15)
red_icon = folium.Icon(color='red')
folium.Marker(
    [latitude, longitude], popup='<div style="white-space: nowrap;">Tu ubicación</div>', tooltip="Tu ubicación", icon=red_icon
).add_to(m)

df['lat_dif'] = [abs(float(lt) - latitude) for i,lt in enumerate(df['Latitud'])]
df['lon_dif'] = [abs(float(lg) - longitude) for i,lg in enumerate(df['Longitud'])]
df['dif_sum'] = df['lat_dif'] + df['lon_dif']

sorted_df = df.sort_values(by='dif_sum', ascending=True)[:num_cafeterias]
sorted_df = sorted_df.reset_index(drop=True)
sorted_df['Metros'] = [haversine_distance(latitude, longitude, e, sorted_df['Longitud'][i]) for i,e in enumerate(sorted_df['Latitud'])]

coords = []
for i,e in enumerate(sorted_df['Latitud']):
    coords.append(str(e) + ", " +str(sorted_df['Longitud'][i]))
sorted_df['coords'] = coords
# sorted_df['Cómo llegar'] = ['https://www.google.com/maps/search/'+convert_coordinates(e) for e in sorted_df['coords']]

for index, row in sorted_df.iterrows():
    # Crea el popup con el enlace clickeable que se abrirá en una nueva ventana
    
    link = sorted_df["Link"][index].replace('"', '%22')
    popup_content = f'<div style="white-space: nowrap;">A {row["Metros"]} metros: <strong><a href="{link}" target="_blank" style="text-decoration: underline; cursor: pointer;">{row["Nombre"]}</a></strong></div>'

    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=popup_content,
    ).add_to(m)

if from_pc:
    folium_static(m, width=1025)
else:
    folium_static(m, width=380)

# ---------------------------------------------------------------------------------------UBI ⬆️-------------------------------------
# --------------------------------------------------------------------------------------MAIL ⬇️-------------------------------------

st.write('')
st.write('')
st.write('')
st.write('## 🏙️ Información sobre los datos')
st.write('###### En el mapa encontrarás datos de diferentes municipios. Principalmente se han seleccionado aquellas localidades con más de 75.000 habitantes en España. Los municipios incluidos son los siguientes:')
st.selectbox('Busca tu municipio:',('A Coruña', 'Albacete', 'Alcázar de San Juan', 'Alcobendas', 'Alcorcón', 'Algeciras', 'Alicante', 'Almería', 'Ávila', 'Avilés', 'Badajoz', 'Badalona', 'Barakaldo', 'Barcelona', 'Bilbao', 'Burgos', 'Cáceres', 'Cádiz', 'Canals', 'Cartagena', 'Castelló de la Plana', 'Ciudad Real', 'Córdoba', 'Cornellà de Llobregat', 'Coslada', 'Cuenca', 'Donosti', 'Dos Hermanas', 'Elche', 'Ferrol', 'Fuenlabrada', 'Getafe', 'Gijón', 'Girona', 'Granada', 'Guadalajara', 'Getxo', 'Herencia', 'Huelva', 'Huesca', 'Jaén', 'Jerez de la Frontera', 'Las Palmas de Gran Canaria', 'Leganés', 'León', 'Lincoln (UK)', 'Lleida', 'Logroño', 'Londres (UK)', 'Lorca', 'Lugo', 'Madrid', 'Málaga', 'Marbella', 'Mataró', 'Mérida', 'Móstoles', 'Oporto (PT)', 'Ourense', 'Oviedo', 'Palencia', 'Palma de Mallorca', 'Pamplona', 'Parla', 'Pontevedra', 'Reus', 'Roma (IT)', 'Sabadell', 'Salamanca', 'San Fernando', 'Santander', 'Sant Boi de Llobregat', 'Santiago de Compostela', 'Santa Cruz de Tenerife', 'Santa Coloma de Gramanet', 'San Cristóbal de la Laguna', 'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Tavalera de la Reina', 'Telde', 'Terrassa', 'Teruel', 'Toledo', 'Torrejón de Ardoz', 'Torrevieja', 'València', 'Valladolid', 'Vigo', 'Vitoria-Gasteiz', 'Xàtiva', 'Zamora', 'Zaragoza'), index=None, placeholder='Encuéntralo aquí')


st.write('')
st.write('###### Si tu pueblo o ciudad no se encuentra en la lista, puedes enviarnos un mensaje con la petición para incluirlo en el siguiente recuadro:')

    
# email_sender = st.text_input('From', 'cafes.mailer@gmail.com', disabled=True)
email_sender = 'cafes.mailer@gmail.com'

# email_receiver = st.text_input('To')
email_receiver = 'cafes.mailer@gmail.com'

# subject = st.text_input('Asunto')

body = st.text_area('Petición de inclusión de pueblo/ciudad:')

# Hide the password input
password = 'nptu ware vlmy lqvr'

if st.button("✉️ Enviar petición"):
    try:
        msg = MIMEText(body)
        msg['From'] = email_sender
        msg['To'] = email_receiver
        msg['Subject'] = f"Petición desde {loc['coords']['latitude']}, {loc['coords']['longitude']}"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(email_sender, password)
        server.sendmail(email_sender, email_receiver, msg.as_string())
        server.quit()

        st.success('Enviado con éxito! 🚀')
    except Exception as e:
        st.error(f"Error al enviar tu petición: {e}")
