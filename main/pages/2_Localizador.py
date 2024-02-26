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
import ast
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
    df = pd.read_excel(data_url, engine='openpyxl', usecols= [ 'Columna1', 'url', 'nombre', 'ciudad', 'precio', 'latitud', 'longitud',
                                                               'rating', 'reviews', 'cerrado', 'cerrado_temporal', 'horarios',
                                                               'ocupacion', 'lgbt', 'aperitivos', 'terraza', 'cerveza',
                                                               'desayuno_almuerzo', 'sentarse', 'llevar', 'postres', 'acepta_reserva',
                                                               'perros', 'perros_fuera', 'wifi', 'wifi_gratis', 'vino',
                                                               'horario_raw_lunes', 'horario_raw', 'horario_raw_martes',
                                                               'horario_martes', 'horario_raw_miércoles', 'horario_miércoles',
                                                               'horario_raw_jueves', 'horario_jueves', 'horario_raw_viernes',
                                                               'horario_viernes', 'horario_raw_sábado', 'horario_sábado',
                                                               'horario_raw_domingo', 'horario_domingo', 'ocupacion_lunes',
                                                               'ocupacion_martes', 'ocupacion_miércoles', 'ocupacion_jueves',
                                                               'ocupacion_viernes', 'ocupacion_sábado', 'ocupacion_domingo' ],
                      nrows=20000)
    df = df.drop('Columna1', axis=1)
    return df

def filter_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    modify = st.checkbox("🎯 Añadir filtros")
    if not modify:
        return df

    df = df.copy()

    modification_container = st.container()

    with modification_container:
        columnas_filtro = ['☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios','⭐ Puntuación', '💬 Nº Comentarios', '📊 % Ocupación Ahora',
                             '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                             '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                          ]
        to_filter_columns = st.multiselect("Filtrar tabla por:", columnas_filtro, placeholder="Selecciona un campo")
        st.write('-----------')
        
        for column in to_filter_columns:
            # Si la columna es '💬 Nº Comentarios', usa un widget especial en la barra lateral
            if column == '💬 Nº Comentarios':
                left, right = st.columns((1, 20))
                # left.write("↳")
                user_num_input = right.number_input(
                    f"{column} mínimo",
                    min_value=int(df[column].min()),
                    max_value=int(df[column].max()),
                    value=int(df[column].min()),
                )
                st.write('-----------')
                df = df[df[column] >= user_num_input]
            else:
                left, right = st.columns((1, 20))
                # left.write("↳")
                # Trata las columnas con < 10 valores únicos como categóricas
                if is_categorical_dtype(df[column]) or df[column].nunique() < 10:
                    user_cat_input = right.multiselect(
                        f"Valores de {column}",
                        sorted(df[column].unique()),
                        default=sorted(list(df[column].unique())),
                    )
                    st.write('-----------')
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
                    st.write('-----------')
                    df = df[df[column].between(*user_num_input)]
                elif is_datetime64_any_dtype(df[column]):
                    user_date_input = right.date_input(
                        f"Valores de {column}",
                        value=(
                            df[column].min(),
                            df[column].max(),
                        ),
                    )
                    st.write('-----------')
                    if len(user_date_input) == 2:
                        user_date_input = tuple(map(pd.to_datetime, user_date_input))
                        start_date, end_date = user_date_input
                        df = df.loc[df[column].between(start_date, end_date)]
                else:
                    user_text_input = right.text_input(
                        f"Buscar {column}",
                    )
                    st.write('-----------')
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

# Función para sustituir valores
def sustituir_valor(val):
    if val == True:
        return "Sí"
    elif val == False:
        return "No"
    else:
        return val 

def sustituir_valor_emoji(val):
    if val == "Sí":
        return "✅"
    elif val == "No":
        return "❌"
    else:
        return val 
# ---------------------------------------------------------------------------------FUNCIONES⬆️-------------------------------------
# --------------------------------------------------------------------------------------UBI ⬇️-------------------------------------

loc = get_geolocation()
    
num_cafeterias = st.sidebar.number_input("Nº de cafeterías", value=10, min_value=1, max_value=1000, step=1, format="%i")

from_pc = st.sidebar.checkbox('Vista para ordenador')


if num_cafeterias != 1:
    st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tus {num_cafeterias} cafeterías más cercanas</h2>", unsafe_allow_html=True)
    st.write('')
else:
    st.markdown(f"<h2 style='margin-top: 0px; margin-bottom: -10px;'>Tu cafetería más cercana</h2>", unsafe_allow_html=True)
    st.write('')
    




# Cargamos el dataframe (necesitamos optimizar esto)
df = get_data()

# Obtener la fecha y hora actual
ahora = datetime.now()
hora_actual_float = datetime.now().hour + datetime.now().minute / 60 + 1
hora_actual = datetime.now().hour + 1

# Obtener el nombre del día de la semana en inglés
dia_semana_ing = ahora.strftime("%A")

# Diccionario para traducir el día de la semana al español
dias_semana_es = {"Monday": "lunes", "Tuesday": "martes", "Wednesday": "miércoles", "Thursday": "jueves", "Friday": "viernes", "Saturday": "sábado", "Sunday": "domingo"}

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

output = []

for horario_str in df[columna_dia_hoy]:
    try:
        # Convertir el string que representa una lista a una lista real
        horario = ast.literal_eval(horario_str)
    except (ValueError, SyntaxError):
        # Si hay un error en la conversión, establecer horario a una lista vacía
        horario = []

    horario_dict = {}

    if len(horario) > 1:
        for i, sublista in enumerate(horario):
            if len(sublista) == 2:
                inicio, fin = sublista
                duracion = fin - inicio
                if duracion < 0:
                    duracion += 12 if i == 0 else 24
                horario_dict[inicio] = duracion
    else:
        for sublista in horario:
            if len(sublista) == 2:
                inicio, fin = sublista
                duracion = fin - inicio
                if duracion < 0:
                    duracion += 24
                horario_dict[inicio] = duracion
                
    output.append(horario_dict)


abierto_ahora = []

for horario_dict in output:
    abierto = False  # Asumimos que inicialmente no está abierto
    for inicio, duracion in horario_dict.items():
        # Calcular si la hora actual está dentro del rango de apertura
        if inicio <= hora_actual_float < (inicio + duracion):
            abierto = True
            break  # No necesitamos seguir revisando otros horarios si ya encontramos uno que está abierto
    abierto_ahora.append(abierto)

df['Abierto Ahora'] = abierto_ahora

columnas_a_modificar = ['Abierto Ahora',
                  'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
                  'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
                 ]
for columna in columnas_a_modificar:
    df[columna] = df[columna].apply(sustituir_valor)

# Reordenamos el dataframe
df = df[['Link', 'Nombre', 'Ciudad','Abierto Ahora', 'Nivel de precios','Latitud','Longitud', 'Puntuación', 'Nº Comentarios', columna_dia_hoy_raw, 'Ocupación Ahora', # columna_ocupacion_hoy
         'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
         'Puedes sentarte', 'Tiene terraza', 'Sirve Cerveza', 'Sirve vino', 'Sirve desayunos/almuerzos', 'Sirve aperitivos', 'Sirve postres', 'Para llevar', 
         'Acepta reserva', 'Acepta perros', 'Acepta perros fuera', 'Tiene Wifi','Tiene Wifi Gratis', 'LGBT+ friendly',
        ]]


# Renombramos las columnas
nuevos_nombres = ['Link', '☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios','Latitud','Longitud', '⭐ Puntuación', '💬 Nº Comentarios', '🕐 Horario hoy', '📊 % Ocupación Ahora',
                  'Cerrado permanentemene', 'Cerrado temporalmente', #'Horario','Porcentaje de Ocupación', 
                  '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                  '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                 ]

df.columns = nuevos_nombres

df = filter_dataframe(df)

# st.write('')
# with st.expander("👀 Ver detalle de cafeterías por cercanía"):
#     st.dataframe(df.drop(['Link', 'Latitud', 'Longitud', 'Cerrado permanentemene', 'Cerrado temporalmente'], axis=1))# df = df.drop_duplicates()

dictio_coords_saviour = {    'A Coruña': '43.35931967283019, -8.408809210188679',
                             'Albacete': '38.99396769451219, -1.8604693884146342',
                             'Alcázar de San Juan': '39.39237252352941, -3.2141288529411765',
                             'Alcobendas': '40.537532506249995, -3.644522027083333',
                             'Alcorcón': '40.346937623076926, -3.8246613384615387',
                             'Algeciras': '36.129599940909095, -5.451225079545455',
                             'Alicante': '38.351139425, -0.4825341448275862',
                             'Almería': '36.842224141358024, -2.444184687037037',
                             'Ávila': '40.65386369111111, -4.692828448888889',
                             'Avilés': '43.55286543295455, -5.921562445454546',
                             'Badajoz': '38.874810194594595, -6.976294775675676',
                             'Badalona': '41.44967363469387, 2.236860312244898',
                             'Barakaldo': '43.292550786585366, -2.989846254878049',
                             'Barcelona': '41.39942715652174, 2.1666052008152175',
                             'Bilbao': '43.26211947838983, -2.9337297305084746',
                             'Burgos': '42.34686996533333, -3.686416834',
                             'Cáceres': '39.47134537816092, -6.376309583908046',
                             'Cádiz': '36.526413873563214, -6.274857685057471',
                             'Canals': '38.9622947, -0.5849458',
                             'Cartagena': '37.621564778527606, -0.9785270920245399',
                             'Castellón de la Plana': '39.98502614605263, -0.0428149125',
                             'Ciudad Real': '38.988141775, -3.9126477033333336',
                             'Córdoba': '37.88608491962617, -4.781265535514019',
                             'Cornellà de Llobregat': '41.3555910125, 2.0773028333333334',
                             'Coslada': '40.42620416756757, -3.5517938',
                             'Cuenca': '40.068779464705884, -2.1353676686274508',
                             'Donostia-San Sebastian': '43.313913859124085, -1.9806090014598539',
                             'Dos Hermanas': '37.29192572666667, -5.927649404',
                             'Elche': '38.26780385649351, -0.6967227350649351',
                             'Ferrol': '43.48838615607477, -8.225633858878505',
                             'Fuenlabrada': '40.287100390361445, -3.797767201204819',
                             'Getafe': '40.308838217857144, -3.7264821589285715',
                             'Gijón': '43.5338167045977, -5.667527423371647',
                             'Girona': '41.97899764090909, 2.818326618939394',
                             'Granada': '37.17808149240506, -3.6034549312236286',
                             'Guadalajara': '40.632373856, -3.1647458360000003',
                             'Getxo': '43.34240160967742, -3.010334016129032',
                             'Herencia': '39.36755, -3.3540527599999996',
                             'Huelva': '37.26272268157895, -6.9426139289473685',
                             'Huesca': '42.149762525, -0.392696121875',
                             'Jaén': '37.78014886506024, -3.7918087891566263',
                             'Jerez de la Frontera': '36.686790102912624, -6.131552945631069',
                             'Las Palmas de Gran Canaria': '28.129645660162602, -15.430950703252032',
                             'Leganés': '40.333947937000005, -3.757634225',
                             'León': '42.599584804651165, -5.575564213953489',
                             'Lincoln': '53.22896717439024, -0.5418955',
                             'Lleida': '41.61688401521739, 0.6256506760869565',
                             'Logroño': '42.462202311695904, -2.4483244959064328',
                             'London': '51.50008564821429, -0.13242266535714287',
                             'Lorca': '37.6701947442623, -1.6944428196721313',
                             'Lugo': '43.00738203163265, -7.556781552040817',
                             'Madrid': '40.4153429, -3.7074007',
                             'Málaga': '36.71417034545454, -4.443067285521885',
                             'Marbella': '36.50773136569343, -4.895492078832117',
                             'Mataró': '41.541815953333334, 2.43999132',
                             'Mérida': '38.91681533529412, -6.344387509803921',
                             'Móstoles': '40.324170957142854, -3.864314089010989',
                             'Oporto': '41.1659195, -8.5950563',
                             'Ourense': '42.3419908415493, -7.862884305633802',
                             'Oviedo': '43.36508059897436, -5.84789066',
                             'Palencia': '42.00696751967214, -4.527581191803279',
                             'Palma': '39.573502170903005, 2.659054004013378',
                             'Pamplona': '42.81446789268293, -1.6490197115853658',
                             'Parla': '40.238003463157895, -3.7672410868421053',
                             'Pontevedra': '42.42860158333333, -8.639992716666667',
                             'Reus': '41.153498245544554, 1.1084743',
                             'Roma': '41.8931647, 12.616129166666667',
                             'Sabadell': '41.547663493, 2.103674539',
                             'Salamanca': '40.968435578472224, -5.663365422916666',
                             'San Fernando': '36.46337692461539, -6.200236218461538',
                             'Santander': '43.461207507738095, -3.8160376904761906',
                             'Sant Boi de Llobregat': '41.34503951290323, 2.0368827032258063',
                             'Santiago de Compostela': '42.8788086, -8.540962632666666',
                             'Santa Cruz de Tenerife': '28.460063417877095, -16.2673412',
                             'Santa Coloma de Gramenet': '41.44995064074074, 2.211956114814815',
                             'San Cristóbal de la Laguna': '28.485085,-16.3169423',
                             'Segovia': '40.943489794444446, -4.116228702777778',
                             'Sevilla': '37.38350618552279, -5.971737966219839',
                             'Soria': '41.76694795, -2.4730200583333333',
                             'Tarragona': '41.11999216492537, 1.2463097619402983',
                             'Talavera de la Reina': '39.96184175538461, -4.832533472307692',
                             'Telde': '27.996769147222224, -15.406813934722221',
                             'Terrassa': '41.56336119652174, 2.0170197269565215',
                             'Teruel': '40.33803205882353, -1.1047350676470589',
                             'Toledo': '39.864105225609755, -4.014731767073171',
                             'Torrejón de Ardoz': '40.45818753157894, -3.4699243245614033',
                             'Torrevieja': '37.98031777575758, -0.6828376313131314',
                             'Valencia': '39.46725873569024, -0.3711913144781145',
                             'Valladolid': '41.64477447202072, -4.730428651295337',
                             'Vigo': '42.22457425679013, -8.72090796728395',
                             'Vitoria-Gasteiz': '42.85090934021739, -2.677926666304348',
                             'Xàtiva': '38.991189223333336, -0.5234018166666667',
                             'Zamora': '41.504066815277774, -5.737835669444444',
                             'Zaragoza': '41.65224518603175, -0.8914068428571429'}


st.write('')
if st.checkbox('📍 Usar mi ubicación'):
    try:
        location = [loc]
        latitud = location[0]['coords']['latitude']
        longitud = location[0]['coords']['longitude']
        st.write(10/0) # Provocamos el error
    except:
        st.error('No hemos podido acceder a tu ubicación. Selecciona tu municipio en el siguiente desplegable para buscar tu cafetería ideal:', icon="⚠️")
        ciudad_seleccionada = st.selectbox('Selecciona una ciudad', options=list(dictio_coords_saviour.keys()),placeholder="Busca tu ubicación más cercana para un relaxing cup of café con leche", index=25)
        if ciudad_seleccionada:
            latitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[0]), 4)
            longitud = round(float(dictio_coords_saviour[ciudad_seleccionada].split(', ')[1]), 4)
try:
    latitud = round(float(latitud), 4)
    longitud = round(float(longitud), 4)
except:
    latitud = 40.4336
    longitud = -3.7043

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

sorted_df = df.sort_values(by='dif_sum', ascending=True) #[:num_cafeterias]
sorted_df = sorted_df.reset_index(drop=True)
sorted_df['Metros'] = [haversine_distance(latitude, longitude, e, sorted_df['Longitud'][i]) for i,e in enumerate(sorted_df['Latitud'])]

sorted_df_show = sorted_df
sorted_df = sorted_df[:num_cafeterias]

coords = []
for i,e in enumerate(sorted_df['Latitud']):
    coords.append(str(e) + ", " +str(sorted_df['Longitud'][i]))
sorted_df['coords'] = coords
# sorted_df['Cómo llegar'] = ['https://www.google.com/maps/search/'+convert_coordinates(e) for e in sorted_df['coords']]

for index, row in sorted_df.iterrows():
    # Crea el popup con el enlace clickeable que se abrirá en una nueva ventana
    
    link = sorted_df["Link"][index].replace('"', '%22')
    popup_content = f'<div style="white-space: nowrap;">A {row["Metros"]} metros: <strong><a href="{link}" target="_blank" style="text-decoration: underline; cursor: pointer;">{row["☕ Nombre"]}</a></strong></div>'

    folium.Marker(
        location=[row["Latitud"], row["Longitud"]],
        popup=popup_content,
    ).add_to(m)

if from_pc:
    folium_static(m, width=1025)
else:
    folium_static(m, width=380)


columnas_a_modificar = ['🔓 Abierto Ahora',
                  '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                  '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                 ]
for columna in columnas_a_modificar:
    sorted_df_show[columna] = sorted_df_show[columna].apply(sustituir_valor_emoji)


sorted_df_show = sorted_df_show[['Link', 'Metros', '☕ Nombre', '🏙️ Ciudad', '🔓 Abierto Ahora', '💲 Nivel de precios', '⭐ Puntuación', '💬 Nº Comentarios', '🕐 Horario hoy', '📊 % Ocupación Ahora', 
                  '🪑 Puedes sentarte', '☀️ Tiene terraza', '🍺 Sirve Cerveza', '🍷 Sirve vino', '🥪 Sirve desayunos/almuerzos', '🫒 Sirve aperitivos', '🍪 Sirve postres', '🚶‍♂️ Para llevar', 
                  '🙋‍♀️ Acepta reserva', '🐕‍🦺 Acepta perros', '🐕 Acepta perros fuera', '🛜 Tiene Wifi','🛜 Tiene Wifi Gratis', '🏳️‍🌈 LGBT+ friendly',
                 ]]
st.write('')
st.markdown('#### Tabla detalle de las cafeterías')
num_cafes_filtradas = len(sorted_df_show)
with st.expander(f"👀 Ver {num_cafes_filtradas} cafeterías (por proximidad)"):
    st.data_editor(
        sorted_df_show,
        column_config={
            "Link": st.column_config.LinkColumn(
                "🔗 Link", display_text = "🌐 Cómo llegar"
            ),
            "Metros": st.column_config.NumberColumn(
            "📏 Distancia",
            help="Medida en metros desde tu ubicación",
            format="%d m",
            ),
            "⭐ Puntuación": st.column_config.ProgressColumn(
                "⭐ Puntuación",
                help="Los valores a 0 son sitios sin votos",
                format="%f",
                min_value=0,
                max_value=5,
            ),
            "📊 % Ocupación Ahora": st.column_config.ProgressColumn(
                "📊 % Ocupación Ahora",
                help="Los valores a 0 pueden ser sitios sin información de ocupación",
                format="%f",
                min_value=0,
                max_value=100,
            ),
        },
        hide_index=True,
    )

# with st.expander("👀 Ver detalle de todas las cafeterías por proximidad"):
#     st.dataframe(sorted_df_show.drop(['Link', 'Latitud', 'Longitud', 'Cerrado permanentemene', 'Cerrado temporalmente', 'lat_dif', 'lon_dif', 'dif_sum', 'Metros'], axis=1))
    
# ---------------------------------------------------------------------------------------UBI ⬆️-------------------------------------
# --------------------------------------------------------------------------------------MAIL ⬇️-------------------------------------

# st.write('')
st.write('')
st.write('')

# ciudades = sorted(sorted_df_show['🏙️ Ciudad'].unique())
# st.write(f'{ciudades}')

municipios_incluidos = ['A Arnoia', 'A Bergueira', 'A Coruña', 'A Groba', 'A Gudiña', 'A Manchica', 'A Pobra de Trives', 'A Pobra do Brollón', 'A Porriña', 'A Rúa', 'A Silva', 'A Valenza', 'Abejar', 'Acebo', 'Adahuesca', 'Aeropuerto de los Rodeos', 'Aguas Nuevas', 'Ágreda',
                        'Aguilar de Campoo', 'Aínsa', 'Alaquàs', 'Alar del Rey', 'Albacete', 'Albaladejo', 'Albalat dels Sorells', 'Albalate de Zorita', 'Albalate del Arzobispo', 'Albarellos', 'Albarracín', 'Albentosa', 'Alboraya', 'Alcalá de los Gazules', 'Alcalá del Obispo', 
                        'Alcalá del Valle', 'Alcaudete', 'Alcañices', 'Alcañiz', 'Alcobendas', 'Alcolea', 'Alcolea de Cinca', 'Alcolea del Pinar', "Alcora (L')", 'Alcorcón', 'Alcorisa', 'Alcántara', 'Alcázar de San Juan', 'Aldaia', 'Aldea del Rey', 'Alfafar', 
                        'Alfara del Patriarca', 'Algeciras', 'Algeciras, Cádiz', 'Algora', 'Algorta', 'Alhambra', 'Alicante', 'Alija del Infantado', 'Allariz', 'Almadrones', 'Almadén', 'Almagro', 'Almazcara', 'Almazán', 'Almería', 'Almodóvar del Campo', 
                        'Almonacid de Zorita', 'Almudévar', 'Almàssera', 'Alovera', 'Alquézar', 'Altafulla', 'Alumbres', 'Ampudia', 'Amusco', 'Andorra', 'Aneiros ,Ferrol', 'Ansoáin', 'Ansó', 'Antas de Ulla', 'Aranzueque', 'Arcenillas', 'Arcos de Jalón', 
                        'Arcos de la Frontera', 'Arcos de la Polvorosa', 'Ardea', 'Areeta (Getxo)', 'Arenals del Sol', 'Arenas de San Juan', 'Arenillas de Nuño Pérez', 'Argamasilla de Alba', 'Argamasilla de Calatrava', 'Armunia', 'Arnuíde', 'Arquillos', 
                        'Arroyo De La Vega', 'Arroyo Frio', 'Arroyo de la Luz', 'Arén', 'As Campiñas', 'As Nogais', 'Astorga', 'Astudillo', 'Astún', 'Atienza', 'Ávila', 'Avilés', 'Ayerbe', 'Ayoó de Vidriales', 'Azucaica', 'Azuqueca de Henares','Badajoz', 
                        'Badalona', 'Baeza', 'Bailén', 'Bajamar', 'Balcon de Telde', 'Baltanás', 'Bande', 'Baracaldo', 'Barajas', 'Barakaldo', 'Baralla', 'Barbadás', 'Barbastro', 'Barbate', 'Barcelona', 'Barco (O)', 'Barking', 'Barral', 'Barriada Río San Pedro', 
                        'Barrio', 'Barruelo de Santullán', 'Base Aerea Conjunta Torrejón', 'Baños de Montemayor', 'Beas de Segura', 'Becerreá', 'Beckenham', 'Begíjar', 'Bellavista', 'Belvedere', 'Belver de Cinca', 'Belvís de Monroy', 'Bembibre', 'Benabarre', 
                        'Benalup-Casas Viejas', 'Benasque', 'Benavente', 'Benavides de Órbigo', 'Benetússer', 'Benlloch', 'Berlanga de Duero', 'Bermillo de Sayago', 'Bernueces', 'Berriozar', 'Betote', 'Bexley', 'Bexleyheath', 'Bielsa', 'Biescas', 'Bilbao', 
                        'Binéfar', 'Boadilla del Monte', 'Bolaños de Calatrava', 'Boltaña', 'Bonanza', 'Bonavista', 'Bonfim', 'Bonrepòs i Mirambell', 'Boqueixon', 'Bornos', 'Boñar', 'Brentford', 'Bretó', 'Brihuega', 'Broadway', 'Bromley', 'Bronchales', 'Broto', 
                        'Brozas', 'Burgos', 'Burjassot', 'Burunchel', 'Bustillo del Páramo', 'Bóveda', "Ca'n Pastilla", 'Cabanillas del Campo', 'Cabezabellosa', 'Cabo de Gata', 'Cabo de Palos', 'Caboalles de Abajo', 'Cabrejas del Pinar', 'Cacabelos', 'Calaceite', 
                        'Calafell', 'Calamocha', 'Calanda', 'Calero (El)', 'Calvos de Randín', 'Calzada de Calatrava', 'Calzadilla', 'Calzadilla de la Cueza', 'Cambados', 'Caminomorisco', 'Caminreal', 'Campanhã', 'Campazas', 'Campillo de Arenas', 'Campo', 
                        'Campo de Criptana', 'Camponaraya', 'Canales', 'Canals', 'Candanchú', 'Candasnos', 'Canena', 'Canfranc-Estación', 'Canredondo', 'Canteras', 'Caraquiz', 'Carbajales de Alba', 'Carcaboso', 'Carrión de Calatrava', 'Carrión de los Condes', 
                        'Carrus', 'Carshalton', 'Cartagena', 'Cartagena, Murcia', 'Cartuja Baja', 'Carucedo', 'Casar de Cáceres', 'Casar de Talavera (El)', 'Casas Nuevas', 'Casas de Don Gómez', 'Casas del Castañar', 'Casaseca de las Chanas', 'Casatejada', 
                        'Cascón de la Nava', 'Castejón', 'Castejón de Sos', 'Castel Romano', 'Castellar de Santiago', 'Castellón de la Plana', 'Castillazuelo', 'Castrillo de Don Juan', 'Castrillo de la Ribera', 'Castro Caldelas', 'Castro de Ribeiras', 'Catarroja', 
                        'Cazorla', 'Ceclavín', 'Cedofeita', 'Cedrillas', 'Celanova', 'Cella', 'Cerro Muriano', 'Cervera de Pisuerga', 'Chantada', 'Chapela', 'Chessington', 'Chiclana de la Frontera', 'Chilluévar', 'Chillón', 'Chipiona', 'Chislehurst', 'Ciampino', 'Cifuentes', 'Cilleros', 'Cimanes de la Vega', 'Cisneros', 'Cistierna', 'Ciudad Quesada', 'Ciudad Real', 'Cogolludo', 'Coles', 'Collado Villalba', 'Collonades', 'Colloto', 'Colungo', 'Conchel', 'Congosto', 'Conil de la Frontera', 'Coria', 'Cornellà de Llobregat', 'Corredoria', 'Cortes', 'Cortijos Nuevos', 'Coslada', 'Coto de Bornos', 'Coto-Ríos', 'Coulsdon', 'Covaleda', 'Coy', 'Cp', 'Cretas', 'Croydon', 'Ctra. Acceso Central Térmica N: S/N', 'Cualedro', 'Cuenca', 'Cuesta Blanca', 'Cuevas de Almudén', 'Curbe', 'Cáceres', 'Cádiz', 'Córdoba', 'Dacón', 'Dagenham', 'Daimiel', 'Dartford', 'Donadío', 'Donostia-San Sebastian', 'Dos Hermanas', 'Duruelo de la Sierra', 'El Albujón', 'El Algar', 'El Alquián', 'El Arenal', 'El Burgo Ranero', 'El Burgo de Osma', 'El Casar', 'El Casar de Talavera', 'El Chaparral', 'El Cuervo', 'El Gastor', 'El Grado', 'El Grao de Castellón', 'El Higueron', 'El Pinar', 'El Poblenou', 'El Portal', 'El Poyo del Cid', 'El Puerto de Sta María', 'El Robledo', 'El Rosario', 'El Torno', 'El Zabal', 'El pilar', 'Elche', 'Elche Parque Industrial', 'Enfield', 'Entrimo', 'Erith', 'Es Pil·larí', 'Es Secar de la Real', 'Escarrilla', 'Esgos', 'Espera', 'Estación', 'Estación Linares-Baeza', 'Estación de Medinaceli', 'Estadilla', 'Estella del Marqués', 'Esteras de Medinaceli', 'Estrecho de San Gines', 'Fabero', 'Facinas', 'Fariza', 'Feltham', 'Fermoselle', 'Ferreira de Pantón', 'Ferrol', "Foia d'Elx", 'Foios', 'Fontanar', 'Formigal', 'Fortanete', 'Fraga', 'Fresno de la Ribera', 'Friamonde', 'Frómista', 'Fuenlabrada', 'Fuenllana', 'Fuente el Fresno', 'Fuentelahiguera de Albatages', 'Fuentelapeña', 'Fuentes de Nava', 'Galapagar', 'Galisteo', 'Galiñáns', 'Gargüera', 'Garrovillas', 'Gata', 'Germans Sàbat', 'Getafe', 'Getxo', 'Gijón', 'Girona', 'Godella', 'Golmayo', 'Gordoncillo', 'Granada', 'Graus', 'Grazalema', 'Grañén', 'Greater', 'Greenford', 'Guadacorte', 'Guadalajara', 'Guadalcacín', 'Guamasa', 'Guardo', 'Guarromán', 'Gustei', 'Hampton', 'Hanwell', 'Harrow', 'Hayes', 'Herencia', 'Herrera de Pisuerga', 'Hervás', 'Hinojares', 'Hontoria', 'Horcajo de los Montes', 'Hornchurch', 'Hornos', 'Hospital de Órbigo', "Hospitalet de Llobregat (L')", 'Hounslow', 'Huelva', 'Huergas de Babia', 'Huesca', 'Humanes', 'IMEPE', 'Ibros', 'Igüeña', 'Ilford', 'Isla Plana', 'Isla de', 'Isleworth', 'Iznatoraf', 'Jabalquinto', 'Jaca', 'Jadraque', 'Jarandilla de la Vera', 'Jaraíz de la Vera', 'Jarilla', 'Jaén', 'Jerez de la Frontera', 'Jerte', 'Josa', 'Jubilee', 'Jódar', 'Keston', 'Kingston upon Thames', "L'Altet", 'La Aljorra', 'La Aparecida', 'La Barca de la Florida', 'La Bañeza', 'La Bóveda de Toro', 'La Camocha', 'La Carolina', 'La Cañada', 'La Escucha', 'La Estación', 'La Fortuna', 'La Garita', 'La Herradura', 'La Hoya', 'La Iruela', 'La Laguna', 'La Línea de la Concepción', 'La Magdalena', 'La Manga', 'La Manga Club', 'La Martina', 'La Mata', 'La Palma', 'La Pardilla', 'La Puebla', 'La Puebla de Valverde', 'La Puerta de Segura', 'La Solana', 'La Virgen del Camino', 'Lampaza', 'Langa de Duero', 'Larouco', 'Las Campas', 'Las Huesas', 'Las Medianias', 'Las Mercedes', 'Las Palmas de Gran Canaria', 'Las Remudas', 'Las Rozas de Madrid', 'Laza', 'Leganés', 'Leiro', 'Les Baies', 'Leystonstone', 'León', 'Linares', 'Lincoln', 'Lleida', 'Lodares', 'Logroño', 'Lombillo de los Barrios', 'London', 'Londres', 'Loporzano', 'Lorca', 'Los Barrios', 'Los Belones', 'Los Cortijillos', 'Los Moriscos', 'Los Nietos', 'Los Rábanos', 'Los Villares', 'Losar de la Vera', 'Lubián', 'Lugo', 'Láncara', 'Lérida', 'Línea De La Concepción ( La )', 'Maceda', 'Madrid', 'Madridanos', 'Madrigal de la Vera', 'Majadahonda', 'Malagón', 'Maliaño', 'Malpartida de Plasencia', 'Mancha Real', 'Manises', 'Mansilla de las Mulas', 'Mantiel', 'Manzanal del Puerto', 'Manzanares', 'Manzaneda', 'Maqueda', 'Marbella', 'Marchamalo', 'Marpequeña', 'Martos', 'Martín del Río', 'Marín', 'Mas de las Matas', 'Masegoso de Tajuña', 'Maside', 'Massanassa', 'Matarrosa del Sil', 'Mataró', 'Matas-Pinar-Monte Rozas ( Las )', 'Matola', 'Medina-Sidonia', 'Medinaceli', 'Meliana', 'Membrilla', 'Membrío', 'Mengíbar', 'Miajadas', 'Middlesex', 'Miguelturra', 'Mirabel', 'Miranda', 'Mislata', 'Mitcham', 'Mogón', 'Mohedas de Granadilla', 'Molina de Aragón', 'Moncada', 'Mondéjar', 'Monfarracinos', 'Monforte de Lemos', 'Monreal del Campo', 'Montalbán', 'Montamarta', 'Monteagudo de las Vicarías', 'Montehermoso', 'Montejos del Camino', 'Montequinto', 'Monterde de Albarracín', 'Monterroso', 'Montiel', 'Monzón', 'Mora de Rubielos', 'Moraleja', 'Moraleja del Vino', 'Morales de Toro', 'Morales del Vino', 'Moralina', 'Morden', 'Moreiras', 'Morón de Almazán', 'Mugueimes', 'Murcia', 'Museros', 'Mutilva', 'Málaga', 'Mérida', 'Móstoles', 'Narón', 'Navalmoral de la Mata', 'Navas de San Juan', 'Navas del Madroño', 'New Malden', 'Noceda', 'Northwood', 'Nueno', 'Nueva Jarilla', 'Nuñomoral', 'O Barco', 'O Carballiño', 'O Corgo', 'O Cotón', 'Ofra', 'Oia', 'Ojos Negros', 'Ojos de Garza', 'Olleros de Sabero', 'Olvera','Ólvega', 'Onzonilla', 'Oporto', 'Orbón', 'Orcera', 'Orpington', 'Ortigal', 'Osorno', 'Ostia', 'Ostia Antica', 'Otero de Bodas', 'Ourense', 'Outeiro de Rei', 'Outomuro', 'Oviedo', 'Padornelo', 'Padrenda', 'Padrenda de Abaixo', 'Paiporta', 'Palas de Rei', 'Palencia', 'Palma', 'Palmones', 'Pamplona', 'Panticosa', 'Paradela', 'Paredes de Nava', 'Pareja', 'Parla', 'Parque de La Laguna', 'Parquelagos', 'Pastrana', 'Paterna', 'Peal de Becerro', 'Pedrafita do Cebreiro', 'Pedro Muñoz', 'Peque', 'Peracense', 'Peraleda de San Román', 'Peralejos', 'Perales de Tajuña', 'Perazancas', 'Perleta', 'Peñarroya de Tastavíns', 'Picanya', 'Piedrabuena', 'Pielas', 'Pinner', 'Pinofranqueado', 'Piornal', 'Pioz', 'Plasencia', 'Plasencia del Monte', 'Poblado de Sancti Petri', 'Pobladura de Pelayo Garcia, Leon', 'Pobladura del Valle', 'Poblete', 'Pol. Ind. El Goro', 'Pol. Ind. Pla de la Vallonga', 'Poligono Industrial de Constantí', 'Ponferrada', 'Ponte Galeria-la Pisana', 'Pontevedra', 'Port Saplaya', 'Porto', 'Portomarín', 'Porzuna', 'Pozo Alcón', 'Pozo Estrecho', 'Pozuelo de Alarcón', 'Pozuelo de Calatrava', 'Pozuelo de Vidriales', 'Prado del Rey', 'Puebla de Sanabria', 'Puebla de Trives', 'Puebla del Príncipe', 'Puente Villarente', 'Puente de Domingo Flórez', 'Puente de Génave', 'Puenteareas', 'Puerto Lápice', 'Puerto Real', 'Puerto Serrano', 'Puerto de la Cruz', 'Puertollano', 'Pumarejo de Tera', 'Punta Prima', 'Punta del Hidalgo', 'Purias', 'Purley', 'Quart de Poblet', 'Quesada', 'Quintana del Marco', 'Quintela', 'Quiroga', 'Rabanal de Arriba', 'Rafal', 'Rainham', 'Raíces Nuevo', 'Real', 'Reboredo', 'Retamar', 'Reus', 'Ribadavia', 'Ribadelago Nuevo', 'Ribadumia', 'Richmond', 'Rio Tinto', 'Riolobos', 'Rioseco de Soria', 'Rioseco de Tapia', 'Risco Negro', 'Rivas-Vaciamadrid', 'Rocafort', 'Rochela', 'Roma', 'Rome', 'Romford', 'Rota', 'Ruidera', 'Ruislip', 'Rábade', 'S. Leonardo de Yagüe', 'Sa Indioteria', 'Sa Vileta-Son Rapinya', 'Sabadell', 'SabesteCoffee', 'Sabiote', 'Sabiñánigo', 'Sabucedo', 'Sacedón', 'Sagunto', 'Sainsbury', 'Salamanca', 'Saldaña', 'Salinetas', 'Sallent de Gállego', 'Salt', 'Samos', 'San Andrés', 'San Andrés del Rabanedo', 'San Carlos del Valle', 'San Cibrao das Viñas', 'San Cristóbal de Entreviñas', 'San Fernando', 'San Fernando de Henares', 'San Gregorio', 'San Jose', 'San Juan', 'San Juan de Mozarrifar', 'San Juan de Ortega', 'San Martín de Trevejo', 'San Matias', 'San Pedro Alcántara', 'San Pedro Bercianos', 'San Pedro de Ceque', 'San Pedro de Olleros', 'San Pedro.', 'San Román', 'San Roque', 'San Sebastián', 'San Sebastián de los Reyes', 'San Vitero', 'San Xulián', 'San cristovo de cea', 'Sancedo', 'Sande', 'Sandiás', 'Sanlúcar de Barrameda', 'Sant Boi de Llobregat', 'Sant Joan Despí', 'Sant Jordi', 'Sant Salvador', 'Sant Vicent del Raspeig', 'Santa Ana', 'Santa Coloma de Gramenet', 'Santa Cruz de Mudela', 'Santa Cruz de Tenerife', 'Santa Cruz de Yanguas', 'Santa Maria de', 'Santa María de Huerta', 'Santa María de Trassierra', 'Santa María del Mar', 'Santander', 'Santiago de Compostela', 'Santiago del Campo', 'Santibañez de la Peña', 'Santibáñez de Vidriales', 'Santibáñez el Bajo', 'Santillana de Campos', 'Santo Tomé', 'Santovenia de la Valdoncina', 'Saravillo', 'Sarreaus', 'Sarria', 'Sarrión', 'Sedaví', 'Segovia', 'Segura de la Sierra', 'Selcetta', 'Serradilla', 'Ses Cadenes', 'Sesué', 'Setenil de las Bodegas', 'Sevilla', 'Sidcup', 'Sigüeiro', 'Sigüenza', 'Siles', 'Siresa', 'Sobradelo', 'Socuéllamos', 'Son Castelló', 'Son Ferriol', 'Son Sardina', 'Son Serra Perera', 'Soria', 'Sotiello', 'South Croydon', 'Southall', 'Souto', 'Sta Coloma de Gramanet', 'Stamford', 'Surbiton', 'Surrey', 'Sutton', 'Tabarca', 'Taboada', 'Taboadela', 'Taco', 'Talavera de la Reina', 'Talayuela', 'Tamajón', 'Tangel', 'Taraguilla', 'Tardesillas', 'Tardienta', 'Tarifa', 'Tarragona', 'Tavernes Blanques', 'Teddington', 'Tejina', 'Telde', 'Tendilla', 'Tenerife', 'Tercia', 'Terrassa', 'Teruel', 'Thornton Heath', 'Toledo', 'Tomelloso', 'Toral de Merayo', 'Toral de los Vados', 'Toreno', 'Torla-Ordesa', 'Toro', 'Torquemada', 'Torre de Juan Abad', 'Torre del Bierzo', 'Torre-romeu', 'Torreblascopedro', 'Torrecera', 'Torredelcampo', 'Torredonjimeno', 'Torrejoncillo', 'Torrejón de Ardoz', 'Torrejón del Rey', 'Torrellano', 'Torrelodones', 'Torremenga', 'Torrente de Cinca', 'Torrenueva', 'Torreorgaz', 'Torreperogil', 'Torres', 'Torres de Albánchez', 'Torrevieja', 'Trabazos', 'Tramacastilla', 'Trasmiras', 'Trebujena', 'Triacastela', 'Trobajo del Camino', 'Trubia', 'Trévago', 'Twickenham', 'Úbeda', 'Ubrique', 'Upminster', 'Urb. Cdad. del Golf', 'Urb. Novo Santi Petri', 'Urb. las Camaretas', 'Urb. los Vergeles', 'Usanos', 'Utebo', 'Utrillas', 'Uxbridge', 'Vadillo', 'Valcabado', 'Valdecabras', 'Valdepeñas', 'Valderas', 'Valderrobres', 'Valdesalor', 'Valencia', 'Valencia de Don Juan', 'Valladolid', 'Valverde de la Virgen', 'Valverde del Fresno', 'Varea', 'Vega de Espinareda', 'Vegaviana', 'Veguellina de Órbigo', 'Vejer de la Frontera', 'Velamazán', 'Velilla del Río Carrión', 'Venta Gaspar', 'Venta de Baños', 'Venta de los Santos', 'Venta del Aire', 'Verín', 'Viana do Bolo', 'Vicolozano', 'Vigo', 'Vila Da Area', 'Vila-seca', 'Vilachá', 'Vilagarcía de Arousa', 'Vilamartín de Valdeorras', 'Vilamor', 'Vilanova de Arousa', 'Vilar', 'Vilarchao', 'Vilasante', 'Vilches', 'Villablino', 'Villabuena del Puente', 'Villacarrillo', 'Villadangos del Paramo', 'Villaestrigo del Páramo', 'Villafranca del Bierzo', 'Villafranca del Campo', 'Villafría', 'Villagarcía de la Vega', 'Villahibiera', 'Villahán', 'Villalpando', 'Villamandos', 'Villamañán', 'Villamuriel de Cerrato', 'Villanueva de la Sierra', 'Villanueva de la Torre', 'Villanueva de los Infantes', 'Villanueva del Arzobispo', 'Villanueva del Campo', 'Villar del Cobo', 'Villaralbo', 'Villardeciervos', 'Villarente', 'Villarramiel', 'Villarrubia de los Ojos', 'Villarta de San Juan', 'Villasabariego', 'Villaseca de Laciana', 'Villel', 'Viloira', 'Vinalesa', 'Vinuesa', 'Viso del Marqués', 'Vitinia', 'Vitoria-Gasteiz', 'Vivel del Río Martín', 'Vrins', 'Wallington', 'Welling', 'Wembley', 'West Drayton', 'West Wickham', 'Westerham', 'Woodford Green', 'Worcester Park', 'Xinzo de Limia', 'Xirivella', 'Xunqueira de Ambía', 'Xàtiva', 'Zahara de los Atunes', 'Zamora', 'Zaragoza', 'Zarcilla de Ramos', 'Zarza de Granadilla', 'Zubieta']

# municipios_incluidos = ['A Coruña', 'Albacete', 'Alcázar de San Juan', 'Alcobendas', 'Alcorcón', 'Algeciras', 'Alicante', 'Almería', 'Ávila', 'Avilés', 'Badajoz', 'Badalona', 'Barakaldo', 'Barcelona', 'Bilbao', 'Burgos', 'Cáceres', 'Cádiz', 'Canals', 'Cartagena', 'Castelló de la Plana', 'Ciudad Real', 'Córdoba', 'Cornellà de Llobregat', 'Coslada', 'Cuenca', 'Donosti', 'Dos Hermanas', 'Elche', 'Ferrol', 'Fuenlabrada', 'Getafe', 'Gijón', 'Girona', 'Granada', 'Guadalajara', 'Getxo', 'Herencia', 'Huelva', 'Huesca', 'Jaén', 'Jerez de la Frontera', 'Las Palmas de Gran Canaria', 'Leganés', 'León', 'Lincoln (UK)', 'Lleida', 'Logroño', 'Londres (UK)', 'Lorca', 'Lugo', 'Madrid', 'Málaga', 'Marbella', 'Mataró', 'Mérida', 'Móstoles', 'Oporto (PT)', 'Ourense', 'Oviedo', 'Palencia', 'Palma de Mallorca', 'Pamplona', 'Parla', 'Pontevedra', 'Reus', 'Roma (IT)', 'Sabadell', 'Salamanca', 'San Fernando', 'Santander', 'Sant Boi de Llobregat', 'Santiago de Compostela', 'Santa Cruz de Tenerife', 'Santa Coloma de Gramanet', 'San Cristóbal de la Laguna', 'Segovia', 'Sevilla', 'Soria', 'Tarragona', 'Talavera de la Reina', 'Telde', 'Terrassa', 'Teruel', 'Toledo', 'Torrejón de Ardoz', 'Torrevieja', 'València', 'Valladolid', 'Vigo', 'Vitoria-Gasteiz', 'Xàtiva', 'Zamora', 'Zaragoza']

st.write('## 🏙️ Información sobre los datos')
st.write('###### En el mapa encontrarás datos de diferentes municipios. Principalmente se han seleccionado aquellas localidades con más de 75.000 habitantes en España (y sus alrrededores). Los municipios incluidos se muestran en el siguiente desplegable:')
st.selectbox('Busca tu municipio 👇',(municipios_incluidos), index=None, placeholder='Encuéntralo aquí')


st.write('')
st.write('###### Si tu pueblo o ciudad no se encuentra en la lista (o echas de menos más datos), puedes enviarnos un mensaje con la petición para incluirlo en el siguiente recuadro:')

    
# email_sender = st.text_input('From', 'cafes.mailer@gmail.com', disabled=True)
email_sender = 'cafes.mailer@gmail.com'

# email_receiver = st.text_input('To')
email_receiver = 'cafes.mailer@gmail.com'

# subject = st.text_input('Asunto')

body = st.text_area('Petición de inclusión de pueblo/ciudad 📥')

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
